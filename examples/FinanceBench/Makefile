run-streamlit:
	@streamlit run streamlit-main.py --server.allowRunOnSave=true --server.runOnSave=true

default-rag-answer:
	@poetry run python rag_default.py ${id}

finetuned-rag-answer:
	@poetry run python rag_finetuned.py ${id}

ooda-ssa-solve:
	@poetry run python ooda_ssa.py ${id}
