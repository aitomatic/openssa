# A bunch of convenience utilities to get the examples built or deployed


# For installing GCloud CLI

TMP_DIR=/tmp
GCLOUD_DOWNLOAD_DIR=$(TMP_DIR)/google-cloud-sdk
OS := $(shell uname -s)
ARCH := $(shell uname -a | awk '{print $$NF}')
ifeq ($(ARCH),arm64)
    GCLOUD_CLI_FILE=google-cloud-cli-437.0.1-darwin-arm.tar.gz
else
    ifeq ($(ARCH),x86_64)
	GCLOUD_CLI_FILE=google-cloud-cli-437.0.1-darwin-x86_64.tar.gz
    endif
endif


none:
	@echo ... This Makefile has only utility targets

#test:
#	@echo ... This will run "npx jest" Javascript testing on all subdirs.
#	@echo ... Make sure you have set up Jest testing with "make dev-setup"
#	npx jest
#
#dev-setup:
#	@echo ... Setting up JS testing environment
#	@echo ""
#	npm install --save-dev fetch-mock
#	npm install --save-dev jest
#	npm install --save-dev jest-fetch-mock
#	npm install --save-dev jsdom @testing-library/jest-dom
#	npm install --save-dev @testing-library/dom
#	npm install --save-dev jest-environment-jsdom


#
# GCloud stuff
#
ifeq ($(ARCH),arm64)
install-gcloud-cli: do-install-gcloud-cli
else
    ifeq ($(ARCH),x86_64)
install-gcloud-cli: do-install-gcloud-cli
    endif
install-gcloud-cli:
	@echo ... Please follow GCloud installation instructions here: https://cloud.google.com/sdk/docs/install
	@open https://cloud.google.com/sdk/docs/install
endif

do-install-gcloud-cli:
	@echo ... Downloading and installing $(GCLOUD_CLI_FILE) ...
	@echo ""
	@GCLOUD_CLI_URL=https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/$(GCLOUD_CLI_FILE) ;\
	mkdir -p $(TMP_DIR) ;\
	cd $(TMP_DIR) && rm -f $(GCLOUD_CLI_FILE) && wget $$GCLOUD_CLI_URL && tar xvf $(GCLOUD_CLI_FILE) ;\
	cd $(GCLOUD_DOWNLOAD_DIR) && ./install.sh ;\
	cd $(TMP_DIR) && rm -fr $(GCLOUD_CLI_FILE) && rm -fr $(GCLOUD_DOWNLOAD_DIR)
	@echo ""
	@echo ... Now run gcloud init
