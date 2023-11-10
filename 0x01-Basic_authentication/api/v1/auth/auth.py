#!/usr/bin/env python3
"""Authentication module"""

from flask import request

from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Required path"""
        if not excluded_paths or not path:
            return True
        path = path if path.endswith("/") else path + "/"
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.strip("*")):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorized header"""
        if request is None:
            return None
        if not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
