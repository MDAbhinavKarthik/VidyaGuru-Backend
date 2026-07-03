.PHONY: run test lint format migrate clean docker-up docker-down

run:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest

lint:
	flake8 controllers models services core schemas
	mypy controllers models services core schemas

format:
	black controllers models services core schemas tests
	isort controllers models services core schemas tests

migrate:
	alembic -c scripts/alembic/alembic.ini upgrade head

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down
