#!/usr/bin/env python3
"""Module contains SessionAuth class"""

from typing import Dict
import uuid

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session Authentication class"""

    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """Create session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns user_id for a gevin session_id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return str(user_id)

    def current_user(self, request=None):
        """Returns user instance based on the cookie value"""
        try:
            session_id = self.session_cookie(request)
            user_id = self.user_id_for_session_id(session_id)
            user = User.get(str(user_id))
            return user
        except Exception:
            return None

    def destroy_session(self, request=None):
        """Deletes user session/logout.
        Returns True if sucess otherwise false"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
