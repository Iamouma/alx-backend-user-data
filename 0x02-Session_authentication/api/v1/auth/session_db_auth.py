#!/usr/bin/env python3
"""SessionDBAuth class"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""
    def create_session(self, user_id=None):
        """Create session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_id = UserSession(user_id=user_id, session_id=session_id)
        user_id.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves user id using session id"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user_id = UserSession.get(session_id)
        if not user_id:
            return None
        return user_id

    def destroy_session(self, request=None):
        """Destroy session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        user_id.delete()
        return True
