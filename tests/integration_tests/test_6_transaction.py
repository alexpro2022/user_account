from uuid import UUID, uuid4

from toolkit.test_tools.base_test_fastapi import BaseTest_API, HTTPMethod
from toolkit.test_tools.mixins import DBMixin
from toolkit.utils.misc_utils import sha256_hash

from src.api.endpoints.transaction import transaction_in
from src.schemas import Transaction
from tests.fixtures.testdata import USER_TEST_DATA


# ARRANGE ===========================================
class T(Transaction):
    def model_dump(self):
        return {
            k: (str(v) if isinstance(v, UUID) else v)
            for k, v in super(self.__class__, self).model_dump().items()
        }


t = T(
    **dict(
        transaction_id="transaction_id",
        user_id=USER_TEST_DATA.uuid,
        account_id=uuid4(),
        amount=10.5,
        signature="invalid",
    )
)


# TESTS ===============================================
class PostMixin:
    http_method = HTTPMethod.POST
    path_func = transaction_in


class Test_TransactionInvalidSignature(PostMixin, BaseTest_API):
    json = t.model_dump()
    expected_status_code = 400
    expected_response_json = {"detail": "Invalid transaction signature."}


t.signature = sha256_hash(t.get_string())


class Test_Transaction(PostMixin, DBMixin, BaseTest_API):
    db_save_obj = USER_TEST_DATA.get_test_obj
    json = t.model_dump()
    expected_status_code = 201
    expected_response_json_exclude = ["id"]
    expected_response_json = {
        "id": "UUID of created transaction",
        "transaction_id": t.transaction_id,
        "account_id": str(t.account_id),
        "amount": t.amount,
    }
