# see: https://www.sphinx-doc.org/en/master/usage/configuration.html

project = 'django-disguise'
copyright = '2020, Mikhail Porokhovnichenko'
author = 'Mikhail Porokhovnichenko'

# The full version, including alpha/beta/rc tags
release = '1.0.0'
pygments_style = 'sphinx'

extensions = []
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

master_doc = 'index'
html_theme = 'alabaster'
html_static_path = ['_static']
