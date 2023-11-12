#!/usr/bin/env python3
"""Module contains SessionExpAuth"""

from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""

    def __init__(self):
        """Initialisation of class"""
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        session_id = super().create_session(user_id)
        if not session_id:
            return
