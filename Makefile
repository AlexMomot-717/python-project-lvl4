install:
	poetry install

make migrate:
	python manage.py migrate

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

start-postgres:
	@docker-compose up -d postgres
	@sleep 2

stop-postgres:
	@docker-compose stop postgres

refresh-postgres-data:
	@docker-compose down --volumes
	@docker-compose build postgres
	@docker-compose up -d postgres
	@sleep 2

build-services:
	@docker-compose build --no-cache

up:
	@docker-compose up -d

down:
	@docker-compose down

start-services:
	@docker-compose start

stop-services:
	@docker-compose stop

restart:
	@docker-compose up --build
