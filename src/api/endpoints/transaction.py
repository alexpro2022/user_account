from fastapi import APIRouter, HTTPException, status
from toolkit.api.fastapi.dependencies import async_session
from toolkit.api.fastapi.utils import try_return

from src import schemas
from src.n_toolkit.utils import sha256_hash
from src.services import payment_service

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
async def transaction_in(
    session: async_session,
    transaction: schemas.Transaction,
):
    if sha256_hash(transaction.get_string()) != transaction.signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction signature.",
        )
    return await try_return(
        return_coro=payment_service.transaction_handler(session, transaction),
        # possible_exception=AlreadyExists,
        # raise_status_code=status.HTTP_400_BAD_REQUEST,
    )
