from flask import Flask
import os
from .models import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-secret-key-123')
    
    # 確保資料夾存在並初始化資料庫
    with app.app_context():
        init_db()
        
    # 註冊藍圖路由
    from .routes import bp
    app.register_blueprint(bp)
    
    return app
