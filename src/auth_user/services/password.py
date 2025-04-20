from passlib.context import CryptContext
from toolkit.types_app import DictType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(password: str) -> str:
    return pwd_context.hash(password)


def hash_password(data: DictType) -> DictType:
    data["hashed_pwd"] = pwd_context.hash(data.pop("password"))
    return data


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
