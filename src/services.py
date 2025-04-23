import sqlalchemy as sa
from toolkit.types_app import _AS, TypePK

from src.models import Account, Payment


async def get_user_accounts(session: _AS, user_id: TypePK):
    user_accounts = sa.select(Account).where(Account.user_id == user_id)
    return (await session.scalars(user_accounts)).all()


async def get_user_payments(session: _AS, user_id: TypePK):
    user_accounts_ids = sa.select(Account.id).where(Account.user_id == user_id)
    user_payments = sa.select(Payment).where(Payment.account_id.in_(user_accounts_ids))
    return (await session.scalars(user_payments)).all()
