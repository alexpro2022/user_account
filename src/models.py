from typing import TypeAlias

from sqlalchemy import ForeignKey, String, orm
from toolkit.models.base import Base, Mapped, mapped_column
from toolkit.types_app import TypePK

# from decimal import Decimal
CurrencyType: TypeAlias = float  # Decimal
NotRequiredStr: TypeAlias = str | None

number_field = lambda: mapped_column(  # noqa
    String(256), unique=True, index=True, nullable=False
)
relation_field = lambda back_pop: orm.relationship(  # noqa
    back_populates=back_pop,
    cascade="all, delete-orphan",
    # lazy="joined",
)


class User(Base):
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    first_name: Mapped[NotRequiredStr]
    last_name: Mapped[NotRequiredStr]
    phone_number: Mapped[NotRequiredStr]
    admin: Mapped[bool] = mapped_column(default=False)
    accounts: Mapped[list["Account"]] = relation_field("user")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Account(Base):
    number = number_field()
    balance: Mapped[CurrencyType] = mapped_column(default=0)
    user_id: Mapped[TypePK] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = orm.relationship(back_populates="accounts")
    payments: Mapped[list["Payment"]] = relation_field("account")


class Payment(Base):
    transaction_id = number_field()
    amount: Mapped[CurrencyType]
    account_id: Mapped[TypePK] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = orm.relationship(back_populates="payments")
