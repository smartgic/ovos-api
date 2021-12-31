"""Models related to network
"""
from pydantic import BaseModel


class Pong(BaseModel):
    """Model for pong
    """
    pong: str


class Internet(BaseModel):
    """Model for connectivity
    """
    connected: bool


class Websocket(BaseModel):
    """Model for Websocket
    """
    listening: bool
