MANAGE := poetry run python task_manager/manage.py

install:
	@poetry install

make-migration:
	@$(MANAGE) makemigrations

migrate: make-migration
	@$(MANAGE) migrate

build: install migrate

start:
	$(MANAGE) runserver

check:
	poetry check

lint:
	poetry run flake8 ./task_manager/task_manager

deploy:
	poetry run gunicorn -w 5 task_manager.task_manager.wsgi
