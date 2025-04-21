import factory

from src.auth.services.password import hash_pwd
from src.models import User

fake = factory.Faker
# from faker import Faker
# Faker.phone_number()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = fake("email")
    hashed_pwd = hash_pwd(str(fake("password")))
    first_name = fake("first_name")
    last_name = fake("last_name")
    phone_number = fake("phone_number")


# Another, different, factory for the same object
class AdminFactory(UserFactory):
    class Meta:
        model = User

    admin = True


# admins = AdminFactory.create_batch(size=3)
# from pprint import pprint
# pprint(admins)
