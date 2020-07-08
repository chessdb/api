migrate: install
	@alembic revision -m "${msg}"

upgrade: install
	@alembic upgrade head

docker-run:
	@docker-compose build
	@docker-compose up -d

docker-logs:
	@docker-compose logs -f

docker-test:
	@docker-compose exec chessdb_api python setup.py test

run: upgrade
	@uvicorn chessdb_api.asgi:app --reload
build:
	@python setup.py build

install: clean
	@python setup.py develop

test: install
	@python setup.py test


DB ?= chessdb_api
clean_db: clean
	@psql -U postgres -d ${DB} -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

lint: yapf pylint

pylint:
	@pip install pylint
	@pylint --rcfile=setup.cfg -r n src > pylint.txt
	@cat pylint.txt

isort:
	@pip install isort
	@isort -c **/*.py

yapf:
	@pip install yapf
	@yapf -dpr src tests migrations

clean:
	@rm -rf __pycache__/ src/chessdb_api.egg-info/ .eggs/ .coverage htmlcov/ dist/ build/ coverage.xml pylint.txt

hooks:
	@pip install pre-commit
	@pre-commit install

fix:
	@yapf -ipr src tests migrations
	@isort --atomic --recursive src migrations tests

.PHONY: clean lint test build install run docker-run migrate clean_db yapf pylint fix
