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

@app.route("/")
def index():
    """Home page route."""
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Handles user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Basic validation
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("register"))

        # Check if user already exists
        if User.query.filter_by(username=username).first() or \
           User.query.filter_by(email=email).first():
            flash("Username or Email already exists.", "danger")
            return redirect(url_for("register"))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles user login."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Logs out the current user."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    """Displays the user's projects."""
    projects = current_user.projects.all()
    return render_template("dashboard.html", projects=projects)


@app.route("/add_project", methods=["GET", "POST"])
@login_required
def add_project():
    """Handles adding a new project."""
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if not name:
            flash("Project name is required.", "danger")
            return redirect(url_for("add_project"))

        # Create new project and link it to the current user
        new_project = Project(
            name=name, description=description, owner=current_user
        )

        # Add the creator to the project members automatically
        new_project.members.append(current_user)

        db.session.add(new_project)
        db.session.commit()
        flash("Project added successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_project.html")


@app.route("/project/<int:project_id>")
@login_required
def project_details(project_id):
    """Displays details for a specific project."""
    # Ensure the project exists and the current user is a member
    project = Project.query.get_or_404(project_id)
    if current_user not in project.members:
        flash("You do not have access to this project.", "danger")
        return redirect(url_for('dashboard'))

    # Separate tasks into their respective statuses
    tasks_todo = project.tasks.filter_by(status='To Do').all()
    tasks_in_progress = project.tasks.filter_by(status='In Progress').all()
    tasks_done = project.tasks.filter_by(status='Done').all()

    return render_template(
        "project_details.html",
        project=project,
        tasks_todo=tasks_todo,
        tasks_in_progress=tasks_in_progress,
        tasks_done=tasks_done
    )


@app.route("/edit_project/<int:project_id>", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    """Handles editing an existing project."""
    project = Project.query.get_or_404(project_id)
    if project.owner != current_user:
        flash("You do not have permission to edit this project.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        project.name = request.form.get("name")
        project.description = request.form.get("description")
        db.session.commit()
        flash("Project updated successfully!", "success")
        return redirect(url_for("project_details", project_id=project.id))

    return render_template("edit_project.html", project=project)


@app.route("/delete_project/<int:project_id>", methods=["POST"])
@login_required
def delete_project(project_id):
    """Handles deleting a project."""
    project = Project.query.get_or_404(project_id)
    if project.owner != current_user:
        flash("You do not have permission to delete this project.", "danger")
        return redirect(url_for("dashboard"))

    # Delete all tasks associated with the project first
    Task.query.filter_by(project_id=project.id).delete()
    # Remove all members from the project
    project.members = []
    # Delete the project itself
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted successfully!", "success")
    return redirect(url_for("dashboard"))


@app.route("/add_task/<int:project_id>", methods=["GET", "POST"])
@login_required
def add_task(project_id):
    """Handles adding a new task to a project."""
    project = Project.query.get_or_404(project_id)
    # Only members can add tasks
    if current_user not in project.members:
        flash("You must be a member of this project to add tasks.", "danger")
        return redirect(url_for('dashboard'))

    # Fetch all users to populate the assignee dropdown
    users = User.query.all()

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        status = request.form.get("status")
        priority = request.form.get("priority")
        due_date_str = request.form.get("due_date")
        assigned_to_id = request.form.get("assigned_to_id")

        if not title:
            flash("Task title is required.", "danger")
            return redirect(url_for("add_task", project_id=project.id))

        due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None

        assigned_to_user = User.query.get(assigned_to_id)

        new_task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            project=project,
            assignee=assigned_to_user
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", "success")
        return redirect(url_for("project_details", project_id=project.id))

    return render_template("add_task.html", project=project, users=users)


@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    """Handles editing an existing task."""
    task = Task.query.get_or_404(task_id)
    project = task.project

    # Only members can edit tasks
    if current_user not in project.members:
        flash("You must be a member of this project to edit tasks.", "danger")
        return redirect(url_for('dashboard'))

    # Fetch all users to populate the assignee dropdown
    users = User.query.all()

    if request.method == "POST":
        task.title = request.form.get("title")
        task.description = request.form.get("description")
        task.status = request.form.get("status")
        task.priority = request.form.get("priority")
        due_date_str = request.form.get("due_date")
        assigned_to_id = request.form.get("assigned_to_id")

        task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None
        task.assigned_to_id = assigned_to_id

        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for("project_details", project_id=project.id))

    return render_template("edit_task.html", task=task, users=users)


@app.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    """Handles deleting a task."""
    task = Task.query.get_or_404(task_id)
    project_id = task.project.id
    # Only the project owner can delete tasks
    if task.project.owner != current_user:
        flash("You do not have permission to delete this task.", "danger")
        return redirect(url_for("project_details", project_id=project_id))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")
    return redirect(url_for("project_details", project_id=project_id))


# --- New Routes for Project Members ---

@app.route("/project/<int:project_id>/members", methods=["GET"])
@login_required
def project_members(project_id):
    """Displays the members of a project and provides a form to add new ones."""
    project = Project.query.get_or_404(project_id)

    # Only members can view the member list
    if current_user not in project.members:
        flash("You do not have access to this page.", "danger")
        return redirect(url_for('dashboard'))

    # Get all users who are not already members of this project
    # Note: This is an efficient way to get the list of potential members
    # by using a query that excludes existing members.
    existing_member_ids = [member.id for member in project.members]
    potential_members = User.query.filter(User.id.notin_(existing_member_ids)).all()

    return render_template(
        "project_members.html",
        project=project,
        potential_members=potential_members
    )


@app.route("/project/<int:project_id>/add_member", methods=["POST"])
@login_required
def add_member_to_project(project_id):
    """Adds a new member to a project."""
    project = Project.query.get_or_404(project_id)
    # Only the project owner can add members
    if project.owner != current_user:
        flash("You do not have permission to add members to this project.", "danger")
        return redirect(url_for('project_members', project_id=project_id))

    member_id = request.form.get("member_id")
    member = User.query.get_or_404(member_id)

    # Check if the user is already a member before adding
    if member not in project.members:
        project.members.append(member)
        db.session.commit()
        flash(f"{member.username} has been added to the project.", "success")
    else:
        flash(f"{member.username} is already a member.", "info")

    return redirect(url_for('project_members', project_id=project_id))


@app.route("/project/<int:project_id>/remove_member/<int:member_id>", methods=["POST"])
@login_required
def remove_member_from_project(project_id, member_id):
    """Removes a member from a project."""
    project = Project.query.get_or_404(project_id)
    member_to_remove = User.query.get_or_404(member_id)

    # Only the project owner can remove members
    if project.owner != current_user:
        flash("You do not have permission to remove members from this project.", "danger")
        return redirect(url_for('project_members', project_id=project_id))

    # Prevent the owner from removing themselves
    if member_to_remove == current_user:
        flash("You cannot remove yourself from a project you own. Delete the project instead.", "danger")
        return redirect(url_for('project_members', project_id=project_id))

    # Check if the user is a member before removing
    if member_to_remove in project.members:
        project.members.remove(member_to_remove)
        db.session.commit()
        flash(f"{member_to_remove.username} has been removed from the project.", "success")
    else:
        flash(f"{member_to_remove.username} is not a member of this project.", "info")

    return redirect(url_for('project_members', project_id=project_id))
