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

develop: lint check
	$(RUN) coverage run --source='.' manage.py test task_manager
	$(RUN) coverage html

test:
	$(MANAGE) test

test-coverage:
	$(RUN) coverage run --source='.' manage.py test task_manager
	$(RUN) coverage lcov

trans_start:
	$(RUN) django-admin makemessages --ignore="static" --ignore=".env"  -l ru

trans_finish:
	$(RUN) django-admin compilemessages

start:
	$(MANAGE) runserver

shell:
	@$(MANAGE) shell

deploy:
	$(RUN) gunicorn task_manager.wsgi:application

clean:
	rm -rf htmlcov
	rm *.lcov
