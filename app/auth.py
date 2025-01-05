from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app import db
from app.models import User
from app.schemas import UserSchema
import bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user_data = user_schema.load(data, session=db.session)
        print(user_data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 422
    
    if User.query.filter_by(email=user_data.email).first():
        return jsonify({"error": "Email already exists"}), 409
    hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.checkpw(data['password'].encode(), user.password_hash.encode()):
        access_token = create_access_token(identity=str(user.id))  # Ensure identity is a string
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_schema.dump(user)), 200
