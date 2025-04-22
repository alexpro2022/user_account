from pydantic import BaseModel, EmailStr, field_validator
from toolkit.schemas.base import Base
from toolkit.types_app import NonEmptyStr

from src.auth.services.password import hash_pwd


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


class DevUser(UserOut):
    hashed_pwd: NonEmptyStr


class UserCreate(UserUpdate, Base):
    email: EmailStr
    password: NonEmptyStr

    @field_validator("password", mode="after")
    @classmethod
    def hash_password(cls, password: str) -> str:
        return hash_pwd(password)
