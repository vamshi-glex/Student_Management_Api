import logging

from models import student
from extensions import db
from exceptions import StudentNotFoundException


# Logger
logger = logging.getLogger(__name__)


# Create student
def create_student_service(data):

    required_fields = ["name", "age", "city", "course"]

    # Check required fields
    if not data or not all(field in data for field in required_fields):
        return {"error": "All fields are required"}, 400

    # Validate name
    if not isinstance(data["name"], str):
        return {"error": "Name must be a string"}, 400

    if not data["name"].strip():
        return {"error": "Name cannot be empty"}, 400

    # Validate age
    if not isinstance(data["age"], int):
        return {"error": "Age must be an integer"}, 400

    if data["age"] <= 0:
        return {"error": "Age must be greater than 0"}, 400

    # Validate city
    if not isinstance(data["city"], str):
        return {"error": "City must be a string"}, 400

    if not data["city"].strip():
        return {"error": "City cannot be empty"}, 400

    # Validate course
    if not isinstance(data["course"], str):
        return {"error": "Course must be a string"}, 400

    if not data["course"].strip():
        return {"error": "Course cannot be empty"}, 400

    # Create student
    stud = student(
        name=data["name"].strip(),
        age=data["age"],
        city=data["city"].strip(),
        course=data["course"].strip()
    )

    # Save to database
    db.session.add(stud)
    db.session.commit()

    # Log creation
    logger.info(f"Student created successfully: {stud.id}")

    return stud.to_dict(), 201


# Get all students
def get_students_service():

    students = student.query.all()

    students_list = [stud.to_dict() for stud in students]

    return students_list, 200


# Get student by ID
def get_student_service(id):

    stud = db.session.get(student, id)

    if not stud:
        raise StudentNotFoundException()

    return stud.to_dict(), 200


# Update student
def update_student_service(id, data):

    stud = db.session.get(student, id)

    if not stud:
        raise StudentNotFoundException()

    # Validate and update name
    if "name" in data:

        if not isinstance(data["name"], str):
            return {"error": "Name must be a string"}, 400

        if not data["name"].strip():
            return {"error": "Name cannot be empty"}, 400

        stud.name = data["name"].strip()

    # Validate and update age
    if "age" in data:

        if not isinstance(data["age"], int):
            return {"error": "Age must be an integer"}, 400

        if data["age"] <= 0:
            return {"error": "Age must be greater than 0"}, 400

        stud.age = data["age"]

    # Validate and update city
    if "city" in data:

        if not isinstance(data["city"], str):
            return {"error": "City must be a string"}, 400

        if not data["city"].strip():
            return {"error": "City cannot be empty"}, 400

        stud.city = data["city"].strip()

    # Validate and update course
    if "course" in data:

        if not isinstance(data["course"], str):
            return {"error": "Course must be a string"}, 400

        if not data["course"].strip():
            return {"error": "Course cannot be empty"}, 400

        stud.course = data["course"].strip()

    # Save changes
    db.session.commit()

    # Log update
    logger.info(f"Student updated successfully: {stud.id}")

    return stud.to_dict(), 200


# Delete student
def delete_student_service(id):

    stud = db.session.get(student, id)

    if not stud:
        raise StudentNotFoundException()

    # Delete student
    db.session.delete(stud)
    db.session.commit()

    # Log deletion
    logger.info(f"Student deleted successfully: {id}")

    return {"message": "Student deleted successfully"}, 200