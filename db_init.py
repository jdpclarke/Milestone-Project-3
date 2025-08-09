# db_init.py

from dotenv import load_dotenv
load_dotenv()

from app import app
from db import db
from models import User, Project, Task

# Ensure the Flask app context is pushed
with app.app_context():
    print("Creating database tables...")
    # Drop all tables first to ensure a clean slate
    db.drop_all()
    db.create_all()
    print("Database tables created successfully!")