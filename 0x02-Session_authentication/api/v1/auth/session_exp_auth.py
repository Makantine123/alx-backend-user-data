#!/usr/bin/env python3
"""Module contains SessionExpAuth"""

from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""

    def __init__(self) -> None:
        """Initialisation of class"""
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """Create session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None):
        """Return user id from session"""
        try:
            if session_id is None:
                return None
            if session_id not in self.user_id_by_session_id:
                return None
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0 or "created_at" not in session_dict:
                return session_dict.get("user_id")
            created_at = session_dict.get("created_at")
            if (created_at + timedelta(seconds=self.session_duration)) < datetime.now():
                return None
            return session_dict.get("user_id")
        except Exception:
            return None
