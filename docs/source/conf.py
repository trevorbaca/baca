import os
import sys

sys.path.insert(0, os.path.abspath("../../source"))

autodoc_member_order = "groupwise"

copyright = "1997-2025, Trevor Bača."

extensions = [
    "abjad.ext.sphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_toggleprompt",
    "uqbar.sphinx.api",
    "uqbar.sphinx.book",
    "uqbar.sphinx.inheritance",
    "uqbar.sphinx.style",
]

graphviz_dot_args = ["-s32"]
graphviz_output_format = "svg"

html_last_updated_fmt = "%b %d, %Y"
html_show_sphinx = False
html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 1,
    "sticky_navigation": False,
    "style_external_links": True,
    "style_nav_header_background": "#996633",
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("http://www.sphinx-doc.org/en/master/", None),
}

project = "Bača"
pygments_style = "sphinx"

smartquotes = True

templates_path = ["_templates"]
todo_include_todos = True

uqbar_api_member_documenter_classes = [
    "uqbar.apis.FunctionDocumenter",
    "uqbar.apis.SummarizingClassDocumenter",
]
uqbar_api_module_documenter_class = "uqbar.apis.SummarizingModuleDocumenter"
uqbar_api_omit_inheritance_diagrams = True
uqbar_api_root_documenter_class = "uqbar.apis.SummarizingRootDocumenter"
uqbar_api_source_paths = ["baca"]
uqbar_api_title = "Bača API"
uqbar_book_console_setup = [
    "import abjad",
    "import baca",
    "import rmakers",
]
uqbar_book_console_teardown = []
uqbar_book_extensions = [
    "abjad.ext.sphinx.LilyPondExtension",
]
uqbar_book_strict = False
uqbar_book_use_black = True
uqbar_book_use_cache = True

version = "3.25"
