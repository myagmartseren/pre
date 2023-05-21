from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
