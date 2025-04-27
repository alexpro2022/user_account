from src import config
from toolkit.test_tools import (
    BaseTest_Config,
    BaseTest_DBConfig,
    BaseTest_RedisConfig,
)


class Test_AppConfig(BaseTest_Config):
    module = config
    conf_name = "app_conf"
    conf_fields = {
        "url_prefix": "/api/v1",
    }


class Test_AuthConfig(BaseTest_Config):
    module = config.auth_config
    conf_name = "auth_conf"
    conf_fields = {
        "TOKEN_URL": "/auth/jwt/login",
    }


class Test_DBConfig(BaseTest_DBConfig):
    module = config.db_config


class Test_TestDBConfig(BaseTest_DBConfig):
    module = config.testdb_config


class Test_RedisConfig(BaseTest_RedisConfig):
    module = config.cache_config
