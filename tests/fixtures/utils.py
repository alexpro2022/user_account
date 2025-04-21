# from collections.abc import AsyncGenerator
# from typing import Any

# import pytest_asyncio
# from httpx import AsyncClient

# from src.config import db_config, testdb_config
# from src.fastapi.main import app
# from toolkit.test_tools.base_test_fastapi import reverse
# from src.auth_user.endpoints.admin import create_user
# from src.auth_user.endpoints.auth import login_user
# from tests.fixtures import test_data
# from src.auth_user.schemas import user, token


# async def create(client, user_data):
#     user.UserOut.model_validate(
#         obj=(await client.post(
#             url=reverse(app.router, create_user),
#             json=user.UserCreate(**user_data).model_dump(),
#         )).json()
#     )


# async def login(client, user_data):
#     return token.Token.model_validate(
#         obj=(await client.post(
#             url=reverse(app.router, login_user),
#             data=user.UserLoginForm(
#                 username=user_data["email"],
#                 password=user_data["password"],
#             ).model_dump()
#         )).json()
#     )


# async def get_header(client, user_data):
#     args = (client, user_data)
#     await create(*args)
#     return {'Authorization': f'Bearer {(await login(*args)).access_token}'}
