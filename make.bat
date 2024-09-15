@echo off


:: DIRECTORY NAMES & PATHS
:: =======================
SET LIB_DIR=openssa

SET EXAMPLES_DIR=examples

SET TESTS_DIR=tests

SET DOCS_DIR=docs
SET DOCS_BUILD_DIR=%DOCS_DIR%\_build


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="get-poetry" GOTO get-poetry

IF "%TARGET%"=="install" GOTO install
IF "%TARGET%"=="install-editable" GOTO install-editable

IF "%TARGET%"=="lint" GOTO lint
IF "%TARGET%"=="lint-flake8" GOTO lint-flake8
IF "%TARGET%"=="lint-pylint" GOTO lint-pylint
IF "%TARGET%"=="lint-ruff" GOTO lint-ruff

IF "%TARGET%"=="test" GOTO test

IF "%TARGET%"=="pre-commit" GOTO pre-commit

IF "%TARGET%"=="build" GOTO build
IF "%TARGET%"=="release" GOTO release

IF "%TARGET%"=="version" GOTO version

IF "%TARGET%"=="launch-solver" GOTO launch-solver


:: POETRY
:: ======
:get-poetry
  python3 -m pip install Poetry --upgrade --user
  GOTO end


:: INSTALLATION
:: ============
:install
  poetry lock
  poetry install ^
    --extras=contrib ^
    --with=docs --with=lint --with=test
  GOTO end

:install-editable
  python3 -m pip install -e ".[contrib, langchain]" --upgrade --user
  GOTO end


:: LINTING
:: =======
:lint
  GOTO lint-flake8
  GOTO lint-pylint
  GOTO lint-ruff
  GOTO end

:lint-flake8
  :: flake8.pycqa.org/en/latest/user/invocation.html
  :: flake8.pycqa.org/en/latest/user/options.html
  poetry run flake8 %LIB_DIR% %DOCS_DIR% %EXAMPLES_DIR% %TESTS_DIR% ^
    --verbose --color always
  GOTO end

:lint-pylint
  :: pylint.readthedocs.io/en/latest/user_guide/usage/run.html
  poetry run pylint %LIB_DIR% %DOCS_DIR% %EXAMPLES_DIR% %TESTS_DIR% --recursive=y
  GOTO end

:lint-ruff
  :: docs.astral.sh/ruff/linter
  poetry run ruff check %LIB_DIR% %DOCS_DIR% %EXAMPLES_DIR% %TESTS_DIR% ^
    --output-format full ^
    --target-version py310 ^
    --preview ^
    --respect-gitignore
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
