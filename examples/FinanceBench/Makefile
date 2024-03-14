run-streamlit:
	@streamlit run streamlit-main.py --server.allowRunOnSave=true --server.runOnSave=true

rag-default-answer:
	@poetry run python rag_default.py ${id}

rag-finetuned-answer:
	@poetry run python rag_finetuned.py ${id}

ooda-solve:
	@poetry run python ooda.py ${id}
