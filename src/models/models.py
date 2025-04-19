from toolkit.models.base import Base, Mapped
from toolkit.types_app import TypePK

from src.auth_user.models import User


class Account(Base):
    balance: Mapped[float]
    user: Mapped[User]
    user_id: Mapped[TypePK]


class Payment(Base):
    account: Mapped[Account]
    account_id: Mapped[TypePK]
