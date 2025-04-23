"""
The router is not a part of the project.
It is just for convenient checking on development.
"""

from fastapi import APIRouter
from toolkit.api.fastapi.dependencies import async_session
from toolkit.types_app import TypePK

from src.models import Account, Payment, User
from src.n_toolkit.services import db_service
from src.services import get_user_accounts, get_user_payments

router = APIRouter(
    prefix="/auth/development",
    tags=["Auth Development"],
)


@router.get(
    "/users",
    summary="All users.",
)
async def get_users_development(session: async_session):
    return await db_service.get_all(session=session, model=User)


@router.get(
    "/accounts",
    summary="All accounts.",
)
async def get_accounts_development(session: async_session):
    return await db_service.get_all(session=session, model=Account)


@router.get(
    "/payments",
    summary="All payments.",
)
async def get_paymentss_development(session: async_session):
    return await db_service.get_all(session=session, model=Payment)


@router.get(
    "/accounts/{user_id}",
    summary="User's accounts ",
    # response_model=user.UserAccounts,
)
async def get_user_accounts_development(
    session: async_session,
    user_id: TypePK,
):
    return await get_user_accounts(session, user_id)


@router.get(
    "/payments/{user_id}",
    summary="User's payments",
    # response_model=user.UserAccounts,
)
async def get_user_payments_development(
    session: async_session,
    user_id: TypePK,
):
    return await get_user_payments(session, user_id)
