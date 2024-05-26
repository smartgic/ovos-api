"""Models related to skills
"""

from typing import Dict, AnyStr, Any
from pydantic import BaseModel


class Skill(BaseModel):
    """Model for individual skill output"""

    active: bool
    id: str


class Skills(BaseModel):
    """Model for skills as results"""

    count: int
    count_active: int
    count_inactive: int
    results: Dict[AnyStr, Skill]


class Setting(BaseModel):
    """Model for setting option"""

    key: Any


class Settings(BaseModel):
    """Model for skill settings as results"""

    results: Setting


class Install(BaseModel):
    """Model for skill install"""

    skill: str
    dialog: str
    lang: str


class Uninstall(Install):
    """Model for skill uninstall"""
