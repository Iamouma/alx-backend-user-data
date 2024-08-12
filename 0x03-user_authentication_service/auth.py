#!/usr/bin/env python3
"""
Hash password
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
    Hash password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
