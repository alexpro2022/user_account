from toolkit.test_tools.base_testdata import UserData

from src.models import User

# The data is also used in model and crud tests
USER_TEST_DATA = UserData(
    model=User,
    create_data={
        "email": "user@user.com",
        "password": "user_pwd",
    },
    update_data={  # email and password are excluded from update schema
        "first_name": "alex",
        "last_name": "prosk",
        "phone_number": "+79213452402",
        "admin": True,
    },
    unique_fields=["email"],
    indexed_fields=["email"],
    default_data={"admin": False},
    nullable_fields=["first_name", "last_name", "phone_number"],
)


ADMIN_TEST_DATA = UserData(
    model=User,
    create_data={
        "email": "adm@adm.com",
        "password": "admin_pwd",
        "first_name": "admin_name",
        "last_name": "admin_surname",
        "phone_number": "+79217778899",
        "admin": True,
    },
    update_data={  # email and password are excluded from update schema
        "first_name": "alex",
        "last_name": "prosk",
        "phone_number": "+79213452402",
    },
)
