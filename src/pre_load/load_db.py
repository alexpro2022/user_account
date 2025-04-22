import logging
from collections.abc import Coroutine

from toolkit.repo.db.exceptions import AlreadyExists

from src.auth.config import auth_conf
from src.auth.services.password import hash_pwd
from src.models.user import User
from src.services import standard as service

from .models import AccountFactory, PaymentFactory, UserFactory

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
    return await service.create(
        User,
        email=auth_conf.EMAIL,
        hashed_pwd=hash_pwd(auth_conf.PASSWORD.get_secret_value()),
        first_name=auth_conf.FIRST_NAME,
        last_name=auth_conf.LAST_NAME,
        phone_number=auth_conf.PHONE_NUMBER,
        admin=True,
    )


async def create_data(size: int = 3):
    users = [await service.create_obj(u) for u in UserFactory.build_batch(size=size)]
    accounts = [
        await service.create_obj(a)
        for u in users
        for a in AccountFactory.build_batch(size=size, user_id=u.id)
    ]
    payments = [
        await service.create_obj(p)
        for a in accounts
        for p in PaymentFactory.build_batch(size=size, account_id=a.id)
    ]
    return users, accounts, payments


async def load_db():
    await try_load(create_admin())
    await try_load(create_data())


"""
import logging
import random

from django.conf import settings
from factory.django import DjangoModelFactory
from users.models import User

from .events_factories import (
    EventFactory,
    Gallery_imageFactory,
    Program_partFactory,
    SpeakerFactory,
)
from .shared_factories import SpecializationFactory, StackFactory




def get_random(
    items: list[DjangoModelFactory], size: int = 3
) -> list[DjangoModelFactory]:
    return (
        sorted(random.choices(items, k=size), key=lambda item: item.id)
        if size < len(items)
        else items
    )


def load_db(*args, **kwargs):
    stacks = get_or_create_batch(StackFactory)
    specializations = get_or_create_batch(SpecializationFactory)
    events = set(get_or_create_batch(EventFactory))
    users = set(User.objects.all())
    for event, user in zip(events, users):
        user.stacks.add(*get_random(stacks))
        user.specializations.add(*get_random(specializations))
        event.participants.add(*get_random(list(users)))
        event.stacks.add(*get_random(stacks))
        event.specializations.add(*get_random(specializations))
        Gallery_imageFactory(event=event)
        Program_partFactory(event=event)
        SpeakerFactory(event=event)
"""
