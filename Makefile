env:
	pip install poetry==1.7.0
	poetry shell

install:
	poetry install

test:
	poetry run pytest tests -v

run:
	poetry run python tic-tac-toe/main.py