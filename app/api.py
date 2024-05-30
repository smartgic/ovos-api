"""Application entrypoint
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.config import get_settings
from app.routers import auth, network, system, voice, skills

settings = get_settings()


def custom_openapi_schema() -> dict:
    """Customize the OpenAPI schema

    :return: Return the customized OpenAPI schema
    :rtype: dict
    """
    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.app_version,
        routes=app.routes,
    )
    openapi_schema["info"] = {
        "title": settings.app_name,
        "version": settings.app_version,
        "description": "API to connect to Open Voice OS message bus system.",
        "termsOfService": "https://smartgic.io/terms/",
        "contact": {
            "name": "Get help with this API",
            "url": "https://smartgic.io/help",
        },
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(title=settings.app_name, version=settings.app_version)

app.openapi = custom_openapi_schema

app.include_router(auth.router, prefix=settings.prefix_version)
app.include_router(skills.router, prefix=settings.prefix_version)
app.include_router(system.router, prefix=settings.prefix_version)
app.include_router(voice.router, prefix=settings.prefix_version)
app.include_router(network.router, prefix=settings.prefix_version)
