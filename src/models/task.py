from sqlalchemy import String

from src.config import bot_config as c
from toolkit.models.base import Base, Mapped, mapped_column


class Task(Base):
    name: Mapped[str] = mapped_column(String(c.bot_conf.name_max_length), unique=True)
    description: Mapped[str] = mapped_column(
        String(c.bot_conf.description_max_length), default="No description"
    )

    def __str__(self) -> str:
        return f"{self.name}\n{self.description}\n"
