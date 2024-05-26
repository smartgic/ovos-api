"""Handles voice requirements
"""

from typing import Dict
from fastapi import HTTPException, status
from app.common.typing import JSONStructure
from app.common.utils import ws_send
from app.config import get_settings
from app.models.voice import Speak

settings = get_settings()


def speaking(speak: Speak) -> JSONStructure:
    """Send a speak request to Mycroft

    Send `speak` message to the bus with the utterance to speak.

    :param speak: Which utterance ans lang to send
    :type speak: Speak
    :return: Return JSON dict with the utterance and the lang
    :rtype: JSONStructure
    """
    try:
        payload: Dict = {
            "type": "speak",
            "data": {"utterance": speak.utterance, "lang": speak.lang},
        }
        ws_send(payload)
        return payload["data"]
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unable to send the utterance",
        ) from err


def stop() -> JSONStructure:
    """Send a stop speech request to Open Voice OS

    Send `mycroft.stop` message to the bus to stop the speech.

    :return: Return HTTP 204 or 400
    :rtype: int
    """
    try:
        payload: Dict = {"type": "mycroft.stop"}
        ws_send(payload)
        return status.HTTP_204_NO_CONTENT
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="unable to stop the speech"
        ) from err


def mute() -> JSONStructure:
    """Send a microphone mute request to Open Voice OS

    Send `mycroft.mic.mute` message to the bus to mute the microphone.

    :return: Return HTTP 204 or 400
    :rtype: int
    """
    try:
        payload: Dict = {"type": "mycroft.mic.mute"}
        ws_send(payload)
        return status.HTTP_204_NO_CONTENT
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="unable to mute microphone"
        ) from err


def unmute() -> JSONStructure:
    """Send a microphone unmute request to Open Voice OS

    Send `mycroft.mic.unmute` message to the bus to unmute the microphone.

    :return: Return HTTP 204 or 400
    :rtype: int
    """
    try:
        payload: Dict = {"type": "mycroft.mic.unmute"}
        ws_send(payload)
        return status.HTTP_204_NO_CONTENT
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unable to unmute microphone",
        ) from err


def listen() -> JSONStructure:
    """Send a recording request to Open Voice OS

    Send `mycroft.mic.listen` message to the bus to start the recording.

    :return: Return HTTP 204 or 400
    :rtype: int
    """
    try:
        payload: Dict = {"type": "mycroft.mic.listen"}
        ws_send(payload)
        return status.HTTP_204_NO_CONTENT
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unable to start the recording",
        ) from err
