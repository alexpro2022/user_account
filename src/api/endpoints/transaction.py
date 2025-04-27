from fastapi import APIRouter, status

from src import schemas
from src.api.dependencies import async_session, transaction
from src.services import payment_service
from toolkit.api.fastapi.responses import response_400

router = APIRouter(
    prefix="/webhook",
    tags=["Payment system"],
)


@router.post(
    "",
    summary="Транзакция от платежной системы",
    description=payment_service.transaction_handler.__doc__,
    response_model=schemas.TransactionOut,
    status_code=status.HTTP_201_CREATED,
    responses=response_400("Invalid transaction signature."),
)
async def transaction_in(s: async_session, t: transaction):
    return await payment_service.transaction_handler(s, t)
