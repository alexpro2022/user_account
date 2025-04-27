from random import randint

import factory as f

from src.models import Account, Payment, User
from toolkit.auth.services.password import hash_password

number_field = lambda name: f.Sequence(lambda n: f"{name}_{n}")  # noqa


class UserFactory(f.Factory):
    class Meta:
        model = User

    first_name = f.Sequence(lambda n: f"User_{n}")
    email = f.LazyAttribute(
        lambda self: f"{self.first_name.lower()}@example.com",
    )
    password = f.LazyAttribute(
        lambda self: hash_password(f"{self.first_name.lower()}_pwd"),
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
    transaction_id = number_field("Payment_ID")
    amount = f.LazyFunction(lambda: randint(0, 10))
