@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="dana-solve" GOTO dana-solve
IF "%TARGET%"=="dana-solve-w-prog-store" GOTO dana-solve-w-prog-store
IF "%TARGET%"=="dana-solve-w-knowledge" GOTO dana-solve-w-knowledge
IF "%TARGET%"=="dana-solve-w-knowledge-and-prog-store" GOTO dana-solve-w-knowledge-and-prog-store
IF "%TARGET%"=="dana-solve-w-llama" GOTO dana-solve-w-llama
IF "%TARGET%"=="dana-solve-w-prog-store-w-llama" GOTO dana-solve-w-prog-store-w-llama
IF "%TARGET%"=="dana-solve-w-knowledge-w-llama" GOTO dana-solve-w-knowledge-w-llama
IF "%TARGET%"=="dana-solve-w-knowledge-and-prog-store-w-llama" GOTO dana-solve-w-knowledge-and-prog-store-w-llama
IF "%TARGET%"=="dana-solve-all-combos" GOTO dana-solve-all-combos

IF "%TARGET%"=="langchain-react-solve" GOTO langchain-react-solve
IF "%TARGET%"=="openai-assist" GOTO openai-assist

IF "%TARGET%"=="rag-default-answer" GOTO rag-default-answer
IF "%TARGET%"=="rag-test" GOTO rag-test
IF "%TARGET%"=="rag-test-gpt4o" GOTO rag-test-gpt4o

IF "%TARGET%"=="eval" GOTO eval
IF "%TARGET%"=="eval-no-refresh" GOTO eval-no-refresh
IF "%TARGET%"=="eval-test" GOTO eval-test

IF "%TARGET%"=="streamlit-run" GOTO streamlit-run


:: BATCH INFERENCING
:: =================
:dana-solve
  poetry run python dana.py %2
  GOTO end

:dana-solve-w-knowledge
  poetry run python dana.py %2 --knowledge
  GOTO end

:dana-solve-w-prog-store
  poetry run python dana.py %2 --prog-store
  GOTO end

:dana-solve-w-knowledge-and-prog-store
  poetry run python dana.py %2 --knowledge --prog-store
  GOTO end

:dana-solve-w-llama
  poetry run python dana.py %2 --llama
  GOTO end

:dana-solve-w-knowledge-w-llama
  poetry run python dana.py %2 --knowledge --llama
  GOTO end

:dana-solve-w-prog-store-w-llama
  poetry run python dana.py %2 --prog-store --llama
  GOTO end

:dana-solve-w-knowledge-and-prog-store-w-llama
  poetry run python dana.py %2 --knowledge --prog-store --llama
  GOTO end

:dana-solve-all-combos
  poetry run python dana.py %2
  poetry run python dana.py %2 --knowledge
  poetry run python dana.py %2 --prog-space
  poetry run python dana.py %2 --knowledge --prog-space
  poetry run python dana.py %2 --llama
  poetry run python dana.py %2 --knowledge --llama
  poetry run python dana.py %2 --prog-space --llama
  poetry run python dana.py %2 --knowledge --prog-space --llama
  GOTO end


:langchain-react-solve
  poetry run python langchain_react.py %2
  GOTO end

:openai-assist
  poetry run python openai_assist.py %2
  GOTO end


:rag-default-answer
  poetry run python rag.py %2
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
