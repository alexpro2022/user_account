import factory as f

from src.auth.services.password import hash_pwd
from src.models import User

fake = f.Faker
# from faker import Faker
# Faker.phone_number()


class UserFactory(f.Factory):
    class Meta:
        model = User

    # first_name = fake("first_name")
    # email = fake("email")
    first_name = f.Sequence(lambda n: f"Name_{n}")
    email = f.LazyAttribute(lambda _self: f"{_self.first_name.lower()}@example.com")
    hashed_pwd = hash_pwd(str(fake("password")))
    last_name = fake("last_name")
    phone_number = fake("msisdn")


# Another, different, factory for the same object
class AdminFactory(UserFactory):
    class Meta:
        model = User

    admin = True


"""
import factory as f
from factory.django import DjangoModelFactory
from users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = f.Sequence(lambda n: f"Username_{n}")
    email = f.LazyAttribute(lambda _self: f"{_self.username.lower()}@example.com")
    first_name = f.Faker("first_name")
    last_name = f.Faker("last_name")
    password = f.Faker("password")
    mobilefone = f.Faker("msisdn")
    workplace = f.Sequence(lambda n: f"Место работы №{n}")
    position = f.Faker("job")
    experience = f.Iterator(User.EXPERIENCE_CHOICES)

"""
