import os
from datetime import timedelta


class Config:
    # Secret key for session management and security
    # IMPORTANT: This will be loaded from the .env file locally,
    # or Heroku env vars in production
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')

    # This is the duration of a "permanent" session, in this case, 30 minutes.
    # This only applies if 'remember=True' is passed to login_user()
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    # Database URI for PostgreSQL
    # Loaded from .env locally, or Heroku's DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Suppresses a warning, set to True for event tracking
