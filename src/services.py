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
        # check(payload.signature)
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

# import base64
# import hashlib
# import hmac

# # ===========================================================================
# from src.config import app_conf


# def verify_webhook(actual, expected):
#     digest = hmac.new(
#         app_conf.secret_key.get_secret_value().encode("utf-8"),
#         data,
#         digestmod=hashlib.sha256,
#     ).digest()
#     computed_hmac = base64.b64encode(digest)

#     return hmac.compare_digest(
#         actual,
#         expected,
#     )


# def check_signature(transaction: schemas.Transaction):
#     def encode(t: schemas.Transaction):
#         (f"{t.account_id}{t.amount}{t.transaction_id}{t.user_id}{app_conf.secret_key}")

#     assert transaction.signature == encode(transaction)
#     """
#     signature должна формироваться через SHA256 хеш для строки состоящей из
#     конкатенации значений объекта в алфавитном порядке ключей и “секретного ключа”
#     хранящегося в конфигурации проекта
#     ({account_id}{amount}{transaction_id}{user_id}{secret_key}).
# Пример, для secret_key gfdmhghif38yrf9ew0jkf32:
# {
#   "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
#   "user_id": 1,
#   "account_id": 1,
#   "amount": 100,
#   "signature": "7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8"
# }
#     """
