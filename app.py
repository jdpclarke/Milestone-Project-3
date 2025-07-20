import os
from dotenv import load_dotenv
load_dotenv()

from flask import (
    Flask, render_template, request, redirect, url_for, flash
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# Initialize Flask app
app = Flask(__name__)


# Load configuration from config.py
app.config.from_object('config.Config')


# Initialize SQLAlchemy (will be used later for models)
db = SQLAlchemy(app)


# Initialize Flask-Login (will be used later for user management)
login_manager = LoginManager()
login_manager.init_app(app)
# Redirect to login page if user tries to access a protected route
login_manager.login_view = 'login'


# Dummy User Loader (will be replaced with actual database query later)
# This is required by Flask-Login even if we don't have a User model yet
class User(UserMixin):
    def get_id(self):
        return "1"  # Return a dummy ID for now


@login_manager.user_loader
def load_user(user_id):
    # In a real app, this would query your database for a user by ID
    # For now, we'll just return a dummy user if it's the dummy ID
    if user_id == "1":
        return User()
    return None


# --- Routes ---

@app.route('/')
def index():
    return "<h1>Hello, CheckMate! Your Flask app is running!</h1>"


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
