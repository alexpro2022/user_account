from pydantic import Field

from src.config import bot_config as c
from toolkit.schemas.base import Base


class TaskCreate(Base):
    name: str = Field(max_length=c.bot_conf.name_max_length)
    description: str | None = Field(None, max_length=c.bot_conf.description_max_length)
