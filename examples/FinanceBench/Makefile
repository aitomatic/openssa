get-doc:
	@poetry run python data.py ${name}


htp-auto-static-oodar-solve:
	@poetry run python htp_oodar_agent.py ${id}

htp-auto-dynamic-oodar-solve:
	@poetry run python htp_oodar_agent.py ${id} --dynamic-exec

htp-expert-static-oodar-solve:
	@poetry run python htp_oodar_agent.py ${id} --expert-plan

htp-expert-dynamic-oodar-solve:
	@poetry run python htp_oodar_agent.py ${id} --expert-plan --dynamic-exec

htp-auto-static-oodar-w-knowledge-solve:
	@poetry run python htp_oodar_agent.py ${id} --knowledge

htp-auto-dynamic-oodar-w-knowledge-solve:
	@poetry run python htp_oodar_agent.py ${id} --knowledge --dynamic-exec

htp-expert-static-oodar-w-knowledge-solve:
	@poetry run python htp_oodar_agent.py ${id} --knowledge --expert-plan

htp-expert-dynamic-oodar-w-knowledge-solve:
	@poetry run python htp_oodar_agent.py ${id} --knowledge --expert-plan --dynamic-exec


ooda-solve:
	@poetry run python ooda.py ${id}


rag-default-answer:
	@poetry run python rag-default.py ${id}

rag-finetuned-embed-answer:
	@poetry run python rag-finetuned-embed-only.py ${id}

rag-finetuned-lm-answer:
	@poetry run python rag-finetuned-lm-only.py ${id}

rag-finetuned-both-answer:
	@poetry run python rag-finetuned-embed-and-lm.py ${id}

rag-gpt4-lm-answer:
	@poetry run python rag-gpt4-lm.py ${id}


ssm-discuss:
	@poetry run python ssm.py ${id}

streamlit-run:
	@poetry run streamlit run streamlit-main.py --server.allowRunOnSave=true --server.runOnSave=true
