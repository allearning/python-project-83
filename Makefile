install:
	poetry install

test:
	poetry run pytest -s

test-cov:
	poetry run pytest --cov=page_analyzer --cov-report xml

lint:
	poetry run flake8 page_analyzer

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

dev:
	poetry run flask --app page_analyzer:app --debug run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

publish:
	poetry publish --dry-run

.PHONY: install test lint selfcheck check build
