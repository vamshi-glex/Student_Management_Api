from flask import Flask # type: ignore
from extensions import   db
from config import config
from routes.students import student_bp
from exceptions import StudentNotFoundException
import logging
import os
from routes.auth import auth_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config.from_object(config)

jwt = JWTManager(app)

db.init_app(app)

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

app.logger.info("Student Management API started")

 

   

app.register_blueprint(student_bp, url_prefix='/students')
app.register_blueprint(auth_bp)


@app.errorhandler(StudentNotFoundException)
def handle_student_not_found(error):
    return {
        "success": False,
        "message": error.message,
        "data": None
    }, 404

@app.errorhandler(Exception)
def handle_general_exception(error):

    app.logger.error(
        f"Unexpected error: {error}",
        exc_info=True
    )

    return {
        "success": False,
        "message": "Internal server error",
        "data": None
    }, 500
from models import student
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return  {
        "message": "Welcome to the Student API"
    }

if __name__ == "__main__":
    app.run(debug=True,port=8000)