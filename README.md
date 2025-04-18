# PROJECT_NAME

[![Test Suite](https://github.com/alexpro2022/infra-template/actions/workflows/flow_branch_test.yaml/badge.svg)](https://github.com/alexpro2022/infra-template/actions/workflows/flow_branch_test.yaml)

===== TO BE REMOVED =====

cp -a toolkit/=new_proj_template/. .
cp .env.example .env


- CI/CD: test-build-push-deploy
- Docker: centralized, development and testing
- DB: Postgres, version on choice (via .env)
- Config: centralized, from .env file
- Requirements: centrilized, to update:
    * requirements.txt according to app stack
- Backend: Any (here simple FastAPI), code in /src, to update:
    * api/
    * app.py (main.py)
- Sevice: , part of App, to update:
    * service.py
- Repository: standard crud, part of App, to update:
    * models.py
- ORM: SQLAlchemy, to make migration, see alembic/env.py
- Tests: to update the following files:
    * unit_tests/test_models/test_models.py
    * integration_tests/ except utils.py

CREATING APP STEPS:

General:
- Clone infra-template from GH
- Adjust Readme.md Tech stack
- Adjust .env and .env.example
- Adjust requirements.txt

==============================================

1. bages here
2. short description here

<br>


## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка приложения](#установка-приложения)
- [Виртуальное окружение](#виртуальное-окружение)
- [Разработка в Docker](#разработка-в-Docker)
- [Удаление приложения](#удаление-приложения)
- [Автор](#автор)

<br>


## Технологии
<details><summary>Подробнее</summary><br>

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue?logo=python)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3-blue?logo=aiogram)](https://aiogram.dev/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?logo=fastapi)](https://fastapi.tiangolo.com/)
[![FastAPI_Users](https://img.shields.io/badge/-FastAPI--Users-464646?logo=fastapi-users)](https://fastapi-users.github.io/fastapi-users/)
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
[![Nginx](https://img.shields.io/badge/-NGINX-464646?logo=NGINX)](https://nginx.org/en/docs/)
[![SWAG](https://img.shields.io/badge/-SWAG-464646?logo=swag)](https://docs.linuxserver.io/general/swag)
[![httpx](https://img.shields.io/badge/-httpx-464646?logo=httpx)](https://www.python-httpx.org/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-asyncio](https://img.shields.io/badge/-Pytest--asyncio-464646?logo=Pytest-asyncio)](https://pypi.org/project/pytest-asyncio/)
[![pytest-cov](https://img.shields.io/badge/-pytest--cov-464646?logo=codecov)](https://pytest-cov.readthedocs.io/en/latest/)
[![deepdiff](https://img.shields.io/badge/-deepdiff-464646?logo=deepdiff)](https://zepworks.com/deepdiff/6.3.1/diff.html)
[![pre-commit](https://img.shields.io/badge/-pre--commit-464646?logo=pre-commit)](https://pre-commit.com/)
[![toolkit](https://img.shields.io/badge/-toolkit-464646?logo=python)](https://pypi.org/project/app-toolkit-package/)

[⬆️Оглавление](#оглавление)

---

</details>
<br>


## Описание работы:

Проект развернут на удаленном сервере.
Техническая документация:
  - Swagger: http://185.221.162.231:9000/docs
  - Redoc: http://185.221.162.231:9000/redoc


Для разработки используются эндпойнты по адресу:
http://185.221.162.231:9000/docs#/Development<br>
Сервисные эндпойнты по адресу:
http://185.221.162.231:9000/docs#/Secrets<br>
Администрирование БД может быть осуществлено через админ панель по адресу:
http://185.221.162.231:9001<br>
<details><summary>Учетные данные для входа в админ-зону</summary><br>

Пароль: `postgres`<br>

![alt text](images/credentials.png)

</details>


[⬆️Оглавление](#оглавление)

<br>


## Установка приложения:
Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, но их можно оставить):

```bash
git clone https://github.com/<proj_name>.git
cd <proj_name>
cp .env.example .env
nano .env
```
Все последующие команды производятся из корневой директории проекта.

[⬆️Оглавление](#оглавление)

<br>


## Виртуальное окружение:
paste from README.Venv.md here

<br>


## Разработка в Docker:
paste from README.Docker.md here

<br>


## Удаление приложения:
```bash
cd .. && rm -fr <proj_name>
```

[⬆️Оглавление](#оглавление)

<br>


## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#project_name)
