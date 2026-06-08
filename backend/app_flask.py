"""
Flask 同步版本后端 API
兼容 Python 3.13 Windows 环境
使用原生 sqlite3，不依赖 SQLAlchemy
"""
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
import os
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'resume.db')

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000", "http://localhost:3001"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["*"]
    }
})


def migrate_db():
    """数据库迁移：添加缺失的列和表"""
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute("PRAGMA table_info(resumes)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'slug' not in columns:
        cursor.execute("ALTER TABLE resumes ADD COLUMN slug VARCHAR(100)")
        db.commit()
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_resumes_slug ON resumes(slug)")
        db.commit()
    if 'user_id' not in columns:
        cursor.execute("ALTER TABLE resumes ADD COLUMN user_id INTEGER")
        db.commit()

    # 创建 user_profiles 表（如果不存在）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            about_text TEXT,
            photo_url VARCHAR(500),
            years_exp VARCHAR(20),
            projects_count VARCHAR(20),
            articles_count VARCHAR(20),
            contributions_count VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    db.commit()
    db.close()


# 启动时执行迁移
migrate_db()


def get_db():
    """获取数据库连接"""
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    """关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """执行查询"""
    db = get_db()
    cur = db.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    if one:
        return rows[0] if rows else None
    return rows


def execute_db(query, args=()):
    """执行插入/更新/删除"""
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    lastrowid = cur.lastrowid
    cur.close()
    return lastrowid


def row_to_dict(row):
    """将 sqlite3.Row 转换为字典"""
    if row is None:
        return None
    result = {key: row[key] for key in row.keys()}
    # 兼容前端字段名：将数据库的 order_num 映射为 order
    if 'order_num' in result:
        result['order'] = result.pop('order_num')
    return result


# ==================== API 路由 ====================

@app.route('/')
def index():
    return jsonify({
        'message': '欢迎使用简历管理系统API',
        'version': '1.0.0',
        'docs': '/api/docs'
    })


@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})


# ==================== 简历 CRUD ====================

@app.route('/api/resumes', methods=['GET'])
def get_resumes():
    """获取所有简历列表"""
    resumes = [row_to_dict(r) for r in query_db('SELECT * FROM resumes ORDER BY id DESC')]
    return jsonify(resumes)


@app.route('/api/resumes', methods=['POST'])
def create_resume():
    """创建简历"""
    user = get_current_user()
    if not user:
        return jsonify({'error': '未登录或登录已过期'}), 401

    data = request.get_json()
    if not data or not data.get('name') or not data.get('title'):
        return jsonify({'error': '姓名和职位标题为必填项'}), 400
    if not data.get('slug'):
        return jsonify({'error': '简历ID为必填项'}), 400

    slug = data.get('slug')
    # 检查 slug 唯一性
    existing = query_db('SELECT id FROM resumes WHERE slug = ?', [slug], one=True)
    if existing:
        return jsonify({'error': '简历ID已存在，请使用其他ID'}), 400

    is_active = 1 if data.get('is_active') else 0
    if is_active:
        # 确保同一用户只有一个激活简历
        execute_db('UPDATE resumes SET is_active = 0 WHERE user_id = ?', [user['id']])

    resume_id = execute_db(
        '''INSERT INTO resumes (name, title, slug, greeting, description, avatar_url, is_active, user_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        [data.get('name'), data.get('title'), slug, data.get('greeting', '你好,我是'),
         data.get('description', ''), data.get('avatar_url', ''),
         is_active, user['id']]
    )
    return jsonify({'id': resume_id, 'message': '创建成功'}), 201


@app.route('/api/resumes/<int:resume_id>', methods=['PUT'])
def update_resume(resume_id):
    """更新简历"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供更新数据'}), 400

    # 检查 slug 唯一性
    if 'slug' in data and data['slug']:
        existing = query_db('SELECT id FROM resumes WHERE slug = ? AND id != ?', [data['slug'], resume_id], one=True)
        if existing:
            return jsonify({'error': '简历ID已存在，请使用其他ID'}), 400

    # 如果激活当前简历，先将该用户的其他简历设为未激活
    if 'is_active' in data and data['is_active']:
        resume = query_db('SELECT user_id FROM resumes WHERE id = ?', [resume_id], one=True)
        if resume:
            execute_db('UPDATE resumes SET is_active = 0 WHERE user_id = ? AND id != ?', [resume['user_id'], resume_id])

    fields = []
    values = []
    for field in ['name', 'title', 'slug', 'greeting', 'description', 'avatar_url', 'is_active']:
        if field in data:
            fields.append(f"{field} = ?")
            values.append((1 if data[field] else 0) if field == 'is_active' else data[field])

    if not fields:
        return jsonify({'error': '没有要更新的字段'}), 400

    values.append(resume_id)
    execute_db(f"UPDATE resumes SET {', '.join(fields)} WHERE id = ?", values)
    return jsonify({'message': '更新成功'})


@app.route('/api/resumes/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    """删除简历"""
    execute_db('DELETE FROM resumes WHERE id = ?', [resume_id])
    return jsonify({'message': '删除成功'})


@app.route('/api/resumes/active')
def get_active_resume():
    """获取激活的完整简历"""
    user_id = request.args.get('user_id', type=int)
    
    if user_id:
        resume = query_db('SELECT * FROM resumes WHERE is_active = 1 AND user_id = ? LIMIT 1', [user_id], one=True)
    else:
        resume = query_db('SELECT * FROM resumes WHERE is_active = 1 LIMIT 1', one=True)
    
    if not resume:
        return jsonify({'error': '没有找到激活的简历'}), 404
    
    resume_dict = row_to_dict(resume)
    resume_id = resume_dict['id']
    
    skills = [row_to_dict(r) for r in query_db(
        'SELECT * FROM skills WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    projects = [row_to_dict(r) for r in query_db(
        'SELECT * FROM projects WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    experiences_raw = query_db(
        'SELECT * FROM experiences WHERE resume_id = ? ORDER BY order_num', [resume_id])
    educations = [row_to_dict(r) for r in query_db(
        'SELECT * FROM educations WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    contacts = [row_to_dict(r) for r in query_db(
        'SELECT * FROM contacts WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    
    experiences = []
    for exp in experiences_raw:
        exp_dict = row_to_dict(exp)
        exp_dict['details'] = json.loads(exp_dict['details'] or '[]')
        exp_dict['tech_stack'] = json.loads(exp_dict['tech_stack'] or '[]')
        experiences.append(exp_dict)
    
    for proj in projects:
        proj['tech_stack'] = json.loads(proj['tech_stack'] or '[]')
    
    return jsonify({
        'resume': resume_dict,
        'skills': skills,
        'projects': projects,
        'experiences': experiences,
        'educations': educations,
        'contacts': contacts
    })


@app.route('/api/resumes/<int:resume_id>')
def get_resume(resume_id):
    """获取指定简历详情"""
    resume = query_db('SELECT * FROM resumes WHERE id = ?', [resume_id], one=True)
    if not resume:
        return jsonify({'error': '简历不存在'}), 404
    
    resume_dict = row_to_dict(resume)
    
    skills = [row_to_dict(r) for r in query_db(
        'SELECT * FROM skills WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    projects = [row_to_dict(r) for r in query_db(
        'SELECT * FROM projects WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    experiences_raw = query_db(
        'SELECT * FROM experiences WHERE resume_id = ? ORDER BY order_num', [resume_id])
    educations = [row_to_dict(r) for r in query_db(
        'SELECT * FROM educations WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    contacts = [row_to_dict(r) for r in query_db(
        'SELECT * FROM contacts WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    
    experiences = []
    for exp in experiences_raw:
        exp_dict = row_to_dict(exp)
        exp_dict['details'] = json.loads(exp_dict['details'] or '[]')
        exp_dict['tech_stack'] = json.loads(exp_dict['tech_stack'] or '[]')
        experiences.append(exp_dict)
    
    for proj in projects:
        proj['tech_stack'] = json.loads(proj['tech_stack'] or '[]')
    
    return jsonify({
        'resume': resume_dict,
        'skills': skills,
        'projects': projects,
        'experiences': experiences,
        'educations': educations,
        'contacts': contacts
    })


@app.route('/api/public/resumes/<int:user_id>/<slug>')
def get_public_resume(user_id, slug):
    """公开访问：通过用户ID和简历slug获取简历详情"""
    resume = query_db(
        '''SELECT r.*, u.username, u.nickname FROM resumes r
           JOIN users u ON r.user_id = u.id
           WHERE u.id = ? AND r.slug = ? LIMIT 1''',
        [user_id, slug], one=True)
    if not resume:
        return jsonify({'error': '简历不存在'}), 404

    resume_dict = row_to_dict(resume)
    resume_id = resume_dict['id']

    skills = [row_to_dict(r) for r in query_db(
        'SELECT * FROM skills WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    projects = [row_to_dict(r) for r in query_db(
        'SELECT * FROM projects WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    experiences_raw = query_db(
        'SELECT * FROM experiences WHERE resume_id = ? ORDER BY order_num', [resume_id])
    educations = [row_to_dict(r) for r in query_db(
        'SELECT * FROM educations WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    contacts = [row_to_dict(r) for r in query_db(
        'SELECT * FROM contacts WHERE resume_id = ? ORDER BY order_num', [resume_id])]

    experiences = []
    for exp in experiences_raw:
        exp_dict = row_to_dict(exp)
        exp_dict['details'] = json.loads(exp_dict['details'] or '[]')
        exp_dict['tech_stack'] = json.loads(exp_dict['tech_stack'] or '[]')
        experiences.append(exp_dict)

    for proj in projects:
        proj['tech_stack'] = json.loads(proj['tech_stack'] or '[]')

    return jsonify({
        'resume': resume_dict,
        'skills': skills,
        'projects': projects,
        'experiences': experiences,
        'educations': educations,
        'contacts': contacts
    })


# ==================== 技能 CRUD ====================

@app.route('/api/skills', methods=['GET'])
def get_all_skills():
    """获取所有技能"""
    skills = [row_to_dict(r) for r in query_db('SELECT * FROM skills ORDER BY order_num')]
    return jsonify(skills)


@app.route('/api/skills', methods=['POST'])
def create_skill():
    """创建技能"""
    data = request.get_json()
    if not data or not data.get('name') or not data.get('resume_id'):
        return jsonify({'error': '技能名称和简历ID为必填项'}), 400
    
    skill_id = execute_db(
        '''INSERT INTO skills (resume_id, name, level, color, category, order_num)
           VALUES (?, ?, ?, ?, ?, ?)''',
        [data.get('resume_id'), data.get('name'), data.get('level', 0),
         data.get('color', '#42b883'), data.get('category', ''), data.get('order', 0)]
    )
    return jsonify({'id': skill_id, 'message': '创建成功'}), 201


@app.route('/api/skills/<int:skill_id>', methods=['PUT'])
def update_skill(skill_id):
    """更新技能"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供更新数据'}), 400
    
    fields = []
    values = []
    field_map = {'name': 'name', 'level': 'level', 'color': 'color', 'category': 'category', 'order': 'order_num'}
    
    for key, db_field in field_map.items():
        if key in data:
            fields.append(f"{db_field} = ?")
            values.append(data[key])
    
    if not fields:
        return jsonify({'error': '没有要更新的字段'}), 400
    
    values.append(skill_id)
    execute_db(f"UPDATE skills SET {', '.join(fields)} WHERE id = ?", values)
    return jsonify({'message': '更新成功'})


@app.route('/api/skills/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    """删除技能"""
    execute_db('DELETE FROM skills WHERE id = ?', [skill_id])
    return jsonify({'message': '删除成功'})


@app.route('/api/skills/resume/<int:resume_id>')
def get_skills(resume_id):
    """获取简历技能"""
    skills = [row_to_dict(r) for r in query_db(
        'SELECT * FROM skills WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    return jsonify(skills)


@app.route('/api/stats/skills')
def get_skill_stats():
    """获取技能统计分布，支持按简历筛选"""
    resume_id = request.args.get('resume_id', type=int)
    if resume_id:
        skills = [row_to_dict(r) for r in query_db(
            'SELECT * FROM skills WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    else:
        skills = [row_to_dict(r) for r in query_db('SELECT * FROM skills ORDER BY order_num')]
    return jsonify(skills)


# ==================== 项目 CRUD ====================

@app.route('/api/projects', methods=['GET'])
def get_all_projects():
    """获取所有项目"""
    projects = [row_to_dict(r) for r in query_db('SELECT * FROM projects ORDER BY order_num')]
    for proj in projects:
        proj['tech_stack'] = json.loads(proj['tech_stack'] or '[]')
    return jsonify(projects)


@app.route('/api/projects', methods=['POST'])
def create_project():
    """创建项目"""
    data = request.get_json()
    if not data or not data.get('title') or not data.get('resume_id'):
        return jsonify({'error': '项目名称和简历ID为必填项'}), 400
    
    project_id = execute_db(
        '''INSERT INTO projects (resume_id, title, type, description, tech_stack, github_url, demo_url, is_featured, order_num)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        [data.get('resume_id'), data.get('title'), data.get('type', ''),
         data.get('description', ''), json.dumps(data.get('tech_stack', [])),
         data.get('github_url', ''), data.get('demo_url', ''),
         1 if data.get('is_featured') else 0, data.get('order', 0)]
    )
    return jsonify({'id': project_id, 'message': '创建成功'}), 201


@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """更新项目"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供更新数据'}), 400
    
    fields = []
    values = []
    field_map = {
        'title': 'title', 'type': 'type', 'description': 'description',
        'github_url': 'github_url', 'demo_url': 'demo_url', 'image_url': 'image_url',
        'is_featured': 'is_featured', 'order': 'order_num'
    }
    
    for key, db_field in field_map.items():
        if key in data:
            fields.append(f"{db_field} = ?")
            values.append(1 if data[key] else 0 if key == 'is_featured' else data[key])
    
    if 'tech_stack' in data:
        fields.append('tech_stack = ?')
        values.append(json.dumps(data['tech_stack']))
    
    if not fields:
        return jsonify({'error': '没有要更新的字段'}), 400
    
    values.append(project_id)
    execute_db(f"UPDATE projects SET {', '.join(fields)} WHERE id = ?", values)
    return jsonify({'message': '更新成功'})


@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """删除项目"""
    execute_db('DELETE FROM projects WHERE id = ?', [project_id])
    return jsonify({'message': '删除成功'})


@app.route('/api/projects/resume/<int:resume_id>')
def get_projects(resume_id):
    """获取简历项目"""
    projects = [row_to_dict(r) for r in query_db(
        'SELECT * FROM projects WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    for proj in projects:
        proj['tech_stack'] = json.loads(proj['tech_stack'] or '[]')
    return jsonify(projects)


# ==================== 工作经历 CRUD ====================

@app.route('/api/experiences', methods=['GET'])
def get_all_experiences():
    """获取所有工作经历"""
    experiences_raw = query_db('SELECT * FROM experiences ORDER BY order_num')
    experiences = []
    for exp in experiences_raw:
        exp_dict = row_to_dict(exp)
        exp_dict['details'] = json.loads(exp_dict['details'] or '[]')
        exp_dict['tech_stack'] = json.loads(exp_dict['tech_stack'] or '[]')
        experiences.append(exp_dict)
    return jsonify(experiences)


@app.route('/api/experiences', methods=['POST'])
def create_experience():
    """创建工作经历"""
    data = request.get_json()
    if not data or not data.get('position') or not data.get('company') or not data.get('resume_id'):
        return jsonify({'error': '职位、公司和简历ID为必填项'}), 400
    
    exp_id = execute_db(
        '''INSERT INTO experiences (resume_id, position, company, period, details, tech_stack, order_num)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        [data.get('resume_id'), data.get('position'), data.get('company'),
         data.get('period', ''), json.dumps(data.get('details', [])),
         json.dumps(data.get('tech_stack', [])), data.get('order', 0)]
    )
    return jsonify({'id': exp_id, 'message': '创建成功'}), 201


@app.route('/api/experiences/<int:exp_id>', methods=['PUT'])
def update_experience(exp_id):
    """更新工作经历"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供更新数据'}), 400
    
    fields = []
    values = []
    field_map = {
        'position': 'position', 'company': 'company', 'period': 'period', 'order': 'order_num'
    }
    
    for key, db_field in field_map.items():
        if key in data:
            fields.append(f"{db_field} = ?")
            values.append(data[key])
    
    if 'details' in data:
        fields.append('details = ?')
        values.append(json.dumps(data['details']))
    
    if 'tech_stack' in data:
        fields.append('tech_stack = ?')
        values.append(json.dumps(data['tech_stack']))
    
    if not fields:
        return jsonify({'error': '没有要更新的字段'}), 400
    
    values.append(exp_id)
    execute_db(f"UPDATE experiences SET {', '.join(fields)} WHERE id = ?", values)
    return jsonify({'message': '更新成功'})


@app.route('/api/experiences/<int:exp_id>', methods=['DELETE'])
def delete_experience(exp_id):
    """删除工作经历"""
    execute_db('DELETE FROM experiences WHERE id = ?', [exp_id])
    return jsonify({'message': '删除成功'})


@app.route('/api/experiences/resume/<int:resume_id>')
def get_experiences(resume_id):
    """获取工作经历"""
    experiences_raw = query_db(
        'SELECT * FROM experiences WHERE resume_id = ? ORDER BY order_num', [resume_id])
    experiences = []
    for exp in experiences_raw:
        exp_dict = row_to_dict(exp)
        exp_dict['details'] = json.loads(exp_dict['details'] or '[]')
        exp_dict['tech_stack'] = json.loads(exp_dict['tech_stack'] or '[]')
        experiences.append(exp_dict)
    return jsonify(experiences)


# ==================== 教育背景 CRUD ====================

@app.route('/api/educations', methods=['GET'])
def get_all_educations():
    """获取所有教育背景"""
    educations = [row_to_dict(r) for r in query_db('SELECT * FROM educations ORDER BY order_num')]
    return jsonify(educations)


@app.route('/api/educations', methods=['POST'])
def create_education():
    """创建教育背景"""
    data = request.get_json()
    if not data or not data.get('school') or not data.get('degree') or not data.get('resume_id'):
        return jsonify({'error': '学校、学历和简历ID为必填项'}), 400
    
    edu_id = execute_db(
        '''INSERT INTO educations (resume_id, school, degree, period, description, order_num)
           VALUES (?, ?, ?, ?, ?, ?)''',
        [data.get('resume_id'), data.get('school'), data.get('degree'),
         data.get('period', ''), data.get('description', ''), data.get('order', 0)]
    )
    return jsonify({'id': edu_id, 'message': '创建成功'}), 201


@app.route('/api/educations/<int:edu_id>', methods=['PUT'])
def update_education(edu_id):
    """更新教育背景"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供更新数据'}), 400
    
    fields = []
    values = []
    field_map = {
        'school': 'school', 'degree': 'degree', 'period': 'period',
        'description': 'description', 'order': 'order_num'
    }
    
    for key, db_field in field_map.items():
        if key in data:
            fields.append(f"{db_field} = ?")
            values.append(data[key])
    
    if not fields:
        return jsonify({'error': '没有要更新的字段'}), 400
    
    values.append(edu_id)
    execute_db(f"UPDATE educations SET {', '.join(fields)} WHERE id = ?", values)
    return jsonify({'message': '更新成功'})


@app.route('/api/educations/<int:edu_id>', methods=['DELETE'])
def delete_education(edu_id):
    """删除教育背景"""
    execute_db('DELETE FROM educations WHERE id = ?', [edu_id])
    return jsonify({'message': '删除成功'})


@app.route('/api/educations/resume/<int:resume_id>')
def get_educations(resume_id):
    """获取教育背景"""
    educations = [row_to_dict(r) for r in query_db(
        'SELECT * FROM educations WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    return jsonify(educations)


# ==================== 联系方式 CRUD ====================

@app.route('/api/contacts', methods=['GET'])
def get_all_contacts():
    """获取所有联系方式"""
    contacts = [row_to_dict(r) for r in query_db('SELECT * FROM contacts ORDER BY order_num')]
    return jsonify(contacts)


@app.route('/api/contacts', methods=['POST'])
def create_contact():
    """创建联系方式"""
    data = request.get_json()
    if not data or not data.get('type') or not data.get('value') or not data.get('resume_id'):
        return jsonify({'error': '类型、内容和简历ID为必填项'}), 400
    
    contact_id = execute_db(
        '''INSERT INTO contacts (resume_id, type, label, value, order_num)
           VALUES (?, ?, ?, ?, ?)''',
        [data.get('resume_id'), data.get('type'), data.get('label', ''),
         data.get('value'), data.get('order', 0)]
    )
    return jsonify({'id': contact_id, 'message': '创建成功'}), 201


@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """更新联系方式"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供更新数据'}), 400
    
    fields = []
    values = []
    field_map = {
        'type': 'type', 'label': 'label', 'value': 'value', 'order': 'order_num'
    }
    
    for key, db_field in field_map.items():
        if key in data:
            fields.append(f"{db_field} = ?")
            values.append(data[key])
    
    if not fields:
        return jsonify({'error': '没有要更新的字段'}), 400
    
    values.append(contact_id)
    execute_db(f"UPDATE contacts SET {', '.join(fields)} WHERE id = ?", values)
    return jsonify({'message': '更新成功'})


@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """删除联系方式"""
    execute_db('DELETE FROM contacts WHERE id = ?', [contact_id])
    return jsonify({'message': '删除成功'})


@app.route('/api/contacts/resume/<int:resume_id>')
def get_contacts(resume_id):
    """获取联系方式"""
    contacts = [row_to_dict(r) for r in query_db(
        'SELECT * FROM contacts WHERE resume_id = ? ORDER BY order_num', [resume_id])]
    return jsonify(contacts)


@app.route('/api/my/contacts')
def get_my_contacts():
    """获取当前用户激活简历的联系方式"""
    user = get_current_user()
    if not user:
        return jsonify({'error': '未登录'}), 401
    
    resume = query_db('SELECT id FROM resumes WHERE user_id = ? AND is_active = 1 LIMIT 1', [user['id']], one=True)
    if not resume:
        return jsonify([])
    
    contacts = [row_to_dict(r) for r in query_db(
        'SELECT * FROM contacts WHERE resume_id = ? ORDER BY order_num', [resume['id']])]
    return jsonify(contacts)


@app.route('/api/my/active-resume')
def get_my_active_resume():
    """获取当前用户的激活简历ID"""
    user = get_current_user()
    if not user:
        return jsonify({'error': '未登录'}), 401
    
    resume = query_db('SELECT id FROM resumes WHERE user_id = ? AND is_active = 1 LIMIT 1', [user['id']], one=True)
    if not resume:
        return jsonify({'error': '没有找到激活的简历'}), 404
    
    return jsonify({'id': resume['id']})


@app.route('/api/messages', methods=['POST'])
def create_message():
    """提交联系消息"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ('name', 'email', 'message')):
        return jsonify({'error': '请提供完整的联系信息'}), 400
    
    message_id = execute_db(
        'INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)',
        [data['name'], data['email'], data['message']]
    )
    
    return jsonify({
        'id': message_id,
        'name': data['name'],
        'email': data['email'],
        'message': data['message'],
        'is_read': False,
        'created_at': datetime.now().isoformat()
    }), 201


@app.route('/api/messages', methods=['GET'])
def get_messages():
    """获取消息列表"""
    messages = [row_to_dict(r) for r in query_db(
        'SELECT * FROM contact_messages ORDER BY created_at DESC')]
    return jsonify(messages)


@app.route('/api/messages/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    """删除留言"""
    execute_db('DELETE FROM contact_messages WHERE id = ?', [msg_id])
    return jsonify({'message': '删除成功'})


@app.route('/api/messages/<int:msg_id>/read', methods=['PUT'])
def mark_message_read(msg_id):
    """标记留言为已读"""
    execute_db('UPDATE contact_messages SET is_read = 1 WHERE id = ?', [msg_id])
    return jsonify({'message': '已标记为已读'})


# ==================== 用户认证 & 用户管理 ====================

# 内存中的 token 存储（生产环境应使用 Redis）
token_store = {}


def get_current_user():
    """获取当前登录用户"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header[7:]
    user_id = token_store.get(token)
    if not user_id:
        return None
    return query_db('SELECT * FROM users WHERE id = ?', [user_id], one=True)


def require_auth():
    """检查用户是否已登录"""
    user = get_current_user()
    if not user:
        return jsonify({'error': '未登录或登录已过期'}), 401
    return None


def require_admin():
    """检查用户是否为管理员"""
    user = get_current_user()
    if not user:
        return jsonify({'error': '未登录或登录已过期'}), 401
    if user['role'] != 'admin':
        return jsonify({'error': '权限不足，需要管理员权限'}), 403
    return None


@app.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供注册信息'}), 400

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    password = data.get('password', '')
    nickname = data.get('nickname', '').strip()

    # 验证必填字段
    if not username or not email or not password:
        return jsonify({'error': '用户名、邮箱和密码为必填项'}), 400

    # 验证密码长度
    if len(password) < 6:
        return jsonify({'error': '密码长度至少6位'}), 400

    # 验证邮箱格式
    import re
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({'error': '邮箱格式不正确'}), 400

    # 检查用户名是否已存在
    existing = query_db('SELECT id FROM users WHERE username = ?', [username], one=True)
    if existing:
        return jsonify({'error': '用户名已被注册'}), 400

    # 检查邮箱是否已存在
    existing = query_db('SELECT id FROM users WHERE email = ?', [email], one=True)
    if existing:
        return jsonify({'error': '邮箱已被注册'}), 400

    # 创建用户
    password_hash = generate_password_hash(password)
    user_id = execute_db(
        '''INSERT INTO users (username, email, phone, password_hash, nickname)
           VALUES (?, ?, ?, ?, ?)''',
        [username, email, phone, password_hash, nickname or username]
    )

    return jsonify({
        'message': '注册成功',
        'user': {
            'id': user_id,
            'username': username,
            'email': email,
            'nickname': nickname or username
        }
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供登录信息'}), 400

    username_or_email = data.get('username', '').strip()
    password = data.get('password', '')

    if not username_or_email or not password:
        return jsonify({'error': '用户名/邮箱和密码为必填项'}), 400

    # 支持用户名或邮箱登录
    user = query_db(
        'SELECT * FROM users WHERE username = ? OR email = ?',
        [username_or_email, username_or_email], one=True
    )

    if not user:
        return jsonify({'error': '用户不存在'}), 404

    if not check_password_hash(user['password_hash'], password):
        return jsonify({'error': '密码错误'}), 401

    if not user['is_active']:
        return jsonify({'error': '账号已被禁用'}), 403

    # 生成 token
    token = str(uuid.uuid4())
    token_store[token] = user['id']

    return jsonify({
        'message': '登录成功',
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'nickname': user['nickname'],
            'phone': user['phone'],
            'role': user['role'],
            'avatar': user['avatar']
        }
    })


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """用户登出"""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
        token_store.pop(token, None)
    return jsonify({'message': '登出成功'})


@app.route('/api/auth/me', methods=['GET'])
def get_current_user_info():
    """获取当前用户信息"""
    user = get_current_user()
    if not user:
        return jsonify({'error': '未登录'}), 401

    return jsonify({
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'nickname': user['nickname'],
        'phone': user['phone'],
        'role': user['role'],
        'avatar': user['avatar']
    })


@app.route('/api/auth/password', methods=['PUT'])
def change_password():
    """修改密码"""
    user = get_current_user()
    if not user:
        return jsonify({'error': '未登录'}), 401

    data = request.get_json()
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')

    if not old_password or not new_password:
        return jsonify({'error': '旧密码和新密码为必填项'}), 400

    if len(new_password) < 6:
        return jsonify({'error': '新密码长度至少6位'}), 400

    if not check_password_hash(user['password_hash'], old_password):
        return jsonify({'error': '旧密码错误'}), 401

    new_hash = generate_password_hash(new_password)
    execute_db('UPDATE users SET password_hash = ? WHERE id = ?', [new_hash, user['id']])
    return jsonify({'message': '密码修改成功'})


# ==================== 个人信息中心 ====================

@app.route('/api/profile', methods=['GET'])
def get_profile():
    """获取当前用户的个人信息"""
    user = get_current_user()
    if not user:
        return jsonify({'error': '未登录'}), 401
    
    profile = query_db('SELECT * FROM user_profiles WHERE user_id = ?', [user['id']], one=True)
    if not profile:
        return jsonify({
            'user_id': user['id'],
            'about_text': '',
            'photo_url': '',
            'years_exp': '0',
            'projects_count': '0',
            'articles_count': '0',
            'contributions_count': '0'
        })
    
    return jsonify(row_to_dict(profile))


@app.route('/api/profile', methods=['PUT'])
def update_profile():
    """更新当前用户的个人信息"""
    user = get_current_user()
    if not user:
        return jsonify({'error': '未登录'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供更新数据'}), 400
    
    # 检查是否已存在记录
    existing = query_db('SELECT id FROM user_profiles WHERE user_id = ?', [user['id']], one=True)
    
    if existing:
        # 更新
        fields = []
        values = []
        field_map = {
            'about_text': 'about_text',
            'photo_url': 'photo_url',
            'years_exp': 'years_exp',
            'projects_count': 'projects_count',
            'articles_count': 'articles_count',
            'contributions_count': 'contributions_count'
        }
        
        for key, db_field in field_map.items():
            if key in data:
                fields.append(f"{db_field} = ?")
                values.append(data[key])
        
        if not fields:
            return jsonify({'error': '没有要更新的字段'}), 400
        
        values.append(user['id'])
        execute_db(f"UPDATE user_profiles SET {', '.join(fields)} WHERE user_id = ?", values)
    else:
        # 创建
        execute_db(
            '''INSERT INTO user_profiles (user_id, about_text, photo_url, years_exp, projects_count, articles_count, contributions_count)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            [user['id'], data.get('about_text', ''), data.get('photo_url', ''),
             data.get('years_exp', '0'), data.get('projects_count', '0'),
             data.get('articles_count', '0'), data.get('contributions_count', '0')]
        )
    
    return jsonify({'message': '保存成功'})


@app.route('/api/public/profile/<int:user_id>')
def get_public_profile(user_id):
    """公开访问：获取用户个人信息"""
    profile = query_db('SELECT * FROM user_profiles WHERE user_id = ?', [user_id], one=True)
    if not profile:
        return jsonify({'error': '个人信息不存在'}), 404
    
    return jsonify(row_to_dict(profile))


# ==================== 用户管理（管理员） ====================

@app.route('/api/users', methods=['GET'])
def get_users():
    """获取所有用户（管理员）"""
    result = require_admin()
    if result:
        return result

    users = [row_to_dict(r) for r in query_db(
        'SELECT id, username, email, phone, nickname, avatar, role, is_active, created_at FROM users ORDER BY id DESC')]
    return jsonify(users)


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用户信息（管理员）"""
    result = require_admin()
    if result:
        return result

    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供更新数据'}), 400

    fields = []
    values = []
    field_map = {
        'nickname': 'nickname',
        'phone': 'phone',
        'role': 'role',
        'is_active': 'is_active'
    }

    for key, db_field in field_map.items():
        if key in data:
            fields.append(f"{db_field} = ?")
            values.append(1 if data[key] else 0 if key == 'is_active' else data[key])

    if not fields:
        return jsonify({'error': '没有要更新的字段'}), 400

    values.append(user_id)
    execute_db(f"UPDATE users SET {', '.join(fields)} WHERE id = ?", values)
    return jsonify({'message': '更新成功'})


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户（管理员）"""
    result = require_admin()
    if result:
        return result

    # 不能删除自己
    current = get_current_user()
    if current and current['id'] == user_id:
        return jsonify({'error': '不能删除当前登录用户'}), 400

    execute_db('DELETE FROM users WHERE id = ?', [user_id])
    return jsonify({'message': '删除成功'})


@app.route('/api/docs')
def api_docs():
    """API 文档"""
    return jsonify({
        'api_endpoints': [
            {'method': 'POST', 'path': '/api/auth/register', 'description': '用户注册'},
            {'method': 'POST', 'path': '/api/auth/login', 'description': '用户登录'},
            {'method': 'POST', 'path': '/api/auth/logout', 'description': '用户登出'},
            {'method': 'GET', 'path': '/api/auth/me', 'description': '获取当前用户信息'},
            {'method': 'PUT', 'path': '/api/auth/password', 'description': '修改密码'},
            {'method': 'GET', 'path': '/api/users', 'description': '获取所有用户（管理员）'},
            {'method': 'PUT', 'path': '/api/users/<id>', 'description': '更新用户（管理员）'},
            {'method': 'DELETE', 'path': '/api/users/<id>', 'description': '删除用户（管理员）'},
            {'method': 'GET', 'path': '/api/resumes', 'description': '获取所有简历'},
            {'method': 'POST', 'path': '/api/resumes', 'description': '创建简历'},
            {'method': 'GET', 'path': '/api/resumes/<id>', 'description': '获取简历详情'},
            {'method': 'PUT', 'path': '/api/resumes/<id>', 'description': '更新简历'},
            {'method': 'DELETE', 'path': '/api/resumes/<id>', 'description': '删除简历'},
            {'method': 'GET', 'path': '/api/resumes/active', 'description': '获取激活的完整简历'},
            {'method': 'GET', 'path': '/api/skills', 'description': '获取所有技能'},
            {'method': 'POST', 'path': '/api/skills', 'description': '创建技能'},
            {'method': 'PUT', 'path': '/api/skills/<id>', 'description': '更新技能'},
            {'method': 'DELETE', 'path': '/api/skills/<id>', 'description': '删除技能'},
            {'method': 'GET', 'path': '/api/projects', 'description': '获取所有项目'},
            {'method': 'POST', 'path': '/api/projects', 'description': '创建项目'},
            {'method': 'PUT', 'path': '/api/projects/<id>', 'description': '更新项目'},
            {'method': 'DELETE', 'path': '/api/projects/<id>', 'description': '删除项目'},
            {'method': 'GET', 'path': '/api/experiences', 'description': '获取所有工作经历'},
            {'method': 'POST', 'path': '/api/experiences', 'description': '创建工作经历'},
            {'method': 'PUT', 'path': '/api/experiences/<id>', 'description': '更新工作经历'},
            {'method': 'DELETE', 'path': '/api/experiences/<id>', 'description': '删除工作经历'},
            {'method': 'POST', 'path': '/api/messages', 'description': '提交联系消息'},
            {'method': 'GET', 'path': '/api/messages', 'description': '获取消息列表'}
        ]
    })


# ==================== 启动应用 ====================
if __name__ == '__main__':
    print("启动 Flask 服务...")
    print("访问地址: http://localhost:8000")
    print("API 文档: http://localhost:8000/api/docs")
    app.run(host='0.0.0.0', port=8000, debug=True)
