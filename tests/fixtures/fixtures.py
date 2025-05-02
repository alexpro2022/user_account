"""Fixtures for API testing."""

from collections.abc import AsyncGenerator
from typing import Any

import pytest_asyncio
from httpx import AsyncClient

from src.config import db_config, testdb_config
from src.main import app
from src.models import User
from tests.fixtures.testdata import ADMIN_TEST_DATA


@pytest_asyncio.fixture(scope="session")
async def async_client(
    generic_async_client,
) -> AsyncGenerator[AsyncClient, Any]:
    async for ac in generic_async_client(app, db_config, testdb_config):
        yield ac


@pytest_asyncio.fixture
async def admin(generic_admin) -> User:
    return await generic_admin(ADMIN_TEST_DATA.get_test_obj())


@pytest_asyncio.fixture
async def admin_header(generic_admin_header, admin) -> dict[str, str]:
    return await generic_admin_header(ADMIN_TEST_DATA.get_login_data())
