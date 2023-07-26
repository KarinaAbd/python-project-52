MANAGE := poetry run python manage.py

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
	poetry run flake8 ./task_manager/

trans_start:
	poetry run django-admin makemessages --ignore="static" --ignore=".env"  -l ru

trans_finish:
	poetry run django-admin compilemessages

deploy:
	poetry run gunicorn -w 5 task_manager.wsgi
