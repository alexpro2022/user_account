from random import randint

import factory as f

from src.auth.services.password import hash_pwd
from src.models import Account, Payment, User

fake = f.Faker
# from faker import Faker
# Faker.phone_number()


class UserFactory(f.Factory):
    class Meta:
        model = User

    # first_name = fake("first_name")
    # email = fake("email")
    first_name = f.Sequence(lambda n: f"Name_{n}")
    email = f.LazyAttribute(lambda self: f"{self.first_name.lower()}@example.com")
    hashed_pwd = hash_pwd(str(fake("password")))
    last_name = fake("last_name")
    phone_number = fake("msisdn")


class AdminFactory(UserFactory):
    class Meta:
        model = User

    admin = True


class AccountFactory(f.Factory):
    class Meta:
        model = Account

    user_id = f.SubFactory(UserFactory)


class PaymentFactory(f.Factory):
    class Meta:
        model = Payment

    account_id = f.SubFactory(AccountFactory)
    amount = f.LazyFunction(lambda: randint(-10, 10))
