from fastapi import FastAPI

from dev_tools.api.development import router
from dev_tools.pre_load.load_db import create_admin, create_data


async def setup_dev(app: FastAPI):
    await create_admin()
    await create_data()
    app.include_router(router)
