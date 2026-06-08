# 简历管理系统后端 API

基于 Flask 和 SQLite 开发的简历管理系统后端服务。

## 功能特性

- 📄 **简历管理**: 完整的简历 CRUD 操作
- 🎯 **技能管理**: 技能展示和分类管理
- 🚀 **项目管理**: 项目作品展示和管理
- 💼 **工作经历**: 工作经历时间线管理
- 🎓 **教育背景**: 教育背景信息管理
- 📧 **联系方式**: 多种联系方式管理
- 💬 **消息系统**: 访客留言管理

## 技术栈

- **Web框架**: Flask 3.0.0
- **数据库**: SQLite (通过 Flask-SQLAlchemy)
- **CORS**: Flask-CORS
- **数据验证**: Pydantic

## 项目结构

```
backend/
├── app_flask.py          # Flask 应用主文件
├── run.py                # 生产环境启动脚本
├── init_db_raw.py        # 数据库初始化脚本
├── requirements.txt      # 依赖包
└── README.md             # 项目文档
```

## 快速开始

### 1. 环境准备

确保已安装 Python 3.9+

### 2. 安装依赖

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt
```

### 3. 初始化数据库

```bash
# 运行初始化脚本,创建示例数据
python init_db_raw.py
```

### 4. 启动服务

```bash
# 生产模式（推荐，无警告）
python run.py

# 开发模式（有警告，但支持热重载）
python app_flask.py
```

服务启动后访问:
- API 文档: http://localhost:8000/api/docs
- 完整简历: http://localhost:8000/api/resumes/active

## API 接口说明

### 公开接口

#### 简历相关
- `GET /api/resumes/active` - 获取激活的完整简历
- `GET /api/resumes/<id>` - 获取指定简历详情

#### 技能相关
- `GET /api/skills/resume/<id>` - 获取简历技能

#### 项目相关
- `GET /api/projects/resume/<id>` - 获取简历项目

#### 工作经历相关
- `GET /api/experiences/resume/<id>` - 获取工作经历

#### 教育背景相关
- `GET /api/educations/resume/<id>` - 获取教育背景

#### 联系方式相关
- `GET /api/contacts/resume/<id>` - 获取联系方式

#### 消息相关
- `POST /api/messages` - 提交联系消息
- `GET /api/messages` - 获取消息列表

## 数据库说明

项目使用 SQLite 数据库,数据库文件为 `resume.db`。

### 数据表

- **resumes**: 简历基本信息
- **skills**: 技能信息
- **projects**: 项目作品
- **experiences**: 工作经历
- **educations**: 教育背景
- **contacts**: 联系方式
- **contact_messages**: 联系消息

## 扩展说明

该后端 API 设计为可扩展的简历管理系统基础:

1. **多简历支持**: 可创建多份简历
2. **模板系统**: 可扩展简历模板功能
3. **导出功能**: 可添加 PDF/Word 导出功能
4. **统计分析**: 可添加访问统计和分析功能

### 建议的扩展方向

- 添加用户认证和授权系统
- 添加简历模板系统
- 实现简历导出为 PDF/Word
- 添加访问统计和分析
- 实现简历分享功能
- 添加在线编辑器
- 实现多语言支持

## 许可证

MIT License
