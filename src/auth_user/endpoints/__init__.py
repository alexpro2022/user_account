# from fastapi import APIRouter
from . import admin, auth, development, user  # noqa

# router = APIRouter(tags=["V1"])

# for mod in (auth, development, user):
#     router.include_router(mod.router)
