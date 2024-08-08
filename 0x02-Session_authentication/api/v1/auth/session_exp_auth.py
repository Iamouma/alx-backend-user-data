#!/usr/bin/env python3
"""Set session expiration"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta

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
        if session_id is None or not isinstance(session_id, str):
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if created_at is None:
            return None

        if datetime.now() > created_at + timedelta(seconds=self.session_duration):
            return None

        return session_dict.get("user_id")
