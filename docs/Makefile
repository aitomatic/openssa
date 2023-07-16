


build: index
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

index:
	@echo ... Generating our index.md from ../README.md
	sed -e 's/(docs\//(/g' ../README.md > index.md
