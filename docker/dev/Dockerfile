# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12


FROM python:${PYTHON_VERSION}-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app


FROM base AS test
# Test =============
COPY pyproject.toml .
RUN python -m pip install --upgrade pip && pip install .[test]
COPY tests tests
# App ==============
COPY src src
# COPY toolkit toolkit


FROM base AS app
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    python -m pip install --upgrade pip && pip install .
# User ========
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
# Migration ========
COPY alembic.ini .
COPY alembic alembic
# App ==============
COPY src src
# COPY toolkit toolkit


# FROM base AS migration
# RUN pip install alembic
# COPY alembic.ini .
# COPY alembic alembic


# TO REMOVE BELOW ==========================
# CMD uvicorn src.app:app --host=0.0.0.0 --port=8000
# CMD uvicorn 'app:app' --host=0.0.0.0 --port=8000

# docker build -t=app --target=app -f=docker/dev/Dockerfile .
# docker build -t=test --target=test -f=docker/dev/Dockerfile .
# docker images | head -5
# docker history back
# docker rmi back

# docker run --name=app -it --rm app
# docker run --name=test -it --rm test
# docker stop back
# docker rm back
