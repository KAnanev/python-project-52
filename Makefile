MANAGE := poetry run python manage.py

.PHONY: install
install:
	@poetry install

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: setup
setup: install migrate

.PHONY: dev
dev:
	@$(MANAGE) runserver

.PHONY: docker-start
pg-start:
	@docker compose --file docker-compose.dev.yaml up -d


.PHONY: docker-stop
pg-stop:
	@docker compose --file docker-compose.dev.yaml down


.PHONY: lint
lint:
	@poetry run flake8 task_manager


.PHONY: test
test:
	@poetry run pytest tests

.PHONY: check-actions
check-actions:
	@act --env-file .env -W .github/workflows/django-check.yml --container-architecture linux/amd64 -v