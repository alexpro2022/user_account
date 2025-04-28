from fastapi import APIRouter, status
from toolkit.api.fastapi.responses import (
    response_400_already_exists,
    response_401,
    response_403,
    response_404,
)
from toolkit.api.fastapi.utils import catch_already_exists, catch_not_found
from toolkit.types_app import TypePK

from src import schemas
from src.api.dependencies import admin_access_only, async_session
from src.config import app_conf, auth_config
from src.services import user_service

_description = dict(description=auth_config.auth_conf.SUPER_ONLY)
_response_model = dict(response_model=schemas.UserOut)
_response_404 = dict(responses=response_404("user"))
_common = {
    **_description,
    **_response_model,
    **_response_404,
}

router = APIRouter(
    prefix=f"{app_conf.url_prefix}/users",
    tags=["Admins"],
    dependencies=admin_access_only,
    responses={
        **response_401(),
        **response_403(),
    },
)


# CREATE ================================================================
@router.post(
    "",
    summary="Create user",
    **_description,
    **_response_model,
    responses=response_400_already_exists("user"),
    status_code=status.HTTP_201_CREATED,
)
@catch_already_exists
async def create_user(
    session: async_session,
    create_data: schemas.UserCreate,
):
    return await user_service.create(
        session=session,
        **create_data.model_dump(exclude_none=True),
    )


# UPDATE ================================================================
@router.patch(
    "/{user_id}",
    summary="Update user",
    **_common,
)
@catch_not_found
async def update_user(
    session: async_session,
    user_id: TypePK,
    update_data: schemas.UserUpdate,
):
    return await user_service.update(
        session=session,
        id=user_id,
        **update_data.model_dump(exclude_none=True),
    )


# DELETE ================================================================
@router.delete(
    "/{user_id}",
    summary="Delete user",
    **_common,
)
@catch_not_found
async def delete_user(
    session: async_session,
    user_id: TypePK,
):
    return await user_service.delete(
        session=session,
        id=user_id,
    )


# GET ================================================================
@router.get(
    "",
    summary="All users short list",
    **_description,
    response_model=list[schemas.UserOut],
)
async def get_users(session: async_session):
    return await user_service.get_all(session=session)


@router.get(
    "/{user_id}",
    summary="Get user",
    **_common,
)
@catch_not_found
async def get_user(
    session: async_session,
    user_id: TypePK,
):
    return await user_service.get(
        session=session,
        id=user_id,
    )


@router.get(
    "/{user_id}/accounts",
    summary="User's accounts",
    **_description,
    **_response_404,
    response_model=list[schemas.Account],
)
@catch_not_found
async def get_user_accounts(
    session: async_session,
    user_id: TypePK,
):
    return await user_service.get_user_accounts(session, user_id)


@router.get(
    "/{user_id}/payments",
    summary="User's payments",
    **_description,
    **_response_404,
    response_model=list[schemas.Payment],
)
@catch_not_found
async def get_user_payments(
    session: async_session,
    user_id: TypePK,
):
    return await user_service.get_user_payments(session, user_id)
