site_name: OpenSSM Documentation

theme: windmill
#theme: material
#theme:
#  name: readthedocs
#  navigation_depth: 5
#  collapse_navigation: True
#  sticky_navigation: True

extra:
#  logo: path
  version: v0.1.6
  article_nav_top: true
  article_nav_bottom: true
  history_buttons: true

extra_css:
    - mkdocs.css
    - https://fonts.googleapis.com/css?family=Sofia
    - https://fonts.googleapis.com/css?family=Oswald
    - https://fonts.googleapis.com/css?family=Open+Sans

plugins:
  - search
  - mike:
      # These fields are all optional; the defaults are as below...
      alias_type: symlink
      redirect_template: null
      deploy_prefix: ''
      canonical_version: null
      version_selector: true
      css_dir: css
      javascript_dir: js
  - mkdocstrings:
      handlers:
        python:
          paths: [/Users/ctn/src/aitomatic/ssm]
          setup_commands:
            - import os
            - import sys
            - sys.path.append('openssm')
            - sys.path.insert(0, os.path.abspath('.'))
            - print(f"sys.path is {sys.pat}")
          options:
            show_source: True
nav:
  - Home: index.md
  - Getting Started: GETTING_STARTED.md
  - Developer Guide:
    - Design Principles: dev/design_principles.md
    - Using Makefile: dev/makefile_info.md
    - Other HowTos: dev/howtos.md
  - Integrations:
    - LlamaIndex: openssm/integrations/llama_index/README.md
    - Vectara: integrations/vectara.md
    - Lepton.AI: integrations/lepton_ai.md
  - Community:
    - Contributing: community/CONTRIBUTING.md
    - Project Philosophy: PROJECT_PHILOSOPHY.md
    - Code of Conduct: community/CODE_OF_CONDUCT.md
    - Support:
      - Support: support/README.md 
      - FAQ: support/FAQ/README.md
      - Troubleshoot: support/troubleshooting_guides/README.md
  - See Also:
    - Diagrams: diagrams/README.md
    - License: LICENSE.md
  - API Reference:
