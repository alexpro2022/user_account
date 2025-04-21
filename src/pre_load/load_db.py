from collections.abc import Coroutine

from toolkit.repo.db.exceptions import AlreadyExists

from src.auth.config import auth_conf
from src.auth.services.password import hash_pwd
from src.models.user import User
from src.services import standard as service

from .models import UserFactory

ADMIN_PK = "43e0231a-9756-43bb-b9dc-f43567aa5010"
USER_PK = "43e0231a-9756-43bb-b9dc-f43567aa5011"


async def try_load(coro: Coroutine):
    try:
        await coro
    except AlreadyExists:
        pass


async def create_admin():
    await service.create(
        User,
        email=auth_conf.EMAIL,
        hashed_pwd=hash_pwd(auth_conf.PASSWORD.get_secret_value()),
        first_name=auth_conf.FIRST_NAME,
        last_name=auth_conf.LAST_NAME,
        phone_number=auth_conf.PHONE_NUMBER,
        admin=True,
    )


async def load_db():
    await try_load(create_admin())
    for user in UserFactory.build_batch(size=3):
        await service.create_obj(user)
