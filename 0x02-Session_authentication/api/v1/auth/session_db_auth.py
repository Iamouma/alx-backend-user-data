#!/usr/bin/env python3
"""SessionDBAuth class"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""
    
    def create_session(self, user_id=None):
        """Create session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves user id using session id"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        UserSession.load_from_file()
        sessions = UserSession.search({"session_id": session_id})
        if not sessions:
            return None
        
        session = sessions[0]
        if self.session_duration <= 0:
            return session.user_id

        if session.created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """Destroy session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        
        UserSession.load_from_file()
        sessions = UserSession.search({"session_id": session_id})
        if not sessions:
            return False
        
        session = sessions[0]
        session.remove()
        return True

