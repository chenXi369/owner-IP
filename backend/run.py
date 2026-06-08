"""
启动脚本 - 使用 Flask 开发服务器
"""
from app_flask import app

if __name__ == '__main__':
    print("启动简历管理系统 API 服务...")
    print("访问地址: http://localhost:8000")
    print("API 文档: http://localhost:8000/api/docs")
    print("按 Ctrl+C 停止服务")
    
    app.run(host='0.0.0.0', port=8000, debug=False)
