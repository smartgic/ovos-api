"""Handles authentication requirements
"""
from fastapi import HTTPException, status
from app.auth.bearer import JWTBearer
from app.auth.handlers import get_user, verify_password, encode_access_jwt, \
    encode_refresh_jwt, refresh_jwt
from app.common.typing import JSONStructure
from app.config import get_settings
from app.models.auth import Tokens, User, AccessToken

settings = get_settings()


def tokens(info: User) -> JSONStructure:
    """Generate access and refresh tokens

    :param info: User and password information
    :type info: User
    :return: Return access and refresh tokens
    :rtype: JSONStructure
    """
    user = get_user(info.user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid user")
    if not verify_password(info.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid password")
    tokens: Tokens = Tokens(
        access_token=encode_access_jwt(info.user),
        refresh_token=encode_refresh_jwt(info.user)
    )
    payload: dict = {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token
    }
    return payload


def refresh(refresh_token: str) -> JSONStructure:
    """Generate access token based on a refresh token

    :param refresh_token: Refresh token
    :type refresh_token: str
    :return: Return an access token
    :rtype: JSONStructure
    """
    auth = JWTBearer()
    auth.verify_refresh_jwt(refresh_token)
    token: AccessToken = AccessToken(
        access_token=refresh_jwt(refresh_token),
    )
    payload: dict = {
        "access_token": token.access_token
    }
    return payload
