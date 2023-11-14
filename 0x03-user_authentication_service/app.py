#!/usr/bin/env python3
"""App"""

from flask import Flask, abort, jsonify, make_response, redirect, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """users"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        AUTH.register_user(email=email, password=password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """login function"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        mydict = jsonify({"email": email, "message": "logged in"})
        response = make_response(mydict)
        response.set_cookie("session_id", session_id)
        return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """logout function"""
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
