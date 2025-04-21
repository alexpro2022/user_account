from toolkit.api.fastapi.dependencies import async_session
from toolkit.api.fastapi.responses import (
    response_400_already_exists,
    response_404,
)
from toolkit.api.fastapi.utils import try_return
from toolkit.repo.db.exceptions import AlreadyExists
from toolkit.types_app import TypePK

from fastapi import APIRouter, status
from src.auth_user.schemas import user as schemas
from src.config import app_conf
from src.services import service

from ..config import auth_conf
from ..dependencies import admin_access_only
from ..models import User
from ..services.password import hash_password

_description = dict(description=auth_conf.SUPER_ONLY)
_response_model = dict(response_model=schemas.UserOut)
_common = {
    **_description,
    **_response_model,
    **dict(responses=response_404("user")),
}

router = APIRouter(
    prefix=f"{app_conf.url_prefix}/users",
    tags=["Admins"],
    dependencies=admin_access_only,
    # responses=401, 403
)


@router.get(
    "",
    summary="All user records.",
    **_description,
    response_model=list[schemas.UserOut],
)
async def get_users(session: async_session):
    return await service.get_all(session, User)


@router.post(
    "",
    summary="create user",
    **_description,
    **_response_model,
    responses=response_400_already_exists("user"),
    status_code=status.HTTP_201_CREATED,
)
async def create_user(session: async_session, user: schemas.UserCreate):
    create_data = hash_password(user.model_dump())
    return await try_return(
        return_coro=service.create(session, User, **create_data),
        possible_exception=AlreadyExists,
        raise_status_code=status.HTTP_400_BAD_REQUEST,
    )


@router.get(
    "/{user_id}",
    summary="get user",
    **_common,
)
async def get_user(session: async_session, user_id: TypePK):
    return await try_return(return_coro=service.get(session, User, id=user_id))


@router.delete(
    "/{user_id}",
    summary="delete user",
    **_common,
)
async def delete_user(session: async_session, user_id: TypePK):
    return await try_return(return_coro=service.delete(session, User, user_id))


@router.patch(
    "/{user_id}",
    summary="delete user",
    **_common,
)
async def update_user(
    session: async_session, user_id: TypePK, user: schemas.UserUpdate
):
    return await try_return(
        return_coro=service.update(
            session, User, user_id, **user.model_dump(exclude_none=True)
        )
    )
