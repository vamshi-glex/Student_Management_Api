from models import User
from extensions import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token


def register_user(data):

    # Validate request
    if not data:
        return {"error": "Request body is required"}, 400

    required_fields = ["username", "email", "password"]

    if not all(field in data for field in required_fields):
        return {"error": "All fields are required"}, 400

    username = data["username"].strip()
    email = data["email"].strip()
    password = data["password"]

    # Validate username
    if not username:
        return {"error": "Username cannot be empty"}, 400

    # Validate email
    if not email:
        return {"error": "Email cannot be empty"}, 400

    # Validate password
    if not password:
        return {"error": "Password cannot be empty"}, 400

    if len(password) < 6:
        return {
            "error": "Password must be at least 6 characters"
        }, 400

    # Check duplicate username
    existing_username = User.query.filter_by(
        username=username
    ).first()

    if existing_username:
        return {
            "error": "Username already exists"
        }, 409

    # Check duplicate email
    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        return {
            "error": "Email already exists"
        }, 409

    # Hash password
    password_hash = generate_password_hash(password)

    # Create user
    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )

    # Save user
    db.session.add(user)
    db.session.commit()

    return user.to_dict(), 201

def login_user(data):

    if not data:
        return {"error": "Request body is required"}, 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {
            "error": "Username and password are required"
        }, 400

    user = User.query.filter_by(
        username=username
    ).first()

    if not user:
        return {
            "error": "Invalid username or password"
        }, 401

    if not check_password_hash(
        user.password_hash,
        password
    ):
        return {
            "error": "Invalid username or password"
        }, 401
    access_token = create_access_token(
        identity=str(user.id)
)

    return {
    "user": user.to_dict(),
    "access_token": access_token
}, 200

    return user.to_dict(), 200