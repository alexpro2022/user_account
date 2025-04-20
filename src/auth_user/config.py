from pydantic import PositiveInt, SecretStr
from toolkit.config import base
from toolkit.types_app import NonEmptyStr

# from enum import Enum


class AuthSettings(base.BaseConf):
    TOKEN_URL: NonEmptyStr = "/auth/jwt/login"
    TOKEN_LIFETIME: PositiveInt = 3600
    SECRET_KEY: SecretStr = (
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    ALGORITHM: NonEmptyStr = "HS256"

    # Endpoint access settings
    SUPER_ONLY: NonEmptyStr = "__Только для суперюзеров:__ "
    AUTH_ONLY: NonEmptyStr = "__Только для авторизованных пользователей:__ "
    ALL_USERS: NonEmptyStr = "__Для всех пользователей:__ "

    # Authentication settings
    # admin_email: EmailStr = "adm@adm.com"
    # admin_password: SecretStr = "adm"
    # password_length: PositiveInt = 3
    # auth_backend_name: str = "jwt"


auth_conf = AuthSettings()
