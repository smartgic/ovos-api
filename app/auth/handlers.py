"""Handlers for JWT authentication
"""
import json
from pathlib import Path
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jwt import encode, decode, DecodeError, InvalidSignatureError
from app.config import get_settings
from app.common.constants import JWT_SCOPES, JWT_ISSUER

settings = get_settings()


def encode_access_jwt(user: str) -> str:
    """Generate an access JWT token

    The token will expire based on the `jwt_access_expiration` option
    in `config.py`.

    :param user: User to use as a subject
    :type user: str
    :return: Return a JWT access token
    :rtype: str
    """
    try:
        # Follow the RFC: https://datatracker.ietf.org/doc/html/rfc7519
        payload: dict = {
            "sub": user,
            "exp": datetime.utcnow() + timedelta(
                days=0, seconds=settings.jwt_access_expiration),
            "iat": datetime.utcnow(),
            "iss": JWT_ISSUER,
            "scope": JWT_SCOPES["access"],
        }
        # Encode the payload based on options from config.py
        #  - jwt_secret
        #  - jwt_algorithm
        token = encode(payload, settings.jwt_secret,
                       algorithm=settings.jwt_algorithm)
        return token
    except InvalidSignatureError as err:
        return err


def encode_refresh_jwt(user: str) -> str:
    """Generate a refresh JWT token

    The token will expire based on the `jwt_refresh_expiration` option
    in `config.py`.

    :param user: User to use as a subject
    :type user: str
    :return: Return a JWT refresh token
    :rtype: str
    """
    try:
        # Follow the RFC: https://datatracker.ietf.org/doc/html/rfc7519
        payload: dict = {
            "sub": user,
            "exp": datetime.utcnow() + timedelta(
                days=0, seconds=settings.jwt_refresh_expiration),
            "iat": datetime.utcnow(),
            "iss": JWT_ISSUER,
            "scope": JWT_SCOPES["refresh"],
        }
        # Encode the payload based on options from config.py
        #  - jwt_secret
        #  - jwt_algorithm
        token = encode(payload, settings.jwt_secret,
                       algorithm=settings.jwt_algorithm)
        return token
    except InvalidSignatureError as err:
        return err


def decode_jwt(token: str) -> str:
    """Decode a JWT token

    :param token: JWT token to decode
    :type token: str
    :return: Decoded a JWT access token
    :rtype: str
    """
    try:
        token = decode(token, settings.jwt_secret,
                       algorithms=[settings.jwt_algorithm])
        return token
    except DecodeError as err:
        return err


def refresh_jwt(token: str) -> str:
    """Refresh a JWT access token

    :param token: JWT refresh token
    :type token: str
    :return: Return a JWT access token
    :rtype: dict
    """
    try:
        payload: dict = decode_jwt(token)
        if payload["scope"] == "refresh":
            return encode_access_jwt(payload['sub'])
        return False
    except DecodeError as err:
        return err


def get_users() -> list:
    """Retrieve user list from a JSON database

    :return: Return list of user and their information
    :rtype: list
    """
    if Path(settings.users_db).is_file():
        try:
            with open(settings.users_db, encoding="utf-8") as data:
                return json.load(data)
        except IOError as err:
            return err
    return False


def get_user(user: str) -> dict:
    """Return user information

    If the user exists and is active then information are returned.

    :return: Return user information
    :rtype: dict
    """
    for data in get_users():
        if data["user"] == user and data["active"]:
            return data
    return False


def verify_password(clear_password: str, hash_password: str) -> bool:
    """Compare clear and hash passwords

    :param clear_password: Password provided by the user
    :type clear_password: str
    :param hash_password: Hashed password from the JSON database
    :type hash_password: str
    :return: Return verify status as boolean
    :rtype: bool
    """
    hasher = CryptContext(schemes=[settings.cryto_scheme])
    return hasher.verify(clear_password, hash_password)
