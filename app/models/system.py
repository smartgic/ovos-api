"""Models related to system
"""

from typing import Any
from pydantic import BaseModel


class Cache(BaseModel):
    """Model for cache POST action"""

    cache_type: str


class Info(BaseModel):
    """Model information"""

    core_version: str
    platform: str
    lang: str
    tts_engine: str
    audio_backend: str
    name: str
    city: str
    country: str
    timezone: str


class InfoResults(BaseModel):
    """Model information output"""

    results: Info


class Config(BaseModel):
    """Model configuration output"""

    key: Any


class ConfigResults(BaseModel):
    """Model configuration output"""

    results: Config
