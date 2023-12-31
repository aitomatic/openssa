# DIRECTORY NAMES & PATHS
# =======================
PROJECT_DIR=$(PWD)
ROOT_DIR=$(PROJECT_DIR)

LIB_DIR_NAME=openssa
LIB_DIR=$(PROJECT_DIR)/$(LIB_DIR_NAME)

EXAMPLES_DIR_NAME=examples
EXAMPLES_DIR=$(PROJECT_DIR)/$(EXAMPLES_DIR_NAME)

TESTS_DIR_NAME=tests
TESTS_DIR=$(PROJECT_DIR)/$(TESTS_DIR_NAME)

DOCS_DIR_NAME=docs
DOCS_DIR=$(PROJECT_DIR)/$(DOCS_DIR_NAME)

DOCS_BUILD_DIR=$(DOCS_DIR)/_build

DOCS_SUBDIRS_TO_PUBLISH := _images _static


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
	poetry install --extras=contrib --with=docs --with=lint --with=test


# LINTING
# =======
lint:
	poetry run pylint $(LIB_DIR_NAME) $(DOCS_DIR_NAME) $(EXAMPLES_DIR_NAME) $(TESTS_DIR_NAME)


# TESTING
# =======
test:
	poetry run pytest


# PRE-COMMIT LINTING & TESTING
# ============================
pre-commit: lint test


# DISTRIBUTION BUILDING & PYPI RELEASE
# ====================================
dist:
	poetry build

pypi-auth:
	@if [ "$(PYPI_TOKEN)" = "" ] ; then \
		echo $(ANSI_RED) Environment var PYPI_TOKEN must be set for pypi publishing $(ANSI_NORMAL) ; \
	else \
		poetry config pypi-token.pypi $(PYPI_TOKEN) ; \
	fi

release: build
	poetry publish


# DOCUMENTATION
# =============
docs: docs-build-clean docs-build-api
	poetry run sphinx-autobuild "$(DOCS_DIR)" "$(DOCS_BUILD_DIR)"

docs-build-clean:
	rm -f "$(DOCS_DIR)"/*.rst
	rm -rf "$(DOCS_BUILD_DIR)"

docs-build-api:
	# generate .rst files from module code & docstrings
	# any pathnames given at the end are paths to be excluded ignored during generation.
	# sphinx-doc.org/en/master/man/sphinx-apidoc.html
	poetry run sphinx-apidoc \
		--force \
		--follow-links \
		--maxdepth 9 \
		--separate \
		--implicit-namespaces \
		--module-first \
		--output-dir "$(DOCS_DIR)" "$(LIB_DIR)" \
		*/contrib/streamlit_ssa_prob_solver/main.py */contrib/streamlit_ssa_prob_solver/pages

	# get rid of undocumented members
	# sed -e /:undoc-members:/d -i .orig "$(DOCS_DIR)"/$(LIB_DIR_NAME)*.rst
	# rm "$(DOCS_DIR)"/*.orig

docs-build: docs-build-clean docs-build-api
	poetry run sphinx-build "$(DOCS_DIR)" "$(DOCS_BUILD_DIR)"

docs-deploy: docs-build
	git fetch --all

	git checkout gh-pages --

	git config user.email "TheVinhLuong@gmail.com"
	git config user.name "The Vinh LUONG (LƯƠNG Thế Vinh)"

	rm *.html
	cp "$(DOCS_BUILD_DIR)"/*.html .
	git add --all "*.html"
	git reset "$(DOCS_DIR_NAME)/*.html"

	for docs_subdir_to_publish in $(DOCS_SUBDIRS_TO_PUBLISH) ; do \
		echo "syncing $$docs_subdir_to_publish..." ; \
		rsync -av --delete --links "$(DOCS_BUILD_DIR)/$$docs_subdir_to_publish"/ $$docs_subdir_to_publish/ ; \
		git add --all "$$docs_subdir_to_publish/*" ; \
	done

	git commit -m "update GitHub Pages documentation site"
	git push

	git checkout docs --


# VERSION MANAGEMENT
# ==================
version:
	poetry version $(v)


# MISC / OTHER
# ============
launch-solver:
	poetry run openssa launch solver

public:
	rsync -av --delete --exclude .git --links . ../openssa/
