dana-solve:
	@poetry run python dana.py ${id}

dana-solve-w-knowledge:
	@poetry run python dana.py ${id} --knowledge

dana-solve-w-prog-store:
	@poetry run python dana.py ${id} --prog-store

dana-solve-w-knowledge-and-prog-store:
	@poetry run python dana.py ${id} --knowledge --prog-store

dana-solve-w-llama3:
	@poetry run python dana.py ${id} --llama3

dana-solve-w-knowledge-w-llama3:
	@poetry run python dana.py ${id} --knowledge --llama3

dana-solve-w-prog-store-w-llama3:
	@poetry run python dana.py ${id} --prog-store --llama3

dana-solve-w-knowledge-and-prog-store-w-llama3:
	@poetry run python dana.py ${id} --knowledge --prog-store --llama3

dana-solve-all-combos:
	@poetry run python dana.py ${id}
	@poetry run python dana.py ${id} --knowledge
	@poetry run python dana.py ${id} --prog-store
	@poetry run python dana.py ${id} --knowledge --prog-store
	@poetry run python dana.py ${id} --llama3
	@poetry run python dana.py ${id} --knowledge --llama3
	@poetry run python dana.py ${id} --prog-store --llama3
	@poetry run python dana.py ${id} --knowledge --prog-store --llama3
