# app.py
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

from flask import (
    Flask, render_template, request, redirect, url_for, flash
)
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)

# Local imports
from db import db
from models import User, Project, Task

# Initialize Flask app
app = Flask(__name__, static_folder='assets')


# Load configuration from config.py
# Heroku will provide its own DATABASE_URL.
# The dotenv will handle local environment variables.
app.config.from_object('config.Config')

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
    """Renders the user dashboard with their projects."""
    user_projects = Project.query.filter_by(
        owner=current_user).order_by(Project.created_at.desc()).all()
    return render_template("dashboard.html", projects=user_projects)


# Add Project route
@app.route("/add_project", methods=["GET", "POST"])
@login_required
def add_project():
    """Handles adding a new project for the current user."""
    if request.method == "POST":
        # Get data from the form
        name_from_form = request.form.get("name")
        description_from_form = request.form.get("description")

        # --- VALIDATION ---
        if not name_from_form:
            flash("Project name is required.", "danger")
            return redirect(url_for("add_project"))

        # Create a new Project object
        new_project = Project(
            name=name_from_form,
            description=description_from_form,
            owner=current_user
        )

        # Add the new project to the database
        db.session.add(new_project)
        db.session.commit()

        flash("Project created successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_project.html")


# Route to edit an existing project
@app.route("/edit_project/<int:project_id>", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    """
    Handles editing an existing project.
    """
    project = Project.query.get_or_404(project_id)

    # Ensure only the owner can edit the project
    if project.owner != current_user:
        flash("You do not have permission to edit this project.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == "POST":
        new_name = request.form.get("name")
        new_description = request.form.get("description")

        # --- VALIDATION ---
        if not new_name:
            flash("Project name is required.", "danger")
            return redirect(url_for('edit_project', project_id=project.id))

        project.name = new_name
        project.description = new_description
        db.session.commit()
        flash("Project updated successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template("edit_project.html", project=project)


# Project Details route
@app.route("/projects/<int:project_id>")
@login_required
def project_details(project_id):
    """Displays the details of a single project."""
    project = Project.query.get_or_404(project_id)
    # Ensure that only the owner can view their project details
    if project.owner != current_user:
        flash("You do not have permission to view this project.", "danger")
        return redirect(url_for('dashboard'))

    # Filter tasks by their status and attach them directly to the project object
    project.tasks_to_do = Task.query.filter_by(project=project, status="To Do").order_by(Task.due_date).all()
    project.tasks_in_progress = Task.query.filter_by(project=project, status="In Progress").order_by(Task.due_date).all()
    project.tasks_done = Task.query.filter_by(project=project, status="Done").order_by(Task.due_date).all()

    return render_template(
        "project_details.html",
        project=project
    )


# Project Delete route
@app.route("/delete_project/<int:project_id>", methods=["POST"])
@login_required
def delete_project(project_id):
    """Deletes a project from the database."""
    project = Project.query.get_or_404(project_id)

    # Ensure only the owner can delete the project
    if project.owner != current_user:
        flash("You do not have permission to delete this project.", "danger")
        return redirect(url_for("dashboard"))

    try:
        # Delete all tasks associated with the project first
        # to avoid a foreign key constraint error.
        for task in project.tasks.all():
            db.session.delete(task)

        # Now delete the project itself
        db.session.delete(project)
        db.session.commit()

        flash(f"Project '{project.name}' and its tasks have been deleted.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while deleting the project: {e}", "danger")

    return redirect(url_for("dashboard"))


# Add Task route
@app.route("/projects/<int:project_id>/add_task", methods=["GET", "POST"])
@login_required
def add_task(project_id):
    """
    Handles adding a new task to a specific project.
    """
    project = Project.query.get_or_404(project_id)
    # Fetch all users to populate the assignee dropdown
    users = User.query.order_by(User.username).all()

    # Ensure only the owner can add tasks to the project
    if project.owner != current_user:
        flash("You do not have permission to add a task to this project.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == "POST":
        # Get data from the form
        title = request.form.get("title")
        description = request.form.get("description")
        due_date_str = request.form.get("due_date")
        status = request.form.get("status")
        priority = request.form.get("priority")
        assigned_to_id = request.form.get("assigned_to_id")

        # --- VALIDATION ---
        if not title:
            flash("Task title is required.", "danger")
            return redirect(url_for("add_task", project_id=project.id))

        # Convert due_date string to a datetime object, if it exists
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

        # Get the assigned user object based on the ID from the form
        assigned_to = User.query.get(assigned_to_id)

        # Create a new Task object
        new_task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            project=project,
            assignee=assigned_to
        )

        db.session.add(new_task)
        db.session.commit()

        flash("Task created successfully!", "success")
        return redirect(url_for('project_details', project_id=project.id))

    return render_template("add_task.html", project=project, users=users)


# Edit Task route
@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    """
    Handles editing an existing task.
    """
    task = Task.query.get_or_404(task_id)
    # Fetch all users to populate the assignee dropdown
    users = User.query.order_by(User.username).all()

    # Ensure only the assignee or project owner can edit the task
    if task.assignee != current_user and task.project.owner != current_user:
        flash("You do not have permission to edit this task.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == "POST":
        # Update the task object with form data
        task.title = request.form.get("title")
        task.description = request.form.get("description")
        due_date_str = request.form.get("due_date")
        task.status = request.form.get("status")
        task.priority = request.form.get("priority")
        assigned_to_id = request.form.get("assigned_to_id")

        # --- VALIDATION ---
        if not task.title:
            flash("Task title is required.", "danger")
            return redirect(url_for("edit_task", task_id=task.id))

        # Convert due_date string to a datetime object, if it exists
        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

        # Update the assignee
        task.assignee = User.query.get(assigned_to_id)

        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for('project_details', project_id=task.project.id))

    return render_template("edit_task.html", task=task, users=users)


# Delete Task route
@app.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    """Deletes a task from the database."""
    task = Task.query.get_or_404(task_id)

    # Ensure only the assignee or project owner can delete the task
    if task.assignee != current_user and task.project.owner != current_user:
        flash("You do not have permission to delete this task.", "danger")
        return redirect(url_for("dashboard"))

    # Get the project_id before deleting the task
    project_id = task.project.id

    try:
        db.session.delete(task)
        db.session.commit()
        flash(f"Task '{task.title}' has been deleted.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while deleting the task: {e}", "danger")

    return redirect(url_for('project_details', project_id=project_id))


# User Profile route
@app.route("/profile")
@login_required
def profile():
    """Displays the current user's profile page."""
    return render_template("profile.html", user=current_user)


# Change Password route
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """
    Handles changing the current user's password.
    """
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")

        # Check if the current password is correct
        if not current_user.check_password(current_password):
            flash("Incorrect current password.", "danger")
            return redirect(url_for('change_password'))

        # Check if the new passwords match
        if new_password != confirm_new_password:
            flash("New passwords do not match.", "danger")
            return redirect(url_for('change_password'))

        # Check if new password is not the same as current one
        if current_user.check_password(new_password):
            flash("New password cannot be the same as the old password.", "danger")
            return redirect(url_for('change_password'))

        # Update the password
        current_user.set_password(new_password)
        db.session.commit()

        flash("Your password has been changed successfully.", "success")
        return redirect(url_for('profile'))

    return render_template("change_password.html")


# Edit Profile route
@app.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    """
    Handles editing the current user's profile.
    """
    if request.method == "POST":
        new_username = request.form.get("username")
        new_email = request.form.get("email")

        # --- VALIDATION ---
        if not new_username or not new_email:
            flash("Username and Email are required.", "danger")
            return redirect(url_for("edit_profile"))

        # Check for existing username or email, but allow the current user's own.
        existing_user_by_username = User.query.filter(User.username == new_username, User.id != current_user.id).first()
        existing_user_by_email = User.query.filter(User.email == new_email, User.id != current_user.id).first()

        if existing_user_by_username:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for("edit_profile"))

        if existing_user_by_email:
            flash("Email already exists. Please choose a different one.", "danger")
            return redirect(url_for("edit_profile"))

        # Update the user's information
        current_user.username = new_username
        current_user.email = new_email
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("edit_profile.html", user=current_user)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
