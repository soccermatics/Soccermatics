# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sphinx_gallery
from sphinx_gallery.sorting import ExplicitOrder
from sphinx_gallery.sorting import ExampleTitleSortKey

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Soccermatics'
copyright = '2022, David Sumpter (code and text), Aleksander Andrzejewski (code)'
author = 'David Sumpter and Aleksander Andrzejewski'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.mathjax',
              'sphinx_gallery.gen_gallery',
              'sphinxcontrib.youtube',
              'myst_parser'
              ]

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

# sphinx gallery

sphinx_gallery_conf = {
    'examples_dirs': ['../lessons'],
    'gallery_dirs': ['gallery'],
	'image_scrapers': ('matplotlib'),
    'matplotlib_animations': True,
	'within_subsection_order': ExampleTitleSortKey,
    'subsection_order': ExplicitOrder(['../lessons/gettingstarted',
                                       '../lessons/lesson1',
                                       '../lessons/lesson2',
                                       '../lessons/lesson3',
                                       '../lessons/lesson4',
                                       '../lessons/lesson5',
                                       '../lessons/lesson6',
                                       '../lessons/lesson7',
                                       '../lessons/lesson8',
                                       '../lessons/lesson9',
                                       '../lessons/lesson10'
                                       ])}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# add logo
html_logo = "images/SoccermaticsLogo.png"
html_theme_options = {'logo_only': True,
                      'display_version': False}

# Options for Markdown  -------------------------------------------------
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "linkify",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist"
]