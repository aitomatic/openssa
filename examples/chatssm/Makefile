# Set these values appropriately, or make sure they are set & exported from the environment
export OPENAI_API_KEY?=DUMMY_OPENAI_API_KEY

# Make sure we include the library directory
PROJECT_DIR=$(PWD)
ROOT_DIR=$(PROJECT_DIR)/../..
LIB_DIR=$(ROOT_DIR)/openssm
TESTS_DIR=$(ROOT_DIR)/tests
EXAMPLES_DIR=$(ROOT_DIR)/examples

export PYTHONPATH=$(ROOT_DIR):$(LIB_DIR):$(EXAMPLES_DIR)

run-dev: poetry.lock
	python app.py

run-prod: poetry.lock
	gunicorn -b 0.0.0.0:8080 chatssm.app:app

build: poetry.lock
	poetry build

poetry.lock:
	poetry install

all: clean requirements.txt build

requirements.txt: pyproject.toml
	poetry export --with dev --format requirements.txt --output requirements.txt

clean:
	rm -fr poetry.lock requirements.txt
