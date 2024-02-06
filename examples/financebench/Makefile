get-poetry:
	@python3 -m pip install Poetry --upgrade --user

install:
	@poetry lock
	@poetry install

run-streamlit:
	@streamlit run streamlit-main.py --server.allowRunOnSave=true --server.runOnSave=true

solve:
	@poetry run python3 ssa_fb/prob_solve.py ${id}
