# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'geojson'
copyright = '2024, Sean Gillies, Matthew Russell, Corey Farwell, Blake Grotewold, \
	Zsolt Ero, Sergey Romaov, Ray Riga'
author = 'Sean Gillies, Matthew Russell, Corey Farwell, Blake Grotewold, Zsolt Ero, \
	Sergey Romaov, Ray Riga'
release = '3.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_path = ['_theme']
html_static_path = ['_static']
