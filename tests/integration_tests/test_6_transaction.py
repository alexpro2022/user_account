from uuid import uuid4

from toolkit.test_tools.base_test_fastapi import BaseTest_API, HTTPMethod
from toolkit.test_tools.mixins import DBMixin

from src.api.endpoints.transaction import transaction_in
from src.models import Payment
from tests.fixtures.testdata import USER_TEST_DATA, get_test_transaction


# UTILS =============================================================
class PostTransaction(BaseTest_API):
    http_method = HTTPMethod.POST
    path_func = transaction_in


# TESTS =============================================================
class Test_TransactionInvalidSignature(PostTransaction):
    json = get_test_transaction(signature="invalid").model_dump()
    expected_status_code = 400
    expected_response_json = {"detail": "Invalid transaction signature."}


class Test_TransactionInvalidUser(DBMixin, PostTransaction):
    FAKE_USER_ID = uuid4()
    json = get_test_transaction(user_id=FAKE_USER_ID).model_dump()
    expected_status_code = 404
    expected_response_json = {
        "detail": (f"Object with attributes {{'id': UUID('{FAKE_USER_ID}')}} not found")
    }


class Test_Transaction(DBMixin, PostTransaction):
    """Checks response against expected value and also
    checks DB record of model=Payment with id taken from response."""

    db_save_obj = USER_TEST_DATA.get_test_obj
    json = get_test_transaction(user_id=USER_TEST_DATA.uuid).model_dump()
    expected_status_code = 201
    expected_response_json_exclude = ["id"]
    expected_response_json = {
        "id": "Arbitrary UUID of created transaction",
        "transaction_id": json["transaction_id"],
        "account_id": str(json["account_id"]),
        "amount": json["amount"],
    }
    db_vs_response = True
    model = Payment
