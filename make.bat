@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="get-poetry" GOTO get-poetry

IF "%TARGET%"=="install" GOTO install

IF "%TARGET%"=="lint" GOTO lint

IF "%TARGET%"=="test" GOTO test


:: DIRECTORY NAMES & PATHS
:: =======================
set LIB_DIR=openssa

set EXAMPLES_DIR=examples

set TESTS_DIR=tests

set DOCS_DIR=docs
set DOCS_BUILD_DIR=%DOCS_DIR%\_build


:: POETRY
:: ======
:get-poetry
  python3 -m pip install Poetry --upgrade --user
  GOTO end


:: INSTALLATION
:: ============
:install
  poetry lock
  poetry install --extras=contrib --with=docs --with=lint --with=test 
  GOTO end


:: LINTING
:: =======
:lint
  GOTO lint-flake8
  GOTO lint-pylint
  GOTO end

:lint-flake8
	poetry run flake8 %LIB_DIR% %DOCS_DIR% %EXAMPLES_DIR% %TESTS_DIR%
  GOTO end

:lint-pylint
	poetry run pylint %LIB_DIR% %DOCS_DIR% %EXAMPLES_DIR% %TESTS_DIR%
  GOTO end


:: TESTING
:: =======
:test
  poetry run pytest
  GOTO end


:: PRE-COMMIT LINTING & TESTING
:: ============================
:pre-commit
  GOTO lint
  GOTO test
  GOTO end


:: DISTRIBUTION BUILDING & PYPI RELEASE
:: ====================================
:build
  poetry build
  GOTO end

:release
  GOTO build
  poetry publish
  GOTO end


:: VERSION MANAGEMENT
:: ==================
:version
  poetry version %2
  GOTO end


:: MISC / OTHER
:: ============
:launch-solver
  poetry run openssa launch solver
  GOTO end


:: END
:: ===
:end
