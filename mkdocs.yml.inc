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
  version: v0.1.3
  article_nav_top: true
  article_nav_bottom: true
  history_buttons: true

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          setup_commands:
            - import os
            - import sys
            - sys.path.append('openssm')
            - sys.path.insert(0, os.path.abspath('.'))
            - print(sys.path)
          options:
            show_source: False
nav:
  - Home: README.md
  - Getting Started: docs.shared/GETTING_STARTED.md
  - Developer Guide:
    - Design Principles: DESIGN_PRINCIPLES.md
    - Using Makefile: docs.shared/MAKEFILE.md
  - Community:
    - Contributing: docs.shared/community/CONTRIBUTING.md
    - Project Philosophy: PROJECT_PHILOSOPHY.md
    - Code of Conduct: docs.shared/community/CODE_OF_CONDUCT.md
    - Support:
      - Support: support/README.md 
      - FAQ: support/FAQ/README.md
      - Troubleshoot: support/troubleshooting_guides/README.md
  - See Also:
    - Diagrams: docs.shared/diagrams/README.md
    - License: docs.shared/LICENSE.md
  - API Reference:
