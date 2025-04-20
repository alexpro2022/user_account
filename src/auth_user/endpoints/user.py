from fastapi import APIRouter
from src.auth_user.schemas import user as schemas
from src.config import app_conf

from ..config import auth_conf
from ..dependencies import current_user

_description = dict(description=auth_conf.AUTH_ONLY)

router = APIRouter(
    prefix=f"{app_conf.url_prefix}/me",
    tags=["Users"],
    # responses=401, 403
)


@router.get(
    "",
    **_description,
    response_model=schemas.Me,
)
async def get_me(user: current_user):
    return schemas.Me.model_validate(user, from_attributes=True)
