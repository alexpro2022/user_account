from toolkit.test_tools import BaseTest_CRUD, BaseTest_Model

from tests.fixtures.testdata import USER_TEST_DATA


class Test_UserModel(BaseTest_Model):
    data = USER_TEST_DATA


class Test_UserCRUD(BaseTest_CRUD):
    data = USER_TEST_DATA
