from typing import Annotated

from toolkit.types_app import NonEmptyStr

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.config import app_conf

# from .models import Role
from .exceptions import AdminAccessOnly
from .models import User
from .schemas.user import UserLoginForm

# from typing_extensions import Doc


AUTH_PREFIX = f"{app_conf.url_prefix}/auth"

jwt_token = Annotated[
    NonEmptyStr,
    Depends(OAuth2PasswordBearer(tokenUrl=f"{AUTH_PREFIX}/token")),
    # Doc(""),
]
login_form_data = Annotated[
    UserLoginForm,
    Depends(OAuth2PasswordRequestForm),
    # Doc(""),
]

from .services.user import authenticate_user, get_current_user  # noqa

authenticated_user = Annotated[
    User,
    Depends(authenticate_user),
    # Doc(
    #     """
    #     Dependency is for `/login` endpoint to obtain a token
    #     for existing user with verified password.
    #     """
    # ),
]
current_user = Annotated[
    User,
    Depends(get_current_user),
    # Doc(""),
]


def get_admin(user: current_user):
    if user.is_admin:
        return user
    raise AdminAccessOnly


admin = Annotated[
    User,
    Depends(get_admin),
    # Doc(""),
]
