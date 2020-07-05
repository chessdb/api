# -*- coding: utf-8 -*-
"""Example Google style docstrings.

"""
import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr

from chessdb_api.schemas import base


class User(base.Base):
    """User.
    """
    identifier: uuid.UUID
    name: str
    email: EmailStr
    password: str
    admin: bool = False


class UserCreateIn(BaseModel):
    """UserCreateIn.
    """

    name: str
    email: EmailStr
    password: str


class UserUpdateIn(BaseModel):
    """UserUpdateIn.
    """

    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
