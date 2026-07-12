"""
AI Resume Analyzer & Career Coach - backend package
Holds the shared SQLAlchemy db instance and login manager so that
models, blueprints, and app.py can all import from one place without
circular imports.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to continue."
login_manager.login_message_category = "warning"
