@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="get-doc" GOTO get-doc

IF "%TARGET%"=="htp-auto-static-oodar-solve" GOTO htp-auto-static-oodar-solve
IF "%TARGET%"=="htp-auto-dynamic-oodar-solve" GOTO htp-auto-dynamic-oodar-solve
IF "%TARGET%"=="htp-expert-static-oodar-solve" GOTO htp-expert-static-oodar-solve
IF "%TARGET%"=="htp-expert-dynamic-oodar-solve" GOTO htp-expert-dynamic-oodar-solve
IF "%TARGET%"=="htp-auto-static-oodar-w-knowledge-solve" GOTO htp-auto-static-oodar-w-knowledge-solve
IF "%TARGET%"=="htp-auto-dynamic-oodar-w-knowledge-solve" GOTO htp-auto-dynamic-oodar-w-knowledge-solve
IF "%TARGET%"=="htp-expert-static-oodar-w-knowledge-solve" GOTO htp-expert-static-oodar-w-knowledge-solve
IF "%TARGET%"=="htp-expert-dynamic-oodar-w-knowledge-solve" GOTO htp-expert-dynamic-oodar-w-knowledge-solve

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
:htp-auto-static-oodar-solve
  poetry run python htp_oodar_agent.py %2
  GOTO end

:htp-auto-dynamic-oodar-solve
  poetry run python htp_oodar_agent.py %2 --dynamic-exec
  GOTO end

:htp-expert-static-oodar-solve
  poetry run python htp_oodar_agent.py %2 --expert-plan
  GOTO end

:htp-expert-dynamic-oodar-solve
  poetry run python htp_oodar_agent.py %2 --expert-plan --dynamic-exec
  GOTO end

:htp-auto-static-oodar-w-knowledge-solve
  poetry run python htp_oodar_agent.py %2 --knowledge
  GOTO end

:htp-auto-dynamic-oodar-w-knowledge-solve
  poetry run python htp_oodar_agent.py %2 --knowledge --dynamic-exec
  GOTO end

:htp-expert-static-oodar-w-knowledge-solve
  poetry run python htp_oodar_agent.py %2 --knowledge --expert-plan
  GOTO end

:htp-expert-dynamic-oodar-w-knowledge-solve
  poetry run python htp_oodar_agent.py %2 --knowledge --expert-plan --dynamic-exec
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
