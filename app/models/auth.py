"""Models related to auth
"""
from pydantic import BaseModel


class User(BaseModel):
    """Model for user
    """
    user: str
    password: str


class Tokens(BaseModel):
    """Model for tokens
    """
    access_token: str
    refresh_token: str


class AccessToken(BaseModel):
    """Model for access token
    """
    access_token: str
