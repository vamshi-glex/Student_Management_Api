from flask import Blueprint, jsonify, request
from models import student 
from extensions import db

student_bp = Blueprint("students", __name__)


@student_bp.route("/", methods=["POST"])
def create_student():
    # Read JSON data from request
    data = request.get_json()

    # Required fields
    required_fields = ["name", "age", "city", "course"]

    # Validate request
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

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
    return jsonify(stud.to_dict()), 201

@student_bp.route("/", methods=["GET"])
def get_students():
    # Query all students
    students = student.query.all()

    # Convert to list of dictionaries
    students_list = [stud.to_dict() for stud in students]

    return jsonify(students_list), 200

@student_bp.route("/<int:id>", methods=["GET"])
def get_student(id):
    # Query student by ID
    stud = student.query.get(id)

    if not stud:
        return jsonify({"error": "Student not found"}), 404
    
    

    return jsonify(stud.to_dict()), 200