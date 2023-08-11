FROM python:3.11

WORKDIR /opt/app

ENV DJANGO_SETTINGS_MODULE "task_manager.settings"

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
COPY Makefile Makefile
RUN python -m pip install --upgrade pip
RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install
