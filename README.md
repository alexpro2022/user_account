# User_accounts

[![CI/CD](https://github.com/alexpro2022/user_account/actions/workflows/flow_ci_cd.yaml/badge.svg)](https://github.com/alexpro2022/user_account/actions/workflows/flow_ci_cd.yaml)
[![Test Suite](https://github.com/alexpro2022/user_account/actions/workflows/flow_branch_test.yaml/badge.svg)](https://github.com/alexpro2022/user_account/actions/workflows/flow_branch_test.yaml)
[![pytest](https://img.shields.io/badge/pytest-93%25-green?logo=pytest)](https://github.com/alexpro2022/user_account/actions/runs/14705769842/job/41265774425#step:7:306)

<br>

Проект развернут на удаленном сервере.
Техническая документация:
  - Swagger: http://185.221.162.231:8000/docs
  - Redoc: http://185.221.162.231:8000/redoc

<!-- Для разработки используются эндпойнты по адресу:
http://185.221.162.231:8000/docs#/Development<br>
Сервисные эндпойнты по адресу:
http://185.221.162.231:8000/docs#/Secrets<br> -->

Администрирование БД может быть осуществлено через админ панель по адресу:
http://185.221.162.231:8001<br>
<details><summary>Учетные данные для входа в админ-зону</summary><br>

Пароль: `postgres`<br>

![alt text](images/credentials.png)

<h1></h1>
</details>


<br>



## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка приложения](#установка-приложения)
- [Разработка в Docker](#разработка-в-Docker)
- [Удаление приложения](#удаление-приложения)
- [Автор](#автор)

<br>



## Технологии
<details><summary>Подробнее</summary><br>

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/pydantic-2-blue?logo=Pydantic)](https://docs.pydantic.dev/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![asyncpg](https://img.shields.io/badge/-asyncpg-464646?logo=PostgreSQL)](https://pypi.org/project/asyncpg/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2-blue?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?logo=alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?logo=Uvicorn)](https://www.uvicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![docker_hub](https://img.shields.io/badge/-Docker_Hub-464646?logo=docker)](https://hub.docker.com/)
[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)
[![httpx](https://img.shields.io/badge/-httpx-464646?logo=httpx)](https://www.python-httpx.org/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-asyncio](https://img.shields.io/badge/-pytest--asyncio-464646?logo=Pytest-asyncio)](https://pypi.org/project/pytest-asyncio/)
[![pytest-cov](https://img.shields.io/badge/-pytest--cov-464646?logo=coverage)](https://pytest-cov.readthedocs.io/en/latest/)
[![pre-commit](https://img.shields.io/badge/-pre--commit-464646?logo=pre-commit)](https://pre-commit.com/)
[![factory_boy](https://img.shields.io/badge/-factory_boy-464646?logo=factory_boy)](https://factoryboy.readthedocs.io/en/stable/index.html)
[![toolkit](https://img.shields.io/badge/-toolkit-464646?logo=rocket)](https://pypi.org/project/app-toolkit-package/)

<h1></h1>
</details>
<br>



## Описание работы:
<details><summary>Подробнее</summary><br>

#### Реализована работа со следующими сущностями:
  ☑ Пользователь<br>
  ☑ Администратор<br>
  ☑ Счет - имеет баланс, привязан к пользователю<br>
  ☑ Платеж(пополнение баланса) - хранит уникальный идентификатор и сумму пополнения счета пользователя<br>

#### Пользователь имеет следующие возможности:
  ☑ Авторизоваться по email/password<br>
  ☑ Получить данные о себе(id, email, full_name)<br>
  ☑ Получить список своих счетов и балансов<br>
  ☑ Получить список своих платежей<br>

#### Администратор дополнительно может:
  ☑ Получить список пользователей<br>
  ☑ Получить/Создать/Удалить/Обновить пользователя<br>
  ☑ Получить список счетов пользователя с балансами<br>
  ☑ Получить список платежей пользователя<br>

#### Для работы с платежами реализован роут эмулирующий обработку вебхука от сторонней платежной системы. При обработке вебхука необходимо:
  ☑ Проверить подпись объекта<br>
  ☑ Проверить существует ли у пользователя такой счет - если нет, его необходимо создать<br>
  ☑ Начислить сумму транзакции на счет пользователя<br>
  ☑ Сохранить транзакцию в базе данных<br>

### Создание и редактирование пользователей, счетов и платежей:

#### Администратор создается при первом запуске приложения по учетным данным из **.env**-файла, по умолчанию:
  ```bash
  EMAIL=admin@admin.com
  PASSWORD=admin_pwd
  FIRST_NAME=admin
  LAST_NAME=admin
  PHONE_NUMBER=+79991112233
  ```

БД заполнена тестовыми данными:
  * Пользователи - 3
  * Счета - 3 на каждого пользователя (итого 9)
  * Платежи - 3 на каждый счет (итого 27)

  #### Пользователь может быть создан с любыми правами.
  - Данные для создания:
  ```json
  {
    "email": "user@user.com",
    "password": "user_pwd",
    "first_name": "user_name",
    "last_name": "user_surname",
    "phone_number": "+79211234567",
    "role": "USER"
  }
  ```
  - и редактирования:

  ```json
  {
    "first_name": "alex",
    "last_name": "pro",
    "phone_number": "+79213452402",
    "role": "ADMIN"
  }
  ```



[⬆️Оглавление](#оглавление)

<h1></h1>
</details>
<br>



## Установка приложения:
Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, но их можно оставить):

```bash
git clone https://github.com/alexpro2022/user_account.git
cd user_account
cp .env.example .env
nano .env
```
Все последующие команды производятся из **корневой** директории проекта.

[⬆️Оглавление](#оглавление)

<br>



## Разработка в Docker:
<!-- <details><summary>Запуск приложения</summary><br> -->
   <details><summary>Предварительные условия</summary><br>

   Предполагается, что пользователь установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине. Проверить наличие можно выполнив команды:

   ```bash
   docker -v && docker compose version
   ```
   <h1></h1>
   </details>
<br>

1. Запуск тестов - после прохождения тестов в консоль будет выведен отчет `pytest` и `coverage`(**xx%**):
```bash
docker compose -f docker/dev/test.docker-compose.yaml --env-file .env up --build --abort-on-container-exit && \
docker compose -f docker/dev/test.docker-compose.yaml --env-file .env down --volumes && docker system prune -f
```
<br>

2. Запуск приложения - проект будет развернут в docker-контейнерах по адресу http://localhost:8000/docs:
```bash
docker compose -f docker/dev/docker-compose.yaml --env-file .env up --build --detach
```
Для работы удобно использовать режим режим разработки:
```bash
docker compose -f docker/dev/docker-compose.yaml --env-file .env watch --prune --quiet
```
<br>

3. Остановить docker и удалить контейнеры можно командой:
```bash
docker compose -f docker/dev/docker-compose.yaml --env-file .env down && docker system prune -f
```

Если также необходимо удалить том базы данных:
```bash
docker compose -f docker/dev/docker-compose.yaml --env-file .env down --volumes && docker system prune -f
```

[⬆️Оглавление](#оглавление)

<br>



## Удаление приложения:
```bash
cd .. && rm -fr user_account
```

[⬆️Оглавление](#оглавление)

<br>



## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#user_accounts)
