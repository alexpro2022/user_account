import sqlalchemy as sa
from toolkit.repo.db.exceptions import NotFound
from toolkit.types_app import _AS, TypeModel, TypePK

from src import schemas
from src.auth.services.password import hash_password
from src.models import Account, CurrencyType, Payment, User
from src.n_toolkit.services.db_service import DBService


class AccountService(DBService):
    model = Account

    async def update_balance(
        self,
        *,
        session: _AS | None = None,
        account_id: TypePK,
        amount: CurrencyType,
    ) -> TypeModel:
        return await self.update(
            session=session,
            id=account_id,
            balance=amount + (await self.get(session=session, id=account_id)).balance,
        )

    async def get_or_create(
        self,
        *,
        session: _AS | None = None,
        account_id: TypePK,
        user_id: TypePK,
    ) -> TypeModel:
        try:
            return await self.get(session=session, id=account_id)
        except NotFound:
            return await self.create(
                session=session,
                id=account_id,
                user_id=user_id,
            )


account_service = AccountService()


class PaymentService(DBService):
    model = Payment

    async def create(
        self,
        *,
        session: _AS | None = None,
        obj: Payment | None = None,
        **create_data,
    ):
        # from toolkit.config.db_config import async_session
        # async def transact(session):
        #     await account_service.update_balance(session=session, id=obj.account_id, amount=obj.amount)
        #     return await super().create(session=session, obj=obj)

        if obj is None:
            obj = Payment(**create_data)
        # if session is not None:
        #     return await transact(session)
        # async with async_session.begin() as session:
        #     return await transact(session)
        await account_service.update_balance(
            session=session, account_id=obj.account_id, amount=obj.amount
        )
        return await super().create(session=session, obj=obj)

    async def transaction_handler(self, session: _AS, transaction: schemas.Transaction):
        """
        При обработке вебхука необходимо:
        \n  * Проверить подпись объекта
        \n  * Проверить существует ли у пользователя такой счет - если нет, его необходимо создать
        \n  * Сохранить транзакцию в базе данных
        \n  * Начислить сумму транзакции на счет пользователя
        """
        await account_service.get_or_create(
            session=session,
            account_id=transaction.account_id,
            user_id=transaction.user_id,
        )
        return await self.create(
            session=session,
            **transaction.model_dump(
                exclude={"user_id", "signature"},
                exclude_none=True,
            ),
        )


class UserService(DBService):
    model = User

    async def create(
        self,
        *,
        session: _AS | None = None,
        obj: User | None = None,
        **create_data,
    ):
        if obj is None:
            obj = User(**create_data)
        obj.password = hash_password(obj.password)
        return await super().create(session=session, obj=obj)

    async def get_user_accounts(self, session: _AS, user_id: TypePK):
        user_accounts = sa.select(Account).where(Account.user_id == user_id)
        return (await session.scalars(user_accounts)).all()

    async def get_user_payments(self, session: _AS, user_id: TypePK):
        user_accounts_ids = sa.select(Account.id).where(Account.user_id == user_id)
        user_payments = sa.select(Payment).where(
            Payment.account_id.in_(user_accounts_ids)
        )
        return (await session.scalars(user_payments)).all()


payment_service = PaymentService()
user_service = UserService()
