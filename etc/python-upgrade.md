Upgrading Python
================

OBJECTIVE: Upgrade from Python 3.6.5 to 3.7.4 under OSX. Then reestablish
virtual environments afterwards.

1.  Note current virtual environment and version of Python

        (abjad3) ✔ ~/Desktop 
        12:46 $ python --version
        Python 3.6.5

    This means that Python 3.6.5 was used to create the abjad3 virtual
    environment.

2.  Download the new Python installer and install:

        https://www.python.org/downloads/mac-osx/

3.  Double-click the installer and install.

4.  Note that the version of Python powering the abjad3 virtual environment
    has not changed.

        (abjad3) ✔ ~/Desktop 
        12:49 $ python --version
        Python 3.6.5

5.  Note that the version of Python 2 has not changed either:

        12:52 $ deactivate
        ✔ ~/Scores/stirrings/stirrings [master|✔] 

        12:52 $ python --version
        Python 2.7.10
        ✔ ~/Scores/stirrings/stirrings [master|✔] 

6.  Note that the new version (3.7) of Python is hiding in the Python versions
    folder:

        16:09 $ ls /Library/Frameworks/Python.framework/Versions/
        3.5 3.6

7.  Edit ~/.profile. Change ...

        PATH="/Library/Frameworks/Python.framework/Versions/3.6/bin:${PATH}"

    ... to ...

        PATH="/Library/Frameworks/Python.framework/Versions/3.7/bin:${PATH}"

    ... instead.

    Restart the terminal.

8.  Confirm that python3 now points to 3.7:

        16:15 $ python3 --version
        Python 3.7.4

9.  Reestablish the abjad3 virtual environment:

        (abjad3) ✔ ~/Desktop 
        12:54 $ trash ~/.virtualenvs/abjad3/
        Moving '/Users/trevorbaca/.virtualenvs/abjad3/' to '/Users/trevorbaca/.Trash'

        (abjad3) ✔ ~/Desktop 
        12:55 $ deactivate
        ✔ ~/Desktop 

        ✘-1 ~/Desktop 
        12:55 $ mkvirtualenv -p python3 abjad3
        (abjad3) ✔ ~/Desktop 
        Running virtualenv with interpreter /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
        Using base prefix '/Library/Frameworks/Python.framework/Versions/3.7'
        /Library/Python/2.7/site-packages/virtualenv.py:1041: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
        import imp
        New python executable in /Users/trevorbaca/.virtualenvs/abjad3/bin/python3
        Also creating executable in /Users/trevorbaca/.virtualenvs/abjad3/bin/python
        Installing setuptools, pip, wheel...done.
        virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/predeactivate
        virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/postdeactivate
        virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/preactivate
        virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/postactivate
        virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/get_env_details

        12:56 $ python --version
        Python 3.7.4

10. Install mypy:

        pip install mypy
        Collecting mypy
        Downloading https://files.pythonhosted.org/packages/0f/c2/8517d62169d10a8217c424af89389e550217e478a7b4d85119a6abeb8b8e/mypy-0.720-cp37-cp37m-macosx_10_6_x86_64.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl (13.6MB)
            |████████████████████████████████| 13.6MB 6.9MB/s 
        Collecting mypy-extensions<0.5.0,>=0.4.0 (from mypy)
        Using cached https://files.pythonhosted.org/packages/4d/72/8d54e2b296631b9b14961d583e56e90d9d7fba8a240d5ce7f1113cc5e887/mypy_extensions-0.4.1-py2.py3-none-any.whl
        Collecting typed-ast<1.5.0,>=1.4.0 (from mypy)
        Downloading https://files.pythonhosted.org/packages/a0/03/266268b053ad81b8aea17bc3f5e6d3cf074bb4372d229336867a67e17076/typed_ast-1.4.0-cp37-cp37m-macosx_10_9_x86_64.whl (215kB)
            |████████████████████████████████| 225kB 12.8MB/s 
        Collecting typing-extensions>=3.7.4 (from mypy)
        Using cached https://files.pythonhosted.org/packages/27/aa/bd1442cfb0224da1b671ab334d3b0a4302e4161ea916e28904ff9618d471/typing_extensions-3.7.4-py3-none-any.whl
        Installing collected packages: mypy-extensions, typed-ast, typing-extensions, mypy
        Successfully installed mypy-0.720 mypy-extensions-0.4.1 typed-ast-1.4.0 typing-extensions-3.7.4

11. Reinstall Abjad in the newly reestablished virtual environment. Use [test]
    to install pytest:

        (abjad3) ✔ ~/abjad [trevor/dev|✔] 
        13:02 $ pip install -e .[test]
        Obtaining file:///Users/trevorbaca/abjad
        Collecting ply (from Abjad==3.0.0)
        Using cached https://files.pythonhosted.org/packages/a3/58/35da89ee790598a0700ea49b2a66594140f44dec458c07e8e3d4979137fc/ply-3.11-py2.py3-none-any.whl
        Collecting roman (from Abjad==3.0.0)
        Downloading https://files.pythonhosted.org/packages/8d/f2/29d1d069555855ed49c74b627e6af73cec7a5f4de27c200ea0d760939da4/roman-3.2-py2.py3-none-any.whl
        Collecting uqbar>=0.4.0 (from Abjad==3.0.0)
        Downloading https://files.pythonhosted.org/packages/a1/db/2dd82549efd9eb5271292afeba314f3b21d79a0fd8872f27297d63c45ac7/uqbar-0.4.1.tar.gz (53kB)
            |████████████████████████████████| 61kB 2.1MB/s 
        < ... snip ... >
        Installing collected packages: ply, roman, sphinxcontrib-jsmath, sphinxcontrib-serializinghtml, pyparsing, six, packaging, pytz, babel, alabaster, imagesize, snowballstemmer, Pygments, docutils, MarkupSafe, Jinja2, sphinxcontrib-devhelp, chardet, certifi, idna, urllib3, requests, sphinxcontrib-applehelp, sphinxcontrib-qthelp, sphinxcontrib-htmlhelp, Sphinx, Unidecode, click, appdirs, toml, attrs, black, sphinx-autodoc-typehints, sphinx-rtd-theme, uqbar, decorator, ipython-genutils, traitlets, jupyter-core, webencodings, bleach, pyrsistent, jsonschema, nbformat, entrypoints, pandocfilters, mistune, defusedxml, testpath, nbconvert, tornado, python-dateutil, pyzmq, jupyter-client, wcwidth, prompt-toolkit, pickleshare, ptyprocess, pexpect, parso, jedi, appnope, backcall, ipython, ipykernel, Send2Trash, terminado, prometheus-client, notebook, widgetsnbextension, ipywidgets, qtconsole, jupyter-console, jupyter, abjad-ext-ipython, Abjad
        Found existing installation: Abjad 3.0.0
            Not uninstalling abjad at /Users/trevorbaca/abjad, outside environment /Users/trevorbaca/.virtualenvs/abjad3/bin/..
            Can't uninstall 'Abjad'. No files were found to uninstall.
        Running setup.py develop for Abjad
        Successfully installed Abjad Jinja2-2.10.1 MarkupSafe-1.1.1 Pygments-2.4.2 Send2Trash-1.5.0 Sphinx-2.1.2 Unidecode-1.1.1 abjad-ext-ipython-3.0.0 alabaster-0.7.12 appdirs-1.4.3 appnope-0.1.0 attrs-19.1.0 babel-2.7.0 backcall-0.1.0 black-19.3b0 bleach-3.1.0 certifi-2019.6.16 chardet-3.0.4 click-7.0 decorator-4.4.0 defusedxml-0.6.0 docutils-0.15.1 entrypoints-0.3 idna-2.8 imagesize-1.1.0 ipykernel-5.1.1 ipython-7.7.0 ipython-genutils-0.2.0 ipywidgets-7.5.0 jedi-0.14.1 jsonschema-3.0.1 jupyter-1.0.0 jupyter-client-5.3.1 jupyter-console-6.0.0 jupyter-core-4.5.0 mistune-0.8.4 nbconvert-5.5.0 nbformat-4.4.0 notebook-6.0.0 packaging-19.0 pandocfilters-1.4.2 parso-0.5.1 pexpect-4.7.0 pickleshare-0.7.5 ply-3.11 prometheus-client-0.7.1 prompt-toolkit-2.0.9 ptyprocess-0.6.0 pyparsing-2.4.1.1 pyrsistent-0.15.4 python-dateutil-2.8.0 pytz-2019.1 pyzmq-18.0.2 qtconsole-4.5.2 requests-2.22.0 roman-3.2 six-1.12.0 snowballstemmer-1.9.0 sphinx-autodoc-typehints-1.7.0 sphinx-rtd-theme-0.4.3 sphinxcontrib-applehelp-1.0.1 sphinxcontrib-devhelp-1.0.1 sphinxcontrib-htmlhelp-1.0.2 sphinxcontrib-jsmath-1.0.1 sphinxcontrib-qthelp-1.0.2 sphinxcontrib-serializinghtml-1.1.3 terminado-0.8.2 testpath-0.4.2 toml-0.10.0 tornado-6.0.3 traitlets-4.3.2 uqbar-0.4.1 urllib3-1.25.3 wcwidth-0.1.7 webencodings-0.5.1 widgetsnbextension-3.5.0

        (abjad3) ✔ ~/abjad [trevor/dev|✔] 
        13:03 $ 

    Do not use [book] installation.

12. Visit and install local abjadext clones into the new virutal environment:

        cd ~/abjad-ext-book
        pip install -e .

        cd ~/abjad-ext-cli
        pip install -e .

        cd ~/abjad-ext-ipython
        pip install -e .

        cd ~/abjad-ext-nauert
        pip install -e .

        cd ~/abjad-ext-rmakers
        pip install -e .

        cd ~/abjad-ext-tonality
        pip install -e .

    Confirmation messaging will look like this in each clone:

        Obtaining file:///Users/trevorbaca/abjad-ext-book
        < ... snip ... >
        Successfully installed abjad-ext-book-3.0.0

13. Use pip to install Bača-specific Python packages:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        13:06 $ pip install inflect
        Collecting inflect
        Downloading https://files.pythonhosted.org/packages/86/02/e6b11020a9c37d25b4767a1d0af5835629f6e75d6f51553ad07a4c73dc31/inflect-2.1.0-py2.py3-none-any.whl (40kB)
            |████████████████████████████████| 51kB 1.8MB/s 
        Installing collected packages: inflect
        Successfully installed inflect-2.1.0

    No list of these currently exists.

14. Run tests:

        cdj
        ..
        !py.test -rf

        cdb
        ..
        !py.test -rf

        cdi
        ..
        !py.test -rf

15. Rebuild APIs:

        apim; apib; apis; apii
