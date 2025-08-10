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


# --- ROUTE DEFINITIONS ---
# You'll need to add your routes here.


@app.route("/")
def index():
    """
    Renders the homepage.
    """
    return render_template("index.html")

# User authentication routes
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login.
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and user.check_password(request.form["password"]):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles user registration.
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
        elif User.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    """
    Handles user logout.
    """
    logout_user()
    return redirect(url_for("index"))


# Profile management
@app.route("/profile")
@login_required
def profile():
    """
    Displays the user's profile page.
    """
    return render_template("profile.html", user=current_user)


@app.route("/edit_profile", methods=["GET", "POST"])
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

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    Handles changing the user's password.
    """
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(old_password):
            flash('Incorrect old password.', 'danger')
        elif new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('profile'))

    return render_template('change_password.html')

# Project routes
@app.route('/dashboard')
@login_required
def dashboard():
    """
    Displays the user's dashboard with their projects.
    """
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', projects=projects)

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    """
    Handles adding a new project.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if name:
            new_project = Project(name=name, description=description, user_id=current_user.id)
            db.session.add(new_project)
            db.session.commit()
            flash('Project created successfully!', 'success')
            return redirect(url_for('dashboard'))
    return render_template('add_project.html')

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """
    Handles editing an existing project.
    """
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('You are not authorized to edit this project.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if name:
            project.name = name
            project.description = description
            db.session.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('dashboard'))

    return render_template('edit_project.html', project=project)


@app.route('/delete_project/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    """
    Deletes a project and all associated tasks.
    """
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('You are not authorized to delete this project.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Delete all tasks associated with the project first
    for task in project.tasks:
        db.session.delete(task)

    db.session.delete(project)
    db.session.commit()
    flash('Project and all its tasks deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


# Task routes
@app.route('/project_details/<int:project_id>')
@login_required
def project_details(project_id):
    """
    Displays the kanban board for a specific project.
    """
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('You are not authorized to view this project.', 'danger')
        return redirect(url_for('dashboard'))

    # Separate tasks by status for the kanban board
    tasks_todo = project.tasks.filter_by(status='To Do').all()
    tasks_progress = project.tasks.filter_by(status='In Progress').all()
    tasks_done = project.tasks.filter_by(status='Done').all()

    return render_template(
        'project_details.html',
        project=project,
        tasks_todo=tasks_todo,
        tasks_progress=tasks_progress,
        tasks_done=tasks_done
    )

@app.route('/add_task/<int:project_id>', methods=['GET', 'POST'])
@login_required
def add_task(project_id):
    """
    Handles adding a new task to a project.
    """
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('You are not authorized to add tasks to this project.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        priority = request.form.get('priority')
        due_date_str = request.form.get('due_date')
        assigned_to_id = request.form.get('assigned_to_id')

        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        
        if title:
            new_task = Task(
                title=title,
                description=description,
                status=status,
                priority=priority,
                due_date=due_date,
                project_id=project_id,
                assigned_to_id=assigned_to_id
            )
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect(url_for('project_details', project_id=project_id))
    
    # Get all users to populate the assignee dropdown
    users = User.query.all()
    return render_template('add_task.html', project=project, users=users)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """
    Handles editing an existing task.
    """
    task = Task.query.get_or_404(task_id)
    if task.project.user_id != current_user.id:
        flash('You are not authorized to edit this task.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.status = request.form.get('status')
        task.priority = request.form.get('priority')
        due_date_str = request.form.get('due_date')
        task.assigned_to_id = request.form.get('assigned_to_id')

        if due_date_str:
            task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        else:
            task.due_date = None

        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('project_details', project_id=task.project.id))
    
    users = User.query.all()
    return render_template('edit_task.html', task=task, users=users)

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """
    Deletes a specific task.
    """
    task = Task.query.get_or_404(task_id)
    if task.project.user_id != current_user.id:
        flash('You are not authorized to delete this task.', 'danger')
        return redirect(url_for('dashboard'))

    project_id = task.project.id
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('project_details', project_id=project_id))


@app.route('/update_task_status/<int:task_id>/<new_status>', methods=['POST'])
@login_required
def update_task_status(task_id, new_status):
    """
    Updates the status of a task from the kanban board.
    """
    task = Task.query.get_or_404(task_id)
    if task.project.user_id != current_user.id:
        flash('You are not authorized to update this task.', 'danger')
        return redirect(url_for('dashboard'))

    task.status = new_status
    db.session.commit()
    flash(f'Task status updated to {new_status}!', 'success')
    return redirect(url_for('project_details', project_id=task.project.id))

# This part ensures the application runs when the script is executed directly
# It runs a development server, which is useful for testing.
if __name__ == '__main__':
    app.run(debug=True)
