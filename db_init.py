from app import app, db
from models import User, Project, Task  # Import models

# Ensure the Flask app context is pushed
# This is necessary when running Flask-SQLAlchemy operations outside the main app.run()
with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database tables created successfully!")
