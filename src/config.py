from pydantic import PositiveInt, SecretStr
from toolkit.config import (  # noqa
    app_config,
    cache_config,
    db_config,
    testdb_config,
)


class SettingsApp(app_config.SettingsApp):
    app_title: str = "Сервис платежей."
    app_description: str = "Описание сервиса платежей"
    secret_min_ttl: PositiveInt = 5 * 60
    secret_key: SecretStr = "wxvQEAtuRjtCHpeL9VPvy7SLVAQHZhlp-Pswcp7RCyw="


app_conf = SettingsApp()
