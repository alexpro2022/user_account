from pydantic import BaseModel, EmailStr
from toolkit.schemas.base import Base
from toolkit.types_app import NonEmptyStr


class Me(Base):
    email: EmailStr
    full_name: NonEmptyStr


class UserUpdate(BaseModel):
    first_name: NonEmptyStr | None = None
    last_name: NonEmptyStr | None = None
    phone_number: NonEmptyStr | None = None
    admin: bool | None = None


class UserCreate(UserUpdate, Base):
    email: EmailStr
    password: NonEmptyStr


class UserOut(UserUpdate, Base):
    email: EmailStr
    admin: bool


class DevUser(UserOut):
    hashed_pwd: NonEmptyStr
