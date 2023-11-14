#!/usr/bin/env python3
"""_hash_password module"""

import bcrypt
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import User
from db import DB


def _hash_password(password: str) -> bytes:
    """hash password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


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
