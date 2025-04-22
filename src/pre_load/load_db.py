import logging
from collections.abc import Coroutine

from toolkit.repo.db.exceptions import AlreadyExists

from src.auth.config import auth_conf
from src.auth.services.password import hash_password
from src.models.user import User

# from src.services import user as user_service
from src.n_toolkit.services import db_service

from .factories import AccountFactory, PaymentFactory, UserFactory

logging.basicConfig(level=logging.INFO)

# ADMIN_PK = "43e0231a-9756-43bb-b9dc-f43567aa5010"
# USER_PK = "43e0231a-9756-43bb-b9dc-f43567aa5011"


async def try_load(coro: Coroutine):
    try:
        logging.info(f"=Loading {coro.__name__} data")
        created = await coro
        logging.info(f"=== {created}")
    except AlreadyExists:
        logging.info(f"{coro.__name__} data already exists... exiting.")
        return None
    return created


async def create_admin():
    return await db_service.create(
        entity=User(
            email=auth_conf.EMAIL,
            password=hash_password(auth_conf.PASSWORD.get_secret_value()),
            first_name=auth_conf.FIRST_NAME,
            last_name=auth_conf.LAST_NAME,
            phone_number=auth_conf.PHONE_NUMBER,
            admin=True,
        )
    )


async def create_data(size: int = 3):
    users = [
        await db_service.create(entity=user)
        for user in UserFactory.build_batch(size=size)
    ]
    accounts = [
        await db_service.create(entity=account)
        for user in users
        for account in AccountFactory.build_batch(size=size, user_id=user.id)
    ]
    payments = [
        await db_service.create(entity=payment)
        for acc in accounts
        for payment in PaymentFactory.build_batch(size=size, account_id=acc.id)
    ]
    return users, accounts, payments


async def load_db():
    await try_load(create_admin())
    await try_load(create_data())
