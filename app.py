from flask import Flask
from extensions import   db
from config import Config

app = Flask(__name__)

app.config.from_object(Config)  

db.init_app(app)    

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