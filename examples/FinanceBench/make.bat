@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="get-doc" GOTO get-doc

IF "%TARGET%"=="agent-solve" GOTO agent-solve
IF "%TARGET%"=="agent-solve-w-prog-space" GOTO agent-solve-w-prog-space
IF "%TARGET%"=="agent-solve-w-knowledge" GOTO agent-solve-w-knowledge
IF "%TARGET%"=="agent-solve-w-knowledge-and-prog-space" GOTO agent-solve-w-knowledge-and-prog-space

IF "%TARGET%"=="ooda-solve" GOTO ooda-solve

IF "%TARGET%"=="rag-default-answer" GOTO rag-default-answer
IF "%TARGET%"=="rag-test" GOTO rag-test
IF "%TARGET%"=="rag-test-gpt4o" GOTO rag-test-gpt4o

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
:agent-solve
  poetry run python htp_oodar_agent.py %2
  GOTO end

:agent-solve-w-knowledge
  poetry run python htp_oodar_agent.py %2 --knowledge
  GOTO end

:agent-solve-w-prog-space
  poetry run python htp_oodar_agent.py %2 --prog-space
  GOTO end

:agent-solve-w-knowledge-and-prog-space
  poetry run python htp_oodar_agent.py %2 --knowledge --prog-space
  GOTO end


:ooda-solve
  poetry run python ooda.py %2
  GOTO end


:rag-default-answer
  poetry run python rag_default.py %2
  GOTO end

:rag-test
  poetry run python rag-test.py %2
  GOTO end

:rag-test-gpt4o
  poetry run python rag-test.py %2 --gpt4o
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
