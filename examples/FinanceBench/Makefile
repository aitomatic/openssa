rag-default-answer:
	@poetry run python rag_default.py ${id}

rag-finetuned-embed-answer:
	@poetry run python rag_finetuned_embed_only.py ${id}

rag-finetuned-lm-answer:
	@poetry run python rag_finetuned_lm_only.py ${id}

rag-finetuned-both-answer:
	@poetry run python rag_finetuned_embed_and_lm.py ${id}

ooda-solve:
	@poetry run python ooda.py ${id}

streamlit-run:
	@poetry run streamlit run streamlit-main.py --server.allowRunOnSave=true --server.runOnSave=true
