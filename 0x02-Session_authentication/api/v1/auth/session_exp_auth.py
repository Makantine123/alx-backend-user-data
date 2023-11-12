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
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        created_at = session_dict.get("created_at")
        if created_at is None:
            del self.user_id_by_session_id[session_id]
            return None
        if self.session_duration > 0:
            expiration_time = created_at + timedelta(seconds=self.session_duration)

            if datetime.now() > expiration_time:
                del self.user_id_by_session_id[session_id]
                return None
        return session_dict.get("user_id") 
