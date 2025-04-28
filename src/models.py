from uuid import uuid4

from sqlalchemy import ForeignKey, orm

from toolkit.models.base import Base, Mapped, mapped_column
from toolkit.models.fields import number_field, relation_field
from toolkit.models.user import BaseUser
from toolkit.types_app import CurrencyType, TypePK


def generate_account_number() -> str:
    """Here might be an account number generation logic.
    Simple uuid patch at the moment.
    """
    return str(uuid4())


class User(BaseUser):
    admin: Mapped[bool] = mapped_column(default=False)
    accounts: Mapped[list["Account"]] = relation_field("user")


class Account(Base):
    number = number_field(default=generate_account_number)
    balance: Mapped[CurrencyType] = mapped_column(default=0)
    user_id: Mapped[TypePK] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = orm.relationship(back_populates="accounts")
    payments: Mapped[list["Payment"]] = relation_field("account")


class Payment(Base):
    transaction_id = number_field()
    amount: Mapped[CurrencyType]
    account_id: Mapped[TypePK] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = orm.relationship(back_populates="payments")
