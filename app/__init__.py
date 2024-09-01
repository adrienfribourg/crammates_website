from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure debug mode is active
    app.config['DEBUG'] = True  # Enforce debug mode

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app

@login.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))