#!/usr/bin/env python3
"""
API routes for authentication services
"""
from auth import Auth
from flask import (Flask, jsonify, request, abort, redirect)

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello_world() -> str:
    """
    Base route for authentication service API
    """
    msg = {"message": "Bienvenue"}
    return jsonify(msg)


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """
    Register a new user if it does not exist
    """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    msg = {"email": email, "message": "user created"}
    return jsonify(msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
