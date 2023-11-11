#!/usr/bin/env python3
"""Session authentication views"""

from os import getenv
from flask import make_response, request, jsonify
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
    if len(founduser) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in founduser:
        if user.is_valid_password(form_password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            cookie = getenv("SESSION_NAME")
            user_dict = user.to_json()
            response = make_response(jsonify(user_dict))
            response.set_cookie(cookie, session_id)
            return response
    return jsonify({"error": "wrong password"}), 401
