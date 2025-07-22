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

# hacked up cmd-ref linking
from sphinx.application import Sphinx
from sphinx.domains import Domain, ObjType
from sphinx.roles import XRefRole

class CommandDomain(Domain):
    name = 'cmd'
    label = 'Yosys commands'

    object_types = {
        'cmd': ObjType('command', 'ref')
    }

    roles = {
        'ref': XRefRole()
    }

    def get_full_qualified_name(self, node):
        """Return full qualified name for a given node"""
        modname = "cmd:def" # ?
        clsname = "DirectiveAdapter" # ‽
        target = node.get('reftarget')
        return '.'.join(filter(None, [modname, clsname, target]))

def setup(app: Sphinx):
    app.add_domain(CommandDomain)
