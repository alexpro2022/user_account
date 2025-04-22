"""Standard DB pass-through service managing sessions."""

from toolkit.types_app import _AS, TypeModel, TypePK

from . import service_session_dependant, service_session_independant


async def get_all(
    *,
    session: _AS | None = None,
    model: TypeModel,
) -> list[TypeModel]:
    if session is None:
        return await service_session_independant.get_all(model)
    return await service_session_dependant.get_all(session, model)


async def get(
    *,
    session: _AS | None = None,
    model: TypeModel,
    **filter_data,
) -> TypeModel:
    if session is None:
        return await service_session_independant.get(model, **filter_data)
    return await service_session_dependant.get(session, model, **filter_data)


async def create(
    *,
    session: _AS | None = None,
    entity: TypeModel | object,
    **create_data,
) -> TypeModel:
    if session is None:
        return await service_session_independant.create(entity, **create_data)
    return await service_session_dependant.create(session, entity, **create_data)


async def update(
    *,
    session: _AS | None = None,
    model: TypeModel,
    id: TypePK,
    **update_data,
) -> TypeModel:
    if session is None:
        return await service_session_independant.update(model, id, **update_data)
    return await service_session_dependant.update(session, model, id, **update_data)


async def delete(
    *,
    session: _AS | None = None,
    model: TypeModel,
    id: TypePK,
) -> TypeModel:
    if session is None:
        return await service_session_independant.delete(model, id)
    return await service_session_dependant.delete(session, model, id)


# If you don't use an alembic -> uncomment below
# async def create_db_and_tables() -> None:
#     await crud.create_db_and_tables()
