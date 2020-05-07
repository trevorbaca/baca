Toolchain updates
=================

OBJECTIVE: Upgrade all applications in Abjad toolchain to latest versions.

See python-upgrade.md for Python.

Applications covered in this document:

    * pip
    * pytest
    * mypy
    * black
    * Sphinx

Check for new versions of LilyPond at www.lilypond.org.

Check for new versions of Python at www.python.org.

Check for new versions of MacOS under Apple menu > System Preferences > Software Update.

1.  Run all tests and build all APIs.

        cdj .. !py.test -rf

        cdr .. .. !py.test -rf

        cdb .. !py.test -rf

        cdi .. tests !py.test -rf

        cds ^^

    Run checkers and beautifiers on all repos:

        cdj ..
        !make black-check
        !make flake8
        !make isort
        !make mypy
        (rerun tests if anything changes)

        cdr .. ..
        !make black-check
        !make flake8
        !make isort
        !make mypy
        (rerun tests if anything changes)

        cdb ..
        !make black-check
        !make flake8
        !make isort
        !make mypy
        (rerun tests if anything changes)


        cdi ..
        !make black-check
        !make flake8
        !make isort
        !make mypy
        (rerun tests if anything changes)

    TODO: also run mypy and black on all repos.

        apim

        apib

        apii

        apis

2.  Inspect applications:

        (abjad3) ~$ lilypond --version
        GNU LilyPond 2.19.84

        (abjad3) ~$ python --version
        Python 3.7.4

        (abjad3) ~$ pip --version
        pip 20.0.2 from ...

        (abjad3) ~$ pytest --version
        This is pytest version 5.3.2, imported from ...
        pytest-helpers-namespace-2019.1.8 at ...
        pytest-cov-2.7.1 at ...

        (abjad3) ~$ mypy --version
        mypy 0.770

        (abjad3) ~$ black --version
        black, version 19.10b0

        (abjad3) ~$ sphinx-build --version
        sphinx-build 2.3.0

3.  Update applications:

        (abjad3) ~$ pip install --upgrade pip

        (abjad3) ~$ pip install --upgrade pytest

        (abjad3) ~$ pip install --upgrade mypy

        (abjad3) ~$ pip install --upgrade black
        black, version 19.10b0

        (abjad3) ~$ pip install --upgrade sphinx

4.  Run all tests and build all APIs.

        cdj .. !py.test -rf

        cdi .. !py.test -rf

        cdb .. !py.test -rf

        cdr .. !py.test -rf

        cds ^^

    TODO: also run mypy and black on all repos.

        apii

        apis

        apib

        apij (?)
