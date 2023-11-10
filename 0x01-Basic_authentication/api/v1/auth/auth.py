#!/usr/bin/env python3
"""Authentication module"""

from flask import request

from typing import List, TypeVar

import fnmatch


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Required path"""
        check = path
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        #if path[-1] != "/":
            check += "/"
        #if check in excluded_paths or path in excluded_paths:
        #    return False
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and fnmatch.fnmatch(path, excluded_path[:-1]):
                return False
            elif path == excluded_path:
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
