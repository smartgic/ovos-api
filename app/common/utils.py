"""Functions use multiple times in different places across the application
"""

import json
from typing import List, Optional, Dict
from time import time
from websocket import create_connection, WebSocketException, WebSocketTimeoutException
from app.config import get_settings
from app.common import constants
from app.common.typing import JSONStructure

settings = get_settings()


def ws_send(
    payload: JSONStructure, wait_for_message: Optional[str] = None
) -> JSONStructure:
    """Handles websocket interactions, from the connection,
    the send/receive message and the closing.

    :param payload: JSON dict to send to the bus
    :type payload: dict
    :param wait_for_message: Message to wait for from the bus
    :type wait_for_message: str, optional
    :return: Return the received message or and empty dict if nothing to retrun
    :rtype: JSONStructure
    """
    websocket = None
    try:
        websocket = create_connection(
            url=settings.ws_uri, timeout=settings.ws_conn_timeout
        )
    except WebSocketTimeoutException as err:
        return err

    try:
        # If message is expected as answer then we enter in a loop. The loop
        # will timeout after 3 seconds if no message equal to wait_for_message
        # is received.
        if wait_for_message:
            timeout_start: float = time()
            data: Dict = {}
            websocket.send(json.dumps(payload))
            while time() < timeout_start + settings.ws_recv_timeout:
                recv: JSONStructure = json.loads(websocket.recv())
                if recv["type"] == wait_for_message and recv["data"]:
                    data = recv
                    break
                # Check for authentication if required.
                if (
                    recv["type"] == wait_for_message
                    and not recv["context"]["authenticated"]
                ):
                    data = recv
                    break
            websocket.close()
            return data

        # Send message without wait for message and return an empty JSON dict.
        websocket.send(json.dumps(payload))
        websocket.close()
        return {}
    except WebSocketException as err:
        websocket.close()
        return err


def requirements() -> bool:
    """Checks for requirements such as skill-restart-api which will
    retrieve local information from Mycroft core instance.

    :return: Return the status of the requirements
    :rtype: bool
    """
    try:
        payload: dict = {
            "type": "skillmanager.list",
        }
        skills: JSONStructure = ws_send(payload, "mycroft.skills.list")
        status: bool = False
        for key in skills["data"]:
            if (
                skills["data"][key]["id"] == constants.API_SKILL_ID
                and skills["data"][key]["active"]
            ):
                status = True
        return status
    except KeyError as err:
        return err


def sanitize(data: JSONStructure) -> JSONStructure:
    """Sanitizes JSON dictionnary to avoid data leaking.

    By default, `password`, `key, `code` and `username` are keys that will
    be popped-out from the dict.

    :param data: JSON dictionnary to sanitize
    :type data: JSONStructure
    :return: Sanitized JSON dictionanry
    :rtype: JSONStructure
    """
    if settings.hide_sensitive_data:
        keys: List = constants.SANITIZE_KEY_LIST
        for key in keys:
            data.pop(key, None)
        return data
    return data
