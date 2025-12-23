# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
from pathlib import Path
import os
sys.path.append(Path(os.path.join(Path(os.getcwd()).parent, "HTMS_Amber")).as_posix())


project_root = Path(__file__).resolve().parent.parent.parent 
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f"Sphinx DEBUG: Added project root '{project_root}' to sys.path.")
else:
    print(f"Sphinx DEBUG: Project root '{project_root}' already in sys.path.")



project = 'HTMS in Amber'
copyright = '2025, Fergus Place'
author = 'Fergus Place'
release = '0.1.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # For Google/NumPy style docstrings
    'sphinx.ext.viewcode', # To link to source code
    'sphinx.ext.autosummary', # For generating summary tables
    'sphinx_mdinclude',
    'myst_parser',
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',
]
#mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
#new for md as landing
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
master_doc = 'index'
myst_enable_extensions = [
    "amsmath",
    "dollarmath",
]
mathjax3_config = {
    "tex": {
        "inlineMath": [["\\(", "\\)"], ["$", "$"]],
        "displayMath": [["\\[", "\\]"], ["$$", "$$"]],
        "processEscapes": True,
        "packages": {'[+]': ['ams', 'color', 'physics', 'cancel', 'extpfeil', 'mhchem', 'ams', 'braket', 'unicode']}, # You can add more packages here if needed for specific LaTeX commands
    },
}

templates_path = ['_templates']
#exclude_patterns = ['old_index.rst']
exclude_patterns = ['old_index.md', "old_index copy.rst"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_baseurl = 'https://fergplace.github.io/HTMS_Amber/'
html_theme = 'alabaster'
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]
autosummary_generate = True