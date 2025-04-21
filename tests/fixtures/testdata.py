from toolkit.test_tools import Data

from src.auth_user.models import Role, User
from src.auth_user.services.password import hash_pwd


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
            full_name=f"{self.create_data['first_name']} {self.create_data['last_name']}",
        )


USER_TEST_DATA = _Data(
    password="user_pwd",
    create_data={
        "email": "user@user.com",
        "first_name": "user_name",
        "last_name": "user_surname",
        "phone_number": "+79211234567",
        "role": Role.USER,
    },
    update_data={  # email and password are excluded from update schema
        "first_name": "alex",
        "last_name": "prosk",
        "phone_number": "+79213452402",
        "role": Role.ADMIN,
    },
    unique_fields=["email"],
    indexed_fields=["email"],
)


ADMIN_TEST_DATA = _Data(
    password="admin_pwd",
    create_data={
        "email": "adm@adm.com",
        "first_name": "admin_name",
        "last_name": "admin_surname",
        "phone_number": "+79217778899",
        "role": Role.ADMIN,
    },
    update_data={  # email and password are excluded from update schema
        "first_name": "alex",
        "last_name": "prosk",
        "phone_number": "+79213452402",
    },
)
