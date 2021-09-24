import validators
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from .constants import status_codes
from .database import User, db

accounts = Blueprint("accounts", __name__, url_prefix="/api/v1/accounts")


@accounts.post("/register")
def register():
    data = request.json

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if len(username) < 3:
        response = {"status": "error", "message": "Username is too short!"}
        return jsonify(response), status_codes.HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        response = {
            "status": "error",
            "message": "Username should be alphanumeric without spaces!",
        }
        return jsonify(response), status_codes.HTTP_400_BAD_REQUEST

    if User.query.filter_by(username=username).first():
        response = {
            "status": "error",
            "message": "Username is already registered!",
        }
        return jsonify(response), status_codes.HTTP_409_CONFLICT

    if not validators.email(email):
        response = {
            "status": "error",
            "message": "Please enter a valid email address!",
        }
        return jsonify(response), status_codes.HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first():
        response = {
            "status": "error",
            "message": "Email address is already registered!",
        }
        return jsonify(response), status_codes.HTTP_409_CONFLICT

    if len(password) < 6:
        response = {"status": "error", "message": "Password is too short!"}
        return jsonify(response), status_codes.HTTP_400_BAD_REQUEST

    password = generate_password_hash(password)
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    del data["password"]

    response = {
        "status": "success",
        "message": "User created successfully",
        "data": {**data},
    }
    return response, status_codes.HTTP_201_CREATED


# @accounts.get("/me")
# def me():
#     return {"user": "Caspian"}
