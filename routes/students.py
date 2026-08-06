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

@student_bp.route("/<int:id>", methods=["PUT"])
def update_student(id):
    # Query student by ID
    stud = student.query.get(id)

    if not stud:
        return jsonify({"error": "Student not found"}), 404

    # Read JSON data from request
    data = request.get_json()

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

    return jsonify(stud.to_dict()), 200

@student_bp.route("/<int:id>", methods=["DELETE"])
def delete_student(id):
    # Query student by ID
    stud = student.query.get(id)

    if not stud:
        return jsonify({"error": "Student not found"}), 404

    # Delete student from database
    db.session.delete(stud)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"}), 200

#search
@student_bp.route("/search", methods=["GET"])
def search_students():
    # Get query parameters
    name = request.args.get("name")
    age = request.args.get("age")
    city = request.args.get("city")
    course = request.args.get("course")

    # Build query
    query = student.query

    if name:
        query = query.filter(student.name.ilike(f"%{name}%"))
    if age:
        query = query.filter_by(age=int(age))
    if city:
        query = query.filter(student.city.ilike(f"%{city}%"))
    if course:
        query = query.filter(student.course.ilike(f"%{course}%"))

    # Execute query
    students = query.all()

    # Convert to list of dictionaries
    students_list = [stud.to_dict() for stud in students]

    return jsonify(students_list), 200

#sort
@student_bp.route("/sort", methods=["GET"])
def sort_students():
    # Get query parameters
    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")

    # Validate sort_by field
    if sort_by not in ["id", "name", "age", "city", "course"]:
        return jsonify({"error": "Invalid sort_by field"}), 400

    # Build query
    query = student.query

    if order == "desc":
        query = query.order_by(getattr(student, sort_by).desc())
    else:
        query = query.order_by(getattr(student, sort_by).asc())

    # Execute query
    students = query.all()

    # Convert to list of dictionaries
    students_list = [stud.to_dict() for stud in students]

    return jsonify(students_list), 200

#pagination
@student_bp.route("/paginate", methods=["GET"])
def paginate_students():
    # Get query parameters
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # Query students with pagination
    pagination = student.query.paginate(page=page, per_page=per_page, error_out=False)

    # Convert to list of dictionaries
    students_list = [stud.to_dict() for stud in pagination.items]

    return jsonify({
        "students": students_list,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }), 200