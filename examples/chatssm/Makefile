# Set these values appropriately, or make sure they are set & exported from the environment

APPNAME=$(notdir $(CURDIR))

# Make sure we include the library directory
PROJECT_DIR=.
ROOT_DIR=$(PROJECT_DIR)/../..
OPENSSM_DIR=$(ROOT_DIR)/openssm
TESTS_DIR=$(ROOT_DIR)/tests
EXAMPLES_DIR=$(ROOT_DIR)/examples
PORT=8080

CONFIG_SECRETS=$(PROJECT_DIR)/config_secrets.py
export OPENAI_API_KEY
export OPENAI_API_URL
export FALCON7B_API_URL
export FALCON7B_API_KEY

ANSI_NORMAL="\033[0m"
ANSI_RED="\033[0;31m"
ANSI_GREEN="\033[0;32m"
ANSI_YELLOW="\033[0;33m"
ANSI_BLUE="\033[0;34m"
ANSI_MAGENTA="\033[0;35m"
ANSI_CYAN="\033[0;36m"
ANSI_WHITE="\033[0;37m"


export PYTHONPATH=$(ROOT_DIR):$(OPENSSM_DIR):$(EXAMPLES_DIR)

echo:
	@echo $(ANSI_GREEN)
	@echo This is the examples/$(APPNAME) app.
	@echo You can ...
	@echo "% make run"
	@echo "% make run-prod"
	@echo "% make build"
	@echo Other targets include ...
	@echo clean, test, etc.
	@echo $(ANSI_NORMAL)


run: run-dev

run-dev: poetry.lock openai-require config-secrets
	@echo $(ANSI_GREEN)... Running app in DEV mode. Point your browser to http://localhost:$(PORT)/ $(ANSI_NORMAL)
	python app.py

run-prod: poetry.lock openai-require config-secrets
	@echo $(ANSI_GREEN)... Running app in PROD mode. Point your browser to http://localhost:$(PORT)/ $(ANSI_NORMAL)
	gunicorn -b 0.0.0.0:8080 $(APPNAME).app:app

build: poetry.lock requirements.txt openai-check favicons config-secrets

rebuild: clean build

poetry.lock:
	@echo $(ANSI_GREEN)... Running poetry install $(ANSI_NORMAL)
	poetry install

all: clean requirements.txt build
	@echo $(ANSI_GREEN)... Cleaning, then remaking requirements.txt, and rebuild $(ANSI_NORMAL)

requirements.txt: pyproject.toml
	@echo $(ANSI_GREEN)... Making requirements.txt from pyproject.toml $(ANSI_NORMAL)
	poetry export --dev --format requirements.txt --output requirements.txt

test:
	npx jest

clean: clear-config-secrets
	@echo $(ANSI_GREEN)... Cleaning things out $(ANSI_NORMAL)
	rm -fr poetry.lock requirements.txt dist/

clear-config-secrets:
	@echo $(ANSI_GREEN)... Emptying $(CONFIG_SECRETS) file $(ANSI_NORMAL)
	echo "" > $(CONFIG_SECRETS)

config-secrets: clear-config-secrets
	@echo $(ANSI_GREEN)... Creating $(CONFIG_SECRETS) file $(ANSI_NORMAL)
	echo "from openssm import Config" >> $(CONFIG_SECRETS)
	echo "" >> $(CONFIG_SECRETS)
	echo "" >> $(CONFIG_SECRETS)
	echo "Config.OPENAI_API_KEY='$(OPENAI_API_KEY)'" >> $(CONFIG_SECRETS)
	echo "Config.OPENAI_API_URL='$(OPENAI_API_URL)'" >> $(CONFIG_SECRETS)
	echo "Config.FALCON7B_API_URL='$(FALCON7B_API_URL)'" >> $(CONFIG_SECRETS)
	echo "Config.FALCON7B_API_KEY='$(FALCON7B_API_KEY)'" >> $(CONFIG_SECRETS)

#
# GCloud project support 
#
GCLOUD_PROJECT_ID := openssm-examples-$(APPNAME)-$(shell whoami)

install-gcloud-cli:
	@cd .. && make $@

gcloud-create:
	@echo $(ANSI_GREEN)... Creating GCloud project $(GCLOUD_PROJECT_ID) $(ANSI_NORMAL)
	@if gcloud projects describe $(GCLOUD_PROJECT_ID) &> /dev/null; then \
	    echo "Project $(GCLOUD_PROJECT_ID) exists." ;\
	else \
	    gcloud projects create $(GCLOUD_PROJECT_ID) ;\
	fi
	@echo $(ANSI_GREEN)... Setting GCloud default project to $(GCLOUD_PROJECT_ID) $(ANSI_NORMAL)
	gcloud config set project $(GCLOUD_PROJECT_ID)
	@echo $(ANSI_GREEN)... Creating app for $(GCLOUD_PROJECT_ID) $(ANSI_NORMAL)
	-gcloud app create

gcloud-enable-cloudbuild:
	@echo $(ANSI_GREEN)... Enabling Cloud-Build for project $(GCLOUD_PROJECT_ID) $(ANSI_NORMAL)
	@gcloud services enable cloudbuild.googleapis.com --project=$(GCLOUD_PROJECT_ID)

gcloud-deploy: gcloud-create gcloud-enable-cloudbuild requirements.txt openai-require favicons
	@echo $(ANSI_GREEN)... Deploying GCloud project $(GCLOUD_PROJECT_ID) $(ANSI_NORMAL)
	@echo $(ANSI_GREEN)... Replacing _PATTERN_OPENAI_API_KEY_ with the value from the env variable $(ANSI_NORMAL)
	@if grep _PATTERN_OPENAI_API_KEY app.yaml ; then \
		mv app.yaml app.yaml.orig ;\
	fi
	@sed -e s/_PATTERN_OPENAI_API_URL_/$(OPENAI_API_URL)/g app.yaml.orig > app.yaml
	@echo $(ANSI_GREEN)... Replacing _PATTERN_OPENAI_API_URL_ with the value from the env variable $(ANSI_NORMAL)
	@if grep _PATTERN_OPENAI_API_URL app.yaml ; then \
		mv app.yaml app.yaml.orig ;\
	fi
	@sed -e s/_PATTERN_OPENAI_API_URL_/$(OPENAI_API_URL)/g app.yaml.orig > app.yaml

	@echo $(ANSI_GREEN)... Now deploying... $(ANSI_NORMAL)
	@yes | gcloud app deploy --project=$(GCLOUD_PROJECT_ID)

	@echo $(ANSI_GREEN)... Restoring the safe and secure app.yaml $(ANSI_NORMAL)
	mv app.yaml.orig app.yaml

gcloud-submit: gcloud-create gcloud-enable-cloudbuild requirements.txt openai-require favicons
	gcloud builds submit --config cloudbuild.yaml .

gcloud-log:
	CLOUDSDK_CORE_PROJECT=$(GCLOUD_PROJECT_ID) gcloud app logs tail -s default

#
# Check for the presence of OPENAI_API_KEY
#
openai-check:
	@if [ -z "$${OPENAI_API_KEY}" ]; then \
	    echo "Warning: OPENAI_API_KEY is not set."; \
	fi

openai-require:
	@if [ -z "$${OPENAI_API_KEY}" ]; then \
	    echo "Error: OPENAI_API_KEY is not set."; \
	    exit 1; \
	fi

#
# Copy favicons from openssm
#
favicons:
	@echo $(ANSI_GREEN)... Copying OpenSSM favicons to this project $(ANSI_NORMAL)
	mkdir -p $(PROJECT_DIR)/static/images/favicon/
	cp -pr $(ROOT_DIR)/docs/resources/favicon/ $(PROJECT_DIR)/static/images/favicon/

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
