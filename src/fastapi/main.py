from fastapi import FastAPI
from src.config import app_config as c
from src.fastapi.api.endpoints import development, secret

# from src.fastapi.api.endpoints import all routers here


# If you don't use an alembic -> uncomment below
# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
#     await service.create_db_and_tables()
#     yield


app = FastAPI(
    title=c.app_conf.app_title,
    description=c.app_conf.app_description,
    # lifespan=lifespan,
)

for router in (
    development.router,
    secret.router,
    # add routers here
):
    app.include_router(router)


@app.get("/healthcheck")
def healthcheck():
    return {"message": "OK"}
