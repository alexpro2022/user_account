from fastapi import APIRouter
from toolkit.api.fastapi.responses import response_401

from src import schemas
from src.api.dependencies import async_session, current_user
from src.config import app_conf, auth_config
from src.services import account_service, payment_service

_description = dict(description=auth_config.auth_conf.AUTH_ONLY)

router = APIRouter(
    prefix=f"{app_conf.url_prefix}/me",
    tags=["Users"],
    responses=response_401(),
)


@router.get(
    "",
    **_description,
    response_model=schemas.Me,
)
def get_me(user: current_user):
    return user


@router.get(
    "/accounts",
    **_description,
    response_model=list[schemas.Account],
)
async def get_me_accounts(
    session: async_session,
    user: current_user,
):
    return await account_service.get_user_accounts(session, user.id)


@router.get(
    "/payments",
    **_description,
    response_model=list[schemas.Payment],
)
async def get_me_payments(
    session: async_session,
    user: current_user,
):
    return await payment_service.get_user_payments(session, user.id)
