from flask import Blueprint, jsonify, request
from models import student 
from flask_jwt_extended import jwt_required
from extensions import db
from utils.response import success_response, error_response
from services.student_service import create_student_service, get_students_service,get_student_service,update_student_service,delete_student_service

student_bp = Blueprint("students", __name__)

#posting data
@student_bp.route("/", methods=["POST"])
@jwt_required()
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
@jwt_required()
def get_students():

    result, status = get_students_service()

    return success_response(
        "Students retrieved successfully",
        result,
        status
    )

# getting data by id
@student_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
def delete_student(id):

    result, status = delete_student_service(id)

    return success_response(
        "Student deleted successfully",
        result,
        status
    )

#search
@student_bp.route("/search", methods=["GET"])
@jwt_required()
def search_students():

    name = request.args.get("name")
    age = request.args.get("age")
    city = request.args.get("city")
    course = request.args.get("course")

    query = student.query

    if name:
        query = query.filter(
            student.name.ilike(f"%{name}%")
        )

    if age:
        query = query.filter_by(age=int(age))

    if city:
        query = query.filter(
            student.city.ilike(f"%{city}%")
        )

    if course:
        query = query.filter(
            student.course.ilike(f"%{course}%")
        )

    students = query.all()

    students_list = [
        stud.to_dict()
        for stud in students
    ]

    return success_response(
        "Students searched successfully",
        students_list,
        200
    )
#sort
@student_bp.route("/sort", methods=["GET"])
@jwt_required()
def sort_students():

    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")

    if sort_by not in ["id", "name", "age", "city", "course"]:
        return error_response(
            "Invalid sort_by field",
            400
        )

    query = student.query

    if order == "desc":
        query = query.order_by(
            getattr(student, sort_by).desc()
        )
    else:
        query = query.order_by(
            getattr(student, sort_by).asc()
        )

    students = query.all()

    students_list = [
        stud.to_dict()
        for stud in students
    ]

    return success_response(
        "Students sorted successfully",
        students_list,
        200
    )

#pagination
@student_bp.route("/paginate", methods=["GET"])
@jwt_required()
def paginate_students():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    per_page = request.args.get(
        "per_page",
        10,
        type=int
    )

    pagination = student.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    students_list = [
        stud.to_dict()
        for stud in pagination.items
    ]

    data = {
        "students": students_list,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }

    return success_response(
        "Students retrieved successfully",
        data,
        200
    )

 