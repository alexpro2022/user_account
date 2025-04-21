from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from toolkit.repo.db.exceptions import AlreadyExists

from src.api.endpoints import admin, development, user
from src.auth.api import endpoints as auth
from src.auth.config import auth_conf
from src.auth.services.password import hash_pwd
from src.config import app_conf
from src.models.user import Role, User
from src.services import standard as service


async def create_admin():
    try:
        await service.create(
            User,
            email=auth_conf.EMAIL,
            hashed_pwd=hash_pwd(auth_conf.PASSWORD.get_secret_value()),
            first_name=auth_conf.FIRST_NAME,
            last_name=auth_conf.LAST_NAME,
            phone_number=auth_conf.PHONE_NUMBER,
            role=Role.ADMIN,
        )
    except AlreadyExists:
        pass


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    await create_admin()
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
