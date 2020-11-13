# -*- coding: utf-8 -*-

"""
flask_server.views.users
~~~~~~~~~~~~~~~~~~~~~

API routes for user management; registration, logins, sessions, etc.

"""
from flask import Blueprint, jsonify, request, session

from flask_server.models import users

users_bp = Blueprint('users', __name__)


@users_bp.route("/api/login", methods=['POST'])
def login():
    username = request.get_json().get('username')
    password = request.get_json().get('password')

    verified = users.authenticate_user(username, password)

    if verified:
        session['logged'] = True
        session['username'] = username

    return jsonify({'success': verified})


@users_bp.route("/api/logout", methods=['POST', 'GET'])
def logout():
    session.clear()
    return jsonify({'success': True})


@users_bp.route("/api/register", methods=['POST'])
def register():
    username = request.get_json().get('username')
    password = request.get_json().get('password')

    # Check preconditions
    if username is None or password is None:
        return jsonify({'success': False, 'message': "Missing fields"})

    # Add user
    success = users.add_user(username, password)
    message = "user correctly created" if success else "username already in use"
    return jsonify({'success': success, 'message': message})


@users_bp.route("/api/token", methods=['GET'])
@users.is_logged_in
def token():
    return jsonify({'token': users.generate_auth_token().decode('utf-8')})