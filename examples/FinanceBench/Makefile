agent-solve:
	@poetry run python htp_oodar_agent.py ${id}

agent-solve-w-knowledge:
	@poetry run python htp_oodar_agent.py ${id} --knowledge

agent-solve-w-prog-space:
	@poetry run python htp_oodar_agent.py ${id} --prog-space

agent-solve-w-knowledge-and-prog-space:
	@poetry run python htp_oodar_agent.py ${id} --knowledge --prog-space

agent-all-combo-solve:
	@poetry run python htp_oodar_agent.py ${id}
	@poetry run python htp_oodar_agent.py ${id} --knowledge
	@poetry run python htp_oodar_agent.py ${id} --prog-space
	@poetry run python htp_oodar_agent.py ${id} --knowledge --prog-space


ooda-solve:
	@poetry run python ooda.py ${id}


rag-default-answer:
	@poetry run python rag_default.py ${id}

rag-finetuned-embed-answer:
	@poetry run python rag-finetuned-embed-only.py ${id}

rag-finetuned-lm-answer:
	@poetry run python rag-finetuned-lm-only.py ${id}

rag-finetuned-both-answer:
	@poetry run python rag-finetuned-embed-and-lm.py ${id}

rag-gpt4-lm-answer:
	@poetry run python rag-gpt4-lm.py ${id}

rag-test:
	@poetry run python rag-test.py ${doc}

rag-test-gpt4o:
	@poetry run python rag-test.py ${doc} --gpt4o


ssm-discuss:
	@poetry run python ssm.py ${id}


eval:
	@poetry run python eval.py ${output}

eval-no-refresh:
	@poetry run python eval.py ${output} --no-refresh

eval-test:
	@poetry run python eval.py answer --no-human-eval


streamlit-run:
	@poetry run streamlit run streamlit-main.py --server.allowRunOnSave=true --server.runOnSave=true
