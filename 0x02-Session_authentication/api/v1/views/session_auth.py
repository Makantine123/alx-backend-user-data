#!/usr/bin/env python3
"""Session authentication views"""

from os import getenv
from flask import make_response, request, jsonify, session
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def session_authentication():
    """Returns a response with user object and set coockie"""
    form_email = request.form.get("email")
    form_password = request.form.get("password")

    if not form_email:
        return jsonify({"error": "email missing"}), 400
    if not form_password:
        return jsonify({"error": "password missing"}), 400
    attributes = {"email": form_email}
    founduser = User.search(attributes)
    if not founduser:
        return jsonify({"error": "no user found for this email"}), 404
    if not founduser[0].is_valid_password(form_password):
        return jsonify({"error": "wrong password"}), 404
    from api.v1.app import auth
    session_id = auth.create_session(founduser[0].id)
    user_dict = founduser[0].to_json()
    response = make_response(jsonify(user_dict))
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response
