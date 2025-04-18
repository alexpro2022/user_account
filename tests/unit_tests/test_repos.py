from src.config import app_conf
from src.models import Secret, Task
from src.services.cipher import encrypt
from toolkit.test_tools import BaseTest_CRUD, BaseTest_Model, Data

# Bot tests ===================================
task_test_data = Data(
    model=Task,
    create_data=dict(name="name"),
    update_data=dict(description="Description"),
    default_data=dict(description="No description"),
    unique_fields=["name"],
)


class Test_TaskModel(BaseTest_Model):
    data = task_test_data


class Test_TaskCRUD(BaseTest_CRUD):
    data = task_test_data


# FastAPI tests ===================================
secret_test_data = Data(
    model=Secret,
    create_data={"secret": encrypt("доступ_к_конфиденциальным_данным")},
    default_data={"ttl_seconds": app_conf.secret_min_ttl},
    nullable_fields=["passphrase"],
)


class Test_SecretModel(BaseTest_Model):
    data = secret_test_data


class Test_SecretCRUD(BaseTest_CRUD):
    data = secret_test_data
