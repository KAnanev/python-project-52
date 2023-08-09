MANAGE := poetry run python manage.py

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: dev
dev:
	@$(MANAGE) runserver

.PHONY: docker-start
pg-start:
	docker compose --file docker-compose.dev.yaml up -d


.PHONY: docker-stop
pg-stop:
	docker compose --file docker-compose.dev.yaml down


.PHONY: lint
lint:
	@poetry run flake8 task_manager