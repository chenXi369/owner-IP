"""
数据库初始化脚本 (使用原生 sqlite3)
创建示例简历数据
"""
import sqlite3
import json
from datetime import datetime
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), "resume.db")


def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建表
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            title VARCHAR(200) NOT NULL,
            greeting VARCHAR(200) DEFAULT '你好,我是',
            description TEXT NOT NULL,
            avatar_url VARCHAR(500),
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER NOT NULL,
            name VARCHAR(100) NOT NULL,
            level INTEGER DEFAULT 0,
            color VARCHAR(50) DEFAULT '#42b883',
            category VARCHAR(100),
            order_num INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resumes (id)
        );
        
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER NOT NULL,
            title VARCHAR(200) NOT NULL,
            type VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            tech_stack TEXT DEFAULT '[]',
            github_url VARCHAR(500),
            demo_url VARCHAR(500),
            image_url VARCHAR(500),
            is_featured BOOLEAN DEFAULT 0,
            order_num INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resumes (id)
        );
        
        CREATE TABLE IF NOT EXISTS experiences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER NOT NULL,
            position VARCHAR(200) NOT NULL,
            company VARCHAR(200) NOT NULL,
            period VARCHAR(100) NOT NULL,
            details TEXT DEFAULT '[]',
            tech_stack TEXT DEFAULT '[]',
            order_num INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resumes (id)
        );
        
        CREATE TABLE IF NOT EXISTS educations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER NOT NULL,
            school VARCHAR(200) NOT NULL,
            degree VARCHAR(200) NOT NULL,
            period VARCHAR(100) NOT NULL,
            description TEXT,
            order_num INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resumes (id)
        );
        
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER NOT NULL,
            type VARCHAR(50) NOT NULL,
            label VARCHAR(100) NOT NULL,
            value VARCHAR(500) NOT NULL,
            icon VARCHAR(100),
            order_num INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resumes (id)
        );
        
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            phone VARCHAR(20),
            password_hash VARCHAR(256) NOT NULL,
            nickname VARCHAR(100),
            avatar VARCHAR(500),
            role VARCHAR(20) DEFAULT 'user',
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    print("数据库表创建完成")
    
    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM resumes")
    count = cursor.fetchone()[0]
    
    # 创建默认管理员（如果不存在）
    from werkzeug.security import generate_password_hash
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    admin_count = cursor.fetchone()[0]
    if admin_count == 0:
        cursor.execute("""
            INSERT INTO users (username, email, phone, password_hash, nickname, role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("admin", "admin@example.com", "13800138000",
              generate_password_hash("admin123"), "管理员", "admin"))
        print("创建默认管理员: admin / admin123")
    
    if count > 0:
        print("数据库已存在简历数据,跳过简历初始化")
        conn.commit()
        conn.close()
        return
    
    # 插入示例简历
    cursor.execute("""
        INSERT INTO resumes (name, title, greeting, description, is_active)
        VALUES (?, ?, ?, ?, ?)
    """, ("前端小李", "全栈开发工程师 & 3D可视化专家", "你好,我是",
          "专注于创建卓越用户体验的全栈开发工程师,热爱Three.js 3D可视化与创意交互设计", 1))
    resume_id = cursor.lastrowid
    print(f"创建示例简历: 前端小李 (ID: {resume_id})")
    
    # 插入技能
    skills = [
        (resume_id, "Vue.js", 95, "#42b883", 1),
        (resume_id, "React", 90, "#61dafb", 2),
        (resume_id, "Three.js", 85, "#ff6b6b", 3),
        (resume_id, "TypeScript", 88, "#3178c6", 4),
        (resume_id, "Node.js", 82, "#68a063", 5),
        (resume_id, "WebGL", 78, "#9b59b6", 6),
    ]
    cursor.executemany("""
        INSERT INTO skills (resume_id, name, level, color, order_num)
        VALUES (?, ?, ?, ?, ?)
    """, skills)
    print(f"创建示例技能: {len(skills)}个")
    
    # 插入项目
    projects = [
        (resume_id, "3D数据可视化平台", "全栈项目",
         "基于Three.js开发的企业级3D数据可视化平台,支持实时数据展示、交互式图表和自定义场景编辑。",
         json.dumps(["Vue.js", "Three.js", "Node.js", "MongoDB"]), 1, 1),
        (resume_id, "电商管理系统", "前端项目",
         "功能完善的电商后台管理系统,包含商品管理、订单处理、数据分析等核心模块。",
         json.dumps(["React", "TypeScript", "Ant Design", "Redux"]), 1, 2),
        (resume_id, "创意作品集网站", "前端项目",
         "个人作品集网站,使用Nuxt.js和Three.js打造沉浸式3D交互体验。",
         json.dumps(["Nuxt.js", "Three.js", "GSAP", "SCSS"]), 0, 3),
        (resume_id, "实时协作工具", "全栈项目",
         "支持多人实时协作的在线白板工具,包含画笔、图形、文本等多种编辑功能。",
         json.dumps(["Vue.js", "Socket.io", "Canvas", "Node.js"]), 0, 4),
    ]
    cursor.executemany("""
        INSERT INTO projects (resume_id, title, type, description, tech_stack, is_featured, order_num)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, projects)
    print(f"创建示例项目: {len(projects)}个")
    
    # 插入工作经历
    experiences = [
        (resume_id, "高级前端工程师", "某科技公司", "2022.03 - 至今",
         json.dumps([
             "负责公司核心产品的前端架构设计与开发",
             "主导3D可视化模块的技术选型与实现",
             "优化前端性能,页面加载速度提升40%",
             "带领5人团队完成多个重要项目交付"
         ]),
         json.dumps(["Vue.js", "Three.js", "TypeScript", "Node.js"]), 1),
        (resume_id, "前端开发工程师", "某互联网公司", "2020.06 - 2022.02",
         json.dumps([
             "参与电商平台前端开发,负责商品展示和购物车模块",
             "开发数据可视化大屏,实现实时数据展示",
             "编写前端组件库,提升团队开发效率"
         ]),
         json.dumps(["React", "Redux", "ECharts", "Webpack"]), 2),
        (resume_id, "初级前端工程师", "某创业公司", "2019.07 - 2020.05",
         json.dumps([
             "负责公司官网和后台管理系统的开发",
             "学习并实践Vue.js框架",
             "参与移动端H5页面开发"
         ]),
         json.dumps(["Vue.js", "JavaScript", "CSS3", "jQuery"]), 3),
    ]
    cursor.executemany("""
        INSERT INTO experiences (resume_id, position, company, period, details, tech_stack, order_num)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, experiences)
    print(f"创建示例工作经历: {len(experiences)}个")
    
    # 插入教育背景
    cursor.execute("""
        INSERT INTO educations (resume_id, school, degree, period, order_num)
        VALUES (?, ?, ?, ?, ?)
    """, (resume_id, "某知名大学", "计算机科学与技术 · 本科", "2015.09 - 2019.06", 1))
    print("创建示例教育背景: 1个")
    
    # 插入联系方式
    contacts = [
        (resume_id, "email", "邮箱", "example@email.com", 1),
        (resume_id, "phone", "电话", "+86 123 4567 8900", 2),
        (resume_id, "address", "地址", "中国 · 北京", 3),
    ]
    cursor.executemany("""
        INSERT INTO contacts (resume_id, type, label, value, order_num)
        VALUES (?, ?, ?, ?, ?)
    """, contacts)
    print(f"创建示例联系方式: {len(contacts)}个")
    
    conn.commit()
    conn.close()
    print("\n数据库初始化完成!")
    print(f"数据库文件: {DB_PATH}")


if __name__ == "__main__":
    init_db()
