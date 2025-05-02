"""Provides central access for all dependencies."""

# Standard dependencies
# Application specific dependencies
from toolkit.api.fastapi.dependencies import (  # noqa
    Annotated,
    Depends,
    async_session,
    existing_user,
)
from toolkit.auth.api.dependencies import (  # noqa
    admin_access_only,
    current_user,
)

from src import schemas, services

transaction = Annotated[
    schemas.Transaction,
    Depends(services.payment_service.check_signature),
]
