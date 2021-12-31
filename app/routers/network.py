"""Network routes
"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.models.network import Pong, Internet, Websocket
from app.config import get_settings
from app.auth.bearer import JWTBearer
from app.handlers import network

router = APIRouter(
    prefix="/network",
    tags=["network"])

settings = get_settings()


@router.get(
    "/ping",
    response_model=Pong,
    status_code=status.HTTP_201_CREATED,
    summary="Get the API status",
    description="Send a request to monitor the API",
    response_description="API status")
async def ping() -> JSONResponse:
    """Get the API status

    :return: Return famous ping pong players
    :rtype: JSONResponse
    """
    return JSONResponse(content=network.ping())


@router.get(
    "/internet",
    response_model=Internet,
    status_code=status.HTTP_201_CREATED,
    summary="Get Internet connection status",
    description="Check for internet connectivity",
    response_description="Connectivity status",
    dependencies=[Depends(JWTBearer())],)
async def internet() -> JSONResponse:
    """Get Internet connection status

    :return: Return Internet connectivity status as boolean
    :rtype: JSONResponse
    """
    return JSONResponse(content=network.internet())


@router.get(
    "/websocket",
    response_model=Websocket,
    status_code=status.HTTP_201_CREATED,
    summary="Get websocket connection status",
    description="Check for websocket connectivity",
    response_description="Connectivity status",
    dependencies=[Depends(JWTBearer())],)
async def websocket() -> JSONResponse:
    """Get websocket connection status

    :return: Return websocket connectivity status as boolean
    :rtype: JSONResponse
    """
    return JSONResponse(content=network.websocket())
