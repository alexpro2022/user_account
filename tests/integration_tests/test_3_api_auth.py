from toolkit.auth.api.endpoints import login_user
from toolkit.auth.schemas import Token
from toolkit.test_tools.base_test_fastapi import BaseTest_API, HTTPMethod
from toolkit.test_tools.mixins import DBMixin

from tests.fixtures.testdata import USER_TEST_DATA


class Login(BaseTest_API):
    http_method = HTTPMethod.POST
    path_func = login_user
    form_data = USER_TEST_DATA.get_login_data()


class Test_LoginNotExistingUser(Login):
    expected_status_code = 401
    expected_response_json = {"detail": "Incorrect email or password"}


class Test_LoginExistingUser(DBMixin, Login):
    # create user in DB
    db_save_obj = USER_TEST_DATA.get_test_obj
    expected_status_code = 201  # token created
    expected_response_model = Token
