from uuid import uuid4

# from toolkit.schemas.base import ExtraForbidMixin
from toolkit.test_tools.base_test_fastapi import BaseTest_API, HTTPMethod
from toolkit.test_tools.mixins import DBMixin

# from src import schemas
from src.api.endpoints import admin, user
from tests.fixtures.testdata import ADMIN_TEST_DATA, USER_TEST_DATA

# UTILS ================================================================
FAKE_UUID = uuid4()


class LoggedInAdmin(DBMixin, BaseTest_API):
    db_save_obj = ADMIN_TEST_DATA.get_test_obj
    login_data = ADMIN_TEST_DATA.get_login_data()


class Found(LoggedInAdmin):
    path_params = {"user_id": ADMIN_TEST_DATA.uuid}


class NotFound(LoggedInAdmin):
    path_params = {"user_id": FAKE_UUID}
    expected_status_code = 404
    expected_response_json = {
        "detail": (f"Object with attributes {{'id': UUID('{FAKE_UUID}')}} not found")
    }


# CREATE ============================================================
class Create(LoggedInAdmin):
    http_method = HTTPMethod.POST
    path_func = admin.create_user


class Test_AdminCreateAlreadyExists(Create):
    json = {  # existing user data
        **ADMIN_TEST_DATA.create_data_json,
        "password": ADMIN_TEST_DATA.password,
    }
    expected_status_code = 400
    expected_response_json = {
        "detail": (
            "Object User("
            "admin=True, email='adm@adm.com', password=None, "
            "first_name='admin_name', last_name='admin_surname', "
            "phone_number='+79217778899', id=None) already exists"
        )
    }


class Test_AdminCreateNewUser(Create):
    json = {  # new user data
        **USER_TEST_DATA.create_data_json,
        "password": USER_TEST_DATA.password,
    }
    expected_status_code = 201
    expected_response_json = USER_TEST_DATA.expected_response_json_create
    expected_response_json_exclude = ["id"]


# UPDATE ============================================================
class UpdateMixin:
    http_method = HTTPMethod.PATCH
    path_func = admin.update_user
    json = ADMIN_TEST_DATA.update_data_json


class Test_AdminUpdateNotFound(UpdateMixin, NotFound):
    pass


class Test_AdminUpdate(UpdateMixin, Found):
    expected_response_json = ADMIN_TEST_DATA.expected_response_json_update
    db_vs_response = True
    # response excludes hash_password, so we exclude it from comparison
    db_vs_response_exclude = ["password"]


# DELETE ============================================================
class DeleteMixin:
    http_method = HTTPMethod.DELETE
    path_func = admin.delete_user


class Test_AdminDeleteNotFound(DeleteMixin, NotFound):
    pass


class Test_AdminDelete(DeleteMixin, Found):
    # expected_response_model = UserOutStrict
    expected_response_json = ADMIN_TEST_DATA.expected_response_json_create
    db_vs_response = True
    db_delete_action = True


# GET ===============================================================
class GetMixin:
    http_method = HTTPMethod.GET


class Test_AdminGetMe(GetMixin, LoggedInAdmin):
    path_func = user.get_me
    expected_response_json = ADMIN_TEST_DATA.get_expected_me_data()


class Test_AdminGetMeAccounts(GetMixin, LoggedInAdmin):
    path_func = user.get_me_accounts
    expected_response_json: list = []


class Test_AdminGetMePayments(GetMixin, LoggedInAdmin):
    path_func = user.get_me_payments
    expected_response_json: list = []


class Test_AdminGetAll(GetMixin, LoggedInAdmin):
    path_func = admin.get_users
    expected_response_json = [ADMIN_TEST_DATA.expected_response_json_create]


class Test_AdminGetNotFound(GetMixin, NotFound):
    path_func = admin.get_user


class Test_AdminGet(GetMixin, Found):
    path_func = admin.get_user
    expected_response_json = ADMIN_TEST_DATA.expected_response_json_create


class Test_AdminGetAccountsNotFound(GetMixin, NotFound):
    path_func = admin.get_user_accounts


class Test_AdminGetAccounts(GetMixin, Found):
    path_func = admin.get_user_accounts
    expected_response_json: list = []


class Test_AdminGetPaymentsNotFound(GetMixin, NotFound):
    path_func = admin.get_user_payments


class Test_AdminGetPayments(GetMixin, Found):
    path_func = admin.get_user_payments
    expected_response_json: list = []
