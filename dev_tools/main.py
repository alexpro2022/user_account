from fastapi import FastAPI

from dev_tools.api.development import router
from dev_tools.pre_load.load_db import load_db


async def setup_dev(app: FastAPI):
    await load_db()
    app.include_router(router)
