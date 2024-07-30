@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="get-doc" GOTO get-doc

IF "%TARGET%"=="htp-oodar-solve" GOTO htp-oodar-solve
IF "%TARGET%"=="htp-oodar-solve-w-prog-space" GOTO htp-oodar-solve-w-prog-space
IF "%TARGET%"=="htp-oodar-solve-w-knowledge" GOTO htp-oodar-solve-w-knowledge
IF "%TARGET%"=="htp-oodar-solve-w-knowledge-and-prog-space" GOTO htp-oodar-solve-w-knowledge-and-prog-space

IF "%TARGET%"=="ooda-solve" GOTO ooda-solve

IF "%TARGET%"=="rag-default-answer" GOTO rag-default-answer
IF "%TARGET%"=="rag-finetuned-embed-answer" GOTO rag-finetuned-embed-answer
IF "%TARGET%"=="rag-finetuned-lm-answer" GOTO rag-finetuned-lm-answer
IF "%TARGET%"=="rag-finetuned-both-answer" GOTO rag-finetuned-both-answer
IF "%TARGET%"=="rag-gpt4-lm-answer" GOTO rag-gpt4-lm-answer
IF "%TARGET%"=="rag-test" GOTO rag-test

IF "%TARGET%"=="ssm-discuss" GOTO ssm-discuss

IF "%TARGET%"=="eval" GOTO eval
IF "%TARGET%"=="eval-no-refresh" GOTO eval-no-refresh
IF "%TARGET%"=="eval-test" GOTO eval-test

IF "%TARGET%"=="streamlit-run" GOTO streamlit-run


:: DATA PROCESSING
:: ===============
:get-doc
  poetry run python data.py %2
  GOTO end


:: BATCH INFERENCING
:: =================
:htp-oodar-solve
  poetry run python htp_oodar_agent.py %2
  GOTO end

:htp-oodar-solve-w-knowledge
  poetry run python htp_oodar_agent.py %2 --knowledge
  GOTO end

:htp-oodar-solve-w-prog-space
  poetry run python htp_oodar_agent.py %2 --prog-space
  GOTO end

:htp-oodar-solve-w-knowledge-and-prog-space
  poetry run python htp_oodar_agent.py %2 --knowledge --prog-space
  GOTO end


:ooda-solve
  poetry run python ooda.py %2
  GOTO end


:rag-default-answer
  poetry run python rag_default.py %2
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

:rag-test
  poetry run python rag-test.py %2
  GOTO end


:ssm-discuss
  poetry run python ssm.py %2
  GOTO end


:: BATCH EVALUATION
:: ================
:eval
  poetry run python eval.py %2
  GOTO end

:eval-no-refresh
  poetry run python eval.py %2 --no-refresh
  GOTO end

:eval-test
  poetry run python eval.py answer --no-human-eval
  GOTO end


:: STREAMLIT APP
:: =============
:streamlit-run
  poetry run streamlit run streamlit-main.py --server.allowRunOnSave=true --server.runOnSave=true
  GOTO end


:: END
:: ===
:end
