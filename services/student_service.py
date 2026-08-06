from models import student
from extensions import db
#for creating a student
def create_student_service(data):
    # Required fields
    required_fields = ["name", "age", "city", "course"]

    # Validate request
    if not data or not all(field in data for field in required_fields):
        return {"error": "All fields are required"}, 400

    # Create Student object
    stud = student(
        name=data["name"],
        age=data["age"],
        city=data["city"],
        course=data["course"]
    )

    # Save to database
    db.session.add(stud)
    db.session.commit()

    # Return created student
    return stud.to_dict(), 201
#for getting all students
def get_students_service():
    # Query all students
    students = student.query.all()

    # Convert to list of dictionaries
    students_list = [stud.to_dict() for stud in students]

    return students_list, 200

def get_student_service(id):
    # Query student by ID
    stud = student.query.get(id)

    if not stud:
        return {"error": "Student not found"}, 404

    return stud.to_dict(), 200

def update_student_service(id, data):
    # Query student by ID
    stud = student.query.get(id)

    if not stud:
        return {"error": "Student not found"}, 404

    # Update fields if provided
    if "name" in data:
        stud.name = data["name"]
    if "age" in data:
        stud.age = data["age"]
    if "city" in data:
        stud.city = data["city"]
    if "course" in data:
        stud.course = data["course"]

    # Save changes to database
    db.session.commit()

    return stud.to_dict(), 200

def delete_student_service(id):
    # Query student by ID
    stud = student.query.get(id)

    if not stud:
        return {"error": "Student not found"}, 404

    # Delete student from database
    db.session.delete(stud)
    db.session.commit()

    return {"message": "Student deleted successfully"}, 200