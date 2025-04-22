# from src.n_toolkit.services import db_service
# from toolkit.types_app import _AS
# from src.auth.services.password import hash_pwd


# async def hash_and_create(
#     *,
#     session: _AS | None = None,
#     obj: object,
# ):
#     obj.hashed_pwd = hash_pwd(obj.hashed_pwd)
#     return await db_service.create(
#         session=session,
#         entity=obj,
#     )
