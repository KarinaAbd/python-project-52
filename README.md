# Study project No. 4 'Task Manager'

[![Actions Status](https://github.com/KarinaAbd/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/KarinaAbd/python-project-52/actions)
[![Python CI](https://github.com/KarinaAbd/python-project-52/actions/workflows/project_CI.yml/badge.svg)](https://github.com/KarinaAbd/python-project-52/actions/workflows/project_CI.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/ff1169bda4822b29f7d7/maintainability)](https://codeclimate.com/github/KarinaAbd/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/ff1169bda4822b29f7d7/test_coverage)](https://codeclimate.com/github/KarinaAbd/python-project-52/test_coverage)

try [Task Manager](https://task-manager-bykarina.onrender.com/) yourself
***

![tutorial](./static/task_manager_usage.gif)

This repository was created as part of [a Hexlet study project](https://ru.hexlet.io/programs/python/projects/52). "Task Manager" is a a web application that allows you to set tasks, assign executors and change their statuses. Registration and authentication are required to work with the system.

## How to install for develop

Make a fork and clone the repository locally.
```bash
cd python-project-52/
# install poetry
make install
```
Create `.env` file based on the `.env_example` for right project work.
And run it local:
```bash
make build
make start
```
