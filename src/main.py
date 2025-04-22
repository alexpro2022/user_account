from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from src.api.endpoints import admin, development, user
from src.auth.api import endpoints as auth
from src.config import app_conf
from src.pre_load.load_db import load_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    await load_db()
    yield
    # final cleanup


app = FastAPI(
    title=app_conf.app_title,
    description=app_conf.app_description,
    lifespan=lifespan,
)

for router in (
    development.router,
    auth.router,
    user.router,
    admin.router,
):
    app.include_router(router)


@app.get("/healthcheck", tags=["Healthcheck"])
def healthcheck():
    return {"message": "OK"}
