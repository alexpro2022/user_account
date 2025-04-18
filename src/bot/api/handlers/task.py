from aiogram import Router, filters, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.bot.api.messages import Message
from src.models import Task
from src.schemas.task import TaskCreate
from src.services import service
from toolkit.api.bot import utils as u
from toolkit.repo.db.exceptions import AlreadyExists, NotFound
from toolkit.types_app import _ASM

router = Router(name=__name__)


class TaskInput(StatesGroup):
    task_name = State()
    task_description = State()


@router.message(filters.Command("add"))
async def add_task_handler(message: types.Message, state: FSMContext) -> None:
    """`/add` command handler. Starts dialog."""
    await state.set_state(TaskInput.task_name)
    await message.answer(
        text=Message.ENTER_TASK_NAME_MSG.format(
            username=u.get_username(message),
        )
    )


@router.message(TaskInput.task_name)
async def task_name_handler(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(TaskInput.task_description)
    await message.answer(
        text=Message.ENTER_TASK_DESCRIPTION_MSG.format(
            username=u.get_username(message),
        )
    )


@router.message(TaskInput.task_description)
async def task_description_handler(
    message: types.Message, state: FSMContext, async_session_maker: _ASM
) -> None:
    async def get_text():
        async with async_session_maker.begin() as session:
            return Message.ADD_TASK_MSG.format(
                username=u.get_username(message),
                task=await service.create(session, Task, **data),
            )

    data = await state.update_data(description=message.text)
    await state.clear()

    valid, info = TaskCreate.is_valid(**data)
    await message.answer(
        text=await u.try_return(
            return_coro=get_text(),
            possible_exception=AlreadyExists,
        )
        if valid
        else info
    )


@router.message(filters.Command("tsk"))
async def list_tasks_handler(
    message: types.Message,
    async_session_maker: _ASM,
) -> None:
    """`/tsk` command handler. Creates the keyboard with the task names buttons."""
    async with async_session_maker() as session:
        await message.answer(
            text=Message.TASK_LIST_MSG.format(
                username=u.get_username(message),
            ),
            reply_markup=u.get_markup(
                *([(t.name, t.name)] for t in await service.get_all(session, Task))
            ),
        )


@router.message()
async def wrong_command_handler(message: types.Message) -> None:
    """Handles all messages except the commands `/start`, `/add`, `/tsk` and
    tips what to type."""
    await message.answer(
        text=Message.WRONG_CMD_MSG.format(
            username=u.get_username(message),
        )
    )


@router.callback_query()
async def task_summary_handler(
    callback: types.CallbackQuery,
    async_session_maker: _ASM,
) -> None:
    """Handles all callback queries - finds a task by name and
    returns a summary of the chosen task."""

    async def get_text():
        async with async_session_maker() as session:
            return Message.TASK_SUMMARY_MSG.format(
                username=u.get_username(callback),
                name=callback.data,
                description=(
                    await service.get(session, Task, name=callback.data)
                ).description,
            )

    await callback.message.edit_text(
        text=await u.try_return(
            return_coro=get_text(),
            possible_exception=NotFound,
        )
    )
