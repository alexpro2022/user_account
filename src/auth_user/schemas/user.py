from pydantic import BaseModel, EmailStr
from toolkit.schemas.base import Base
from toolkit.types_app import NonEmptyStr

from ..models import Role


class UserLoginForm(BaseModel):
    username: EmailStr
    password: NonEmptyStr


class UserOut(Base):
    email: EmailStr
    first_name: NonEmptyStr
    last_name: NonEmptyStr
    phone_number: NonEmptyStr
    role: Role


class Me(Base):
    email: EmailStr
    full_name: NonEmptyStr


class User(UserOut):
    hashed_pwd: NonEmptyStr


class UserCreate(UserOut):
    password: NonEmptyStr


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: NonEmptyStr | None = None
    first_name: NonEmptyStr | None = None
    last_name: NonEmptyStr | None = None
    phone_number: NonEmptyStr | None = None
    role: Role | None = None
