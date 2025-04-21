"""Standard FastAPI pass-through service for session as dependency."""

from toolkit.repo.db import crud
from toolkit.types_app import _AS, TypeModel, TypePK


async def get_all(session: _AS, model: TypeModel) -> list[TypeModel]:
    return await crud.get_all(session, model)


async def get(session: _AS, model: TypeModel, **filter_data) -> TypeModel:
    return await crud.get_one(session, model, **filter_data)


async def create(session: _AS, model: TypeModel, **create_data) -> TypeModel:
    assert session.in_transaction()
    return await crud.create(session, model(**create_data))


async def update(
    session: _AS, model: TypeModel, id: TypePK, **update_data
) -> TypeModel:
    assert session.in_transaction()
    return await crud.update(session, model, id, **update_data)


async def delete(session: _AS, model: TypeModel, id: TypePK) -> TypeModel:
    assert session.in_transaction()
    return await crud.delete(session, model, id)


# If you don't use an alembic -> uncomment below
# async def create_db_and_tables() -> None:
#     await crud.create_db_and_tables()
