from fastapi import status
from toolkit.test_tools.base_test_fastapi import BaseTest_API, HTTPMethod
from toolkit.test_tools.mixins import DBMixin

from src import schemas
from src.api.endpoints import admin, user
from tests.fixtures.testdata import USER_TEST_DATA
from tests.integration_tests.utils import PathParamMixin


class LoggedInUser(DBMixin, BaseTest_API):
    db_save_obj = USER_TEST_DATA.get_test_obj
    login_data = USER_TEST_DATA.get_login_data()


class Test_AuthGetMe(LoggedInUser):
    http_method = HTTPMethod.GET
    path_func = user.get_me
    expected_response_model = schemas.Me
    expected_response_json = USER_TEST_DATA.get_expected_me_data()


class Test_AuthGetMeAccounts(LoggedInUser):
    http_method = HTTPMethod.GET
    path_func = user.get_me_accounts
    expected_response_json: list = []


class Test_AuthGetMePayments(LoggedInUser):
    http_method = HTTPMethod.GET
    path_func = user.get_me_payments
    expected_response_json: list = []


class Forbidden(LoggedInUser):
    expected_status_code = status.HTTP_403_FORBIDDEN
    expected_response_json = {"detail": "Admin access only"}


class Test_AuthCreate(Forbidden):
    http_method = HTTPMethod.POST
    path_func = admin.create_user


class Test_AuthUpdate(PathParamMixin, Forbidden):
    http_method = HTTPMethod.PATCH
    path_func = admin.update_user


class Test_AuthDelete(PathParamMixin, Forbidden):
    http_method = HTTPMethod.DELETE
    path_func = admin.delete_user


class Test_AuthGetAll(Forbidden):
    http_method = HTTPMethod.GET
    path_func = admin.get_users


class Test_AuthGet(PathParamMixin, Forbidden):
    http_method = HTTPMethod.GET
    path_func = admin.get_user


class Test_AnonGetUserAccounts(PathParamMixin, Forbidden):
    http_method = HTTPMethod.GET
    path_func = admin.get_user_accounts


class Test_AnonGetUserPayments(PathParamMixin, Forbidden):
    http_method = HTTPMethod.GET
    path_func = admin.get_user_payments
