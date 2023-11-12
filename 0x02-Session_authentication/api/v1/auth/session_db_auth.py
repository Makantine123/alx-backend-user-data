#!/usr/bin/env python3
"""Module contains SessionDBAuth class"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession

class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id=None):
        """Creates a user session"""
        user_session = UserSession()
        user_id = user_session.user_id
        return super().create_session(user_id)

    def user_id_for_session_id(self, session_id: str = None):
        """Returns user id by requesting UserSession in the DB based on session_id"""
        attributes = {"session_id": session_id}
        try:
            user_id = UserSession.search(attributes)
            return user_id
        except Exception:
            return None

    def destroy_session(self, request=None):
        return super().destroy_session(request)
