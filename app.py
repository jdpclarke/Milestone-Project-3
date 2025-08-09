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

# After the index route, add the register and login routes
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        # Redirect to the dashboard if the user is already logged in
        return redirect(url_for("index"))

    if request.method == "POST":
        # Get data from the registration form
        username_from_form = request.form.get("username")
        email_from_form = request.form.get("email")
        password_from_form = request.form.get("password")

        # Check if username or email already exists
        existing_user_by_username = User.query.filter_by(username=username_from_form).first()
        existing_user_by_email = User.query.filter_by(email=email_from_form).first()
        if existing_user_by_username or existing_user_by_email:
            flash("Username or Email already exists. Please choose a different one.", "danger")
            return redirect(url_for("register"))

        # Hash the password for security using Flask-Bcrypt
        hashed_password = bcrypt.generate_password_hash(password_from_form).decode("utf-8")

        # Create a new User object
        new_user = User(
            username=username_from_form,
            email=email_from_form,
            password_hash=hashed_password,
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Flash a success message and redirect to the login page
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
