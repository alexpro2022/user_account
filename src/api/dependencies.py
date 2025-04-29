"""Application concrete dependencies."""

from typing import Annotated

from fastapi import Depends
from toolkit.api.fastapi.dependencies import async_session  # noqa
from toolkit.auth.api.dependencies import (  # noqa
    admin_access_only,
    current_user,
)

from src import schemas
from src.services import payment_service

transaction = Annotated[
    schemas.Transaction,
    Depends(payment_service.check_signature),
]
