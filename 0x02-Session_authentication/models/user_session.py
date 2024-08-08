#!/usr/bin/env python3
""" UserSession module """

from models.base import Base
from datetime import datetime


class UserSession(Base):
    """ UserSession class to store session information """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a new UserSession """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        self.created_at = datetime.now()
