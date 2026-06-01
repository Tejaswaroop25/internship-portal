import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-development-key-change-me')

    default_db_path = os.path.join(PROJECT_ROOT, 'database', 'db.sqlite')
    default_db_uri = f"sqlite:///{default_db_path.replace('\\', '/')}"

    database_url = os.environ.get('DATABASE_URL', default_db_uri)
    if database_url.startswith('sqlite:///'):
        sqlite_path = database_url[len('sqlite:///'):]
        if sqlite_path and not os.path.isabs(sqlite_path):
            sqlite_path = os.path.abspath(os.path.join(PROJECT_ROOT, sqlite_path))
            database_url = f"sqlite:///{sqlite_path.replace('\\', '/')}"

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
