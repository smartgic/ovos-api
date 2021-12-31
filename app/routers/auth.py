"""Auth routes
"""
from fastapi import APIRouter, status, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.models.auth import User, Tokens, AccessToken
from app.config import get_settings
from app.handlers import auth

router = APIRouter(
    prefix="/auth",
    tags=["auth"])

settings = get_settings()


@router.post(
    "/tokens",
    response_model=Tokens,
    status_code=status.HTTP_201_CREATED,
    summary="Get access and refresh tokens",
    description="Send a request to retrieve an access and a refresh token"
                "based on user password authentication",
    response_description="Tokens created")
async def tokens(info: User) -> JSONResponse:
    return JSONResponse(content=auth.tokens(info))


@router.get(
    "/refresh",
    response_model=AccessToken,
    status_code=status.HTTP_200_OK,
    summary="Get refreshed access token",
    description="Send a request to refresh an access token based on a"
                "refresh token",
    response_description="Token refreshed")
async def refresh(credentials: HTTPAuthorizationCredentials =
                  Security(HTTPBearer())) -> JSONResponse:
    return JSONResponse(content=auth.refresh(credentials.credentials))
