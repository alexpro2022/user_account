from pydantic import BaseModel, Field, PositiveInt, model_validator

from src.config import app_conf
from src.services import cipher
from toolkit.types_app import NonEmptyStr


class SecretKey(BaseModel):
    """
    Пример ответа (JSON) на POST-запрос:
    {
    "secret_key": "уникальный_идентификатор"
    }
    """

    secret_key: NonEmptyStr = Field(
        description="Уникальный_идентификатор секретных данных, например первичный ключ формата UUID.",
        examples=["уникальный_идентификатор"],
    )


class SecretDelete(BaseModel):
    """
    Пример ответа (JSON):
    {
    "status": "secret_deleted"
    }
    """

    status: NonEmptyStr = Field(examples=["secret_deleted"])


class _Secret(BaseModel):
    """
    Пример ответа (JSON):
    {
    "secret": "доступ_к_конфиденциальным_данным"
    }
    """

    secret: NonEmptyStr = Field(
        description="обязательный параметр, конфиденциальные данные.",
        examples=["доступ_к_конфиденциальным_данным"],
    )


class SecretOut(_Secret):
    @model_validator(mode="after")
    def decode_secret(self) -> "SecretOut":
        self.secret = cipher.decrypt(self.secret)
        return self


class SecretIn(_Secret):
    @model_validator(mode="after")
    def encode_secret(self) -> "SecretIn":
        self.secret = cipher.encrypt(self.secret)
        return self


class SecretCreate(SecretIn):
    """
    Тело POST-запроса (JSON) может содержать:
    * secret (string) — обязательный параметр, конфиденциальные данные.
    * passphrase (string) — опциональный параметр, фраза-пароль для дополнительной защиты (например, может потребоваться при удалении).
    * ttl_seconds (number) — опциональный параметр, время жизни секрета в секундах.

    Пример тела запроса:
    {
    "secret": "доступ_к_конфиденциальным_данным",
    "passphrase": "my_passphrase",
    "ttl_seconds": 3600
    }
    """

    passphrase: NonEmptyStr | None = Field(
        default=None,
        description="Опциональный параметр, фраза-пароль для дополнительной защиты (например, может потребоваться при удалении).",
        examples=["my_passphrase"],
    )
    ttl_seconds: PositiveInt | None = Field(
        default=app_conf.secret_min_ttl,
        description="Опциональный параметр, время жизни секрета в секундах.",
        ge=app_conf.secret_min_ttl,
        examples=["30"],
    )
