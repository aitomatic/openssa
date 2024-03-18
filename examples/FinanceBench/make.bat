@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="rag-default-answer" GOTO rag-default-answer
IF "%TARGET%"=="rag-finetuned-embed-answer" GOTO rag-finetuned-embed-answer
IF "%TARGET%"=="rag-finetuned-lm-answer" GOTO rag-finetuned-lm-answer
IF "%TARGET%"=="rag-finetuned-both-answer" GOTO rag-finetuned-both-answer
IF "%TARGET%"=="ooda-solve" GOTO ooda-solve
IF "%TARGET%"=="ssm-discuss" GOTO ssm-discuss

IF "%TARGET%"=="streamlit-run" GOTO streamlit-run


:: BATCH INFERENCING
:: =================
:rag-default-answer
  poetry run python rag_default.py %2
  GOTO end

:rag-finetuned-embed-answer
  poetry run python rag_finetuned_embed_only.py %2
  GOTO end

:rag-finetuned-lm-answer
  poetry run python rag_finetuned_lm_only.py %2
  GOTO end

:rag-finetuned-both-answer
  poetry run python rag_finetuned_embed_and_lm.py %2
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
