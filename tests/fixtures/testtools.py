from typing import Any, TypeAlias

from httpx import AsyncClient, Response
from toolkit.test_tools.base_test_fastapi import (
    _AS,
    _F,
    TypeHTTPMethod,
    TypeResponseJson,
    assert_equal,
    check_db,
    get_http_method,
    reverse,
    setup_db,
)

from fastapi import APIRouter
from src.auth_user.endpoints.auth import login_user
from src.auth_user.schemas import token, user
from src.fastapi.main import app

TypeResponseModel: TypeAlias = Any | None
TypeHeader: TypeAlias = dict[str, str]


def check_response(
    *,
    response: Response,
    expected_status_code: int = 200,
    expected_response_json: TypeResponseJson = None,
    expected_response_model: TypeResponseModel = None,
    expected_response_headers: TypeHeader = {},
) -> Response:
    resp_json = response.json()
    assert response.status_code == expected_status_code, (
        response.status_code,
        resp_json,
    )
    if expected_response_json is not None:
        assert_equal(resp_json, expected_response_json)
    if expected_response_model is not None:
        expected_response_model.model_validate(resp_json)
    for k, v in expected_response_headers.items():
        assert_equal(response.headers.get(k), v)
    return response


async def request(
    async_client: AsyncClient,
    *,
    router: APIRouter | None = None,
    http_method: TypeHTTPMethod,
    path_func: _F,
    expected_status_code: int = 200,
    expected_response_json: TypeResponseJson = None,
    expected_response_model: TypeResponseModel = None,
    expected_response_headers: TypeHeader = {},
    headers: TypeHeader | None = None,
    query_params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    **path_params,
) -> Response:
    return check_response(
        expected_status_code=expected_status_code,
        expected_response_json=expected_response_json,
        expected_response_model=expected_response_model,
        expected_response_headers=expected_response_headers,
        response=await getattr(async_client, get_http_method(http_method))(
            url=reverse(router=router, path_func=path_func, **path_params),
            params=query_params,
            **(dict(headers=headers) if headers is not None else {}),
            **(dict(data=data) if data is not None else {}),
            **(dict(json=json) if json is not None else {}),
        ),
    )


async def get_header(client: AsyncClient, login_data: dict[str, Any]):
    t = token.Token.model_validate(
        obj=(
            await client.post(
                url=reverse(
                    router=app.router,
                    path_func=login_user,
                ),
                data=user.UserLoginForm(**login_data).model_dump(),
            )
        ).json()
    )
    return {"Authorization": f"Bearer {t.access_token}"}


class BaseTest_API:
    router: APIRouter | None = None
    http_method: TypeHTTPMethod
    path_func: _F  # type: ignore [valid-type]
    path_params: dict[str, Any] = {}
    query_params: dict[str, Any] | None = None
    form_data: dict[str, Any] | None = None
    json: dict[str, Any] | None = None
    expected_status_code: int = 200
    expected_response_json: TypeResponseJson = None
    expected_response_model: TypeResponseModel = None
    expected_response_headers: TypeHeader = {}
    login_data: dict[str, Any] | None = None

    async def test__endpoint(
        self, async_client: AsyncClient, get_test_session: _AS
    ) -> None:
        await setup_db(self, get_test_session)
        response = await request(
            async_client,
            router=self.router,
            http_method=self.http_method,
            path_func=self.path_func,
            **self.path_params,
            query_params=self.query_params,
            data=self.form_data,
            json=self.json,
            headers=(
                await get_header(async_client, self.login_data)
                if self.login_data is not None
                else None
            ),
            expected_status_code=self.expected_status_code,
            expected_response_json=self.expected_response_json,
            expected_response_model=self.expected_response_model,
            expected_response_headers=self.expected_response_headers,
        )
        await check_db(self, get_test_session, response)
