"""Configuration file for the application behavior
"""
from base64 import b64encode
from functools import lru_cache
from pydantic import BaseSettings
from decouple import config


class Settings(BaseSettings):
    """Class that host the application options.
    All the variables ara casted by Pydantic.
    """
    app_name: str = "Mycroft AI API"
    app_version: str = "1.0.0"
    app_key: str = b64encode(config("API_KEY").encode("utf-8"))
    cryto_scheme: str = "bcrypt"
    users_db: str = config("USERS_DB")
    prefix_version: str = "/v1"
    ws_uri: str = f'ws://{config("WS_HOST")}:{config("WS_PORT")}/core'
    ws_conn_timeout: int = 10
    ws_recv_timeout: int = 5
    jwt_algorithm: str = "HS256"
    jwt_secret: str = config("SECRET")
    jwt_access_expiration: int = 1800
    jwt_refresh_expiration: int = 21600
    hide_sensitive_data: bool = True


@lru_cache()
def get_settings():
    """Expose the settings

    :return: Return the settings
    :rtype: Settings
    """
    return Settings()
