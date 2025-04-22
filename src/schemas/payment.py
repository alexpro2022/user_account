from toolkit.schemas.base import Base
from toolkit.types_app import TypePK

from src.models.user import CurrencyType


class Payment(Base):
    # TODO: to remove account_id
    account_id: TypePK
    amount: CurrencyType


class PaymentsMixin:
    accounts: list[Payment]
