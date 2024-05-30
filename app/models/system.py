"""Models related to system
"""

from typing import Any
from pydantic import BaseModel


class Cache(BaseModel):
    """Model for cache POST action"""

    cache_type: str


class InfoLocales(BaseModel):
    city: str
    country: str
    timezone: str
    lang: str


class InfoSystem(BaseModel):
    architecture: str
    os: str
    kernel: str

class Info(BaseModel):
    """Model information"""
    name: str
    core_version: str
    tts_engine: str
    locales: InfoLocales
    log_level: str
    system: InfoSystem


class InfoResults(BaseModel):
    """Model information output"""

    results: Info


class Config(BaseModel):
    """Model configuration output"""

    key: Any


class ConfigResults(BaseModel):
    """Model configuration output"""

    results: Config
