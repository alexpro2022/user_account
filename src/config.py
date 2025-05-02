"""Provides central access for all configs."""

# Standard configs
from toolkit.config import (  # noqa
    app_config,
    auth_config,
    cache_config,
    db_config,
    testdb_config,
)


# Application specific configs
class SettingsApp(app_config.SettingsApp):
    app_title: str = "Пользовательские счета и платежи"
    app_description: str = (
        "HTTP-сервис на FastAPI, в котором можно хранить конфиденциальные данные"
    )


app_conf = SettingsApp()
