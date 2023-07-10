# Set these values appropriately, or make sure they are set & exported from the environment
export OPENAI_API_KEY?=DUMMY_OPENAI_API_KEY

# Make sure we include the library directory
PROJECT_DIR=$(PWD)
ROOT_DIR=$(PROJECT_DIR)/../..
LIB_DIR=$(ROOT_DIR)/openssm
TESTS_DIR=$(ROOT_DIR)/tests
EXAMPLES_DIR=$(ROOT_DIR)/examples
PORT=8080
ANSI_NORMAL="\033[0m"
ANSI_RED="\033[0;31m"
ANSI_GREEN="\033[0;32m"
ANSI_YELLOW="\033[0;33m"
ANSI_BLUE="\033[0;34m"
ANSI_MAGENTA="\033[0;35m"
ANSI_CYAN="\033[0;36m"
ANSI_WHITE="\033[0;37m"


export PYTHONPATH=$(ROOT_DIR):$(LIB_DIR):$(EXAMPLES_DIR)

run: run-dev

run-dev: poetry.lock openai-require
	@echo $(ANSI_GREEN)... Running app in DEV mode. Point your browser to http://localhost:$(PORT)/ $(ANSI_NORMAL)
	python app.py

run-prod: poetry.lock openai-require
	@echo $(ANSI_GREEN)... Running app in PROD mode. Point your browser to http://localhost:$(PORT)/ $(ANSI_NORMAL)
	gunicorn -b 0.0.0.0:8080 chatssm.app:app

build: poetry.lock openai-check favicons

rebuild: clean build

poetry.lock:
	@echo $(ANSI_GREEN)... Running poetry install $(ANSI_NORMAL)
	poetry install

all: clean requirements.txt build
	@echo $(ANSI_GREEN)... Cleaning, then remaking requirements.txt, and rebuild $(ANSI_NORMAL)

requirements.txt: pyproject.toml
	@echo $(ANSI_GREEN)... Making requirements.txt from pyproject.toml $(ANSI_NORMAL)
	poetry export --with dev --format requirements.txt --output requirements.txt

test:
	npx jest

clean:
	@echo $(ANSI_GREEN)... Cleaning things out $(ANSI_NORMAL)
	rm -fr poetry.lock requirements.txt


# GCloud project support 
GCLOUD_PROJECT_ID := openssm-examples-chatssm-$(shell whoami)

gcloud-create:
	@echo $(ANSI_GREEN)... Creating GCloud project $(GCLOUD_PROJECT_ID) $(ANSI_NORMAL)
	@if gcloud projects describe $(GCLOUD_PROJECT_ID) &> /dev/null; then \
	    echo "Project $(GCLOUD_PROJECT_ID) exists." ;\
	else \
	    gcloud projects create $(GCLOUD_PROJECT_ID) ;\
	fi

gcloud-enable-cloudbuild:
	@echo $(ANSI_GREEN)... Enabling Cloud-Build for project $(GCLOUD_PROJECT_ID) $(ANSI_NORMAL)
	@gcloud services enable cloudbuild.googleapis.com --project=$(GCLOUD_PROJECT_ID)

gcloud-deploy: gcloud-create gcloud-enable-cloudbuild requirements.txt openai-require favicons
	@echo $(ANSI_GREEN)... Deploying GCloud project $(GCLOUD_PROJECT_ID) $(ANSI_NORMAL)
	@echo $(ANSI_GREEN)... Replacing _PATTERN_OPENAI_API_KEY_ with the value from the env variable $(ANSI_NORMAL)
	mv app.yaml app.yaml.orig
	@sed -e s/_PATTERN_OPENAI_API_KEY_/$(OPENAI_API_KEY)/g app.yaml.orig > app.yaml

	@echo $(ANSI_GREEN)... Now deploying... $(ANSI_NORMAL)
	@gcloud app deploy --project=$(GCLOUD_PROJECT_ID)

	@echo $(ANSI_GREEN)... Restoring the safe and secure app.yaml $(ANSI_NORMAL)
	mv app.yaml.orig app.yaml


# Check for the presence of OPENAI_API_KEY
openai-check:
	@if [ -z "$${OPENAI_API_KEY}" ]; then \
	    echo "Warning: OPENAI_API_KEY is not set."; \
	fi

openai-require:
	@if [ -z "$${OPENAI_API_KEY}" ]; then \
	    echo "Error: OPENAI_API_KEY is not set."; \
	    exit 1; \
	fi

# Copy favicons from openssm
favicons:
	@echo $(ANSI_GREEN)... Copying OpenSSM favicons to this project $(ANSI_NORMAL)
	mkdir -p $(PROJECT_DIR)/static/images/favicon/
	cp -pr $(ROOT_DIR)/docs/resources/favicon/ $(PROJECT_DIR)/static/images/favicon/
