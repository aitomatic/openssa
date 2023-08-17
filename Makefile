# Set these values appropriately, or make sure they are set & exported from the environment
export OPENAI_API_KEY?=DUMMY_OPENAI_API_KEY
export OPENAI_API_URL?=DUMMY_OPENAI_API_URL

# Make sure we include the library directory
PROJECT_DIR=$(PWD)
ROOT_DIR=$(PROJECT_DIR)
LIB_DIR=$(PROJECT_DIR)/openssm
TESTS_DIR=$(PROJECT_DIR)/tests
EXAMPLES_DIR=$(PROJECT_DIR)/examples
DIST_DIR=$(PROJECT_DIR)/dist

# Colorized output
ANSI_NORMAL="\033[0m"
ANSI_RED="\033[0;31m"
ANSI_GREEN="\033[0;32m"
ANSI_YELLOW="\033[0;33m"
ANSI_BLUE="\033[0;34m"
ANSI_MAGENTA="\033[0;35m"
ANSI_CYAN="\033[0;36m"
ANSI_WHITE="\033[0;37m"


export PYTHONPATH=$(ROOT_DIR):$(LIB_DIR)
#export PYTHONPATH=$(ROOT_DIR)
#export PYTHONPATH=$(LIB_DIR)
#export PYTHONPATH=

########

test: test-py test-js

test-console: test-py-console test-js

test-py:
	@echo $(ANSI_GREEN)
	@echo "--------------------------------"
	@echo "|                              |"
	@echo "|        Python Testing        |"
	@echo "|                              |"
	@echo "--------------------------------"
	@echo $(ANSI_NORMAL)
	PYTHONPATH=$(PYTHONPATH):$(TESTS_DIR) poetry run pytest $(OPTIONS)

test-py-console:
	@echo $(ANSI_GREEN)
	@echo "--------------------------------"
	@echo "|                              |"
	@echo "|        Python Testing        |"
	@echo "|                              |"
	@echo "--------------------------------"
	@echo $(ANSI_NORMAL)
	PYTHONPATH=$(PYTHONPATH):$(TESTS_DIR) poetry run pytest $(OPTIONS) --capture=no

test-js:
	@echo $(ANSI_GREEN)
	@echo "--------------------------------"
	@echo "|                              |"
	@echo "|      Javascript Testing      |"
	@echo "|                              |"
	@echo "--------------------------------"
	@echo $(ANSI_NORMAL)
	cd $(TESTS_DIR) && npx jest


LINT_DIRS = openssm tests examples
lint: lint-py lint-js

lint-py:
	@for dir in $(LINT_DIRS) ; do \
		echo $(ANSI_GREEN) ... Running pylint on $$dir $(ANSI_NORMAL); \
		pylint $$dir ; \
	done

lint-js:
	@-[ -e site/ ] && mv site/ /tmp/site/  # don’t lint the site/ directory
	cd $(TESTS_DIR) && npx eslint ..
	@-[ -e /tmp/site/ ] && mv -f /tmp/site/ site/  # put site/ back where it belongs

pre-commit: lint test

build: poetry-setup
	poetry build

rebuild: clean build

install: local-install

dev-setup: poetry-install poetry-init poetry-setup pytest-setup pylint-setup jest-setup eslint-setup bumpversion-setup

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
		echo $(ANSI_RED) Environment var PYPI_TOKEN must be set for pypi publishing $(ANSI_NORMAL) ;\
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

poetry-init:
	-poetry init

#
# For Python testing & liniting support
#
pytest-setup:
	@echo $(ANSI_GREEN) ... Setting up PYTEST testing environment $(ANSI_NORMAL)
	@echo ""
	pip install pytest

pylint-setup:
	@echo $(ANSI_GREEN) ... Setting up PYLINT linting environment $(ANSI_NORMAL)
	@echo ""
	pip install pylint

#
# For JS testing & liniting support
#
jest-setup:
	@echo $(ANSI_GREEN) ... Setting up JEST testing environment $(ANSI_NORMAL)
	@echo ""
	cd $(TESTS_DIR) ;\
	npm install --omit=optional --save-dev fetch-mock ;\
	npm install --omit=optional --save-dev jest ;\
	npm install --omit=optional --save-dev jest-fetch-mock ;\
	npm install --omit=optional --save-dev jsdom @testing-library/jest-dom ;\
	npm install --omit=optional --save-dev @testing-library/dom ;\
	npm install --omit=optional --save-dev jsdom ;\
	npm install --omit=optional --save-dev jest-environment-jsdom ;\
	npm install --omit=optional --save-dev babel-eslint ;\
	npm install eslint-plugin-react@latest --save-dev
	-ln -s tests/node_modules .

eslint-setup:
	@echo $(ANSI_GREEN) ... Setting up ESLINT linting environment $(ANSI_NORMAL)
	@echo ""
	-ln -s tests/node_modules .
	cd $(TESTS_DIR) ;\
	npm init @eslint/config -- --config semistandard 

#
# Misc
#
requirements.txt: pyproject.toml
	# poetry export --with dev --format requirements.txt --output requirements.txt
	 poetry export --format requirements.txt --output requirements.txt

pip-install: requirements.txt
	pip install -r requirements.txt

oss-publish:
	@echo temporary target
	# rsync -av --delete --dry-run ../ssm/ ../openssm/
	rsync -av --exclude .git --delete ../ssm/ ../openssm/

#
# For web-based documentation
#

docs: docs-build

docs-build:
	@PYTHONPATH=$(PYTHONPATH) cd docs && make build

docs-deploy: docs-build
	@PYTHONPATH=$(PYTHONPATH) cd docs && make deploy

#
# For version management
#
bumpversion-setup:
	pip install --upgrade bump2version

bumpversion-patch:
	bump2version --allow-dirty patch
	cd docs && make build

bumpversion-minor:
	bump2version --allow-dirty minor
	cd docs && make build

bumpversion-major:
	bump2version --allow-dirty major
	cd docs && make build
