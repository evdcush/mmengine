# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

from sphinx.util import logging
from sphinx.builders.latex import LaTeXBuilder

logger = logging.getLogger(__name__)

#import pytorch_sphinx_theme
import furo

sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------

project = 'mmengine'
copyright = '2022, mmengine contributors'
author = 'mmengine contributors'

version_file = '../../mmengine/version.py'
with open(version_file) as f:
    exec(compile(f.read(), version_file, 'exec'))
__version__ = locals()['__version__']
# The short X.Y version
version = __version__
# The full version, including alpha/beta/rc tags
release = __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx.ext.autodoc.typehints',
    'sphinx_tabs.tabs',
]  # yapf: disable
autodoc_typehints = 'description'
myst_heading_anchors = 4
myst_enable_extensions = ['colon_fence']

# Configuration for intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'torch': ('https://pytorch.org/docs/stable/', None),
    'mmcv': ('https://mmcv.readthedocs.io/en/2.x/', None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.gif']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'pytorch_sphinx_theme'
#html_theme_path = [pytorch_sphinx_theme.get_html_theme_path()]
html_theme = "furo"

html_theme_options = {
    'menu': [
        {
            'name': 'GitHub',
            'url': 'https://github.com/open-mmlab/mmengine'
        },
    ],
    # Specify the language of shared menu
    'menu_lang': 'en',
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ['css/readthedocs.css']

# -- Extension configuration -------------------------------------------------
# Ignore >>> when copying code
copybutton_prompt_text = r'>>> |\.\.\. '
copybutton_prompt_is_regexp = True


def setup(app):
    LaTeXBuilder.supported_image_types = [
        'image/png', 'image/jpeg', 'application/pdf'
    ]

    def skip_unsupported_images(app, doctree, docname):
        if app.builder.format != 'latex':
            return
        nodes_to_remove = []
        for node in doctree.traverse():
            if node.tagname == 'image':
                if not any(node['uri'].endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.pdf']):
                    logger.warning(f"Skipping unsupported image format in LaTeX build: {node['uri']}")
                    nodes_to_remove.append(node)

        for node in nodes_to_remove:
            node.parent.remove(node)

    app.connect('doctree-resolved', skip_unsupported_images)
