from src.bot.api.handlers import start as s
from src.bot.api.handlers import task as t
from src.bot.api.messages import Message
from tests.unit_tests.test_repos import task_test_data as DATA
from toolkit.api.bot.utils import get_markup
from toolkit.test_tools.base_test_bot import (
    BaseTest_CallbackUpdate,
    BaseTest_MessageUpdate,
    StateMixin,
    get_user,
)
from toolkit.test_tools.mixins import DBMixin

USERNAME_KWARGS = {"username": get_user().full_name}
TASK_NAME = DATA.get_test_obj().name  # "test_input_task_name"
TASK_DESCRIPTION = "No description"  # "test_input_task_description"


# def get_obj():
#     return Task(name=TASK_NAME, description=TASK_DESCRIPTION)


class Test_WrongCommandRouter(BaseTest_MessageUpdate):
    input_message_text = "wrong_command"
    expected_handler = t.wrong_command_handler
    expected_text = Message.WRONG_CMD_MSG.format(**USERNAME_KWARGS)


class Test_StartCommandRouter(BaseTest_MessageUpdate):
    input_message_text = "/start"
    expected_handler = s.start_handler
    expected_text = Message.GREETING_MSG.format(**USERNAME_KWARGS)


class Test_AddCommandRouter(StateMixin, BaseTest_MessageUpdate):
    input_message_text = "/add"
    expected_handler = t.add_task_handler
    expected_text = Message.ENTER_TASK_NAME_MSG.format(**USERNAME_KWARGS)
    expected_state = t.TaskInput.task_name.state


class Test_TaskNameRouter(StateMixin, BaseTest_MessageUpdate):
    input_message_text = TASK_NAME
    expected_handler = t.task_name_handler
    expected_text = Message.ENTER_TASK_DESCRIPTION_MSG.format(**USERNAME_KWARGS)
    expected_state = t.TaskInput.task_description.state
    expected_state_data = {"name": TASK_NAME}


# Create router ====================================================
class TaskCreateRouter(StateMixin, DBMixin, BaseTest_MessageUpdate):
    input_message_text = TASK_DESCRIPTION
    expected_handler = t.task_description_handler


class Test_TaskDescriptionRouterCreates(TaskCreateRouter):
    expected_text = Message.ADD_TASK_MSG.format(
        **USERNAME_KWARGS, task=f"{TASK_NAME}\n{TASK_DESCRIPTION}\n"
    )


class Test_TaskDescriptionRouterValidation(TaskCreateRouter):
    current_state = t.TaskInput.task_description.state
    expected_text = (
        "1 validation error for TaskCreate -> name -> Field required [type=missing]"
    )


class Test_TaskDescriptionRouterAlreadyExists(TaskCreateRouter):
    db_save_obj = DATA.get_test_obj
    current_state = t.TaskInput.task_description.state
    current_state_data = {"name": TASK_NAME}
    expected_text = f"Object Task(name='{TASK_NAME}', description='{TASK_DESCRIPTION}', id=None) already exists"


# List router ======================================================
class ListTaskRouter(DBMixin, BaseTest_MessageUpdate):
    input_message_text = "/tsk"
    expected_handler = t.list_tasks_handler
    expected_text = Message.TASK_LIST_MSG.format(**USERNAME_KWARGS)


class Test_ListTaskRouterReturnsEmpty(ListTaskRouter):
    expected_reply_markup = get_markup([])


class Test_ListTaskRouterReturnsOk(ListTaskRouter):
    db_save_obj = DATA.get_test_obj
    expected_reply_markup = get_markup(
        [(TASK_NAME, TASK_NAME)],
    )


# Summary router ================================================
class TaskSummaryRouter(DBMixin, BaseTest_CallbackUpdate):
    input_callback_data = TASK_NAME
    expected_handler = t.task_summary_handler


class Test_TaskSummaryRouterReturnsNotFound(TaskSummaryRouter):
    expected_text = f"Object with attributes {{'name': '{TASK_NAME}'}} not found"


class Test_TaskSummaryRouterReturnsOk(TaskSummaryRouter):
    db_save_obj = DATA.get_test_obj
    expected_text = Message.TASK_SUMMARY_MSG.format(
        **USERNAME_KWARGS,
        name=TASK_NAME,
        description=TASK_DESCRIPTION,
    )


# KEEP COMMENTS WITH MOCKS FOR EXAMPLE !!!
# class TestTaskDescriptionRouter(StateMixin, SessionPathMixin, BaseTest_MessageUpdate):
# async def mock(self, *args, **kwargs) -> str:
#     self._mock_counter += 1
#     return f"{TASK_NAME}\n{kwargs['description']}\n"
#
# funcs_to_mock = (
#     ("src.bot.services.task", "create_task", mock),
# )
# expected_mock_counter = 2
# input_message_text = TASK_DESCRIPTION
# expected_handler = t.task_description_handler
# expected_text = Message.ADD_TASK_MSG.format(
#     **USERNAME_KWARGS, task=f"{TASK_NAME}\n{TASK_DESCRIPTION}\n"
# )
# service_session_path = SERVICE_SESSION_PATH


# class TestListTaskRouter(SessionPathMixin, BaseTest_MessageUpdate):
# async def mock(self, session, model):
#     self._mock_counter += 1
#     assert session.in_transaction() is True
#     return [model(name=TASK_NAME, description=TASK_DESCRIPTION)]
#
# funcs_to_mock = (
#     ("src.repo.db.crud", "get_all", mock),
# )
# expected_mock_counter = 2
# input_message_text = "/tsk"
# expected_handler = t.list_tasks_handler
# expected_text = Message.TASK_LIST_MSG.format(**USERNAME_KWARGS)
# expected_reply_markup = get_markup([(TASK_NAME, TASK_NAME)],)


# class TestTaskSummaryRouterMock(BaseTest_CallbackUpdate):
# async def mock(self, session, model, **kwargs):
#     self._mock_counter += 1
#     assert session.in_transaction() is True
#     return model(description=TASK_DESCRIPTION, **kwargs)
#
# funcs_to_mock = (
#     ("src.repo.db.crud", "get_one", mock),
# )
# expected_mock_counter = 3
# input_callback_data = TASK_NAME
# expected_handler = t.task_summary_handler
# expected_text = "Object with attributes {'name': 'test_input_task_name'} not found"
# service_session_path = SERVICE_SESSION_PATH
