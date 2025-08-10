# app.py
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

from flask import (
    Flask, render_template, request, redirect, url_for, flash, abort
)
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from sqlalchemy import or_

# Local imports
from db import db
# Import new ProjectMember model
from models import User, Project, Task, ProjectMember

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

@app.route('/')
def index():
    """
    Renders the homepage.
    """
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
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

        # Check for existing user
        existing_user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()

        if existing_user:
            flash(
                'Username or email already exists. Please choose a different one.',
                'danger'
            )
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """
    Logs out the current user.
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    """
    Displays the current user's profile.
    """
    # Fetch the user from the database
    user = User.query.get(current_user.id)
    if user is None:
        abort(404)
    return render_template('profile.html', user=user)


@app.route('/edit-profile', methods=['GET', 'POST'])
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


@app.route('/dashboard')
@login_required
def dashboard():
    """
    Displays the user's dashboard with projects they own or are a member of.
    """
    # Find all projects where the current user is a member
    projects = Project.query.join(ProjectMember).filter(ProjectMember.user_id == current_user.id).order_by(Project.created_at.desc()).all()

    return render_template('dashboard.html', projects=projects)


@app.route('/projects/new', methods=['GET', 'POST'])
@login_required
def add_project():
    """
    Handles the creation of a new project.
    """
    if request.method == 'POST':
        project_name = request.form.get('name')
        description = request.form.get('description')

        if not project_name:
            flash('Project name is required.', 'danger')
            return redirect(url_for('add_project'))

        new_project = Project(
            name=project_name,
            description=description,
            owner_id=current_user.id  # Set the owner
        )
        db.session.add(new_project)
        db.session.commit()

        # Add the creator as the owner member of the project
        owner_member = ProjectMember(
            project_id=new_project.id,
            user_id=current_user.id,
            role='owner'
        )
        db.session.add(owner_member)
        db.session.commit()

        flash(f'Project "{new_project.name}" created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_project.html')


@app.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """
    Handles editing a project. Only the owner can edit.
    """
    project = Project.query.get_or_404(project_id)
    # Check if the user is the owner
    is_owner = ProjectMember.query.filter_by(
        project_id=project.id,
        user_id=current_user.id,
        role='owner'
    ).first()

    if not is_owner:
        flash("You do not have permission to edit this project.", "danger")
        return redirect(url_for('project_details', project_id=project.id))

    if request.method == 'POST':
        project.name = request.form.get('name')
        project.description = request.form.get('description')

        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('project_details', project_id=project.id))

    return render_template('edit_project.html', project=project)


@app.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    """
    Handles deleting a project. Only the owner can delete.
    """
    project = Project.query.get_or_404(project_id)

    # Check if the user is the owner
    is_owner = ProjectMember.query.filter_by(
        project_id=project.id,
        user_id=current_user.id,
        role='owner'
    ).first()

    if not is_owner:
        flash("You do not have permission to delete this project.", "danger")
        return redirect(url_for('project_details', project_id=project.id))

    # Delete all associated tasks and project members first
    Task.query.filter_by(project_id=project.id).delete()
    ProjectMember.query.filter_by(project_id=project.id).delete()
    db.session.delete(project)
    db.session.commit()
    flash('Project and all its tasks have been deleted.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/projects/<int:project_id>')
@login_required
def project_details(project_id):
    """
    Displays the details and tasks for a specific project.
    """
    project = Project.query.get_or_404(project_id)

    # Check if the current user is a member of this project
    is_member = ProjectMember.query.filter_by(
        project_id=project.id,
        user_id=current_user.id
    ).first()

    if not is_member:
        flash("You do not have permission to view this project.", "danger")
        return redirect(url_for('dashboard'))

    # Determine user's role for this project
    user_role = is_member.role

    # Fetch tasks and filter by status
    tasks_todo = Task.query.filter_by(project_id=project.id, status='To Do').all()
    tasks_in_progress = Task.query.filter_by(project_id=project.id, status='In Progress').all()
    tasks_done = Task.query.filter_by(project_id=project.id, status='Done').all()

    # Fetch all users for the assignee dropdown in the task forms
    users = User.query.order_by(User.username).all()

    # Fetch project members
    members = ProjectMember.query.filter_by(project_id=project.id).all()

    return render_template(
        'project_details.html',
        project=project,
        tasks_todo=tasks_todo,
        tasks_in_progress=tasks_in_progress,
        tasks_done=tasks_done,
        users=users,
        user_role=user_role,
        members=members
    )


@app.route('/projects/<int:project_id>/tasks/new', methods=['GET', 'POST'])
@login_required
def add_task(project_id):
    """
    Handles adding a new task to a project.
    """
    project = Project.query.get_or_404(project_id)

    # Check if the user is a member of the project
    is_member = ProjectMember.query.filter_by(
        project_id=project.id,
        user_id=current_user.id
    ).first()

    if not is_member:
        flash("You do not have permission to add tasks to this project.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        status = request.form.get('status')
        priority = request.form.get('priority')
        assigned_to_id = request.form.get('assigned_to_id')

        due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

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
        flash('Task added successfully!', 'success')
        return redirect(url_for('project_details', project_id=project.id))

    users = User.query.order_by(User.username).all()
    return render_template('add_task.html', project=project, users=users)


@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """
    Handles editing a task. Only members can edit.
    """
    task = Task.query.get_or_404(task_id)

    # Check if the current user is a member of the project
    is_member = ProjectMember.query.filter_by(
        project_id=task.project_id,
        user_id=current_user.id
    ).first()

    if not is_member:
        flash("You do not have permission to edit this task.", "danger")
        return redirect(url_for('project_details', project_id=task.project_id))

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        task.status = request.form.get('status')
        task.priority = request.form.get('priority')
        task.assigned_to_id = request.form.get('assigned_to_id')

        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('project_details', project_id=task.project_id))

    users = User.query.order_by(User.username).all()
    return render_template('edit_task.html', task=task, users=users)


@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """
    Handles deleting a task.
    """
    task = Task.query.get_or_404(task_id)

    # Check if the current user is a member of the project
    is_member = ProjectMember.query.filter_by(
        project_id=task.project_id,
        user_id=current_user.id
    ).first()

    if not is_member:
        flash("You do not have permission to delete this task.", "danger")
        return redirect(url_for('project_details', project_id=task.project_id))

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.', 'success')
    return redirect(url_for('project_details', project_id=task.project_id))


@app.route('/projects/<int:project_id>/invite', methods=['POST'])
@login_required
def invite_member(project_id):
    """
    Invites a user to a project.
    Only the project owner can invite other members.
    """
    project = Project.query.get_or_404(project_id)

    # Check if the current user is the owner
    is_owner = ProjectMember.query.filter_by(
        project_id=project.id,
        user_id=current_user.id,
        role='owner'
    ).first()

    if not is_owner:
        flash("You do not have permission to invite members.", "danger")
        return redirect(url_for('project_details', project_id=project.id))

    invited_user_identifier = request.form.get('invited_user_identifier')

    # Try to find the user by username or email
    invited_user = User.query.filter(
        or_(User.username == invited_user_identifier, User.email == invited_user_identifier)
    ).first()

    if not invited_user:
        flash('User not found.', 'danger')
        return redirect(url_for('project_details', project_id=project.id))

    # Check if the user is already a member
    is_already_member = ProjectMember.query.filter_by(
        project_id=project.id,
        user_id=invited_user.id
    ).first()

    if is_already_member:
        flash('This user is already a member of the project.', 'warning')
        return redirect(url_for('project_details', project_id=project.id))

    # Add the new member with a 'member' role
    new_member = ProjectMember(
        project_id=project.id,
        user_id=invited_user.id,
        role='member'
    )
    db.session.add(new_member)
    db.session.commit()
    flash(f'User "{invited_user.username}" has been added to the project.', 'success')

    return redirect(url_for('project_details', project_id=project.id))


@app.route('/projects/<int:project_id>/remove-member/<int:user_id>', methods=['POST'])
@login_required
def remove_member(project_id, user_id):
    """
    Removes a member from a project.
    Only the project owner can remove members.
    The owner cannot remove themselves.
    """
    project = Project.query.get_or_404(project_id)

    # Check if the current user is the owner
    is_owner = ProjectMember.query.filter_by(
        project_id=project.id,
        user_id=current_user.id,
        role='owner'
    ).first()

    if not is_owner:
        flash("You do not have permission to remove members.", "danger")
        return redirect(url_for('project_details', project_id=project.id))

    # The owner cannot remove themselves
    if current_user.id == user_id:
        flash("You cannot remove yourself as the project owner.", "danger")
        return redirect(url_for('project_details', project_id=project.id))

    member_to_remove = ProjectMember.query.filter_by(
        project_id=project.id,
        user_id=user_id
    ).first()

    if member_to_remove:
        db.session.delete(member_to_remove)
        db.session.commit()
        flash('Member removed successfully.', 'success')
    else:
        flash('Member not found.', 'danger')

    return redirect(url_for('project_details', project_id=project.id))


@app.route('/projects/<int:project_id>/status', methods=['POST'])
@login_required
def update_project_status(project_id):
    """
    Updates the status of a project (e.g., 'Completed', 'Archived').
    Only the project owner can change the status.
    """
    project = Project.query.get_or_404(project_id)

    # Check if the current user is the owner
    is_owner = ProjectMember.query.filter_by(
        project_id=project.id,
        user_id=current_user.id,
        role='owner'
    ).first()

    if not is_owner:
        flash("You do not have permission to change the project status.", "danger")
        return redirect(url_for('project_details', project_id=project.id))

    new_status = request.form.get('status')
    if new_status in ['Completed', 'Archived', 'Active']:
        project.status = new_status
        db.session.commit()
        flash(f'Project status updated to "{new_status}".', 'success')
    else:
        flash('Invalid status.', 'danger')

    return redirect(url_for('project_details', project_id=project.id))


if __name__ == '__main__':
    app.run(debug=True)
