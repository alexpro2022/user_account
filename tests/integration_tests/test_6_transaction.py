from uuid import uuid4

from src import schemas
from src.api.endpoints.transaction import transaction_in
from tests.fixtures.testdata import USER_TEST_DATA
from toolkit.test_tools.base_test_fastapi import BaseTest_API, HTTPMethod
from toolkit.test_tools.mixins import DBMixin
from toolkit.utils.misc_utils import sha256_hash

# ARRANGE ===========================================
json_data_invalid = dict(
    transaction_id=str(uuid4()),
    user_id=str(USER_TEST_DATA.uuid),
    account_id=str(uuid4()),
    amount=10.5,
    signature="1",
)
json_data = json_data_invalid.copy()
tr = schemas.Transaction(**json_data)
json_data["signature"] = sha256_hash(tr.get_string())


# TESTS ===============================================
class Test_TransactionInvalidSignature(BaseTest_API):
    http_method = HTTPMethod.POST
    path_func = transaction_in
    json = json_data_invalid
    expected_status_code = 400
    expected_response_json = {"detail": "Invalid transaction signature."}


class Test_Transaction(DBMixin, BaseTest_API):
    db_save_obj = USER_TEST_DATA.get_test_obj
    http_method = HTTPMethod.POST
    path_func = transaction_in
    json = json_data
    expected_status_code = 201
    expected_response_json_exclude = ["id"]
    expected_response_json = {
        "id": "UUID of created transaction",
        "transaction_id": tr.transaction_id,
        "account_id": str(tr.account_id),
        "amount": tr.amount,
    }
