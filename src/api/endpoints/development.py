"""
The router is not a part of the project.
It is just for convenient checking on development.
"""

from fastapi import APIRouter

from src.api.dependencies import async_session
from src.services import account_service, payment_service, user_service
from toolkit.api.fastapi.utils import try_return
from toolkit.types_app import TypePK

router = APIRouter(
    prefix="/development",
    tags=["Development"],
)


@router.get(
    "/users",
    summary="All users.",
)
async def get_users_development(session: async_session):
    return await user_service.get_all(session=session)


@router.get(
    "/accounts",
    summary="All accounts.",
)
async def get_accounts_development(session: async_session):
    return await account_service.get_all(session=session)


@router.get(
    "/payments",
    summary="All payments.",
)
async def get_paymentss_development(session: async_session):
    return await payment_service.get_all(session=session)


@router.get(
    "/{user_id}/accounts",
    summary="User's accounts ",
)
async def get_user_accounts_development(
    session: async_session,
    user_id: TypePK,
):
    return await try_return(
        return_coro=user_service.get_user_accounts(session, user_id)
    )


@router.get(
    "/{user_id}/payments",
    summary="User's payments",
)
async def get_user_payments_development(
    session: async_session,
    user_id: TypePK,
):
    return await try_return(
        return_coro=user_service.get_user_payments(session, user_id)
    )
