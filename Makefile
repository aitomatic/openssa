# Set these values appropriately, or make sure they are set & exported from the environment
export OPENAI_API_KEY?=DUMMY_OPENAI_API_KEY

# Make sure we include the library directory
PROJECT_DIR=$(PWD)
ROOT_DIR=$(PROJECT_DIR)
LIB_DIR=$(PROJECT_DIR)/openssm
TESTS_DIR=$(PROJECT_DIR)/tests
EXAMPLES_DIR=$(PROJECT_DIR)/examples

export PYTHONPATH=$(ROOT_DIR):$(LIB_DIR)

test:
	PYTHONPATH=$(PYTHONPATH):$(TESTS_DIR) \
	    poetry run pytest

tests: test

test-console:
	PYTHONPATH=$(PYTHONPATH):$(TESTS_DIR) \
	    poetry run pytest --capture=no

build:
	poetry build

all: clean poetry-install requirements.txt build

pypi-publish:
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
