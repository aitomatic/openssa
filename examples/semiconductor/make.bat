@echo off


:: TARGETS
:: =======
SET TARGET=%1

IF "%TARGET%"=="agent-solve" GOTO agent-solve

IF "%TARGET%"=="semikong-answer" GOTO semikong-answer

IF "%TARGET%"=="streamlit-run" GOTO streamlit-run


:: INFERENCING
:: ===========
:agent-solve
  poetry run python htp_oodar_agent.py %2
  GOTO end

:semikong-answer
  poetry run python semikong_lm.py %2
  GOTO end


:: STREAMLIT APP
:: =============
:streamlit-run
  poetry run streamlit run streamlit-main.py --server.allowRunOnSave=true --server.runOnSave=true
  GOTO end


:: END
:: ===
:end
