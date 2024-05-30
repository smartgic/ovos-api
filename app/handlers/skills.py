"""Handles skills requirements
"""

import json
from typing import Optional, Dict
from fastapi import HTTPException, status
from app.common.typing import JSONStructure
from app.models.skills import Skills, Install, Uninstall
from app.common.utils import ws_send, requirements, sanitize
from app.config import get_settings
from app.common.constants import API_SKILL_ID

settings = get_settings()


def retrieve_list(sort: Optional[bool] = False) -> Skills:
    """Retrieve skill list by leveraging skill-rest-api

    Send `skillmanager.list` message and wait for `mycroft.skills.list`
    message to appear on the bus.

    :param sort: Sort alphabetically the skills
    :type sort: bool, optional
    :return: Return the skill list
    :rtype: JSONStructure
    """
    try:
        payload = {
            "type": "skillmanager.list",
        }
        skills: JSONStructure = ws_send(payload, "mycroft.skills.list")

        active: int = 0
        inactive: int = 0
        for key in skills["data"]:
            if skills["data"][key]["active"]:
                active = active + 1
            else:
                inactive = inactive + 1
        if sort:
            skills = json.loads(json.dumps(skills, sort_keys=True))
        data: Skills = {
            "count": len(skills["data"]),
            "count_active": active,
            "count_inactive": inactive,
            "results": skills["data"],
        }
        return data
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unable to retrieve skill list",
        ) from err


def retrieve_settings(skill_id: str) -> JSONStructure:
    """Retrieves skill's settings by leveraging skill-rest-api

    Send `skillmanager.list` message and wait for `mycroft.skills.list`
    message to appear on the bus.

    :param skill_id: Skill ID to retrieve the settings
    :type skill_id: str
    :return: Return the sanitized skill settings
    :rtype: JSONStructure
    """
    status_code: int = status.HTTP_400_BAD_REQUEST
    msg: str = "unable to retrieve skill settings"
    try:
        skills: Skills = retrieve_list()
        for key in skills["results"]:
            if skills["results"][key]["id"] == skill_id:
                payload: Dict = {
                    "type": "ovos.api.skill_settings",
                    "data": {"app_key": settings.app_key, "skill": skill_id},
                }
                info: JSONStructure = ws_send(payload, "ovos.api.skill_settings.answer")
                if requirements():
                    if info["context"]["authenticated"]:
                        return sanitize({"results": info["data"]})
                    status_code = status.HTTP_401_UNAUTHORIZED
                    msg = "unable to authenticate with skill-rest-api"
                    raise Exception
                status_code = status.HTTP_401_UNAUTHORIZED
                msg = "skill-rest-api is not installed on ovos core"
                raise Exception
        status_code = status.HTTP_404_NOT_FOUND
        msg = f"skill {skill_id} not found"
        raise Exception
    except Exception as err:
        raise HTTPException(status_code=status_code, detail=msg) from err


def deactivate(skill_id: str) -> int:
    """Deactivate a skill

    Send `skillmanager.deactivate` message with the skill ID as payload.

    :param skill_id: Skill ID to deactivate
    :type skill_id: str
    :return: Return HTTP 204 or 400
    :rtype: int
    """
    try:
        skills: JSONStructure = retrieve_list()
        for key in skills["results"]:
            if skills["results"][key]["id"] == skill_id:
                payload = {
                    "type": "skillmanager.deactivate",
                    "data": {"skill": skill_id},
                }
                ws_send(payload)
                return status.HTTP_204_NO_CONTENT
        return status.HTTP_400_BAD_REQUEST
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="unable to deactivate skill"
        ) from err


def activate(skill_id: str) -> int:
    """Activate a skill

    Send `skillmanager.activate` message with the skill ID as payload.

    :param skill_id: Skill ID to activate
    :type skill_id: str
    :return: Return HTTP 204 or 400
    :rtype: int
    """
    try:
        skills: JSONStructure = retrieve_list()
        for key in skills["results"]:
            if skills["results"][key]["id"] == skill_id:
                payload: Dict = {
                    "type": "skillmanager.activate",
                    "data": {"skill": skill_id},
                }
                ws_send(payload)
                return status.HTTP_204_NO_CONTENT
        return status.HTTP_400_BAD_REQUEST
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="unable to activate skill"
        ) from err


# def update() -> int:
#     """Request immediate update of all skillsResponse(status_code=
#     Send `skillmanager.update` message to the bus.

#     :return: Return HTTP 204 or 400
#     :rtype: int
#     """
#     try:
#         payload = {"type": "skillmanager.update"}
#         ws_send(payload)
#         return status.HTTP_204_NO_CONTENT
#     except Exception as err:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="unable to update skills"
#         ) from err


# def install(skill: Install, confirm: Optional[bool] = False) -> Install:
#     """Install skill by leveraging skill-rest-api

#     Send `mycroft.api.skill_install` message to the bus.

#     :param skill: Information about the skill to install
#     :type skill: dict
#     :return: Return JSON payload used
#     :rtype: dict
#     """
#     status_code: int = status.HTTP_400_BAD_REQUEST
#     msg: str = "unable to install the skill"
#     try:
#         data: Install = Install(skill=skill.skill, dialog=skill.dialog, lang=skill.lang)
#         payload: Dict = {
#             "type": "mycroft.api.skill_install",
#             "data": {
#                 "app_key": settings.app_key,
#                 "skill": data.skill,
#                 "confirm": confirm,
#                 "dialog": data.dialog,
#                 "lang": data.lang,
#             },
#         }
#         if requirements():
#             skill: JSONStructure = ws_send(payload, "mycroft.api.skill_install.answer")
#             if skill["context"]["authenticated"]:
#                 return skill["data"]
#             status_code = status.HTTP_401_UNAUTHORIZED
#             msg = "unable to authenticate with mycroft-api skill"
#             raise Exception
#         status_code = status.HTTP_401_UNAUTHORIZED
#         msg = "mycroft-api skill is not installed on mycroft core"
#         raise Exception
#     except Exception as err:
#         raise HTTPException(status_code=status_code, detail=msg) from err


# def uninstall(skill: Uninstall, confirm: Optional[bool] = False) -> Uninstall:
#     """Uninstall skill by leveraging skill-rest-api

#     Send `mycroft.api.skill_uninstall` message to the bus.

#     :param skill: Information about the skill to uninstall
#     :type skill: dict
#     :return: Return JSON payload used
#     :rtype: dict
#     """
#     status_code: int = status.HTTP_400_BAD_REQUEST
#     msg: str = "unable to uninstall the skill"
#     try:
#         data: Uninstall = Uninstall(
#             skill=skill.skill, dialog=skill.dialog, lang=skill.lang
#         )
#         payload: Dict = {
#             "type": "mycroft.api.skill_uninstall",
#             "data": {
#                 "app_key": settings.app_key,
#                 "skill": data.skill,
#                 "confirm": confirm,
#                 "dialog": data.dialog,
#                 "lang": data.lang,
#             },
#         }
#         if requirements():
#             skills: JSONStructure = retrieve_list()
#             for key in skills["results"]:
#                 if (
#                     skills["results"][key]["id"] == data.skill
#                     and skills["results"][key]["id"] != API_SKILL_ID
#                 ):
#                     skill: JSONStructure = ws_send(
#                         payload, "mycroft.api.skill_uninstall.answer"
#                     )
#                     if skill["context"]["authenticated"]:
#                         return skill["data"]
#                     status_code = status.HTTP_401_UNAUTHORIZED
#                     msg = "unable to authenticate with mycroft-api skill"
#                     raise Exception
#             status_code = status.HTTP_404_NOT_FOUND
#             msg = "skill is not installed"
#             raise Exception
#         status_code = status.HTTP_401_UNAUTHORIZED
#         msg = "mycroft-api skill is not installed on mycroft core"
#         raise Exception
#     except Exception as err:
#         raise HTTPException(status_code=status_code, detail=msg) from err
