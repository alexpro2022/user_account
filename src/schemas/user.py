from pydantic import BaseModel, EmailStr, field_validator
from toolkit.schemas.base import Base
from toolkit.types_app import NonEmptyStr

from src.auth.services.password import hash_password
from src.schemas.account import AccountsMixin
from src.schemas.payment import PaymentsMixin


class Me(Base):
    email: EmailStr
    full_name: NonEmptyStr


class MeAccounts(AccountsMixin, Me):
    pass


class MePayments(PaymentsMixin, Me):
    pass


class UserUpdate(BaseModel):
    first_name: NonEmptyStr | None = None
    last_name: NonEmptyStr | None = None
    phone_number: NonEmptyStr | None = None
    admin: bool | None = None


class UserOut(UserUpdate, Base):
    email: EmailStr
    admin: bool


class UserAccounts(AccountsMixin, UserOut):
    pass


class UserCreate(UserUpdate, Base):
    email: EmailStr
    password: NonEmptyStr

    @field_validator("password", mode="after")
    @classmethod
    def hash_pwd(cls, password: str) -> str:
        return hash_password(password)
