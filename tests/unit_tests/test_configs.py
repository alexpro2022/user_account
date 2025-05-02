from toolkit.test_tools import (
    BaseTest_Config,
    BaseTest_DBConfig,
    BaseTest_RedisConfig,
)

from src import config
from src.main import app, lifespan


async def test__lifespan():
    """Test lifespan is properly handling missing dev_tools import."""
    async with lifespan(app) as ls:
        assert ls is None


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
