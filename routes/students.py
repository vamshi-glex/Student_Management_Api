from flask import Blueprint, jsonify, request
from models import student 
from extensions import db
from utils.response import success_response, error_response
from services.student_service import create_student_service, get_students_service,get_student_service,update_student_service,delete_student_service

student_bp = Blueprint("students", __name__)

#posting data
@student_bp.route("/", methods=["POST"])
def create_student_route():

    data = request.get_json()

    result, status = create_student_service(data)

    if status != 201:
        return error_response(result["error"], status)

    return success_response(
        "Student created successfully",
        result,
        201
    )

#getting data
@student_bp.route("/", methods=["GET"])
def get_students():

    result, status = get_students_service()

    return success_response(
        "Students retrieved successfully",
        result,
        status
    )

# getting data by id
@student_bp.route("/<int:id>", methods=["GET"])
def get_student(id):

    result, status = get_student_service(id)

    if status != 200:
        return error_response(result["error"], status)

    return success_response(
        "Student retrieved successfully",
        result,
        200
    )


@student_bp.route("/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.get_json()

    result, status = update_student_service(id, data)

    if status != 200:
        return error_response(result["error"], status)

    return success_response(
        "Student updated successfully",
        result,
        200
    )



@student_bp.route("/<int:id>", methods=["DELETE"])
def delete_student(id):

    result, status = delete_student_service(id)

    return success_response(
        "Student deleted successfully",
        result,
        status
    )

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