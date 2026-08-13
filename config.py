import os
from dotenv import load_dotenv

load_dotenv()


class config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "development-jwt-secret"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///students.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = os.getenv(
        "DEBUG",
        "False"
    ) == "True"