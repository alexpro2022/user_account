from functools import wraps

from fastapi import HTTPException, status
from toolkit.api.fastapi.utils import try_return
from toolkit.repo.db.exceptions import AlreadyExists

InvalidTransactionSignature = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid transaction signature.",
)


# TODO: to move to toolkit
def catch_not_found(coro):
    @wraps(coro)
    async def wrapper(*args, **kwargs):
        return await try_return(
            return_coro=coro(*args, **kwargs),
        )

    return wrapper


# TODO: to move to toolkit
def catch_already_exists(coro):
    @wraps(coro)
    async def wrapper(*args, **kwargs):
        return await try_return(
            return_coro=coro(*args, **kwargs),
            possible_exception=AlreadyExists,
            raise_status_code=status.HTTP_400_BAD_REQUEST,
        )

    return wrapper
