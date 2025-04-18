from src.config import app_conf
from toolkit.models.base import Base, Mapped, mapped_column


class Secret(Base):
    secret: Mapped[str]
    passphrase: Mapped[str | None]
    ttl_seconds: Mapped[int] = mapped_column(default=app_conf.secret_min_ttl)
