from flask import Flask # type: ignore
from extensions import   db
from config import config
from routes.students import student_bp

app = Flask(__name__)

app.config.from_object(config)  

db.init_app(app)    

app.register_blueprint(student_bp, url_prefix='/students')

from models import student
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return  {
        "message": "Welcome to the Student API"
    }

if __name__ == "__main__":
    app.run(debug=True)