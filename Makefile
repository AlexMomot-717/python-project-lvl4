install:
	poetry install

migrations:
	@python manage.py makemigrations
	@python manage.py migrate

run:
	python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

pre-commit:
	pre-commit run --all-files

lint:
	poetry run flake8

test:
	pytest -s

test-coverage:
	pytest --cov=task_manager --cov-report xml --cov-report=html
