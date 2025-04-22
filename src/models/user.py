from typing import TypeAlias

from sqlalchemy import ForeignKey, orm
from toolkit.models.base import Base, Mapped, mapped_column
from toolkit.types_app import TypePK

# from decimal import Decimal
CurrencyType: TypeAlias = float  # Decimal
NotRequiredStr: TypeAlias = str | None


class User(Base):
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    first_name: Mapped[NotRequiredStr]
    last_name: Mapped[NotRequiredStr]
    phone_number: Mapped[NotRequiredStr]
    admin: Mapped[bool] = mapped_column(default=False)
    accounts: Mapped[list["Account"]] = orm.relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        # lazy="joined",
    )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Account(Base):
    user_id: Mapped[TypePK] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = orm.relationship(back_populates="accounts")
    balance: Mapped[CurrencyType] = mapped_column(default=0)
    payments: Mapped[list["Payment"]] = orm.relationship(
        back_populates="account",
        cascade="all, delete-orphan",
        # lazy="joined",
    )


class Payment(Base):
    account_id: Mapped[TypePK] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = orm.relationship(back_populates="payments")
    amount: Mapped[CurrencyType]
