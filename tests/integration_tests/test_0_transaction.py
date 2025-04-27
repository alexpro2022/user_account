from uuid import uuid4

from src.api.endpoints.transaction import transaction_in
from toolkit.test_tools.base_test_fastapi import BaseTest_API, HTTPMethod
from toolkit.test_tools.mixins import DBMixin


class Test_TransactionInvalidSignature(DBMixin, BaseTest_API):
    http_method = HTTPMethod.POST
    path_func = transaction_in
    json = dict(
        transaction_id=str(uuid4()),
        user_id=str(uuid4()),
        account_id=str(uuid4()),
        amount=10.5,
        signature="1",
    )
    expected_status_code = 400
    expected_response_json = {"detail": "Invalid transaction signature."}
