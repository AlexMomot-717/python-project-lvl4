install:
	poetry install

run:
	python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

pre-commit:
	pre-commit run --all-files

lint:
	poetry run flake8
