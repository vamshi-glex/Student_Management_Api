from flask import Blueprint, request
from services.auth_service import register_user,login_user
from utils.response import success_response, error_response


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    result, status = register_user(data)

    if status != 201:
        return error_response(
            result["error"],
            status
        )

    return success_response(
        "User registered successfully",
        result,
        201
    )
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    result, status = login_user(data)

    if status != 200:
        return error_response(
            result["error"],
            status
        )

    return success_response(
        "Login successful",
        result,
        200
    )