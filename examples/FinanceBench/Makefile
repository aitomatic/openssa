agent-solve:
	@poetry run python htp_oodar_agent.py ${id}

agent-solve-w-knowledge:
	@poetry run python htp_oodar_agent.py ${id} --knowledge

agent-solve-w-prog-store:
	@poetry run python htp_oodar_agent.py ${id} --prog-store

agent-solve-w-knowledge-and-prog-store:
	@poetry run python htp_oodar_agent.py ${id} --knowledge --prog-store

agent-solve-w-llama3:
	@poetry run python htp_oodar_agent.py ${id} --llama3

agent-solve-w-knowledge-w-llama3:
	@poetry run python htp_oodar_agent.py ${id} --knowledge --llama3

agent-solve-w-prog-store-w-llama3:
	@poetry run python htp_oodar_agent.py ${id} --prog-store --llama3

agent-solve-w-knowledge-and-prog-store-w-llama3:
	@poetry run python htp_oodar_agent.py ${id} --knowledge --prog-store --llama3

agent-solve-all-combos:
	@poetry run python htp_oodar_agent.py ${id}
	@poetry run python htp_oodar_agent.py ${id} --knowledge
	@poetry run python htp_oodar_agent.py ${id} --prog-store
	@poetry run python htp_oodar_agent.py ${id} --knowledge --prog-store
	@poetry run python htp_oodar_agent.py ${id} --llama3
	@poetry run python htp_oodar_agent.py ${id} --knowledge --llama3
	@poetry run python htp_oodar_agent.py ${id} --prog-store --llama3
	@poetry run python htp_oodar_agent.py ${id} --knowledge --prog-store --llama3


langchain-react-solve:
	@poetry run python langchain_react.py ${id}

openai-assist:
	@poetry run python openai_assist.py ${id}


rag-default-answer:
	@poetry run python rag.py ${id}

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
