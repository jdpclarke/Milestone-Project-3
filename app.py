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
from settings import Config

# Initialize Flask app
app = Flask(__name__, static_folder='assets')


# Load configuration from config.py
# Heroku will provide its own DATABASE_URL.
# The dotenv will handle local environment variables.
app.config.from_object(Config)


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


# --- ROUTES ---

@app.route("/")
def index():
    """
    Renders the homepage.
    If a user is logged in, they are shown a welcome message.
    Otherwise, they are prompted to log in or register.
    """
    return render_template('index.html')


@app.route("/dashboard")
@login_required
def dashboard():
    """
    Renders the user's dashboard with a list of their projects.
    """
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', projects=projects)


@app.route("/add_project", methods=['GET', 'POST'])
@login_required
def add_project():
    """
    Handles creating a new project.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if not name:
            flash("Project name is required.", "danger")
            return redirect(url_for('add_project'))

        new_project = Project(
            name=name,
            description=description,
            user_id=current_user.id
        )
        db.session.add(new_project)
        db.session.commit()
        flash("Project created successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('add_project.html')


@app.route("/project/<int:project_id>", methods=['GET'])
@login_required
def project_details(project_id):
    """
    Renders the details for a specific project, including its tasks.
    Also handles sorting and filtering of tasks.
    """
    project = Project.query.get_or_404(project_id)

    # Make sure the current user has access to this project
    if project.user_id != current_user.id:
        flash("You do not have permission to view this project.", "danger")
        return redirect(url_for('dashboard'))

    # Get sorting parameters from the URL
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')

    # Get all tasks for the project and then sort them
    all_tasks = project.tasks.all()

    # Sort the tasks based on the 'sort_by' and 'sort_order' parameter
    if sort_by == 'due_date':
        all_tasks.sort(key=lambda x: (x.due_date is None, x.due_date), reverse=(sort_order == 'desc'))
    elif sort_by == 'priority':
        priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
        all_tasks.sort(key=lambda x: priority_order.get(x.priority, 99), reverse=(sort_order == 'desc'))
    else:
        # Default to sorting by creation date
        all_tasks.sort(key=lambda x: x.created_at, reverse=(sort_order == 'desc'))

    # Separate tasks by status for the kanban view
    tasks_todo = [t for t in all_tasks if t.status == 'To Do']
    tasks_in_progress = [t for t in all_tasks if t.status == 'In Progress']
    tasks_done = [t for t in all_tasks if t.status == 'Done']

    return render_template(
        'project_details.html',
        project=project,
        tasks_todo=tasks_todo,
        tasks_in_progress=tasks_in_progress,
        tasks_done=tasks_done,
        sort_by=sort_by,
        sort_order=sort_order
    )


@app.route("/edit_project/<int:project_id>", methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """
    Handles editing an existing project.
    """
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash("You do not have permission to edit this project.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        project.name = request.form.get('name')
        project.description = request.form.get('description')
        db.session.commit()
        flash("Project updated successfully!", "success")
        return redirect(url_for('project_details', project_id=project.id))

    return render_template('edit_project.html', project=project)


@app.route("/delete_project/<int:project_id>", methods=['POST'])
@login_required
def delete_project(project_id):
    """
    Handles deleting a project.
    """
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash("You do not have permission to delete this project.", "danger")
        return redirect(url_for('dashboard'))

    # Delete all tasks associated with the project first
    for task in project.tasks.all():
        db.session.delete(task)

    db.session.delete(project)
    db.session.commit()
    flash("Project deleted successfully!", "success")
    return redirect(url_for('dashboard'))


@app.route("/add_task/<int:project_id>", methods=['GET', 'POST'])
@login_required
def add_task(project_id):
    """
    Handles adding a new task to a project.
    """
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash("You do not have permission to add tasks to this project.", "danger")
        return redirect(url_for('dashboard'))

    users = User.query.all()

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        status = request.form.get('status')
        priority = request.form.get('priority')
        assigned_to_id = request.form.get('assigned_to_id')

        due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

        if not title:
            flash("Task title is required.", "danger")
            return redirect(url_for('add_task', project_id=project.id))

        new_task = Task(
            title=title,
            description=description,
            due_date=due_date,
            status=status,
            priority=priority,
            project_id=project.id,
            assigned_to_id=assigned_to_id
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", "success")
        return redirect(url_for('project_details', project_id=project.id))

    return render_template('add_task.html', project=project, users=users)


@app.route("/edit_task/<int:task_id>", methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """
    Handles editing a task.
    """
    task = Task.query.get_or_404(task_id)
    if task.project.user_id != current_user.id:
        flash("You do not have permission to edit this task.", "danger")
        return redirect(url_for('dashboard'))

    users = User.query.all()

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        task.status = request.form.get('status')
        task.priority = request.form.get('priority')
        task.assigned_to_id = request.form.get('assigned_to_id')

        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for('project_details', project_id=task.project.id))

    return render_template('edit_task.html', task=task, users=users)


@app.route("/delete_task/<int:task_id>", methods=['POST'])
@login_required
def delete_task(task_id):
    """
    Handles deleting a task.
    """
    task = Task.query.get_or_404(task_id)
    if task.project.user_id != current_user.id:
        flash("You do not have permission to delete this task.", "danger")
        return redirect(url_for('dashboard'))

    project_id = task.project.id
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")
    return redirect(url_for('project_details', project_id=project_id))


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # --- VALIDATION ---
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash("Email already exists. Please choose a different one.", "danger")
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    """
    Handles user logout.
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))


@app.route("/profile")
@login_required
def profile():
    """
    Renders the user's profile page.
    """
    return render_template('profile.html', user=current_user)


@app.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Handles editing the current user's profile.
    """
    if request.method == "POST":
        new_username = request.form.get("username")
        new_email = request.form.get("email")
        new_first_name = request.form.get("first_name")
        new_last_name = request.form.get("last_name")

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
        current_user.first_name = new_first_name
        current_user.last_name = new_last_name
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("edit_profile.html", user=current_user)


@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    """
    Handles changing the user's password.
    """
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        if not current_user.check_password(old_password):
            flash("Incorrect old password.", "danger")
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash("Password updated successfully!", "success")
            return redirect(url_for('profile'))

    return render_template('change_password.html')


if __name__ == '__main__':
    app.run(debug=True)
