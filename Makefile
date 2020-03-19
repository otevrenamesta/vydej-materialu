venv:
	python -m venv .venv

install:
	pip install -r requirements/base.txt -r requirements/dev.txt

install-hooks:
	pre-commit install --install-hooks

hooks:
	pre-commit run -a

run:
	python manage.py runserver 8008

shell:
	python manage.py shell_plus

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate
