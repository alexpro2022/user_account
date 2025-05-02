import sqlalchemy as sa
from toolkit.repo.db.exceptions import NotFound
from toolkit.services.db_service import DBService
from toolkit.services.user import BaseUserService
from toolkit.types_app import _AS, TypePK
from toolkit.utils.misc_utils import sha256_hash

from src import schemas
from src.api.exceptions import InvalidTransactionSignature
from src.models import Account, CurrencyType, Payment, User

# USER ================================================
user_service = BaseUserService(User)


# ACCOUNT =============================================
class AccountService(DBService):
    async def update_balance(
        self,
        *,
        session: _AS | None = None,
        account_id: TypePK,
        amount: CurrencyType,
    ) -> Account:
        return await self.update(
            session=session,
            id=account_id,
            balance=(await self.get(session=session, id=account_id)).balance + amount,
        )

    async def get_or_create(
        self,
        *,
        session: _AS | None = None,
        account_id: TypePK,
        user_id: TypePK,
    ) -> Account:
        try:
            return await self.get(session=session, id=account_id)
        except NotFound:
            _ = await user_service.exists(
                session=session, raise_not_found=True, id=user_id
            )
            return await self.create(session=session, id=account_id, user_id=user_id)

    async def get_user_accounts(
        self,
        session: _AS,
        user_id: TypePK,
    ) -> list[Account]:
        return await self.get_all(session=session, user_id=user_id)


account_service = AccountService(Account)


# PAYMENT =============================================
class PaymentService(DBService):
    async def create(
        self,
        *,
        session: _AS | None = None,
        obj: Payment | None = None,
        **create_data,
    ) -> Payment:
        if obj is None:
            obj = self.model(**create_data)

        payment: Payment = await super().create(session=session, obj=obj)
        _ = await account_service.update_balance(
            session=session, account_id=obj.account_id, amount=obj.amount
        )
        return payment

    @staticmethod
    def check_signature(
        transaction: schemas.Transaction,
    ) -> schemas.Transaction:
        if sha256_hash(transaction.get_string()) == transaction.signature:
            return transaction
        raise InvalidTransactionSignature

    async def transaction_handler(
        self,
        session: _AS,
        transaction: schemas.Transaction,
    ) -> Payment:
        """
        При обработке вебхука необходимо:
        \n  * Проверить подпись объекта
        \n  * Проверить существует ли у пользователя такой счет - если нет, его необходимо создать
        \n  * Сохранить транзакцию в базе данных
        \n  * Начислить сумму транзакции на счет пользователя
        """
        _ = await account_service.get_or_create(
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

    async def get_user_payments(
        self,
        session: _AS,
        user_id: TypePK,
    ) -> list[Payment]:
        user_accounts_ids = sa.select(Account.id).where(Account.user_id == user_id)
        user_payments = sa.select(self.model).where(
            self.model.account_id.in_(user_accounts_ids)
        )
        return (await session.scalars(user_payments)).all()


payment_service = PaymentService(Payment)
