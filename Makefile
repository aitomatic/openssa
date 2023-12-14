# DIRECTORY PATHS
# ===============
PROJECT_DIR=$(PWD)
ROOT_DIR=$(PROJECT_DIR)
LIB_DIR_NAME=openssa
LIB_DIR=$(PROJECT_DIR)/$(LIB_DIR_NAME)
DIST_DIR=$(PROJECT_DIR)/dist
EXAMPLES_DIR=$(PROJECT_DIR)/examples
TESTS_DIR=$(PROJECT_DIR)/tests

DOCS_DIR=$(PROJECT_DIR)/docs
DOCS_BUILD_DIR=$(DOCS_DIR)/_build
DOCS_BUILD_DOCTREES_DIR=$(DOCS_BUILD_DIR)/.doctrees
DOCS_BUILD_IMAGES_DIR_NAME=_images
DOCS_BUILD_IMAGES_DIR=$(DOCS_BUILD_DIR)/$(DOCS_BUILD_IMAGES_DIR_NAME)
DOCS_BUILD_SOURCES_DIR=$(DOCS_BUILD_DIR)_sources
DOCS_BUILD_STATIC_DIR_NAME=_static
DOCS_BUILD_STATIC_DIR=$(DOCS_BUILD_DIR)/$(DOCS_BUILD_STATIC_DIR_NAME)


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
	poetry install --with=lint --with=test --with=docs


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

docs-build-clean:
	rm -f $(DOCS_DIR)/*.rst
	rm -f $(DOCS_BUILD_DIR)/*.html
	rm -f $(DOCS_BUILD_DOCTREES_DIR)/*.doctree
	rm -f $(DOCS_BUILD_IMAGES_DIR)/*
	rm -f $(DOCS_BUILD_SOURCES_DIR)/*.txt
	rm -f $(DOCS_BUILD_STATIC_DIR)/*

docs-build-api:
	# generate .rst files from module code & docstrings
	# any pathnames given at the end are paths to be excluded ignored during generation.
	# sphinx-doc.org/en/master/man/sphinx-apidoc.html
	sphinx-apidoc \
		--force \
		--follow-links \
		--maxdepth 4 \
		--separate \
		--implicit-namespaces \
		--module-first \
		--output-dir $(DOCS_DIR) $(LIB_DIR)

	# get rid of undocumented members
	# grep -C2 ":undoc-members:" $(DOCS_DIR)/$(LIB_DIR_NAME)*.rst
	sed -e /:undoc-members:/d -i .orig $(DOCS_DIR)/$(LIB_DIR_NAME)*.rst
	rm $(DOCS_DIR)/*.orig

docs-build: docs-build-clean docs-build-api
	poetry run sphinx-autobuild $(DOCS_DIR) $(DOCS_BUILD_DIR)

docs-deploy:
	git checkout gh-pages

	rm *.html
	cp $(DOCS_BUILD_DIR)/*.html ./
	git add *.html

	# rsync -av --delete --links $(DOCS_BUILD_IMAGES_DIR)/ $(DOCS_BUILD_IMAGES_DIR_NAME)/
	# git add $(DOCS_BUILD_IMAGES_DIR_NAME)/*

	rsync -av --delete --links $(DOCS_BUILD_STATIC_DIR)/ $(DOCS_BUILD_STATIC_DIR_NAME)/
	git add $(DOCS_BUILD_STATIC_DIR_NAME)/*

	cp $(DOCS_BUILD_DIR)/.nojekyll .nojekyll
	git add .nojekyll

	git commit -m "update documentation"
	git push
	git checkout docs


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
	rsync -av --delete --exclude .git --links . ../openssa/
