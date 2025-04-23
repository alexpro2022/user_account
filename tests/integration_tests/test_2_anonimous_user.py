from fastapi import status
from toolkit.test_tools.base_test_fastapi import HTTPMethod

from src.api.endpoints import admin, user
from tests.fixtures.testtools import BaseTest_API
from tests.integration_tests.utils import PathParamMixin


class UnAuthorized(BaseTest_API):
    expected_status_code = status.HTTP_401_UNAUTHORIZED
    expected_response_json = {"detail": "Not authenticated"}


class Test_AnonGetMe(UnAuthorized):
    http_method = HTTPMethod.GET
    path_func = user.get_me


class Test_AnonGetAllRecords(UnAuthorized):
    http_method = HTTPMethod.GET
    path_func = admin.get_users


class Test_AnonCreateRecord(UnAuthorized):
    http_method = HTTPMethod.POST
    path_func = admin.create_user


class Test_AnonGetRecord(PathParamMixin, UnAuthorized):
    http_method = HTTPMethod.GET
    path_func = admin.get_user


class Test_AnonDeleteRecord(PathParamMixin, UnAuthorized):
    http_method = HTTPMethod.DELETE
    path_func = admin.delete_user


class Test_AnonUpdateRecord(PathParamMixin, UnAuthorized):
    http_method = HTTPMethod.PATCH
    path_func = admin.update_user
