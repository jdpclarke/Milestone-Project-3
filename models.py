# models.py
from db import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# User model for authentication and profiles
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: A user can be a member of many projects through ProjectMember
    projects = db.relationship(
        'ProjectMember', back_populates='member_user', lazy='dynamic'
    )
    # Relationship: A user can be assigned many tasks
    assigned_tasks = db.relationship(
        'Task', foreign_keys='Task.assigned_to_id',
        backref='assignee', lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# Project model for organising tasks
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Status of the project, e.g., 'Active', 'Completed', 'Archived'
    status = db.Column(db.String(64), default='Active', nullable=False)

    # Relationship: A project can have many members
    members = db.relationship(
        'ProjectMember', back_populates='member_project', lazy='dynamic'
    )
    # Relationship: A project can have many tasks
    tasks = db.relationship('Task', backref='project', lazy='dynamic')

    # The original owner_id column will be used to automatically assign the owner role
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Project {self.name}>'


# ProjectMember model for the many-to-many relationship between users and projects
class ProjectMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Role of the user in the project, e.g., 'owner', 'member'
    role = db.Column(db.String(64), default='member', nullable=False)

    # Relationships for easy access
    member_project = db.relationship('Project', back_populates='members')
    member_user = db.relationship('User', back_populates='projects')


# Task model for individual items within a project
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    # e.g., 'To Do', 'In Progress', 'Done'
    status = db.Column(db.String(64), default='To Do', nullable=False)
    # e.g., 'Low', 'Medium', 'High'
    priority = db.Column(db.String(64), default='Medium', nullable=False)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f'<Task {self.title}>'
