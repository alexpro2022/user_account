from functools import partial
from uuid import UUID, uuid4

from httpx import AsyncClient
from toolkit.repo.db import crud
from toolkit.test_tools.base_test_fastapi import HTTPMethod, request
from toolkit.test_tools.utils import assert_equal, assert_isinstance
from toolkit.types_app import _AS
from toolkit.utils.converter import jsonable_converter as jsonify

from src.api.endpoints import admin as adm
from src.api.endpoints import transaction as trans
from src.api.endpoints import user as me
from src.models import Account, Payment
from tests.fixtures.testdata import (
    ADMIN_TEST_DATA,
    TRANSACTION_TEST_DATA,
    USER_TEST_DATA,
    get_test_transaction,
)

# UTILS =============================================================
trans_common_attrs = dict(
    http_method=HTTPMethod.POST,
    path_func=trans.transaction_in,
)


def not_found_common_attrs(id) -> dict:
    return dict(
        expected_status_code=404,
        expected_response_json={
            "detail": f"Object with attributes {{'id': UUID('{id}')}} not found"
        },
    )


def not_found_user_common_attrs(id) -> dict:
    return dict(
        user_id=id,
        **not_found_common_attrs(id),
    )


async def validate_seq(session: _AS, model, size: int) -> list:
    seq = await crud.get_all(session, model)
    assert_equal(len(seq), size)
    for obj in seq:
        await session.refresh(obj)
    return seq


def validate_account(
    account: Account,
    expected_account_id,
    expected_user_id,
    expected_balance,
) -> Account:
    assert_equal(account.id, expected_account_id)
    assert_isinstance(account.number, str)
    assert_equal(str(account.user_id), expected_user_id)
    assert_equal(account.balance, expected_balance)
    return account


def validate_payment(
    payment: Payment,
    expected_transaction_id,
    expected_account_id,
    expected_amount=TRANSACTION_TEST_DATA["amount"],
) -> Payment:
    assert_isinstance(payment.id, UUID)
    assert_equal(payment.transaction_id, expected_transaction_id)
    assert_equal(
        payment.account_id,
        expected_account_id,
    )
    assert_equal(payment.amount, expected_amount)
    return payment


# TESTS =============================================================
async def test__scenario(
    async_client: AsyncClient,
    admin_header: dict,
    get_test_session: _AS,
):
    """
    Admin actions:
    + Get admin
    + Create user -> 201
    + Get all -> [admin, user]
    + Create same user again -> 400, already exists
    + Get all -> [admin, user] - no changes
    + Update user
    + Get all -> [intact admin, updated user ]

    Webhook actions for user:
    + New transaction -> 400, invalid signature
    + New transaction -> 404, user not found
    + CRUD: check accounts=0, payments=0
    + First transaction -> 201, new account/recalc balance -> new payment
    + CRUD: check accounts=1/balance, payments=1
    + Same transaction -> 400, Already exists
    + CRUD: check accounts, payments - no changes
    + Second transaction -> 201, same account/recalc balance -> new payment
    + CRUD: check accounts=1/recalc balance, payments=2

    Admin actions:
    + Get me
    + Get me/accounts=[]
    + Get me/payments=[]
    + Get user/accounts=1
    + Get user/payments=2
    + Delete user -> expected CASCADE deletion
    + CRUD: check CASCADE deletion
    + Get, Update, Delete user -> 404, user not found
    + Get user/accounts -> 404, user not foun
    + Get user/payments -> 404, user not found
    """
    # Admin request
    adm_req = partial(request, async_client, headers=admin_header)

    # Transaction request
    trans_req = partial(request, async_client)

    # Get admin
    admin_json = (
        await adm_req(
            http_method=HTTPMethod.GET,
            path_func=adm.get_users,
            expected_response_json=[ADMIN_TEST_DATA.expected_response_json_create],
        )
    ).json()[0]
    ADMIN_ID = admin_json["id"]

    # Create user -> 201
    created_json = (
        await adm_req(
            http_method=HTTPMethod.POST,
            path_func=adm.create_user,
            json=USER_TEST_DATA.create_data,
            expected_status_code=201,
            expected_response_json=USER_TEST_DATA.expected_response_json_create,
            expected_response_json_exclude=["id"],
        )
    ).json()
    USER_ID = created_json["id"]

    # Get all -> [admin, user]
    _ = await adm_req(
        http_method=HTTPMethod.GET,
        path_func=adm.get_users,
        expected_response_json=[admin_json, created_json],
    )

    # Create same user again -> 400, already exists
    _ = await adm_req(
        http_method=HTTPMethod.POST,
        path_func=adm.create_user,
        json=USER_TEST_DATA.create_data,
        expected_status_code=400,
    )

    # Get all -> [admin, user] - no changes
    _ = await adm_req(
        http_method=HTTPMethod.GET,
        path_func=adm.get_users,
        expected_response_json=[admin_json, created_json],
    )

    # Update user
    updated_json = (
        await adm_req(
            http_method=HTTPMethod.PATCH,
            path_func=adm.update_user,
            user_id=USER_ID,
            json=USER_TEST_DATA.update_data,
            expected_response_json=USER_TEST_DATA.expected_response_json_update,
            expected_response_json_exclude=["id"],
        )
    ).json()

    # Get all -> [intact admin, updated user ]
    _ = await adm_req(
        http_method=HTTPMethod.GET,
        path_func=adm.get_users,
        expected_response_json=[admin_json, updated_json],
    )

    # New transaction -> 400, invalid signature
    _ = await trans_req(
        **trans_common_attrs,
        json=jsonify(get_test_transaction(signature="invalid").model_dump()),
        expected_status_code=400,
        expected_response_json={"detail": "Invalid transaction signature."},
    )

    # New transaction -> 404, not found user
    FAKE_ID = uuid4()
    _ = await trans_req(
        **trans_common_attrs,
        json=jsonify(get_test_transaction(user_id=FAKE_ID).model_dump()),
        **not_found_common_attrs(FAKE_ID),
    )

    # CRUD: check accounts=0, payments=0
    for model in (Account, Payment):
        await validate_seq(get_test_session, model, size=0)

    first_transaction = get_test_transaction(user_id=USER_ID)
    for attrs in (
        dict(  # First transaction -> 201, new account/recalc balance -> new payment
            expected_status_code=201,
            expected_response_json_exclude=["id"],
            expected_response_json={
                "id": "Arbitrary UUID of created transaction",
                "transaction_id": TRANSACTION_TEST_DATA["transaction_id"],
                "account_id": str(TRANSACTION_TEST_DATA["account_id"]),
                "amount": TRANSACTION_TEST_DATA["amount"],
            },
        ),
        dict(  # Again same transaction -> 400, Already exists
            expected_status_code=400,
            expected_response_json={
                "detail": (
                    f"Object Payment("
                    f"transaction_id='{first_transaction.transaction_id}', "
                    f"amount={first_transaction.amount}, "
                    f"account_id=UUID('{first_transaction.account_id}'), "
                    f"id=None"
                    f") already exists"
                )
            },
        ),
    ):
        _ = await trans_req(
            **trans_common_attrs,
            json=jsonify(first_transaction.model_dump()),
            **attrs,
        )
        # CRUD: check accounts=1/balance, payments=1
        accounts = await validate_seq(get_test_session, Account, size=1)
        validate_account(
            account=accounts[0],
            expected_account_id=first_transaction.account_id,
            expected_user_id=first_transaction.user_id,
            expected_balance=first_transaction.amount,
        )
        payments = await validate_seq(get_test_session, Payment, size=1)
        validate_payment(
            payment=payments[0],
            expected_transaction_id=first_transaction.transaction_id,
            expected_account_id=first_transaction.account_id,
            expected_amount=first_transaction.amount,
        )

    # Second transaction -> 201, same account/recalc balance -> new payment
    second_transaction = get_test_transaction(
        transaction_id="second_transaction_id",
        user_id=USER_ID,
    )
    _ = await trans_req(
        **trans_common_attrs,
        json=jsonify(second_transaction.model_dump()),
        expected_status_code=201,
        expected_response_json_exclude=["id"],
        expected_response_json={
            "id": "Arbitrary UUID of created transaction",
            "transaction_id": second_transaction.transaction_id,
            "account_id": str(TRANSACTION_TEST_DATA["account_id"]),
            "amount": TRANSACTION_TEST_DATA["amount"],
        },
    )

    # CRUD: check accounts=1/recalc balance, payments=2
    accounts = await validate_seq(get_test_session, Account, size=1)
    ACCOUNT_ID = str(
        validate_account(
            account=accounts[0],
            expected_account_id=first_transaction.account_id,
            expected_user_id=first_transaction.user_id,
            expected_balance=first_transaction.amount + second_transaction.amount,
        ).id
    )
    payments = await validate_seq(get_test_session, Payment, size=2)
    validate_payment(
        payment=payments[0],
        expected_transaction_id=first_transaction.transaction_id,
        expected_account_id=first_transaction.account_id,
        expected_amount=first_transaction.amount,
    )
    validate_payment(
        payment=payments[1],
        expected_transaction_id=second_transaction.transaction_id,
        expected_account_id=first_transaction.account_id,
        expected_amount=second_transaction.amount,
    )

    # Get me
    _ = await adm_req(
        http_method=HTTPMethod.GET,
        path_func=me.get_me,
        expected_response_json={
            "id": ADMIN_ID,
            "email": "adm@adm.com",
            "full_name": "admin_name admin_surname",
        },
    )

    # Get me/accounts=[]
    _ = await adm_req(
        http_method=HTTPMethod.GET,
        path_func=me.get_me_accounts,
        expected_response_json=[],
    )

    # Get me/payments=[]
    _ = await adm_req(
        http_method=HTTPMethod.GET,
        path_func=me.get_me_payments,
        expected_response_json=[],
    )

    # Get user/accounts=1
    _ = await adm_req(
        http_method=HTTPMethod.GET,
        path_func=adm.get_user_accounts,
        user_id=USER_ID,
        expected_response_json_exclude=["id", "number"],
        expected_response_json=[
            {
                "id": "arbitrary UUID",
                "number": "arbitrary UUID",
                "user_id": USER_ID,
                "balance": first_transaction.amount + second_transaction.amount,
            }
        ],
    )

    # Get user/payments=2
    _ = await adm_req(
        http_method=HTTPMethod.GET,
        path_func=adm.get_user_payments,
        user_id=USER_ID,
        expected_response_json_exclude=["id"],
        expected_response_json=[
            {
                "id": "arbitrary UUID",
                "account_id": ACCOUNT_ID,
                "transaction_id": first_transaction.transaction_id,
                "amount": first_transaction.amount,
            },
            {
                "id": "arbitrary UUID",
                "account_id": ACCOUNT_ID,
                "transaction_id": second_transaction.transaction_id,
                "amount": second_transaction.amount,
            },
        ],
    )

    # Delete user -> expected CASCADE deletion
    _ = await adm_req(
        http_method=HTTPMethod.DELETE,
        path_func=adm.delete_user,
        user_id=USER_ID,
        expected_response_json=USER_TEST_DATA.expected_response_json_update,
        expected_response_json_exclude=["id"],
    )

    # CRUD: check CASCADE deletion
    for model in (Account, Payment):
        await validate_seq(get_test_session, model, size=0)

    # Get/Update/Delete user -> 404, not found user
    _ = await adm_req(
        http_method=HTTPMethod.GET,
        path_func=adm.get_user,
        **not_found_user_common_attrs(USER_ID),
    )
    _ = await adm_req(
        http_method=HTTPMethod.PATCH,
        path_func=adm.update_user,
        json=USER_TEST_DATA.update_data,
        **not_found_user_common_attrs(USER_ID),
    )
    _ = await adm_req(
        http_method=HTTPMethod.DELETE,
        path_func=adm.delete_user,
        **not_found_user_common_attrs(USER_ID),
    )

    # Get user/accounts -> 404, not found user
    _ = await adm_req(
        http_method=HTTPMethod.GET,
        path_func=adm.get_user_accounts,
        **not_found_user_common_attrs(USER_ID),
    )

    # Get user/payments -> 404, not found user
    _ = await adm_req(
        http_method=HTTPMethod.GET,
        path_func=adm.get_user_payments,
        **not_found_user_common_attrs(USER_ID),
    )
