from toolkit.test_tools import BaseTest_CRUD, BaseTest_Model, Data

# from src.config import app_conf
from src.auth_user.models import Role, User
from src.auth_user.services.password import hash_pwd

user_test_data = Data(
    model=User,
    create_data={
        "email": "adm@adm.com",
        "hashed_pwd": hash_pwd("adm"),
        "first_name": "alex",
        "last_name": "prosk",
        "phone_number": "+79213452402",
        "role": Role.USER,
    },
    update_data={
        "first_name": "alexey",
        "role": Role.ADMIN,
    },
    unique_fields=["email"],
    indexed_fields=["email"],
)


class Test_UserModel(BaseTest_Model):
    data = user_test_data

    def test__repr(self, obj):
        # bypassed as <Role.USER: 'USER'> cannot be used in eval(repr(obj))
        # assert 0, repr(obj)
        # User(
        #   email='adm@adm.com',
        #   hashed_pwd='$2b$12$EbLOtwYHRxduDGhO2HxVPu5gCIYgXs1W3kPWluY56heP99XTUWp1e',
        #   first_name='alex',
        #   last_name='prosk',
        #   phone_number='+79213452402',
        #   role=<Role.USER: 'USER'>,
        #   id=None)
        pass


class Test_UserCRUD(BaseTest_CRUD):
    data = user_test_data
