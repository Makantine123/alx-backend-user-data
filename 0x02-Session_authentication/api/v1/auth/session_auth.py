#!/usr/bin/env python3
"""Module contains SessionAuth class"""

from typing import Dict
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
