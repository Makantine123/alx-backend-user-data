#!/usr/bin/env python3
"""Authentication module"""

from flask import request

from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Required path"""
        if path.endswith("/"):
            path_with_slash = path
        else:
            path_with_slash = path + "/"
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for exclude in excluded_paths:
            if exclude.endswith("/"):
                exclude_with_slash = exclude
            else:
                exclude_with_slash = exclude + "/"
            last_segment = exclude_with_slash.split("/")[-1]
            if last_segment.endswith("*"):
                last_segment = last_segment[:-1]
                if last_segment in path_with_slash:
                    return False
        if path_with_slash in excluded_paths or path in excluded_paths:
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
