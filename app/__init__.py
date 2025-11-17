"""
Alliance Management System - Flask Application
Initialize Flask app with database and authentication
"""
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

# Environment variables
APP_NAME = os.getenv("APP_NAME", "Alliance Management System")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key-change-in-production")

# Create Flask app
app = Flask(__name__)

# Configure Flask app
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alliance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT configuration
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)  # 2 hour session

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'web_login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

from app import routes, models

# Flask-Login user loader
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

# JWT token blocklist callback
from app.models import TokenBlocklist

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """Check if token is in blocklist"""
    jti = jwt_payload['jti']
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None

# Register auth blueprint
from app.auth import auth_bp
app.register_blueprint(auth_bp)

# Exempt auth routes from CSRF
csrf.exempt(auth_bp)
