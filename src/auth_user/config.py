from toolkit.config import base

# from enum import Enum


class AuthSettings(base.BaseConf):
    TOKEN_LIFETIME: int = 3600
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"


auth_conf = AuthSettings()
