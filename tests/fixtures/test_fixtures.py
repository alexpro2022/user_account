from httpx import AsyncClient
from toolkit.test_tools.base_test_fastapi import API_Router
from toolkit.test_tools.fixtures import BASE_URL
from toolkit.test_tools.utils import assert_equal, assert_isinstance

from src.config import db_config, testdb_config
from src.main import app
from src.models import User
from tests.fixtures.testdata import ADMIN_TEST_DATA


def test__async_client_fixture(async_client: AsyncClient):
    # Test client
    assert_isinstance(async_client, AsyncClient)
    assert_equal(async_client.base_url, BASE_URL)
    # Test dependencies
    assert_equal(
        actual=app.dependency_overrides,
        expected={
            db_config.get_async_session: testdb_config.get_async_session,
        },
    )
    assert_equal(API_Router.router, app.router)


async def test__admin_fixture(admin: User):
    assert_isinstance(admin, User)
    assert_equal(
        actual=admin.model_dump(),
        expected={
            "id": ADMIN_TEST_DATA.uuid,  # random uuid4()
            "admin": True,
            "email": "adm@adm.com",
            "first_name": "admin_name",
            "last_name": "admin_surname",
            "password": ADMIN_TEST_DATA.create_data["password"],  # random salt
            "phone_number": "+79217778899",
        },
    )


async def test__admin_header_fixture(admin_header):
    assert_isinstance(admin_header, dict)
    assert admin_header["Authorization"].startswith("Bearer ")
