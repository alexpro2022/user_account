from uuid import uuid4

from toolkit.test_tools.base_testdata import UserData
from toolkit.types_app import TypePK
from toolkit.utils.misc_utils import sha256_hash

from src.models import User
from src.schemas import Transaction

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


TRANSACTION_TEST_DATA = dict(
    transaction_id="transaction_id",
    user_id=USER_TEST_DATA.uuid,
    account_id=uuid4(),
    amount=10.5,
)


def get_test_transaction(
    transaction_id: str | None = None,
    user_id: TypePK = None,
    signature: str = "None",
):
    tr = Transaction(
        **TRANSACTION_TEST_DATA,
        signature=signature,
    )
    if transaction_id is not None:
        tr.transaction_id = transaction_id
    if user_id is not None:
        tr.user_id = user_id
    if tr.signature == "None":
        tr.signature = sha256_hash(tr.get_string())
    return tr
