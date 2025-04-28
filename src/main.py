from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from toolkit.auth.api import endpoints as auth

from src.api.endpoints import admin, transaction, user
from src.config import app_conf


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    try:
        import dev_tools.main as dev

        await dev.setup_dev(app)
    except ImportError:
        pass
    yield
    # final cleanup


app = FastAPI(
    title=app_conf.app_title,
    description=app_conf.app_description,
    lifespan=lifespan,
)

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
