.PHONY: install install-local install-docker run run-local run-docker test test-local test-docker init init-local init-docker docker-is-running docker-build-onbuild-ci docker-push-onbuild-ci

PLATFORM?=docker
TMP_HOOKS:=/tmp/.chessdb_api_hooks_empty.target
VERSION:=src/chessdb_api/core/version.py

.DEFAULT:help
help:
	@printf "\n\e[96m%s\e[0m" \
		"By default chessdb_api is running via Docker, to instead run it "\
		"locally, either export PLATFORM=local or use make PLATFORM=local "\
		"target (where target fx is run) each time, or just call the make "\
		"local-x taget directly. There's also a PLATFORM=ci for when running "\
		"in the pipeline"
	@printf "\n\n_____________________________________\n"
	@printf "The following commands are available:\n\n"
	@printf "\e[92m%s\e[0m\n" "make hooks"
	@echo " - setup pre-commit hooks"
	@printf "\e[92m%s\e[0m\n" "make test"
	@echo " - run tests"
	@printf "\e[92m%s\e[0m\n" "make lint"
	@echo " - Autoformats code and sorts imports (unless running as 'ci')."
	@printf "\e[92m%s\e[0m\n" "make run"
	@echo " - runs chessdb_api"

.env:
	@test -e .env || cp .example.env .env

${VERSION}:
	@echo "__version__ = \"$(shell git describe --always)\"" > ${VERSION}

test: test-$(PLATFORM)
run: run-$(PLATFORM)
lint: lint-$(PLATFORM)


hooks:${TMP_HOOKS}
${TMP_HOOKS}:.pre-commit-config.yaml
	@pip install pre-commit > /dev/null
	@pre-commit install > /dev/null
	@pre-commit run --all-files || \
		(printf "\e[93m%s\e[0m\n" "Run same make target again";exit 1)
	@printf "\e[92m%s\e[0m\n" "Pre-commit hooks ran successfully"
	@touch /tmp/.chessdb_api_hooks_empty_target

# CI
test-ci: ${VERSION} .env
	@python3 setup.py install
	@python3 setup.py test

lint-ci: ${VERSION} .env
	@pip install yapf pylint 'isort<5.0'
	@yapf --style google -dpr src tests migrations
	@pylint --rcfile=setup.cfg -r n src migrations tests > pylint.txt


test-local: .env ${VERSION}
	@python3 setup.py test

run-local: .env ${VERSION}
	@uvicorn chessdb_api.asgi:app --reload --port 10001

lint-local: hooks
	@isort --recursive src migrations tests
	@yapf --style google -ipr src migrations tests
	@pylint --rcfile=setup.cfg src migrations tests

test-docker: .env ${VERSION}
	@docker-compose up -d
	@docker-compose exec -T chessdb_api make test-local

run-docker: hooks .env ${VERSION}
	@docker-compose up -d

lint-docker: lint-local

clean:
	@find src migrations tests | grep -E "(__pycache__|\.pyc)" | xargs rm -rf
	@rm -rf src/chessdb_api.egg-info/ .eggs/ .coverage htmlcov/ dist/ build/ coverage.xml \
		pylint.txt
