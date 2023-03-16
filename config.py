import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "kdfjkldsfl"
    UPLOAD_PATH = os.path.join(BASE_DIR, 'covers')
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(BASE_DIR, 'home_library.db')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
