import sphinx_rtd_theme
from pygments.formatters.latex import LatexFormatter
from sphinx.highlighting import PygmentsBridge


class CustomLatexFormatter(LatexFormatter):
    def __init__(self, **options):
        super(CustomLatexFormatter, self).__init__(**options)
        self.verboptions = r"""formatcom=\footnotesize"""


PygmentsBridge.latex_formatter = CustomLatexFormatter

### CORE ###

add_function_parentheses = True
copyright = "1997-2021, Trevor Bača"
exclude_patterns = []

extensions = [
    "abjad.ext.sphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "uqbar.sphinx.api",
    "uqbar.sphinx.book",
    "uqbar.sphinx.inheritance",
    "uqbar.sphinx.style",
]

master_doc = "index"
project = "Bača API"
pygments_style = "sphinx"
release = ""
source_suffix = ".rst"
templates_path = ["_templates"]
version = ""

### HTML ###

html_last_updated_fmt = "%b %d, %Y"
html_show_sourcelink = True
html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": True,
    "navigation_depth": -1,
    "sticky_navigation": True,
    "style_external_links": True,
}
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

### HTML HELP ###

htmlhelp_basename = "BačaAPIdoc"

### LATEX ###

latex_elements = {
    "inputenc": r"\usepackage[utf8x]{inputenc}",
    "utf8extra": "",
    "papersize": "letterpaper",
    "pointsize": "10pt",
    "preamble": r"""
    \usepackage{upquote}
    \pdfminorversion=5
    \setcounter{tocdepth}{2}
    \definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
    \definecolor{VerbatimBorderColor}{rgb}{1.0,1.0,1.0}
    \hypersetup{unicode=true}
    """,
}

latex_documents = [("index", "BačaAPI.tex", "Bača API", "Trevor Bača", "manual")]

latex_domain_indices = False

### EXTESNIONS ###

autodoc_member_order = "groupwise"
graphviz_dot_args = ["-s32"]
graphviz_output_format = "svg"
intersphinx_mapping = {
    "http://josiahwolfoberholtzer.com/uqbar/": None,
    "http://www.sphinx-doc.org/en/master/": None,
    "https://docs.python.org/3.7/": None,
}
todo_include_todos = True

uqbar_api_title = "Bača API"
uqbar_api_source_paths = ["baca"]
uqbar_api_root_documenter_class = "uqbar.apis.SummarizingRootDocumenter"
uqbar_api_module_documenter_class = "uqbar.apis.SummarizingModuleDocumenter"
uqbar_api_member_documenter_classes = [
    "uqbar.apis.FunctionDocumenter",
    "uqbar.apis.SummarizingClassDocumenter",
]

uqbar_book_console_setup = [
    "import abjad",
    "import baca",
    "import ide",
    "from abjadext import rmakers",
]
uqbar_book_console_teardown = []
uqbar_book_extensions = [
    "uqbar.book.extensions.GraphExtension",
    "abjad.ext.sphinx.LilyPondExtension",
]
uqbar_book_strict = False
uqbar_book_use_black = True
uqbar_book_use_cache = True
