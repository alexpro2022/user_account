from random import randint

import factory as f

from src.auth.services.password import hash_password
from src.models import Account, Payment, User

number_field = lambda name: f.Sequence(lambda n: f"{name}_{n}")  # noqa


class UserFactory(f.Factory):
    class Meta:
        model = User

    first_name = f.Sequence(lambda n: f"User_{n}")
    email = f.LazyAttribute(lambda self: f"{self.first_name.lower()}@example.com")
    password = f.LazyAttribute(
        lambda self: hash_password(f"{self.first_name.lower()}_pwd")
    )
    last_name = f.Faker("last_name")
    phone_number = f.Faker("msisdn")


class AdminFactory(UserFactory):
    class Meta:
        model = User

    admin = True


class AccountFactory(f.Factory):
    class Meta:
        model = Account

    user_id = f.SubFactory(UserFactory)
    number = number_field("Account_No")


class PaymentFactory(f.Factory):
    class Meta:
        model = Payment

    account_id = f.SubFactory(AccountFactory)
    number = number_field("Payment_ID")
    amount = f.LazyFunction(lambda: randint(0, 10))


# from faker import Faker
# Faker.phone_number()
# first_name = fake("first_name")
# email = fake("email")
# fake("password")
# f.Sequence(lambda n: f"Account_No_{n}")
# f.Sequence(lambda n: f"Payment_ID_{n}")
