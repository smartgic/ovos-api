"""Skill routes
"""
from typing import Optional
from fastapi import APIRouter, Depends, status, Query, Path, Body
from fastapi.responses import JSONResponse, Response
from app.models.skills import Skills, Settings, Install, Uninstall
from app.config import get_settings
from app.auth.bearer import JWTBearer
from app.handlers import skills

router = APIRouter(
    prefix="/skills",
    tags=["skills"])

settings = get_settings()


@router.get(
    "",
    response_model=Skills,
    summary="Collect a complete list of installed skills",
    description="Send `skillmanager.list` message to the bus and wait \
        for `mycroft.skills.list` response",
    response_description="Retrieved skill list",
    dependencies=[Depends(JWTBearer())])
@router.get(
    "/",
    response_model=Skills,
    dependencies=[Depends(JWTBearer())],
    include_in_schema=False)
async def retrieve_list(
    sort: Optional[bool] = Query(
        default=False,
        description="Sort alphabetically the skills")) -> JSONResponse:
    """Route to retrieve a complete skill list

    :param sort: Sort alphabetically the skills
    :type sort: bool, optional
    :return: Return the skill list
    :rtype: JSONResponse
    """
    return JSONResponse(content=skills.retrieve_list(sort))


@router.get(
    "/{skill_id}/settings",
    response_model=Settings,
    summary="Collect skill settings",
    description="Send `mycroft.api.skill_settings` message to the bus \
        and wait for `mycroft.api.skill_settings.answer` response. This \
        route leverage the `mycroft-api` skill.",
    response_description="Retrieved skill settings",
    dependencies=[Depends(JWTBearer())])
async def retrieve_settings(
    skill_id: str = Path(
        default=None,
        description="Skill to retrieve settings",
        example="`mycroft-joke.mycroftai`")) -> JSONResponse:
    """Route to retrieve skill settingss

    :param skill_id: Skill ID to retrieve the settings
    :type skill_id: str
    :return: Return the skill settings
    :rtype: JSONResponse
    """
    return JSONResponse(content=skills.retrieve_settings(skill_id))


@router.put(
    "/{skill_id}/deactivate",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deactivate a skill",
    description="Send `skillmanager.deactivate` message to the bus",
    dependencies=[Depends(JWTBearer())])
async def deactivate(
    skill_id: str = Path(
        default=None,
        description="Skill to deactivate",
        example="`mycroft-joke.mycroftai`")) -> int:
    """Route to deactivate a skill

    :param skill_id: Skill ID to deactivate
    :type skill_id: str
    :return: HTTP status code
    :rtype: int
    """
    return Response(status_code=skills.deactivate(skill_id))


@router.put(
    "/{skill_id}/activate",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Activate a skill",
    description="Send `skillmanager.activate` message to the bus mostly \
                after a skill has been deactivated",
    dependencies=[Depends(JWTBearer())])
async def activate(
    skill_id: str = Path(
        default=None,
        description="Skill to activate",
        example="`mycroft-joke.mycroftai`")) -> int:
    """Route to activate a skill

    :param skill_id: Skill ID to deactivate
    :type skill_id: str
    :return: HTTP status code
    :rtype: int
    """
    return Response(status_code=skills.activate(skill_id))


@router.put(
    "/update",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Request immediate update of all skills",
    description="Send `skillmanager.update` message to the bus",
    dependencies=[Depends(JWTBearer())])
async def update() -> int:
    """Route to update the skills

    :return: HTTP status code
    :rtype: int
    """
    return Response(status_code=skills.update())


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=Install,
    summary="Install a skill",
    description="Send `mycroft.api.skill_install` message to the bus. \
        This route leverage the `mycroft-api` skill.",
    response_description="Skill installed",
    dependencies=[Depends(JWTBearer())])
@router.post(
    "/",
    response_model=Install,
    dependencies=[Depends(JWTBearer())],
    include_in_schema=False)
async def install(
    skill: Install = Body(
        default=None,
        description="Information about the skill to install",
        example='{"skill": "https://github.com/JarbasSkills/skill-parrot.git",\
                  "dialog": "the skill-parrot skill has been installed", \
                  "lang": "en-us"}'),
    confirm: Optional[bool] = Query(
        default=False,
        description="Play a confirmation message"),
        ) -> Install:
    """Install a skill

    :param skill: Information about the skill to install
    :type skill: dict
    :param confirm: Play a confirmation message
    :type confirm: bool, optional
    :return: Return JSON payload used
    :rtype: JSONResponse
    """
    return JSONResponse(skills.install(skill, confirm))


@router.delete(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=Uninstall,
    summary="Uninstall a skill",
    description="Send `mycroft.api.skill_uninstall` message to the bus. \
        This route leverage the `mycroft-api` skill.",
    response_description="Skill uninstalled",
    dependencies=[Depends(JWTBearer())])
@router.delete(
    "/",
    response_model=Uninstall,
    dependencies=[Depends(JWTBearer())],
    include_in_schema=False)
async def uninstall(
    skill: Uninstall = Body(
        default=None,
        description="Information about the skill to uninstall",
        example='{"skill": "https://github.com/JarbasSkills/skill-parrot.git",\
                  "dialog": "the skill-parrot skill has been uninstalled", \
                  "lang": "en-us"}'),
    confirm: Optional[bool] = Query(
        default=False,
        description="Play a confirmation message"),
        ) -> Install:
    """Uninstall a skill

    :param skill: Information about the skill to uninstall
    :type skill: dict
    :param confirm: Play a confirmation message
    :type confirm: bool, optional
    :return: Return JSON payload used
    :rtype: JSONResponse
    """
    return JSONResponse(skills.uninstall(skill, confirm))
