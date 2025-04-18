from aiogram import Bot, Dispatcher

from toolkit.test_tools import assert_isinstance


def test__bot_fixture(bot: Bot) -> None:
    assert_isinstance(bot, Bot)


def test__dispatcher_fixture(dispatcher: Dispatcher) -> None:
    assert_isinstance(dispatcher, Dispatcher)
