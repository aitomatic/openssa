@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="rag-default-answer" GOTO rag-default-answer
IF "%TARGET%"=="rag-finetuned-answer" GOTO rag-finetuned-answer
IF "%TARGET%"=="ooda-solve" GOTO ooda-solve

IF "%TARGET%"=="streamlit-run" GOTO streamlit-run


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
