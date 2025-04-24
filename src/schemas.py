from typing import Annotated

from pydantic import BaseModel, EmailStr, Field
from toolkit.schemas.base import Base
from toolkit.types_app import NonEmptyStr, TypePK

from src.config import app_conf
from src.models import CurrencyType, generate_account_number

# FIELDS =========================================================
TransactionType = Annotated[
    NonEmptyStr,
    Field(
        description="уникальный идентификатор транзакции в “сторонней системе”",
        examples=["5eae174f-7cd0-472c-bd36-35660f00132b"],
    ),
]
UserType = Annotated[
    TypePK,
    Field(
        description="уникальный идентификатор пользователя",
        examples=["5eae174f-7cd0-472c-bd36-35660f00132b"],
    ),
]
AccountType = Annotated[
    TypePK,
    Field(
        description="уникауникальный идентификатор счета пользователя",
        examples=["5eae174f-7cd0-472c-bd36-35660f00132b"],
    ),
]
AmountType = Annotated[
    CurrencyType,
    Field(
        description="сумма пополнения счета пользователя",
        examples=[10.5],
    ),
]
BalanceType = Annotated[
    CurrencyType,
    Field(
        description="баланс счета пользователя",
        examples=[10.5],
    ),
]
AccountNumberType = Annotated[
    CurrencyType,
    Field(
        description="номер счета пользователя",
        examples=[generate_account_number()],
    ),
]
SignatureType = Annotated[
    NonEmptyStr,
    Field(
        description="подпись объекта",
        examples=["5eae174f-7cd0-472c-bd36-35660f00132b"],
    ),
]


# SCHEMAS =======================================================
class Transaction(BaseModel):
    transaction_id: TransactionType
    user_id: UserType
    account_id: AccountType
    amount: AmountType
    signature: SignatureType

    def get_string(self, secret_key: str = app_conf.secret_key):
        return f"{self.account_id}{self.amount}{self.transaction_id}{self.user_id}{secret_key}"


class Payment(Base):
    account_id: AccountType
    transaction_id: TransactionType
    amount: AmountType


class Account(Base):
    user_id: UserType
    number: AccountNumberType
    balance: BalanceType


class Me(Base):
    email: EmailStr
    full_name: NonEmptyStr


class UserUpdate(BaseModel):
    first_name: NonEmptyStr | None = None
    last_name: NonEmptyStr | None = None
    phone_number: NonEmptyStr | None = None
    admin: bool | None = None


class UserOut(UserUpdate, Base):
    email: EmailStr
    admin: bool


class UserCreate(UserUpdate, Base):
    email: EmailStr
    password: NonEmptyStr
