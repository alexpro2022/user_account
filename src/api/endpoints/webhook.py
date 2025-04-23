# from fastapi import APIRouter
# from toolkit.api.fastapi.dependencies import async_session

# from src import schemas
# from src.services import user_service

# router = APIRouter(
#     prefix="/webhook",
#     tags=["Payment system"],
# )


# @router.post(
#     "",
#     summary="Транзакция от платежной системы",
#     # response_model=,
#     # responses=response_400_already_exists("user"),
#     # status_code=status.HTTP_201_CREATED,
# )
# async def payment_in(
#     session: async_session,
#     payload: schemas.Transaction,
# ):
#     return await try_return(
#         return_coro=user_service.create(
#             session=session,
#             # entity=User,
#             **create_data.model_dump(exclude_none=True),
#         ),
#         possible_exception=AlreadyExists,
#         raise_status_code=status.HTTP_400_BAD_REQUEST,
#     )
