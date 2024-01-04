# DIRECTORY NAMES & PATHS
# =======================
LIB_DIR=openssa

EXAMPLES_DIR=examples

TESTS_DIR=tests

DOCS_DIR=docs
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

install-editable:
	python3 -m pip install -e ".[contrib]" --upgrade --user


# LINTING
# =======
lint: lint-flake8 lint-pylint lint-ruff

lint-flake8:
	# flake8.pycqa.org/en/latest/user/invocation.html
	# flake8.pycqa.org/en/latest/user/options.html
	poetry run flake8 $(LIB_DIR) $(DOCS_DIR) $(EXAMPLES_DIR) $(TESTS_DIR) \
		--verbose --color always

lint-pylint:
	# pylint.readthedocs.io/en/latest/user_guide/usage/run.html
	poetry run pylint $(LIB_DIR) $(DOCS_DIR) $(EXAMPLES_DIR) $(TESTS_DIR)

lint-ruff:
	# docs.astral.sh/ruff/linter
	poetry run ruff check $(LIB_DIR) $(DOCS_DIR) $(EXAMPLES_DIR) $(TESTS_DIR) \
		--show-source \
		--output-format text \
		--target-version py310 \
		--preview \
		--respect-gitignore


# TESTING
# =======
test:
	poetry run pytest


# PRE-COMMIT LINTING & TESTING
# ============================
pre-commit: lint test


# DISTRIBUTION BUILDING & PYPI RELEASE
# ====================================
build:
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
	# sed -e /:undoc-members:/d -i .orig "$(DOCS_DIR)"/$(LIB_DIR)*.rst
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
	git reset "$(DOCS_DIR)/*.html"

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
	rsync . ../openssa/ \
		--archive \
		--delete \
		--exclude .git \
		--exclude __pycache__ --exclude .mypy_cache --exclude .pytest_cache --exclude .ruff_cache \
		--exclude .venv --exclude venv \
		--exclude *.rst --exclude "docs/_build" \
		--links \
		--verbose
