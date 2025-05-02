from fastapi import status
from toolkit.test_tools.base_test_fastapi import BaseTest_API, HTTPMethod

from src.api.endpoints import admin, user
from tests.integration_tests.utils import PathParamMixin


# UTILS ================================================================
class UnAuthorized(BaseTest_API):
    expected_status_code = status.HTTP_401_UNAUTHORIZED
    expected_response_json = {"detail": "Not authenticated"}


# TESTS ================================================================
class Test_AnonGetMe(UnAuthorized):
    http_method = HTTPMethod.GET
    path_func = user.get_me


class Test_AnonGetMeAccounts(UnAuthorized):
    http_method = HTTPMethod.GET
    path_func = user.get_me_accounts


class Test_AnonGetMePayments(UnAuthorized):
    http_method = HTTPMethod.GET
    path_func = user.get_me_payments


class Test_AnonCreate(UnAuthorized):
    http_method = HTTPMethod.POST
    path_func = admin.create_user


class Test_AnonUpdate(PathParamMixin, UnAuthorized):
    http_method = HTTPMethod.PATCH
    path_func = admin.update_user


class Test_AnonDelete(PathParamMixin, UnAuthorized):
    http_method = HTTPMethod.DELETE
    path_func = admin.delete_user


class Test_AnonGetAll(UnAuthorized):
    http_method = HTTPMethod.GET
    path_func = admin.get_users


class Test_AnonGet(PathParamMixin, UnAuthorized):
    http_method = HTTPMethod.GET
    path_func = admin.get_user


class Test_AnonGetUserAccounts(PathParamMixin, UnAuthorized):
    http_method = HTTPMethod.GET
    path_func = admin.get_user_accounts


class Test_AnonGetUserPayments(PathParamMixin, UnAuthorized):
    http_method = HTTPMethod.GET
    path_func = admin.get_user_payments
