#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ This class manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method for validating if endpoint requires auth
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        # Check if the path matches any excluded path with a wildcard
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and path.startswith(excluded_path
                                                               [:-1]):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method that handles authorization header
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('user'):
        """
        Validats current user
        """
        return None
