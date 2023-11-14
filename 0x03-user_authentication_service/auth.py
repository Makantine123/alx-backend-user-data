#!/usr/bin/env python3
"""_hash_password module"""

import bcrypt

from user import User
from db import DB


def _hash_password(password: str) -> str:
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
        """Valid login"""
        try:
            user = self._db.find_user_by(email=email)
            stored_hashed_password = user.hashed_password.encode("utf-8")
            provided_password = password.encode("utf-8")
            return bcrypt.checkpw(provided_password, stored_hashed_password)
        except Exception:
            return False
