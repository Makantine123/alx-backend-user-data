#!/usr/bin/env python3
"""Module contains SessionAuth class"""

from typing import Dict, TypeVar
import uuid

from .auth import Auth


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

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns user instance based on the cookie value"""
        if request:
            try:
                session_id = self.session_cookie(request)
                if session_id:
                    user_id = self.user_id_by_session_id(session_id)
                    if user_id:
                        user = User.get(user_id)
                        if user:
                            return user
            except Exception:
                return None
