from fastapi import APIRouter

from ..config import auth_conf
from ..dependencies import authenticated_user
from ..schemas.token import Token
from ..services.token import create_access_token

router = APIRouter(
    prefix=auth_conf.TOKEN_URL,
    tags=["Authentication"],
)


@router.post(
    "",
    summary="",
    description="",
    response_model=Token,
)
async def login_user(user: authenticated_user):
    return Token(access_token=create_access_token(user))
