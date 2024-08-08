#!/usr/bin/env python3
"""Set session expiration"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """Session expiration class"""
    def __init__(self):
        """Constructor"""
        self.session_duration = getenv("SESSION_DURATION", 0)
        try:
            self.session_duration = int(self.session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create session for user id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves user id using session id"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        if user_id is None:
            return None
        if self.session_duration <= 0:
            return user_id
        user_id1 = user_id.get("user_id")
        if user_id1 is None:
            return None
        created_at = user_id.get("created_at")
        if created_at is None:
            return None
        if (datetime.now() - created_at).seconds > self.session_duration:
            return None
        return user_id1
