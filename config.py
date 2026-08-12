import os

from dotenv import load_dotenv

load_dotenv()


class config:

    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

    SQLALCHEMY_DATABASE_URI = "sqlite:///students.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = os.getenv("DEBUG", "False") == "True"