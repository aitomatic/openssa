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

test:
	PYTHONPATH=$(PYTHONPATH):$(TESTS_DIR) \
	    poetry run pytest

tests: test

test-console:
	PYTHONPATH=$(PYTHONPATH):$(TESTS_DIR) \
	    poetry run pytest --capture=no

build: poetry-install
	poetry build
	poetry run pip install xformers==0.0.20

rebuild: clean build

install: local-install

local-install: build
	pip install $(DIST_DIR)/*.whl

local-uninstall:
	pip uninstall -y $(DIST_DIR)/*.whl

publish: pypi-publish

all: clean poetry-install requirements.txt build

pypi-publish: build
	poetry publish

pypi-auth:
	echo poetry config pypi-token.pypi $(PYPI_TOKEN)

poetry-install:
	poetry lock
	poetry install

poetry-init:
	-poetry init

requirements.txt: pyproject.toml
	poetry export --with dev --format requirements.txt --output requirements.txt

clean:
	rm -fr poetry.lock dist/ requirements.txt

oss-publish:
	@echo temporary target
	# rsync -av --delete --dry-run ../ssm/ ../openssm/
	rsync -av --exclude .git --delete ../ssm/ ../openssm/
