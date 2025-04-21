from toolkit.test_tools import Data

from src.auth.services.password import hash_pwd
from src.models.user import User


class _Data(Data):
    def __init__(self, password: str, **kwargs):
        self.password = password
        kwargs["create_data"]["hashed_pwd"] = hash_pwd(self.password)
        kwargs["model"] = User
        super().__init__(**kwargs)
        self.expected_response_json_create.pop("hashed_pwd")
        self.expected_response_json_update.pop("hashed_pwd")

    def get_login_data(self):
        return {
            "username": self.create_data["email"],
            "password": self.password,
        }

    def get_expected_me_data(self):
        return dict(
            id=str(self.item_uuid),
            email=self.create_data["email"],
            full_name=f"{self.create_data.get('first_name')} {self.create_data.get('last_name')}",
        )


# The data is also used in model and crud tests
USER_TEST_DATA = _Data(
    password="user_pwd",
    create_data={"email": "user@user.com"},  # password is added in constructor
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


ADMIN_TEST_DATA = _Data(
    password="admin_pwd",
    create_data={
        "email": "adm@adm.com",
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
