"""This is just an example of simple service for non-FastAPI app."""

from toolkit.config.db_config import async_session  # , get_async_session
from toolkit.repo.db import crud
from toolkit.types_app import TypeModel, TypePK


async def get_all(model: TypeModel) -> list[TypeModel]:
    # async for session in get_async_session():
    async with async_session() as session:
        # assert session.in_transaction() is False
        return await crud.get_all(session, model)


async def get(model: TypeModel, **filter_data) -> TypeModel:
    # async for session in get_async_session():
    async with async_session() as session:
        # assert session.in_transaction() is False
        return await crud.get_one(session, model, **filter_data)


async def create(model: TypeModel, **create_data) -> TypeModel:
    # async for session in get_async_session():
    async with async_session.begin() as session:
        # assert session.in_transaction() is True
        return await crud.create(session, model(**create_data))


async def update(model: TypeModel, id: TypePK, **update_data) -> TypeModel:
    # async for session in get_async_session():
    async with async_session.begin() as session:
        # assert session.in_transaction() is True
        return await crud.update(session, model, id, **update_data)


async def delete(model: TypeModel, id: TypePK) -> TypeModel:
    # session = await anext(get_async_session())
    # async for session in get_async_session():
    async with async_session.begin() as session:
        # assert session.in_transaction() is True
        return await crud.delete(session, model, id)  # , commit=AUTO_COMMIT)


# If you don't use an alembic -> uncomment below
# async def create_db_and_tables() -> None:
#     await crud.create_db_and_tables()
