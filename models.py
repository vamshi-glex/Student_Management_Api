from extensions import db
class student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    course=db.Column(db.String(100), nullable=False)
     

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'city': self.city,
            'course': self.course
             
        }
 


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
         