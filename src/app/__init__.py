from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config

# Initialize the Flask extensions
db = SQLAlchemy()
login = LoginManager()

def create_app():
    # Create the Flask application instance
    app = Flask(__name__)

    # Load the application configuration
    app.config.from_object(Config)
    # app.file_service = file_service

    # Initialize the Flask extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login.init_app(app)

    # Register the blueprints
    from app.views.users import users_bp
    from app.views.files import files_bp
    from app.auth import auth_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(auth_bp)

    # Register services
    from app.services.user_service import UserService
    app.user_service = UserService()

    # Register error handlers
    return app
