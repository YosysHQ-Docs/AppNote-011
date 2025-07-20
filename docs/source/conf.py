#!/usr/bin/env python3
project = 'YosysHQ AppNote-011'
author = 'YosysHQ GmbH'
copyright ='2025 YosysHQ GmbH'

# select HTML theme
html_theme = "furo-ys"
html_css_files = ['custom.css']
html_theme_options: dict[str] = {
    "source_repository": "https://github.com/YosysHQ-Docs/AppNote-011/",
    "source_branch": "main",
    "source_directory": "docs/source/",
}

# These folders are copied to the documentation's HTML output
html_static_path = ['_static']

extensions = ['sphinx.ext.autosectionlabel']

# referencing across different docs
extensions += ['sphinx.ext.intersphinx']
intersphinx_mapping = {
    'base': ('https://yosyshq.readthedocs.io/en/latest', None),
    'yosys': ('https://yosyshq.readthedocs.io/projects/yosys/en/latest', None),
    'sby': ('https://yosyshq.readthedocs.io/projects/sby/en/latest', None),
}
