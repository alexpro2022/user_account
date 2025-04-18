# import os
# import sys
# sys.path.append(os.getcwd())
# NO NEED ABOVE SINCE IT RUNS AS MODULE alembic upgrade head && python -m src.bot
import asyncio
import logging

from aiogram import Bot
from toolkit.api.bot import utils
from toolkit.config.db_config import async_session

from src.bot.api.handlers import start, task
from src.config import bot_config as c

# from src.bot.api.handlers  import all handlers here


async def app() -> None:
    bot = Bot(token=c.bot_conf.token.get_secret_value())
    dp = utils.get_dispatcher(
        # add your routers here
        start.router,
        task.router,
        # add your dependencies here
        async_session_maker=async_session,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(app())
