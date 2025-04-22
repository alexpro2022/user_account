from fastapi import APIRouter
from toolkit.api.fastapi.dependencies import async_session

from src.auth.api.dependencies import current_user
from src.auth.config import auth_conf
from src.config import app_conf
from src.schemas import user as schemas
from src.services import user as service

_description = dict(description=auth_conf.AUTH_ONLY)

router = APIRouter(
    prefix=f"{app_conf.url_prefix}/me",
    tags=["Users"],
    # responses=401, 403
)


@router.get(
    "",
    **_description,
    response_model=schemas.Me,
)
async def get_me(user: current_user):
    return user


@router.get(
    "/accounts",
    **_description,
    response_model=schemas.MeAccounts,
)
async def get_me_accounts(session: async_session, user: current_user):
    return await service.get_user_accounts(session, user.id)


@router.get(
    "/payments",
    **_description,
    response_model=schemas.MePayments,
)
async def get_me_payments(session: async_session, user: current_user):
    return await service.get_user_payments(session, user.id)
