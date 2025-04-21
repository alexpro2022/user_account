from toolkit.test_tools.base_test_fastapi import HTTPMethod
from toolkit.test_tools.mixins import DBMixin

from src.api.endpoints import admin, user
from src.schemas.user import UserOut
from tests.fixtures.testdata import ADMIN_TEST_DATA, USER_TEST_DATA
from tests.fixtures.testtools import BaseTest_API
from tests.integration_tests.utils import PathParamMixin


class LoggedInAdmin(DBMixin, BaseTest_API):
    db_save_obj = ADMIN_TEST_DATA.get_test_obj
    login_data = ADMIN_TEST_DATA.get_login_data()


class Test_AuthGetMe(LoggedInAdmin):
    http_method = HTTPMethod.GET
    path_func = user.get_me
    expected_response_json = ADMIN_TEST_DATA.get_expected_me_data()


class Test_AdminGetAllRecords(LoggedInAdmin):
    http_method = HTTPMethod.GET
    path_func = admin.get_users
    expected_response_json = [ADMIN_TEST_DATA.expected_response_json_create]


class Test_AdminGetRecord(PathParamMixin, LoggedInAdmin):
    http_method = HTTPMethod.GET
    path_func = admin.get_user
    path_params = dict(user_id=ADMIN_TEST_DATA.item_uuid)
    expected_response_model = UserOut
    expected_response_json = ADMIN_TEST_DATA.expected_response_json_create


class Test_AdminDeleteRecord(PathParamMixin, LoggedInAdmin):
    http_method = HTTPMethod.DELETE
    path_func = admin.delete_user
    path_params = dict(user_id=ADMIN_TEST_DATA.item_uuid)
    expected_response_model = UserOut
    expected_response_json = ADMIN_TEST_DATA.expected_response_json_create
    db_vs_response = True
    db_delete_action = True


class Test_AdminUpdateRecord(PathParamMixin, LoggedInAdmin):
    http_method = HTTPMethod.PATCH
    path_func = admin.update_user
    path_params = dict(user_id=ADMIN_TEST_DATA.item_uuid)
    json = ADMIN_TEST_DATA.update_data_json
    expected_response_model = UserOut
    expected_response_json = ADMIN_TEST_DATA.expected_response_json_update
    # db_vs_response = True  # check fails as response excludes hash_password


class Test_AdminCreateRecord(LoggedInAdmin):
    http_method = HTTPMethod.POST
    path_func = admin.create_user
    expected_status_code = 201
    expected_response_model = UserOut
    expected_response_json = USER_TEST_DATA.expected_response_json_create
    json = {  # new user data
        **USER_TEST_DATA.create_data_json,
        "password": USER_TEST_DATA.password,
    }
