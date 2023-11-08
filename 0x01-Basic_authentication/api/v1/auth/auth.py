#!/usr/bin/env python3
"""Authentication module"""

from flask import request

from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Required path"""
        check = path
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            check += "/"
        if check in excluded_paths or path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorized header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
