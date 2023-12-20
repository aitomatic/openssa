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
set LIB_DIR_NAME=openssa
set LIB_DIR=.\%LIB_DIR_NAME%

set EXAMPLES_DIR_NAME=examples
set EXAMPLES_DIR=.\%EXAMPLES_DIR_NAME%

set TESTS_DIR_NAME=tests
set TESTS_DIR=.\%TESTS_DIR_NAME%

set DOCS_DIR_NAME=docs
set DOCS_DIR=.\%DOCS_DIR_NAME%

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
	poetry run flake8 %LIB_DIR_NAME% %DOCS_DIR_NAME% %EXAMPLES_DIR_NAME% %TESTS_DIR_NAME%
  GOTO end

:lint-pylint
	poetry run pylint %LIB_DIR_NAME% %DOCS_DIR_NAME% %EXAMPLES_DIR_NAME% %TESTS_DIR_NAME%
  GOTO end


:: TESTING
:: =======
:test
  poetry run pytest
  GOTO end


:: END
:: ===
:end
