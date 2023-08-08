MANAGE := poetry run python manage.py

.PHONY: dev
dev:
	@$(MANAGE) runserver

.PHONY: docker-start
docker-start:
	docker compose --file docker-compose.dev.yaml up -d


.PHONY: docker-start
docker-stop:
	docker compose --file docker-compose.dev.yaml up -d