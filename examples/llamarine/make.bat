@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="agent-solve" GOTO agent-solve

IF "%TARGET%"=="streamlit-run" GOTO streamlit-run


:: STREAMLIT APP
:: =============
:streamlit-run
  poetry run streamlit run app.py --server.allowRunOnSave=true --server.runOnSave=true
  GOTO end


:: END
:: ===
:end
