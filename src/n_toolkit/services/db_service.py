"""Standard DB pass-through service managing sessions."""

from toolkit.types_app import _AS, TypeModel, TypePK

from . import service_session_dependent, service_session_independent


class DBService:
    model: TypeModel

    @staticmethod
    def get_service(method: str, session: _AS | None, *args, **kwargs):
        if session is None:
            return getattr(service_session_independent, method)(*args, **kwargs)
        return getattr(service_session_dependent, method)(session, *args, **kwargs)

    async def get_all(
        self,
        *,
        session: _AS | None = None,
        # model: TypeModel,
    ) -> list[TypeModel]:
        return await self.get_service("get_all", session, self.model)
        # if session is None:
        #     return await service_session_independent.get_all(model)
        # return await service_session_dependant.get_all(session, model)

    async def get(
        self,
        *,
        session: _AS | None = None,
        # model: TypeModel,
        **filter_data,
    ) -> TypeModel:
        return await self.get_service("get", session, self.model, **filter_data)
        # if session is None:
        #     return await service_session_independent.get(model, **filter_data)
        # return await service_session_dependant.get(session, model, **filter_data)

    async def create(
        self,
        *,
        session: _AS | None = None,
        obj: object | None = None,
        **create_data,
    ) -> TypeModel:
        if bool(obj) == bool(create_data):
            raise ValueError(
                f"CREATE {self.model}: cannot be `obj` and `create_data` at the same time!!!"
            )
        return await self.get_service(
            "create", session, obj or self.model, **create_data
        )
        # if session is None:
        #     return await service_session_independent.create(entity, **create_data)
        # return await service_session_dependant.create(session, entity, **create_data)

    async def update(
        self,
        *,
        session: _AS | None = None,
        # model: TypeModel,
        id: TypePK,
        **update_data,
    ) -> TypeModel:
        return await self.get_service("update", session, self.model, id, **update_data)
        # if session is None:
        #     return await service_session_independent.update(model, id, **update_data)
        # return await service_session_dependant.update(session, model, id, **update_data)

    async def delete(
        self,
        *,
        session: _AS | None = None,
        # model: TypeModel,
        id: TypePK,
    ) -> TypeModel:
        return await self.get_service("delete", session, self.model, id)
        # if session is None:
        #     return await service_session_independent.delete(model, id)
        # return await service_session_dependant.delete(session, model, id)


# If you don't use an alembic -> uncomment below
# async def create_db_and_tables() -> None:
#     await crud.create_db_and_tables()
