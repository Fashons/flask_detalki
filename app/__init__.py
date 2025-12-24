from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name='default'):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    # Импорт blueprint'ов
    from app.controller.main_controller import bp as main_bp
    from app.controller.equipment_controller import bp as equipment_bp
    from app.controller.auth_controller import bp as auth_bp
    from app.controller.users_controller import bp as users_bp

    # Регистрация blueprint'ов
    app.register_blueprint(main_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.model.user import User
    return User.query.get(int(user_id))