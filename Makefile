MANAGE := poetry run python manage.py

.PHONY: install
install:
	@poetry install

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: create_superuser
create_superuser:
	@$(MANAGE) create_superuser

.PHONY: collect_static
collect_static:
	@$(MANAGE) collectstatic --no-input

.PHONY: setup
setup: install migrate

PORT ?= 8000
.PHONY: start
start:
	@poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

.PHONY: dev
dev:
	@$(MANAGE) runserver

.PHONY: compose-build
compose-build:
	@docker compose --file docker-compose.dev.yaml build

.PHONY: compose-start
compose-start:
	@docker compose --file docker-compose.dev.yaml up -d

.PHONY: compose-stop
compose-stop:
	@docker compose --file docker-compose.dev.yaml down

.PHONY: compose-restart
compose-restart: compose-stop compose-build compose-start

.PHONY: lint
lint:
	@poetry run flake8 task_manager --exclude migrations

.PHONY: test
test:
	@poetry run pytest tests

.PHONY: coverage
coverage:
	poetry run pytest --cov=task_manager --cov-report xml

.PHONY: makemessages
makemessages:
	@$(MANAGE) makemessages -l en

.PHONY: compilemessages
compilemessages:
	@$(MANAGE) compilemessages

.PHONY: coverage-html
coverage-html:
	poetry run pytest --cov=task_manager --cov-report html

