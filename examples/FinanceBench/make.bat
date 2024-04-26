@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="get-doc" GOTO get-doc

IF "%TARGET%"=="rag-default-answer" GOTO rag-default-answer
IF "%TARGET%"=="rag-finetuned-embed-answer" GOTO rag-finetuned-embed-answer
IF "%TARGET%"=="rag-finetuned-lm-answer" GOTO rag-finetuned-lm-answer
IF "%TARGET%"=="rag-finetuned-both-answer" GOTO rag-finetuned-both-answer
IF "%TARGET%"=="rag-gpt4-lm-answer" GOTO rag-gpt4-lm-answer
IF "%TARGET%"=="ooda-solve" GOTO ooda-solve
IF "%TARGET%"=="ssm-discuss" GOTO ssm-discuss

IF "%TARGET%"=="streamlit-run" GOTO streamlit-run


:: DATA PROCESSING
:: ===============
:get-doc
  poetry run python data.py %2
  GOTO end


:: BATCH INFERENCING
:: =================
:rag-default-answer
  poetry run python rag-default.py %2
  GOTO end

:rag-finetuned-embed-answer
  poetry run python rag-finetuned-embed-only.py %2
  GOTO end

:rag-finetuned-lm-answer
  poetry run python rag-finetuned-lm-only.py %2
  GOTO end

:rag-finetuned-both-answer
  poetry run python rag-finetuned-embed-and-lm.py %2
  GOTO end

:rag-gpt4-lm-answer
  poetry run python rag-gpt4-lm.py %2
  GOTO end

:ooda-solve
  poetry run python ooda.py %2
  GOTO end

:ssm-discuss
  poetry run python ssm.py %2
  GOTO end


:: STREAMLIT APP
:: =============
:streamlit-run
  poetry run streamlit run streamlit-main.py --server.allowRunOnSave=true --server.runOnSave=true
  GOTO end


:: END
:: ===
:end
