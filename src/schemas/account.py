from toolkit.schemas.base import Base
from toolkit.types_app import TypePK

from src.models.user import CurrencyType


class Account(Base):
    # TODO: to remove user_id
    user_id: TypePK
    balance: CurrencyType


class AccountsMixin:
    accounts: list[Account]
