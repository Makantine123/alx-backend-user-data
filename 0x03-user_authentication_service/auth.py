#!/usr/bin/env python3
"""_hash_password module"""

import bcrypt
import uuid
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import User
from db import DB


def _hash_password(password: str) -> bytes:
    """hash password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generates a new uuid"""
    new_uuid = uuid.uuid4()
    return str(new_uuid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initialisation of class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except ValueError as err:
            raise err
        except Exception:
            hash_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hash_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks if passed password matches encrypted password on database
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            else:
                return False
        except (InvalidRequestError, NoResultFound):
            return False

    def create_session(self, email: str) -> str:
        """Creates a new session ID"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (InvalidRequestError, NoResultFound):
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get user from session id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (InvalidRequestError, NoResultFound):
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys user session"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except (InvalidRequestError, NoResultFound):
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Reset token"""
        try:
            user = self._db.find_user_by(email=email)
        except (InvalidRequestError, NoResultFound):
            user = None
        if user is None:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates password using reset token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        hashed_pwd = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_pwd,
            reset_token=None,
        )
