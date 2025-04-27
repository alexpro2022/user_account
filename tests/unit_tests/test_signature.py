from src import schemas
from toolkit.test_tools.utils import assert_equal
from toolkit.utils.misc_utils import sha256_hash

TEST_DATA = {
    "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
    "user_id": 1,
    "account_id": 1,
    "amount": 100,
    "signature": "7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8",
    "secret_key": "gfdmhghif38yrf9ew0jkf32",
}


class TransactionTest(schemas.Transaction):
    # Needs to adjust the types to test data
    # originally it is UUID and float
    user_id: int
    account_id: int
    amount: int


def test__transaction_signature():
    transaction = TransactionTest.model_validate(TEST_DATA)
    assert_equal(
        actual=sha256_hash(transaction.get_string(TEST_DATA["secret_key"])),
        expected=transaction.signature,
    )
