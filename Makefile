MANAGE := poetry run python manage.py

install:
	@poetry install

make-migration:
	@$(MANAGE) makemigrations

migrate: make-migration
	@$(MANAGE) migrate

build: install migrate

lint:
	poetry run flake8 ./task_manager/

check:
	poetry check

develop: lint check
	poetry run coverage run --source='.' manage.py test task_manager
	poetry run coverage html

test:
	$(MANAGE) test

test-coverage:
	poetry run coverage run --source='.' manage.py test task_manager
	poetry run coverage lcov

trans_start:
	poetry run django-admin makemessages --ignore="static" --ignore=".env"  -l ru

trans_finish:
	poetry run django-admin compilemessages

start:
	$(MANAGE) runserver

shell:
	@$(MANAGE) shell

deploy:
	poetry run gunicorn -w 5 task_manager.wsgi

clean:
	rm -rf htmlcov
	rm *.lcov
