from fastapi import FastAPI
from src.auth_user.endpoints import auth, development, user

# router as auth_user_router
from src.config import app_config as c

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
    auth.router,
    development.router,
    user.router,
):
    app.include_router(router)


@app.get("/healthcheck", tags=["Healthcheck"])
def healthcheck():
    return {"message": "OK"}
