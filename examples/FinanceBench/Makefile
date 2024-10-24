dana-solve:
	@poetry run python dana.py ${id}

dana-solve-w-knowledge:
	@poetry run python dana.py ${id} --knowledge

dana-solve-w-prog-store:
	@poetry run python dana.py ${id} --prog-store

dana-solve-w-knowledge-and-prog-store:
	@poetry run python dana.py ${id} --knowledge --prog-store

dana-solve-w-llama:
	@poetry run python dana.py ${id} --llama

dana-solve-w-knowledge-w-llama:
	@poetry run python dana.py ${id} --knowledge --llama

dana-solve-w-prog-store-w-llama:
	@poetry run python dana.py ${id} --prog-store --llama

dana-solve-w-knowledge-and-prog-store-w-llama:
	@poetry run python dana.py ${id} --knowledge --prog-store --llama

dana-solve-all-combos:
	@poetry run python dana.py ${id}
	@poetry run python dana.py ${id} --knowledge
	@poetry run python dana.py ${id} --prog-store
	@poetry run python dana.py ${id} --knowledge --prog-store
	@poetry run python dana.py ${id} --llama
	@poetry run python dana.py ${id} --knowledge --llama
	@poetry run python dana.py ${id} --prog-store --llama
	@poetry run python dana.py ${id} --knowledge --prog-store --llama


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
