#import abjad # remove?
import os
import sphinx_rtd_theme
import sys
#from docutils import nodes
from pygments.formatters.latex import LatexFormatter
from sphinx.highlighting import PygmentsBridge


# REMOVE?
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', '..')))

class CustomLatexFormatter(LatexFormatter):
    def __init__(self, **options):
        super(CustomLatexFormatter, self).__init__(**options)
        self.verboptions = r'''formatcom=\footnotesize'''


PygmentsBridge.latex_formatter = CustomLatexFormatter

### CORE ###

add_function_parentheses = True

copyright = u'1997-2018, Trevor Bača'

exclude_patterns = []

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx_autodoc_typehints',
    'uqbar.sphinx.inheritance',
    'uqbar.sphinx.style',
    'abjad.docs.ext.abjadbook',
    ]

master_doc = 'index'

project = u'Bača API'

pygments_style = 'sphinx'

release = ''

source_suffix = '.rst'

templates_path = ['_templates']

version = ''

# REMOVE?
#doctest_path = [
#    os.path.abspath(abjad.__path__[0]),
#    ]
#
#doctest_global_setup = r'''
#from __future__ import print_function
#import abjad
#import baca
#'''
#
#doctest_global_cleanup = r'''
#for server in servertools.Server._servers.values():
#    server.quit()
#'''
#
#nodes.doctest_block = nodes.literal_block

### HTML ###

html_theme = 'default'

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']

### HTML HELP ###

htmlhelp_basename = 'BačaAPIdoc'

### LATEX ###

latex_elements = {
    'inputenc': r'\usepackage[utf8x]{inputenc}',
    'utf8extra': '',
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': r'''
    \usepackage{upquote}
    \pdfminorversion=5
    \setcounter{tocdepth}{2}
    \definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
    \definecolor{VerbatimBorderColor}{rgb}{1.0,1.0,1.0}
    \hypersetup{unicode=true}
    ''',
    }

latex_documents = [
    (
        'index',
        u'BačaAPI.tex',
        u'Bača API',
        u'Trevor Bača',
        'manual',
        ),
    ]

#latex_use_parts = True

latex_domain_indices = False

### MAN ###

man_pages = [
    (
        'index',
        u'BačaAPI',
        u'Bača API',
        [u'Trevor Bača'],
        1,
        )
    ]

### TEXINFO ###

texinfo_documents = [
    (
        'index',
        u'BačaAPI',
        u'Bača API',
        u'Trevor Bača',
        u'BačaAPI',
        'One line description of project.',
        'Miscellaneous',
        ),
    ]

### EXTESNIONS ###

abjadbook_ignored_documents = ()
abjadbook_console_module_names = ('baca',)
autodoc_member_order = 'groupwise'
graphviz_dot_args = ['-s32']
graphviz_output_format = 'svg'
intersphinx_mapping = {
    'abjad': ('http://abjad.mbrsi.org', None),
    'python': ('http://docs.python.org/3.2', None),
    }
#todo_include_todos = True

uqbar_api_title = u'Bača API'
uqbar_api_source_paths = ['baca']
uqbar_api_root_documenter_class = 'uqbar.apis.SummarizingRootDocumenter'
uqbar_api_module_documenter_class = 'uqbar.apis.SummarizingModuleDocumenter'
uqbar_api_member_documenter_classes = [
    'uqbar.apis.FunctionDocumenter',
    'uqbar.apis.SummarizingClassDocumenter',
    ]
