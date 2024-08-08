#!/usr/bin/env python3
"""
Create SessionAuth that inherits form Auth
"""
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """ Session authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create session for user id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        id = str(uuid4())
        self.user_id_by_session_id[id] = user_id

        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves user id using session id"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """Use session id to Identify user"""
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Destroy sessions"""
        if request is None:
            return False
        session_id_cookie = self.session_cookie(request)
        if not session_id_cookie:
            return False
        user_id = self.user_id_for_session_id(session_id_cookie)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id_cookie]
        return True
