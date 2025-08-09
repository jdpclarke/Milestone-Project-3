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

from models import User


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


# User Loader
@login_manager.user_loader
def load_user(user_id):
    # The User.query.get() method is a Flask-SQLAlchemy shortcut
    # to get a record by its primary key (ID).
    return User.query.get(int(user_id))


# --- Routes ---

@app.route('/')
def index():
    return "<h1>Hello, CheckMate! Your Flask app is running!</h1>"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
