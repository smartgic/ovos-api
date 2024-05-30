"""Handles systems requirements
"""

import json
from typing import Dict, Optional
from fastapi import HTTPException, status
from app.common.typing import JSONStructure
from app.models.system import InfoResults, Cache, Config
from app.models.voice import Speak
from app.common.utils import ws_send, requirements, sanitize
from app.config import get_settings
from app.handlers.voice import speaking

settings = get_settings()


def get_info(sort: Optional[bool] = False) -> InfoResults:
    """Retrieves system information by leveraging the skill-rest-api

    Send `"ovos.api.info` message and wait for `ovos.api.info.answer`
    message to appear on the bus.

    :param sort: Sort alphabetically the information
    :type sort: bool, optional
    :return: Return information
    :rtype: InfoResults
    """
    status_code: int = status.HTTP_400_BAD_REQUEST
    msg: str = "unable to retrieve system information"
    try:
        payload: Dict = {
            "type": "ovos.api.info",
            "data": {"app_key": settings.app_key},
        }
        if requirements():
            info: JSONStructure = ws_send(payload, "ovos.api.info.answer")
            if info["context"]["authenticated"]:
                if sort:
                    info = json.loads(json.dumps(info, sort_keys=True))
                return {"results": info["data"]}
            status_code = status.HTTP_401_UNAUTHORIZED
            msg = "unable to authenticate with skill-rest-api"
            raise Exception
        status_code = status.HTTP_401_UNAUTHORIZED
        msg = "skill-rest-api is not installed on ovos core"
        raise Exception
    except Exception as err:
        raise HTTPException(status_code=status_code, detail=msg) from err


# def get_config(sort: Optional[bool] = False,
#                core: Optional[bool] = False) -> Config:
#     """Retrieves local or core configuration by leveraging the
#     mycroft-api skill

#     Send `"mycroft.api.config` message and wait for `mycroft.api.config.answer`
#     message to appear on the bus.

#     :param sort: Sort alphabetically the configuration
#     :type sort: bool, optional
#     :param core: Retrieve the core configuration
#     :type core: bool, optional
#     :return: Return configuration
#     :rtype: Config
#     """
#     status_code: int = status.HTTP_400_BAD_REQUEST
#     msg: str = "unable to retrieve configuration"
#     try:
#         payload: Dict = {
#             "type": "mycroft.api.config",
#             "data": {
#                 "app_key": settings.app_key,
#                 "core": core
#             }
#         }
#         if requirements():
#             config: JSONStructure = ws_send(
#                 payload, "mycroft.api.config.answer")
#             if config["context"]["authenticated"]:
#                 if sort:
#                     config = json.loads(json.dumps(config, sort_keys=True))
#                 return sanitize(config["data"])
#             status_code = status.HTTP_401_UNAUTHORIZED
#             msg = "unable to authenticate with mycrfot-api skill"
#             raise Exception
#         status_code = status.HTTP_401_UNAUTHORIZED
#         msg = "mycroft-api skill is not installed on mycroft core"
#         raise Exception
#     except Exception as err:
#         raise HTTPException(
#             status_code=status_code,
#             detail=msg) from err


# def log_level(level: str, bus: Optional[bool] = True) -> int:
#     """Change the log level and the bus message logging.

#     Send `mycroft.debug.log` message with the log level and the bus status
#     as payload.

#     :param level: Skill ID to deactivate
#     :type level: str
#     :param bus: Enable or disable the bus message logging
#     :type bus: bool, optional
#     :return: Return HTTP 204 or 400
#     :rtype: int
#     """
#     try:
#         payload: Dict = {
#             "type": "mycroft.debug.log",
#             "data": {"level": level, "bus": bus},
#         }
#         ws_send(payload)
#         return status.HTTP_204_NO_CONTENT
#     except Exception as err:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="unable to change the services log level",
#         ) from err


def sleep(confirm: Optional[bool] = True, dialog: Optional[Speak] = None) -> Speak:
    """Put OVOS into sleep mode

    Send `recognizer_loop:sleep` message to the bus.

    :param confirm: Ask for a confirmation
    :type confirm: bool, optional
    :param dialog: Confirmation message to send
    :type dialog: Speak, optional
    :return: Return JSON payload
    :rtype: dict
    """
    status_code: int = status.HTTP_400_BAD_REQUEST
    msg: str = "unable to put mycroft into sleep moden"
    try:
        payload: Dict = {
            "type": "recognizer_loop:sleep",
            "data": {"app_key": settings.app_key},
        }
        if requirements():
            sleep: JSONStructure = ws_send(payload, "ovos.api.sleep.answer")
            if sleep["context"]["authenticated"]:
                if confirm and dialog:
                    payload = Speak(utterance=dialog.utterance, lang=dialog.lang)
                    return speaking(payload)
                return {"sleep_mode": "enabled"}
            status_code = status.HTTP_401_UNAUTHORIZED
            msg = "unable to authenticate with skill-rest-api"
            raise Exception
        status_code = status.HTTP_401_UNAUTHORIZED
        msg = "skill-rest-api is not installed on ovos core"
        raise Exception
    except Exception as err:
        raise HTTPException(status_code=status_code, detail=msg) from err


def wake_up(confirm: Optional[bool] = True, dialog: Optional[Speak] = None) -> Speak:
    """Wake up OVOS from sleep mode

    Send `recognizer_loop:wake_up` message to the bus.

    :param confirm: Ask for a confirmation
    :type confirm: bool, optional
    :param dialog: Confirmation message to send
    :type dialog: Speak, optional
    :return: Return JSON payload
    :rtype: dict
    """
    status_code: int = status.HTTP_400_BAD_REQUEST
    msg: str = "unable to wake up mycroft"
    try:
        payload: Dict = {
            "type": "recognizer_loop:wake_up",
            "data": {"app_key": settings.app_key},
        }
        wake_up: JSONStructure = ws_send(payload, "ovos.api.wake_up.answer")
        if requirements():
            if wake_up["context"]["authenticated"]:
                if confirm and dialog:
                    payload: Speak = Speak(utterance=dialog.utterance, lang=dialog.lang)
                    return speaking(payload)
                return {"sleep_mode": "disabled"}
            status_code = status.HTTP_401_UNAUTHORIZED
            msg = "unable to authenticate with skill-rest-api"
            raise Exception
        status_code = status.HTTP_401_UNAUTHORIZED
        msg = "skill-rest-api is not installed on ovos core"
    except Exception as err:
        raise HTTPException(status_code=status_code, detail=msg) from err


def is_awake() -> JSONStructure:
    """Retrieve sleep mode status by leveraging the skill-rest-api

    Send `mycroft.api.is_awake` message and wait for
    `mycroft.api.is_awake.answer` message to appear on the bus.

    :return: Return sleep mode status
    :rtype: JSONStructure
    """
    status_code: int = status.HTTP_400_BAD_REQUEST
    msg: str = "unable to get sleep mode status"
    try:
        payload = {
            "type": "ovos.api.is_awake",
            "data": {"app_key": settings.app_key},
        }
        if requirements():
            info: JSONStructure = ws_send(payload, "ovos.api.is_awake.answer")
            if info["context"]["authenticated"]:
                return info["data"]
            status_code = status.HTTP_401_UNAUTHORIZED
            msg = "unable to authenticate with skill-rest-api"
            raise Exception
        status_code = status.HTTP_401_UNAUTHORIZED
        msg = "skill-rest-api is not installed on ovos core"
        raise Exception
    except Exception as err:
        raise HTTPException(status_code=status_code, detail=msg) from err


def caching(cache: Cache) -> JSONStructure:
    """Delete cached files by leveraging the kill-rest-api

    Send `ovos.api.cache` message to the bus.

    :return: Return deleted cache type
    :rtype: dict
    """
    status_code: int = status.HTTP_400_BAD_REQUEST
    msg: str = "unable to clear cache"
    try:
        data: Cache = Cache(cache_type=cache.cache_type)
        payload: Dict = {
            "type": "ovos.api.cache",
            "data": {"app_key": settings.app_key, "cache_type": data.cache_type},
        }
        if requirements():
            cache: JSONStructure = ws_send(payload, "ovos.api.cache.answer")
            if cache["context"]["authenticated"]:
                return cache["data"]
            status_code = status.HTTP_401_UNAUTHORIZED
            msg = "unable to authenticate with skill-rest-api"
            raise Exception
        status_code = status.HTTP_401_UNAUTHORIZED
        msg = "skill-rest-api is not installed on ovos core"
        raise Exception
    except Exception as err:
        raise HTTPException(status_code=status_code, detail=msg) from err


# def reload_config() -> int:
#     """Reload configuration

#     Send `configuration.updated` message to the bus, services will reload
#     the configuration file.

#     :return: Return HTTP 204 or 400
#     :rtype: int
#     """
#     try:
#         payload: Dict = {
#             "type": "configuration.updated"
#         }
#         ws_send(payload)
#         return status.HTTP_204_NO_CONTENT
#     except Exception as err:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="unable to reload the configuration ") from err
