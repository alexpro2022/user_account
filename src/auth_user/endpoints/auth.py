from fastapi import APIRouter

from ..dependencies import AUTH_PREFIX, authenticated_user
from ..schemas.token import Token
from ..services.token import create_access_token

router = APIRouter(
    prefix=AUTH_PREFIX,
    tags=["Authentication"],
)


@router.post(
    "/token",
    summary="",
    description="",
    response_model=Token,
)
async def login_user(user: authenticated_user):
    return Token(access_token=create_access_token(user))
