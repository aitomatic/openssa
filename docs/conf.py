# Configuration file for the Sphinx documentation builder.

# For the full list of built-in configuration values, see the documentation:
# sphinx-doc.org/en/master/usage/configuration.html


from collections.abc import Sequence
from datetime import date
from pathlib import Path
import tomllib


# Project information
# sphinx-doc.org/en/master/usage/configuration.html#project-information
# ---------------------------------------------------------------------

with open(file=Path(__file__).parent.parent / 'pyproject.toml', mode='rb') as f:
    pkg_meta: dict[str, str] = tomllib.load(f)['tool']['poetry']

project: str = pkg_meta['name']
author: str = pkg_meta['authors'][0]
copyright: str = f'{date.today().year}, {author}'  # pylint: disable=redefined-builtin
release: str = pkg_meta['version']


# General configuration
# sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# -----------------------------------------------------------------------

extensions: Sequence[str] = [
    'myst_parser',  # parse Markdown
    'sphinx.ext.autodoc',  # include documentation from docstrings
]

templates_path: Sequence[str] = ['_templates']
exclude_patterns: Sequence[str] = ['_build', 'Thumbs.db', '.DS_Store']


# Options for HTML output
# sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# -------------------------------------------------------------------------

html_theme: str = 'press'  # sphinx-themes.org
html_static_path: Sequence[str] = ['_static']


# Markdown Sources
# sphinx-doc.org/en/master/usage/markdown.html
# --------------------------------------------

source_suffix: dict[str, str] = {'.md': 'markdown', '.rst': 'restructuredtext'}
