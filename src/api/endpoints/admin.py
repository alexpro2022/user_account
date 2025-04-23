from fastapi import APIRouter, status
from toolkit.api.fastapi.dependencies import async_session
from toolkit.api.fastapi.responses import (
    response_400_already_exists,
    response_404,
)
from toolkit.api.fastapi.utils import try_return
from toolkit.repo.db.exceptions import AlreadyExists
from toolkit.types_app import TypePK

from src import schemas
from src.auth.api.dependencies import admin_access_only
from src.auth.config import auth_conf
from src.config import app_conf
from src.services import user_service

_description = dict(description=auth_conf.SUPER_ONLY)
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
    # responses=401, 403
)


@router.post(
    "",
    summary="Create user",
    **_description,
    **_response_model,
    responses=response_400_already_exists("user"),
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    session: async_session,
    create_data: schemas.UserCreate,
):
    return await try_return(
        return_coro=user_service.create(
            session=session,
            # entity=User,
            **create_data.model_dump(exclude_none=True),
        ),
        possible_exception=AlreadyExists,
        raise_status_code=status.HTTP_400_BAD_REQUEST,
    )


@router.patch(
    "/{user_id}",
    summary="Update user",
    **_common,
)
async def update_user(
    session: async_session,
    user_id: TypePK,
    update_data: schemas.UserUpdate,
):
    return await try_return(
        return_coro=user_service.update(
            session=session,
            # model=User,
            id=user_id,
            **update_data.model_dump(exclude_none=True),
        )
    )


@router.delete(
    "/{user_id}",
    summary="Delete user",
    **_common,
)
async def delete_user(
    session: async_session,
    user_id: TypePK,
):
    return await try_return(
        return_coro=user_service.delete(
            session=session,
            # model=User,
            id=user_id,
        )
    )


@router.get(
    "",
    summary="All users short list",
    **_description,
    response_model=list[schemas.UserOut],
)
async def get_users(session: async_session):
    return await user_service.get_all(session=session)  # , model=User)


@router.get(
    "/{user_id}",
    summary="User's accounts",
    **_description,
    **_response_404,
    response_model=list[schemas.Account],
)
async def get_user(
    session: async_session,
    user_id: TypePK,
):
    return await try_return(
        return_coro=user_service.get_user_accounts(session, user_id)
    )
