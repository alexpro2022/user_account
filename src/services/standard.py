"""Standard non-FastAPI pass-through service for session created in place."""

from toolkit.config.db_config import async_session
from toolkit.repo.db import crud
from toolkit.types_app import TypeModel, TypePK


async def get_all(model: TypeModel) -> list[TypeModel]:
    async with async_session() as session:
        return await crud.get_all(session, model)


async def get(model: TypeModel, **filter_data) -> TypeModel:
    async with async_session() as session:
        return await crud.get_one(session, model, **filter_data)


async def create(model: TypeModel, **create_data) -> TypeModel:
    async with async_session.begin() as session:
        return await crud.create(session, model(**create_data))


async def create_obj(obj) -> TypeModel:
    async with async_session.begin() as session:
        return await crud.create(session, obj)


async def update(model: TypeModel, id: TypePK, **update_data) -> TypeModel:
    async with async_session.begin() as session:
        return await crud.update(session, model, id, **update_data)


async def delete(model: TypeModel, id: TypePK) -> TypeModel:
    async with async_session.begin() as session:
        return await crud.delete(session, model, id)


# If you don't use an alembic -> uncomment below
# async def create_db_and_tables() -> None:
#     await crud.create_db_and_tables()
