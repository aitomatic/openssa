PROJECT_DIR := $(shell cd .. && pwd)
OPENSSM_DIR=$(PROJECT_DIR)/openssm
INIT_PY=$(OPENSSM_DIR)/__init__.py
TMP_INIT_PY=$(OPENSSM_DIR)/__tmp__init__.py
DOCS_DIR=$(PROJECT_DIR)/docs
SITE_DIR=$(PROJECT_DIR)/site
VERSION := $(shell cd $(OPENSSM_DIR) && cat VERSION)

#MKDOCS=mkdocs -v
MKDOCS=mkdocs
PYTHONPATH=$(PROJECT_DIR):$(OPENSSM_DIR)

# Colorized output
ANSI_NORMAL="\033[0m"
ANSI_RED="\033[0;31m"
ANSI_GREEN="\033[0;32m"
ANSI_YELLOW="\033[0;33m"
ANSI_BLUE="\033[0;34m"
ANSI_MAGENTA="\033[0;35m"
ANSI_CYAN="\033[0;36m"
ANSI_WHITE="\033[0;37m"


PYTHONPATH=$(PROJECT_DIR):$(OPENSSM_DIR)


build:
	@echo $(ANSI_YELLOW) $(PYTHONPATH)
	@echo $(ANSI_GREEN) ... Generating API navigation $(ANSI_NORMAL)
	python api_nav.py
	@echo $(ANSI_GREEN) ... Building docs $(ANSI_NORMAL)
	# @make move-files
	@make copy-files
	cd .. && $(MKDOCS) build
	# @make unmove-files

serve:
	@# cd .. && $(MKDOCS) serve
	# cd $(SITE_DIR) && python3 -m http.server 8000
	cd $(SITE_DIR) && mike serve

deploy: build
	#cd .. && $(MKDOCS) gh-deploy
	# cd .. && ghp-import -p $(SITE_DIR)
	cd .. && mike deploy $(VERSION) latest --deploy-prefix $(VERSION)

install-mkdocs:
	pip install mkdocs
	pip install mkdocstrings
	pip install 'mkdocstrings[python]'
	pip install 'mkdocstrings[crystal]'
	pip install mkdocs-material
	pip install mkdocs-windmill
	pip install mkdocs-custommill

index-unused:
	@# sed -e 's/docs\///g' ../README.md > index.md
	@# sed -e 's#\(\.\./\)*docs/##g' ../README.md > index.md
	sed -e 's#\(\.\./\)*docs/#/#g' ../README.md > index.md

copy-files:
	#
	# Copying known files
	#
	@echo $(ANSI_GREEN) ... Generating our index.md from ../README.md $(ANSI_NORMAL)
	sed -e 's#\(\.\./\)*docs/#/#g' ../README.md > index.md
	@echo $(ANSI_GREEN) ... Working on other files $(ANSI_NORMAL)
	FILE=openssm/integrations/llama_index/README.md ;\
	sed -e 's#\.\./\(\.\./\)*docs/#/#g' $(PROJECT_DIR)/$$FILE > $(DOCS_DIR)/$$FILE

move-files:
	#
	# __init__.py is giving us some undocumented issue. Move it out of the way first...
	#
	@-mv $(INIT_PY) $(TMP_INIT_PY)


unmove-files:
	#
	# ... then move __init__.py back in its place
	#
	@-mv $(TMP_INIT_PY) $(INIT_PY)
