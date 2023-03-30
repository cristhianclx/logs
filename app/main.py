# -*- coding: utf-8 -*-

from logging import config as logging_config, getLogger
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

from routes import base, v1
from settings.active import (  # noqa:F401 # pylint:disable=unused-import
    ALLOWED_HOSTS,
    NAME,
    STAGE,
    STATIC_DIR,
    TEMPLATES_DIR,
    VERSION,
)

app: FastAPI = FastAPI(
    debug=True,
    title=f"{NAME} - {STAGE}",
    redoc_url=None,
    version=f"{VERSION}",
)

logging_config.fileConfig("logging.conf", disable_existing_loggers=False)

log = getLogger(__name__)


@app.middleware("http")
async def log_api_calls(request: Request, call_next: Any) -> Any:
    if request.headers["user-agent"] == "testclient":
        return await call_next(request)
    response = await call_next(request)
    log.info(f"request : {request.method} : {request.url} : {request.headers.items()}")
    log.info(f"response : {response.status_code}")
    return response


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routes
app.include_router(base.router, tags=["base"])
app.include_router(v1.router, prefix="/v1")


# /
@app.get("/", include_in_schema=False)
async def root() -> Any:
    """
    /
    """
    return RedirectResponse("/docs")


# /robots.txt
@app.get("/robots.txt", include_in_schema=False, response_class=FileResponse)
async def robots_txt() -> str:
    """
    robots.txt to now allow spiders
    """
    return f"{TEMPLATES_DIR}/robots.txt"


# /favicon.ico
@app.get("/favicon.ico", include_in_schema=False, response_class=FileResponse)
async def favicon_ico() -> str:
    """
    favicon.ico
    """
    return f"{STATIC_DIR}/ico/favicon.ico"
