@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="get-poetry" GOTO get-poetry

IF "%TARGET%"=="install" GOTO install

IF "%TARGET%"=="rag-default-answer" GOTO rag-default-answer
IF "%TARGET%"=="rag-finetuned-answer" GOTO rag-finetuned-answer
IF "%TARGET%"=="ooda-solve" GOTO ooda-solve

IF "%TARGET%"=="streamlit-run" GOTO streamlit-run


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


:: BATCH INFERENCING
:: =================
:rag-default-answer
  poetry run python rag_default.py %2
  GOTO end

:rag-finetuned-answer
  poetry run python rag_finetuned.py %2
  GOTO end

:ooda-solve
  poetry run python ooda.py %2
  GOTO end


:: STREAMLIT APP
:: =============
:streamlit-run
  poetry run streamlit run streamlit-main.py --server.allowRunOnSave=true --server.runOnSave=true
  GOTO end


:: END
:: ===
:end
