#!/usr/bin/make -f

PYTHON = python
VENV   = .venv
PORT   = 8008

DATABASE_URL ?= postgres://vydej:vydej@localhost:5432/vydej

export DATABASE_URL


help:
	@echo "Setup:"
	@echo "  venv           Setup virtual environment"
	@echo "  install        Install dependencies to venv"
	@echo "  install-hooks  Install pre-commit hooks"
	@echo "  hooks          Run pre-commit hooks manually"
	@echo ""
	@echo "Application:"
	@echo "  run            Run the application on port ${PORT}"
	@echo "  shell          Run Django shell"
	@echo ""
	@echo "Database:"
	@echo "  migrations     Generate migrations"
	@echo "  migrate        Run migrations"
	@echo ""
	@echo "Docker:"
	@echo "  build          Build image"
	@echo "  release        Upload image"
	@echo ""

venv: .venv/bin/python
.venv/bin/python:
	${PYTHON} -m venv ${VENV}

install: venv
	${VENV}/bin/pip install -r requirements/base.txt -r requirements/dev.txt

install-hooks:
	pre-commit install --install-hooks

hooks:
	pre-commit run -a

run: venv
	${VENV}/bin/python manage.py runserver ${PORT}

shell: venv
	${VENV}/bin/python manage.py shell_plus

migrations: venv
	${VENV}/bin/python manage.py makemigrations

migrate: venv
	${VENV}/bin/python manage.py migrate

build:
	docker build -t vydej-materialu:latest .

release:
	docker tag vydej-materialu:latest janbednarik/vydej-materialu:latest
	docker push janbednarik/vydej-materialu:latest

.PHONY: help venv install install-hooks hooks run shell
.PHONY: migrations migrate build release

# EOF
