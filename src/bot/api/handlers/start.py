from aiogram import Router, filters, types

from src.bot.api.messages import Message
from toolkit.api.bot.utils import get_username

router = Router(name=__name__)


@router.message(filters.CommandStart())
async def start_handler(message: types.Message) -> None:
    """`/start` command handler."""
    await message.answer(
        text=Message.GREETING_MSG.format(
            username=get_username(message),
        )
    )
