from fastapi import APIRouter

from src.api.dependencies import async_session, transaction
from src.services import payment_service
from toolkit.api.fastapi.utils import try_return

router = APIRouter(
    prefix="/webhook",
    tags=["Payment system"],
)


@router.post(
    "",
    summary="Транзакция от платежной системы",
    description=payment_service.transaction_handler.__doc__,
    # response_model=,
    # responses=response_400_already_exists("user"),
    # status_code=status.HTTP_201_CREATED,
)
async def transaction_in(s: async_session, t: transaction):
    return await try_return(
        return_coro=payment_service.transaction_handler(s, t),
        # possible_exception=AlreadyExists,
        # raise_status_code=status.HTTP_400_BAD_REQUEST,
    )
