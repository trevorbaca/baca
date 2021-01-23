#!/usr/bin/env python
import sys

import setuptools

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================

This version of the Bača API requires Python {}.{}, but you're trying to
install it on Python {}.{}.

This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:

    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install baca

This will install the latest version of the Bača API which works on your
version of Python.
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)

install_requires = [
    "abjad",
    "mypy",
    "roman",
    "sphinx",
    "sphinx-rtd-theme",
    "uqbar>=0.2.13",
]

keywords = [
    "abjad",
    "music composition",
    "music notation",
    "lilypond",
]

if __name__ == "__main__":
    setuptools.setup(
        author="Trevor Bača",
        author_email="trevor.baca@gmail.com",
        description="Trevor Bača's Abjad library.",
        install_requires=install_requires,
        keywords=", ".join(keywords),
        license="MIT",
        name="baca",
        packages=["baca"],
        platforms="Any",
        url="https://github.com/trevorbaca/baca",
        version="3.2",
    )
