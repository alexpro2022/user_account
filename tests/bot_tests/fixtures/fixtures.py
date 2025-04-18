import pytest
from aiogram import Bot, Dispatcher

from src.bot.api.handlers import start, task
from src.config import bot_config as c
from toolkit.config.testdb_config import async_session


@pytest.fixture(scope="session")
def bot(generic_bot) -> Bot:
    return generic_bot(token=c.TEST_TOKEN)


@pytest.fixture(scope="session")
def dispatcher(generic_dispatcher) -> Dispatcher:
    return generic_dispatcher(
        # add your routers here
        start.router,
        task.router,
        # add your dependencies here
        async_session_maker=async_session,
    )
