# db_init.py

from sqlalchemy import text
from db import db
from app import app
from dotenv import load_dotenv
load_dotenv()


# Ensure the Flask app context is pushed
with app.app_context():
    print("Dropping all tables with CASCADE...")

    # Use raw SQL to drop the entire public schema, which forces
    # all tables and their dependent objects (like foreign keys) to be dropped.
    try:
        db.session.execute(text('DROP SCHEMA public CASCADE;'))
        db.session.execute(text('CREATE SCHEMA public;'))
        db.session.commit()
        print("Existing database schema dropped and recreated successfully.")
    except Exception as e:
        print(f"Error dropping schema: {e}")
        db.session.rollback()

    print("Creating new database tables...")
    db.create_all()
    print("Database tables created successfully!")
