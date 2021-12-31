"""Handles network requirements
"""
from random import choice
from typing import List
from fastapi import HTTPException, status
from app.common.utils import ws_send, requirements
from app.common.typing import JSONStructure
from app.config import get_settings

settings = get_settings()


def ping() -> JSONStructure:
    """Get the API status

    :return: Return famous ping pong players
    :rtype: JSONResponse
    """
    try:
        players: List = [
            "Jan-Ove Waldner",
            "Liu Guoliang",
            "Deng Yaping",
            "Qiao Hong",
            "Guo Yue",
            "Xu Xin",
            "Wang Liqin",
            "Ma Long"
        ]
        return {"pong": choice(players)}
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unable to retrieve the api status") from err


def internet() -> JSONStructure:
    """Get Internet connection status

    :return: Return Internet connectivity status as boolean
    :rtype: JSONResponse
    """
    status_code: int = status.HTTP_400_BAD_REQUEST
    msg: str = "unable to retrieve the connectivity status"
    try:
        payload = {
            "type": "mycroft.api.internet",
            "data": {
                "app_key": settings.app_key,
            }
        }
        if requirements():
            internet: JSONStructure = ws_send(
                payload, "mycroft.api.internet.answer")
            if internet["context"]["authenticated"]:
                return {"connected": internet["data"]}
            status_code = status.HTTP_401_UNAUTHORIZED
            msg = "unable to authenticate with mycroft-api skill"
            raise Exception
        status_code = status.HTTP_401_UNAUTHORIZED
        msg = "mycroft-api skill is not installed on mycroft core"
        raise Exception
    except Exception as err:
        raise HTTPException(
            status_code=status_code,
            detail=msg) from err


def websocket() -> JSONStructure:
    """Get websocket connection status

    :return: Return websocket connection status as boolean
    :rtype: JSONResponse
    """
    status_code: int = status.HTTP_200_OK
    msg: dict = {"listening": False}
    try:
        payload = {
            "type": "mycroft.api.websocket",
            "data": {
                "app_key": settings.app_key,
            }
        }
        if requirements():
            websocket: JSONStructure = ws_send(
                payload, "mycroft.api.websocket.answer")
            if websocket["context"]["authenticated"]:
                return {"listening": websocket["data"]["listening"]}
            status_code = status.HTTP_401_UNAUTHORIZED
            msg = "unable to authenticate with mycroft-api skill"
            raise Exception
        status_code = status.HTTP_401_UNAUTHORIZED
        msg = "mycroft-api skill is not installed on mycroft core"
        raise Exception
    except Exception as err:
        raise HTTPException(
            status_code=status_code,
            detail=msg) from err
