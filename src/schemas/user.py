from pydantic import BaseModel, EmailStr
from toolkit.schemas.base import Base
from toolkit.types_app import NonEmptyStr

from src.models.user import Role


class Me(Base):
    email: EmailStr
    full_name: NonEmptyStr


class UserOut(Base):
    email: EmailStr
    first_name: NonEmptyStr
    last_name: NonEmptyStr
    phone_number: NonEmptyStr
    role: Role


class User(UserOut):
    hashed_pwd: NonEmptyStr


class UserCreate(UserOut):
    password: NonEmptyStr


class UserUpdate(BaseModel):
    first_name: NonEmptyStr | None = None
    last_name: NonEmptyStr | None = None
    phone_number: NonEmptyStr | None = None
    role: Role | None = None
