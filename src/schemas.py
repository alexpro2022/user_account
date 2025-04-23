from pydantic import BaseModel, EmailStr
from toolkit.schemas.base import Base
from toolkit.types_app import NonEmptyStr, TypePK

# from src.auth.services.password import hash_password
from src.models import CurrencyType


class Transaction(BaseModel):
    transaction_id: NonEmptyStr
    user_id: TypePK
    account_id: TypePK
    amount: CurrencyType
    signature: NonEmptyStr


class Payment(Base):
    # TODO: to remove account_id
    account_id: TypePK
    transaction_id: NonEmptyStr
    amount: CurrencyType


class Account(Base):
    # TODO: to remove user_id
    user_id: TypePK
    number: NonEmptyStr
    balance: CurrencyType


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

    # @field_validator("password", mode="after")
    # @classmethod
    # def hash_pwd(cls, password: str) -> str:
    #     return hash_password(password)


# class PaymentsMixin:
#     accounts: list[Payment]
# class AccountsMixin:
#     accounts: list[Account]
# class MeAccounts(AccountsMixin, Me):
#     pass
# class MePayments(PaymentsMixin, Me):
#     pass
# class UserAccounts(AccountsMixin, UserOut):
#     pass
