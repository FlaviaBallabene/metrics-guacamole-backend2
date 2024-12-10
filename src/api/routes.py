"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Role, Campaign, Location, WeeklyData, Project, Platform
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import datetime
import hashlib

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

def hash_password(password):
    """Hashes a password using SHA-256."""

    # Create a SHA-256 hash object
    hasher = hashlib.sha256()

    # Encode the password as bytes and update the hash object
    hasher.update(password.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_password = hasher.hexdigest()

    return hashed_password
    
@api.route("/signup", methods=["POST"])
def signup():
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    role_id = request.json.get("role_id")
    if None in [email, role_id, first_name, last_name]:
        return jsonify ({"msg": "Some required fields are missing"}), 400
    verify_email = User.query.filter_by(email=email).first()
    if verify_email:
        return jsonify ({"msg": "An account with this email already exists"}), 409
    verify_role = Role.query.filter_by(id=role_id).first()
    if verify_role is None:
        return jsonify ({"msg": "Role not found"}), 404
        
    current_year = datetime.now().year
    password = last_name[:3] + first_name[:3] + str(current_year)  
    user = User(email=email,role_id=role_id, password=hash_password(password), first_name=first_name, last_name=last_name)

    db.session.add(user)
    db.session.commit()

    response_body = {
        "msg": "Successfully created user",
        "user": user.serialize()
    }

    return jsonify(response_body), 201




# @api.route("/signup", methods=["POST"])
# def signup():
#     request_body = request.get_json(force=True)

#     required_fields = ["email", "password"]
#     for field in required_fields:
#         if field not in request_body or not request_body[field]:
#             raise APIException(f'The "{field}" field cannot be empty', 400)

#     verify_email = User.query.filter_by(email=request_body["email"]).first()
#     if verify_email:
#         raise APIException("An account with this email already exists", 400)

#     user = User(email=request_body["email"], password=request_body["password"])

#     db.session.add(user)

#     try:
#         db.session.commit()
#     except:
#         raise APIException('Internal error', 500)

#     response_body = {
#         "msg": "Successfully created user",
#         "user": user.serialize()
#     }

#     return jsonify(response_body), 200


@api.route('/login', methods=['POST'])
def login():
    request_body = request.get_json(force=True)
    email = request_body["email"]
    password = request_body["password"]
    if None in [email, password]:
        return jsonify("Some required fields are missing")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify("Account with this email does not exist"), 404

    if user.password != hash_password(password):
        return jsonify("Incorrect password"), 401

    access_token = create_access_token(identity=user.id)
    print(access_token)

    response_body = {
        "msg": "logged",
        "user": user.serialize(),
        "token": access_token
    }
    print(response_body),
    return jsonify(response_body), 200


@api.route('/user', methods=['GET'])
def get_user():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@api.route("/roles", methods=["GET"])
def get_roles():
    roles = Role.query.all()

    response_body = {
        "roles": [role.serialize() for role in roles]
    }

    return jsonify(response_body), 200