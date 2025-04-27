from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from src.api.endpoints import admin, transaction, user
from src.config import app_conf
from src.pre_load.load_db import load_db
from toolkit.auth.api import endpoints as auth


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

try:
    from src.api.endpoints import development

    app.include_router(development.router)
except ImportError:
    pass

for router in (
    transaction.router,
    auth.router,
    user.router,
    admin.router,
):
    app.include_router(router)


@app.get("/healthcheck", tags=["Healthcheck"])
def healthcheck():
    return {"message": "OK"}
