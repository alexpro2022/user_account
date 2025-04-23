from src.auth.config import auth_conf
from src.auth.services.password import hash_password
from src.models import User
from src.n_toolkit.services import db_service
from src.pre_load.factories import AccountFactory, PaymentFactory, UserFactory
from src.pre_load.log import logger


@logger("=ADMIN=")
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


@logger("=DATA=")
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
    await create_admin()
    await create_data()
