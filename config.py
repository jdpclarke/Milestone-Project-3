import os


class Config:
    # Secret key for session management and security
    # IMPORTANT: This will be loaded from the .env file locally,
    # or Heroku env vars in production
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database URI for PostgreSQL
    # Loaded from .env locally, or Heroku's DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Suppresses a warning, set to True for event tracking
