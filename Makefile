MANAGE := poetry run python manage.py
RUN := poetry run

install:
	@poetry install

make-migration:
	@$(MANAGE) makemigrations

migrate: make-migration
	@$(MANAGE) migrate

build: install migrate

lint:
	$(RUN) flake8 ./task_manager/

check:
	poetry check

test-html-coverage:
	$(RUN) coverage run --source='.' manage.py test task_manager
	$(RUN) coverage html

develop: lint check test-html-coverage

test:
	$(MANAGE) test

test-coverage:
	$(RUN) coverage run --source='.' manage.py test task_manager
	$(RUN) coverage lcov

build-messages:
	$(RUN) django-admin makemessages --ignore="static" --ignore=".env"  -l ru

compile-messages:
	$(RUN) django-admin compilemessages

start:
	$(MANAGE) runserver

shell:
	@$(MANAGE) shell

deploy:
	$(RUN) gunicorn task_manager.wsgi

clean:
	rm .coverage
	rm -rf *lcov
