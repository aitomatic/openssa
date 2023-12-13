# DIRECTORY PATHS
# ===============
PROJECT_DIR=$(PWD)
ROOT_DIR=$(PROJECT_DIR)
LIB_DIR=$(PROJECT_DIR)/openssa
DIST_DIR=$(PROJECT_DIR)/dist
EXAMPLES_DIR=$(PROJECT_DIR)/examples
TESTS_DIR=$(PROJECT_DIR)/tests

export PYTHONPATH=$(ROOT_DIR)


# COLORIZED OUTPUT
# ================
ANSI_NORMAL="\033[0m"
ANSI_RED="\033[0;31m"
ANSI_GREEN="\033[0;32m"
ANSI_YELLOW="\033[0;33m"
ANSI_BLUE="\033[0;34m"
ANSI_MAGENTA="\033[0;35m"
ANSI_CYAN="\033[0;36m"
ANSI_WHITE="\033[0;37m"


# POETRY
# ======
get-poetry:
	python3 -m pip install Poetry --upgrade


# INSTALLATION
# ============
install:
	poetry lock
	poetry install --with=lint --with=test


# LINTING
# =======
lint:
	poetry run pylint openssa tests examples


# TESTING
# =======
test:
	@echo $(ANSI_GREEN)
	@echo "--------------------------------"
	@echo "|        Python Testing        |"
	@echo "--------------------------------"
	@echo $(ANSI_NORMAL)
	PYTHONPATH=$(PYTHONPATH):$(TESTS_DIR) poetry run pytest $(OPTIONS)


# PRE-COMMIT LINTING & TESTING
# ============================
pre-commit: lint test


# DISTRIBUTION BUILDING & PYPI RELEASE
# ====================================
build:
	poetry build

pypi-auth:
	@if [ "$(PYPI_TOKEN)" = "" ] ; then \
		echo $(ANSI_RED) Environment var PYPI_TOKEN must be set for pypi publishing $(ANSI_NORMAL) ;\
	else \
		poetry config pypi-token.pypi $(PYPI_TOKEN) ;\
	fi

release: build
	poetry publish


# DOCUMENTATION
# =============
docs: docs-build

docs-build:
	@PYTHONPATH=$(PYTHONPATH) cd docs && make build

docs-deploy: docs-build
	@PYTHONPATH=$(PYTHONPATH) cd docs && make deploy


# VERSION MANAGEMENT
# ==================
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


# MISC / OTHER
# ============
public:
	rsync -av --exclude .git --delete . ../openssa/
