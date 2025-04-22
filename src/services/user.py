from sqlalchemy import select
from sqlalchemy.orm import joinedload
from toolkit.types_app import _AS, TypePK

from src.models.user import User


async def get_user_accounts(session: _AS, user_id: TypePK):
    return (
        (
            await session.scalars(
                statement=select(User)
                .filter_by(id=user_id)
                .options(joinedload(User.accounts))
            )
        )
        .unique()
        .one()
    )


async def get_user_payments(session: _AS, user_id: TypePK):
    pass
