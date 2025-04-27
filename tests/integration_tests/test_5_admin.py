from uuid import uuid4

from src.api.endpoints import admin, user
from src.schemas import UserOut
from tests.fixtures.testdata import ADMIN_TEST_DATA, USER_TEST_DATA
from toolkit.test_tools.base_test_fastapi import BaseTest_API, HTTPMethod
from toolkit.test_tools.mixins import DBMixin

# UTILS ================================================================
FAKE_UUID = uuid4()


class LoggedInAdmin(DBMixin, BaseTest_API):
    db_save_obj = ADMIN_TEST_DATA.get_test_obj
    login_data = ADMIN_TEST_DATA.get_login_data()


class NotFound(LoggedInAdmin):
    path_params = {"user_id": FAKE_UUID}
    expected_status_code = 404
    expected_response_json = {
        "detail": f"Object with attributes {{'id': UUID('{FAKE_UUID}')}} not found",
    }


class Found(LoggedInAdmin):
    path_params = {"user_id": ADMIN_TEST_DATA.uuid}


# CREATE ================================================================
class Test_AdminCreateRecordAlreadyExists(LoggedInAdmin):
    http_method = HTTPMethod.POST
    path_func = admin.create_user
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


class Test_AdminCreateRecord(LoggedInAdmin):
    http_method = HTTPMethod.POST
    path_func = admin.create_user
    json = {  # new user data
        **USER_TEST_DATA.create_data_json,
        "password": USER_TEST_DATA.password,
    }
    expected_status_code = 201
    expected_response_model = UserOut
    expected_response_json = USER_TEST_DATA.expected_response_json_create
    expected_response_json_exclude = ["id"]


# UPDATE ================================================================
class Test_AdminUpdateRecordNotFound(NotFound):
    http_method = HTTPMethod.PATCH
    path_func = admin.update_user
    json = ADMIN_TEST_DATA.update_data_json


class Test_AdminUpdateRecord(Found):
    http_method = HTTPMethod.PATCH
    path_func = admin.update_user
    json = ADMIN_TEST_DATA.update_data_json
    expected_response_model = UserOut
    expected_response_json = ADMIN_TEST_DATA.expected_response_json_update
    # db_vs_response = True  # check fails as response excludes hash_password


# DELETE ================================================================
class Test_AdminDeleteRecordNotFound(NotFound):
    http_method = HTTPMethod.DELETE
    path_func = admin.delete_user


class Test_AdminDeleteRecord(Found):
    http_method = HTTPMethod.DELETE
    path_func = admin.delete_user
    expected_response_model = UserOut
    expected_response_json = ADMIN_TEST_DATA.expected_response_json_create
    db_vs_response = True
    db_delete_action = True


# GET ================================================================
class Test_AuthGetMe(LoggedInAdmin):
    http_method = HTTPMethod.GET
    path_func = user.get_me
    expected_response_json = ADMIN_TEST_DATA.get_expected_me_data()


class Test_AdminGetAllRecords(LoggedInAdmin):
    http_method = HTTPMethod.GET
    path_func = admin.get_users
    expected_response_json = [ADMIN_TEST_DATA.expected_response_json_create]


class Test_AdminGetRecordNotFound(NotFound):
    http_method = HTTPMethod.GET
    path_func = admin.get_user


class Test_AdminGetRecord(Found):
    http_method = HTTPMethod.GET
    path_func = admin.get_user
    expected_response_model = UserOut
    expected_response_json = ADMIN_TEST_DATA.expected_response_json_create


class Test_AdminGetAccountsNotFound(NotFound):
    http_method = HTTPMethod.GET
    path_func = admin.get_user_accounts


class Test_AdminGetAccounts(Found):
    http_method = HTTPMethod.GET
    path_func = admin.get_user_accounts
    expected_response_json = []


class Test_AdminGetPaymentsNotFound(NotFound):
    http_method = HTTPMethod.GET
    path_func = admin.get_user_payments


class Test_AdminGetPayments(Found):
    http_method = HTTPMethod.GET
    path_func = admin.get_user_payments
    expected_response_json = []
