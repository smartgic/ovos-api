"""System routes
"""

from typing import Optional
from fastapi.responses import JSONResponse, Response
from fastapi import APIRouter, Depends, status, Query, Body

from app.models.system import InfoResults, Cache, ConfigResults
from app.models.voice import Speak
from app.config import get_settings
from app.auth.bearer import JWTBearer
from app.handlers import system


router = APIRouter(prefix="/system", tags=["system"])

settings = get_settings()


@router.get(
    "/info",
    response_model=InfoResults,
    summary="Collect information",
    description="Send `ovos.api.info` message to the bus and wait \
        for `ovos.api.info.answer` response. This route leverage the \
        `skill-rest-api`.",
    response_description="Retrieved information",
    dependencies=[Depends(JWTBearer())],
)
async def info(
    sort: Optional[bool] = Query(
        default=False, description="Sort alphabetically the settings"
    )
) -> JSONResponse:
    """Collect information

    :param sort: Sort alphabetically the information
    :type sort: bool, optional
    :return: Return the information
    :rtype: JSONResponse
    """
    return JSONResponse(content=system.get_info(sort))


@router.get(
    "/config",
    response_model=ConfigResults,
    summary="Collect local or core configuration",
    description="Send `mycroft.api.config` message to the bus and wait \
        for `ovos.api.config.answer` response. This route leverage the \
        `skill-rest-api`.",
    response_description="Retrieved configuration",
    dependencies=[Depends(JWTBearer())],
)
async def config(
    sort: Optional[bool] = Query(
        default=False, description="Sort alphabetically the settings"
    )
) -> JSONResponse:
    """Collect local or core configuration

    :param sort: Sort alphabetically the configuration
    :type sort: bool, optional
    :return: Return the configuration
    :rtype: JSONResponse
    """
    return JSONResponse(content=system.get_config(sort))


@router.post(
    "/sleep",
    status_code=status.HTTP_201_CREATED,
    response_model=Speak,
    summary="Put OVOS in sleep mode",
    description="Send `recognizer_loop:sleep` message to the bus, the \
        `confirm` parameters will send a `speak` message to the bus",
    response_description="Mycroft is now asleep",
    dependencies=[Depends(JWTBearer())],
)
async def sleep(
    confirm: Optional[bool] = Query(
        default=False, description="Play a confirmation message"
    ),
    dialog: Optional[Speak] = Body(
        default=None,
        description="Confirmation message to play",
        example='{"utterance": "going to sleep", "lang": "en-us"}',
    ),
) -> Speak:
    """Put OVOS in sleep mode

    :param confirm: Play a confirmation message
    :type confirm: bool, optional
    :param dialog: Confirmation message to play
    :type dialog: dict, optional
    :return: Return payload sent
    :rtype: JSONResponse
    """
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=system.sleep(confirm, dialog)
    )


@router.post(
    "/wakeup",
    status_code=status.HTTP_201_CREATED,
    response_model=Speak,
    summary="Wake up OVOS from sleep mode",
    description="Send `recognizer_loop:wake_up` message to the bus, the \
        `confirm` parameters will send a `speak` message to the bus",
    response_description="Mycroft is now awake",
    dependencies=[Depends(JWTBearer())],
)
async def wake_up(
    confirm: Optional[bool] = Query(
        default=False, description="Play a confirmation message"
    ),
    dialog: Optional[Speak] = Body(
        default=None,
        description="Confirmation message to play",
        example='{"utterance": "i am awake", "lang": "en-us"}',
    ),
) -> Speak:
    """Wake up OVOS from sleep mode

    :param confirm: Play a confirmation message
    :type confirm: bool, optional
    :param dialog: Confirmation message to play
    :type dialog: dict, optional
    :return: Return payload sent
    :rtype: JSONResponse
    """
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=system.wake_up(confirm, dialog)
    )


@router.get(
    "/sleep",
    summary="Get sleep mode state",
    description="Read a file created by the `skill-rest-api` to retrieve \
        the information about Mycroft sleep state. This route leverage the \
        `skill-rest-api`.",
    response_description="Retrieved sleep state",
    dependencies=[Depends(JWTBearer())],
)
async def is_awake() -> JSONResponse:
    """Get sleep mode state

    :return: Return sleep state
    :rtype: JSONResponse
    """
    return JSONResponse(content=system.is_awake())


@router.delete(
    "/cache",
    status_code=status.HTTP_201_CREATED,
    response_model=Cache,
    summary="Clear caches",
    description="Clear different types of caches. For example the `tts` \
        cache type will retrieve the current TTS engine used and delete \
        the cached files. This route leverage the `skill-rest-api`.",
    response_description="Cache cleared",
    dependencies=[Depends(JWTBearer())],
)
async def caching(
    cache_type: Cache = Body(
        default=None,
        description="Type of cache to clear",
        example='{"cache_type": "tts"}',
    )
) -> Cache:
    """Clear caches

    :param cache_type: Type of cache to clear
    :type cache_type: dict
    :return: Return cache type deleted
    :rtype: JSONResponse
    """
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=system.caching(cache_type)
    )
