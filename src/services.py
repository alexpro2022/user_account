import sqlalchemy as sa
from toolkit.types_app import _AS, TypePK

from src.auth.services.password import hash_password
from src.models import Account, Payment, User
from src.n_toolkit.services.db_service import DBService


class AccountService(DBService):
    model = Account


class PaymentService(DBService):
    model = Payment


class UserService(DBService):
    model = User

    async def create(
        self,
        *,
        session: _AS | None = None,
        obj: object | None = None,
        **create_data,
    ):
        if obj is not None:
            obj.password = hash_password(obj.password)
        elif create_data:
            create_data["password"] = hash_password(create_data["password"])
        return await super().create(session=session, obj=obj, **create_data)

    async def get_user_accounts(self, session: _AS, user_id: TypePK):
        user_accounts = sa.select(Account).where(Account.user_id == user_id)
        return (await session.scalars(user_accounts)).all()

    async def get_user_payments(self, session: _AS, user_id: TypePK):
        user_accounts_ids = sa.select(Account.id).where(Account.user_id == user_id)
        user_payments = sa.select(Payment).where(
            Payment.account_id.in_(user_accounts_ids)
        )
        return (await session.scalars(user_payments)).all()


account_service = AccountService()
payment_service = PaymentService()
user_service = UserService()
