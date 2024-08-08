#!/usr/bin/env python3
"""
Import Flask from flask module
"""
from flask import request, jsonify, session
from models.user import User
from api.v1.views import app_views
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session() -> str:
    """Auth session"""
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    if user_email is None or user_email == "":
        return {"error": "email missing"}, 400
    if user_password is None or user_password == "":
        return {"error": "password missing"}, 400
    users = User.search({'email': user_email})
    if users is None or users == []:
        return {"error": "no user found for this email"}, 404

    for user in users:
        if user.is_valid_password(user_password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            session_name = getenv("SESSION_NAME")
            response = jsonify(user.to_json())
            response.set_cookie(session_name, session_id)
            return response
    return {"error": "wrong password"}, 401


@app_views.\
    route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def auth_session_logout() -> str:
    """Logout"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return {}, 200
    return {"error": "no user found"}, 404
