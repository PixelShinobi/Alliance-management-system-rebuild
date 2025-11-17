from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User, TokenBlocklist
from app.schemas import register_schema, login_schema
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from marshmallow import ValidationError
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        # Validate request data with schema
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    # Hash password
    password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=password_hash,
        role=data.get('role', 'user')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'role': new_user.role
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT tokens"""
    try:
        # Validate request data
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    # Find user by username
    user = User.query.filter_by(username=data['username']).first()

    # Verify user exists and password is correct
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Create JWT access token with user identity and role claim
    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role}  
    )

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user and add token to blocklist"""
    jti = get_jwt()['jti']  # Get JWT ID
    token_type = get_jwt()['type'] 

    # Add token to blocklist
    blocklist_token = TokenBlocklist(jti=jti, token_type=token_type)
    db.session.add(blocklist_token)
    db.session.commit()

    return jsonify({'message': 'Logged out successfully'}), 200
