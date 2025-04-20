from toolkit.api.fastapi.dependencies import async_session
from toolkit.repo.db import crud, exceptions

from ..dependencies import jwt_token, login_form_data
from ..exceptions import IncorrectLoginCredentials, InvalidTokenPayload
from ..models import User
from .password import verify_password
from .token import get_token_payload


async def authenticate_user(
    session: async_session,
    data: login_form_data,
) -> User:
    try:
        user: User = await crud.get_one(session, User, email=data.username)
    except exceptions.NotFound:
        raise IncorrectLoginCredentials
    if not verify_password(data.password, user.hashed_pwd):
        raise IncorrectLoginCredentials
    return user


async def get_current_user(
    session: async_session,
    token: jwt_token,
) -> User:
    try:
        user: User = await crud.get_one(
            session, User, email=get_token_payload(token).sub
        )
    except exceptions.NotFound:
        raise InvalidTokenPayload
    return user
