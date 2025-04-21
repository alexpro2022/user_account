from toolkit.config import (  # noqa
    app_config,
    cache_config,
    db_config,
    testdb_config,
)


class SettingsApp(app_config.SettingsApp):
    app_title: str = "Сервис платежей."
    app_description: str = "Описание сервиса платежей"


app_conf = SettingsApp()
