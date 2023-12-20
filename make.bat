@echo off


:: TARGETS
:: =======
SET TARGET=%1

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


:: INSTALLATION
:: ============
:install
  :: package with main & contrib dependencies
  python3 -m pip install -e ".[contrib]" --upgrade --user
  :: extra developer dependencies
  python3 -m pip install -r requirements/docs.txt -r requirements/lint.txt -r requirements/test.txt --upgrade --user
  GOTO end


:: LINTING
:: =======
:lint
  GOTO lint-flake8
  GOTO lint-pylint
  GOTO end

:lint-flake8
	flake8 %LIB_DIR_NAME% %DOCS_DIR_NAME% %EXAMPLES_DIR_NAME% %TESTS_DIR_NAME%
  GOTO end

:lint-pylint
	pylint %LIB_DIR_NAME% %DOCS_DIR_NAME% %EXAMPLES_DIR_NAME% %TESTS_DIR_NAME%
  GOTO end


:: TESTING
:: =======
:test
  pytest
  GOTO end


:: END
:: ===
:end
