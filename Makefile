MANAGE := poetry run python manage.py

.PHONY: dev
migrate:
	@$(MANAGE) runserver