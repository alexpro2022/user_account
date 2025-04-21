"""
The endpoints are not a part of the project.
They are just for convenient checking on development.
"""

from fastapi import APIRouter
from toolkit.api.fastapi.dependencies import async_session

from src.models.user import User
from src.schemas import user
from src.services import standard_fastapi as service

router = APIRouter(
    prefix="/auth/development",
    tags=["Auth Development"],
)


# @router.get(
#     "/roles",
#     summary="All role records.",
#     description="The endpoint is just for convenient roles checking on development.",
# )
# async def get_roles(session: async_session):
#     return await service.get_all(session, Role)


@router.get(
    "/users",
    summary="All user records.",
    description="The endpoint is just for convenient users checking on development.",
    response_model=list[user.User],
)
async def get_users_development(session: async_session):
    return await service.get_all(session, User)
