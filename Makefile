# Set these values appropriately, or make sure they are set & exported from the environment
export OPENAI_API_KEY?=DUMMY_OPENAI_API_KEY

# Make sure we include the library directory
PROJECT_DIR=$(PWD)
ROOT_DIR=$(PROJECT_DIR)
LIB_DIR=$(PROJECT_DIR)/openssm
TESTS_DIR=$(PROJECT_DIR)/tests
EXAMPLES_DIR=$(PROJECT_DIR)/examples
DIST_DIR=$(PROJECT_DIR)/dist

export PYTHONPATH=$(ROOT_DIR):$(LIB_DIR)
export PYTHONPATH=$(LIB_DIR)
export PYTHONPATH=

########

test: test-py test-js

test-console: test-py-console test-js

test-py:
	@echo "--------------------------------"
	@echo "|                              |"
	@echo "|        Python Testing        |"
	@echo "|                              |"
	@echo "--------------------------------"
	PYTHONPATH=$(PYTHONPATH):$(TESTS_DIR) poetry run pytest $(OPTIONS)

test-py-console:
	@echo "--------------------------------"
	@echo "|                              |"
	@echo "|        Python Testing        |"
	@echo "|                              |"
	@echo "--------------------------------"
	PYTHONPATH=$(PYTHONPATH):$(TESTS_DIR) poetry run pytest $(OPTIONS) --capture=no

test-js:
	@echo "--------------------------------"
	@echo "|                              |"
	@echo "|      Javascript Testing      |"
	@echo "|                              |"
	@echo "--------------------------------"
	cd $(TESTS_DIR) && npx jest


LINT_DIRS = openssm tests examples
lint: lint-py lint-js

lint-py:
	@for dir in $(LINT_DIRS) ; do \
		echo ... Running pylint on $$dir; \
		pylint $$dir ; \
	done

lint-js:
	cd $(TESTS_DIR) && npx eslint ..

pre-commit: lint test

build: poetry-setup
	poetry build
	poetry run pip install xformers==0.0.20

rebuild: clean build

install: local-install

dev-setup: poetry-install poetry-init poetry-setup pytest-setup pylint-setup jest-setup eslint-setup

local-install: build
	pip install $(DIST_DIR)/*.whl

local-uninstall:
	pip uninstall -y $(DIST_DIR)/*.whl

publish: pypi-publish

all: clean poetry-install requirements.txt build

clean:
	rm -fr poetry.lock dist/ requirements.txt

#
# Pypi PIP-related
#
#
pypi-publish: build
	poetry publish

pypi-auth:
	@if [ "$(PYPI_TOKEN)" = "" ] ; then \
		echo Environment var PYPI_TOKEN must be set for pypi publishing ;\
	else \
		poetry config pypi-token.pypi $(PYPI_TOKEN) ;\
	fi

#
# Poetry-related
#
poetry-install:
	curl -sSL https://install.python-poetry.org | python3 -
	if [ "$(GITHUB_PATH)" -ne "" ] ; then \
		echo $(HOME)/.local/bin >> $(GITHUB_PATH) ;\
	fi

poetry-setup:
	poetry lock
	poetry install
	poetry run pip install xformers==0.0.20

poetry-init:
	-poetry init

#
# For Python testing & liniting support
#
pytest-setup:
	@echo ... Setting up PYTEST testing environment
	@echo ""
	pip install pytest

pylint-setup:
	@echo ... Setting up PYLINT linting environment
	@echo ""
	pip install pylint

#
# For JS testing & liniting support
#
jest-setup:
	@echo ... Setting up JEST testing environment
	@echo ""
	cd $(TESTS_DIR) ;\
	npm install --omit=optional --save-dev fetch-mock ;\
	npm install --omit=optional --save-dev jest ;\
	npm install --omit=optional --save-dev jest-fetch-mock ;\
	npm install --omit=optional --save-dev jsdom @testing-library/jest-dom ;\
	npm install --omit=optional --save-dev @testing-library/dom ;\
	npm install --omit=optional --save-dev jsdom ;\
	npm install --omit=optional --save-dev jest-environment-jsdom

eslint-setup:
	@echo ... Setting up ESLINT linting environment
	@echo ""
	ln -s testsnode_modules
	cd $(TESTS_DIR) ;\
	npm init @eslint/config -- --config semistandard 

#
# Misc
#
requirements.txt: pyproject.toml
	poetry export --with dev --format requirements.txt --output requirements.txt

oss-publish:
	@echo temporary target
	# rsync -av --delete --dry-run ../ssm/ ../openssm/
	rsync -av --exclude .git --delete ../ssm/ ../openssm/

