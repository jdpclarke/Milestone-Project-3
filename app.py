# app.py
import os
from dotenv import load_dotenv
load_dotenv()

from flask import (
    Flask, render_template, request, redirect, url_for, flash
)
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Local imports
from db import db
from models import User

# Initialize Flask app
app = Flask(__name__)


# Load configuration from config.py
app.config.from_object('config.Config')


# Initialize SQLAlchemy
db.init_app(app)


# Initialize Flask-Login (will be used later for user management)
login_manager = LoginManager()
login_manager.init_app(app)
# Redirect to login page if user tries to access a protected route
login_manager.login_view = 'login'


# User Loader
@login_manager.user_loader
def load_user(user_id):
    """
    Given a user ID, return the corresponding User object.
    This function is required by Flask-Login.
    """
    return User.query.get(int(user_id))


# --- Routes ---

# Define a simple index route for the main page
@app.route("/")
def index():
    """Renders the main index page."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


# User registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles user registration.
    Displays the registration form on GET request.
    Processes the form data and creates a new user on POST request.
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username_from_form = request.form.get("username")
        email_from_form = request.form.get("email")
        password_from_form = request.form.get("password")

        existing_user_by_username = User.query.filter_by(
            username=username_from_form).first()
        existing_user_by_email = User.query.filter_by(
            email=email_from_form).first()

        if existing_user_by_username or existing_user_by_email:
            flash("Username or Email already exists. Please choose a different one.",
                  "danger")
            return redirect(url_for("register"))

        new_user = User(
            username=username_from_form,
            email=email_from_form
        )
        new_user.set_password(password_from_form)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# User login route
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login.
    Displays the login form on GET request.
    Validates credentials and logs in the user on POST request.
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username_from_form = request.form.get("username")
        password_from_form = request.form.get("password")

        user = User.query.filter_by(username=username_from_form).first()

        if user and user.check_password(password_from_form):
            login_user(user)
            flash(f"Logged in successfully as {user.username}.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))
        else:
            flash("Login Unsuccessful. Please check username and password.",
                  "danger")

    return render_template("login.html")


# User logout route
@app.route("/logout")
@login_required
def logout():
    """Logs out the current user."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


# Dashboard route
@app.route("/dashboard")
@login_required
def dashboard():
    """Renders the user dashboard."""
    return render_template("dashboard.html")


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
