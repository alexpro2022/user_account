from uuid import UUID

from httpx import AsyncClient

from src.fastapi.api.endpoints import development, secret
from src.schemas.log import Log as log_schema
from tests.fastapi_tests.integration_tests.test_api_secret import MSG_NOT_FOUND
from tests.unit_tests.test_repos import secret_test_data as DATA
from toolkit.test_tools.base_test_fastapi import HTTPMethod, request
from toolkit.test_tools.utils import assert_equal


async def test_scenario(init_db, async_client: AsyncClient):
    """
    Scenario:
      - Create
      - Get one - OK
      - Get one - not found
      - Create
      - Delete - OK
      - Get one - not found
    """

    async def post_request():
        """Create new secret."""
        return await request(
            async_client,
            http_method=HTTPMethod.POST,
            path_func=secret.create_secret,
            json=DATA.create_data_json,
            expected_status_code=201,
        )

    async def get_request_not_found():
        """Check secret not found."""
        return await request(
            async_client,
            http_method=HTTPMethod.GET,
            path_func=secret.get_secret,
            secret_key=secret_key,
            expected_status_code=404,
            expected_response_json={
                "detail": MSG_NOT_FOUND.format(item_id=repr(UUID(secret_key)))
            },
        )

    # Test GET one time
    secret_key = (await post_request()).json().get("secret_key")
    await request(
        async_client,
        http_method=HTTPMethod.GET,
        path_func=secret.get_secret,
        secret_key=secret_key,
        expected_response_json={"secret": DATA.create_data["secret"]},
    )
    assert await get_request_not_found()

    # Test DELETE
    secret_key = (await post_request()).json().get("secret_key")
    await request(
        async_client,
        http_method=HTTPMethod.DELETE,
        path_func=secret.get_secret,
        secret_key=secret_key,
        expected_response_json={"status": "secret_deleted"},
    )
    assert await get_request_not_found()

    # Tests LOG
    logs = (
        await request(
            async_client,
            http_method=HTTPMethod.GET,
            path_func=development.get_logs,
        )
    ).json()
    assert logs
    assert_equal(len(logs), 5)
    for logged in logs:
        log_schema.model_validate(logged)

    # Test delayed deletion
    # from toolkit.utils.asyncio_utils import get_task
    # task = get_task(task_name=DATA.expected_create["id"])
    # assert task
    # assert task.cancelled()
