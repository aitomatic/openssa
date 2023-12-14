# Configuration file for the Sphinx documentation builder.

# For the full list of built-in configuration values, see the documentation:
# sphinx-doc.org/en/master/usage/configuration.html


from collections.abc import Sequence


# pylint: disable=invalid-name


# Project information
# sphinx-doc.org/en/master/usage/configuration.html#project-information
# ---------------------------------------------------------------------

project = 'OpenSSA'
copyright = '2023, Aitomatic, Inc.'  # pylint: disable=redefined-builtin
author = 'Aitomatic, Inc.'
release = '0.23.12.12'


# General configuration
# sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# -----------------------------------------------------------------------

extensions: Sequence[str] = [
    'myst_parser',  # parse Markdown
    'sphinx.ext.autodoc',  # include documentation from docstrings
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# Options for HTML output
# sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# -------------------------------------------------------------------------

html_theme = 'press'  # sphinx-themes.org
html_static_path = ['_static']


# Markdown Sources
# sphinx-doc.org/en/master/usage/markdown.html
# --------------------------------------------

source_suffix = {'.md': 'markdown', '.rst': 'restructuredtext'}
