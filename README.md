# Study project No. 4 'Task Manager'

[![Actions Status](https://github.com/KarinaAbd/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/KarinaAbd/python-project-52/actions)
[![Python CI](https://github.com/KarinaAbd/python-project-52/actions/workflows/project_CI.yml/badge.svg)](https://github.com/KarinaAbd/python-project-52/actions/workflows/project_CI.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/ff1169bda4822b29f7d7/maintainability)](https://codeclimate.com/github/KarinaAbd/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/ff1169bda4822b29f7d7/test_coverage)](https://codeclimate.com/github/KarinaAbd/python-project-52/test_coverage)

## About

try [Task Manager](https://task-manager-bykarina.onrender.com/) on render.com

This repository was created as part of [a Hexlet study project](https://ru.hexlet.io/programs/python/projects/52). "Task Manager" is a web application that allows you:
 - to register in the application using the registration form provided;
 - to log in using the information from the registration form;
 - to see the list of all registered **_users_** on the corresponding page without authorization. But you can change or delete information only about yourself. If a user is the author or performer of a task, it cannot be deleted;
 - to view, add, update, and delete task **_statuses_** & task **_labels_** if you are logged in. Statuses and labels corresponding to any tasks cannot be deleted;
 - to view, add, and update **_tasks_** if you are logged in. Only the task creator can delete tasks. You can also filter tasks on the corresponding page with specified statuses, performers, and labels;

![tutorial](./static/task_manager_usage.gif)
***

## Built With

    python = "^3.10"
    django = "^4.2.3"
    poetry = "1.2.2"
    django-bootstrap5 = "^23.3"
    dj-database-url = "^2.0.0"
    psycopg2-binary = "^2.9.6"
    python-dotenv = "^1.0.0"
    django-filter = "^23.2"
    gunicorn = "^20.1.0"
    whitenoise = "^6.5.0"
    rollbar = "^0.16.3"
    coverage = "^7.2.7"
    flake8 = "^6.0.0"

## How to install for develop
[Install poetry](https://python-poetry.org/docs/#installation) if you haven't already. Make a fork and clone the repository locally. Then:
```bash
cd python-project-52/
make install # install the dependencies
```
Create `.env` file  (based on the `.env.sample`) in the root folder for right project work and run it local:
```bash
make migrate
make start
```
To get to know the rest of the commands, see Makefile.
