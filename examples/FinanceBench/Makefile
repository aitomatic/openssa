agent-solve:
	@poetry run python htp_oodar_agent.py ${id}

agent-solve-w-knowledge:
	@poetry run python htp_oodar_agent.py ${id} --knowledge

agent-solve-w-prog-space:
	@poetry run python htp_oodar_agent.py ${id} --prog-space

agent-solve-w-knowledge-and-prog-space:
	@poetry run python htp_oodar_agent.py ${id} --knowledge --prog-space

agent-solve-all-combos:
	@poetry run python htp_oodar_agent.py ${id}
	@poetry run python htp_oodar_agent.py ${id} --knowledge
	@poetry run python htp_oodar_agent.py ${id} --prog-space
	@poetry run python htp_oodar_agent.py ${id} --knowledge --prog-space


openai-assist:
	@poetry run python openai_assist.py ${id}


rag-default-answer:
	@poetry run python rag_default.py ${id}

rag-test:
	@poetry run python rag-test.py ${doc}

rag-test-gpt4o:
	@poetry run python rag-test.py ${doc} --gpt4o


eval:
	@poetry run python eval.py ${output}

eval-no-refresh:
	@poetry run python eval.py ${output} --no-refresh

eval-test:
	@poetry run python eval.py answer --no-human-eval


streamlit-run:
	@poetry run streamlit run streamlit-main.py --server.allowRunOnSave=true --server.runOnSave=true
