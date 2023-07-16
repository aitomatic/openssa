


build:
	@echo ... Generating API navigation
	python api_nav.py
	@echo ... Building docs
	cd .. && mkdocs build

serve:
	cd .. && mkdocs serve

deploy: build
	cd .. && mkdocs gh-deploy

install-mkdocs:
	pip install mkdocs
	pip install mkdocstrings
	pip install 'mkdocstrings[python]'
	pip install 'mkdocstrings[crystal]'
	pip install mkdocs-material
	pip install mkdocs-windmill
	pip install mkdocs-custommill
