Upgrading Python
================

OBJECTIVE: Upgrade from Python 3.5.1 to 3.5.3 under OSX. Then reestablish
virtual environments afterwards.

1.  Note current virtual environment and version of Python

        (abjad3) ✔ ~/Desktop 
        12:46 $ python --version
        Python 3.5.1

    This means that Python 3.5.1 was used to create the abjad3 virtual
    environment.

2.  Download the new Python installer and install:

        https://www.python.org/downloads/mac-osx/

3.  Double-click the installer and install.

4.  Note that the version of Python powering the abjad3 virtual environment
    has not changed but that the new version of Python is installed outside of
    the context of virtual environments:

        (abjad3) ✔ ~/Desktop 
        12:49 $ python --version
        Python 3.5.1

        12:52 $ deactivate
        ✔ ~/Scores/stirrings/stirrings [master|✔] 

        12:52 $ python --version
        Python 2.7.10
        ✔ ~/Scores/stirrings/stirrings [master|✔] 

        12:52 $ python3 --version
        Python 3.5.3

5.  Note that when upgrading from Python 3.5 to Python 3.6 that Python 3.6 is
    not yet visible:

        16:09 $ python --version
        Python 2.7.10

        16:09 $ python3 --version
        Python 3.5.3

    But Python 3.6 is installed:

        16:09 $ which python3
        /Library/Frameworks/Python.framework/Versions/3.5/bin/python3

        16:09 $ ls /Library/Frameworks/Python.framework/Versions/
        3.5 3.6

    The solution was to muck around in ~/.profile.

    Make sure Python 3.6 appears in PATH. Then things look lik this:

        16:15 $ python3 --version
        Python 3.6.2

6.  Reestablish the abjad3 virtual environment:

        (abjad3) ✔ ~/Desktop 
        12:54 $ trash ~/.virtualenvs/abjad3/
        Moving '/Users/trevorbaca/.virtualenvs/abjad3/' to '/Users/trevorbaca/.Trash'

        (abjad3) ✔ ~/Desktop 
        12:55 $ deactivate
        ✔ ~/Desktop 

        ✘-1 ~/Desktop 
        12:55 $ mkvirtualenv -p python3 abjad3
        Running virtualenv with interpreter /Library/Frameworks/Python.framework/Versions/3.5/bin/python3
        Using base prefix '/Library/Frameworks/Python.framework/Versions/3.5'
        New python executable in /Users/trevorbaca/.virtualenvs/abjad3/bin/python3
        Also creating executable in /Users/trevorbaca/.virtualenvs/abjad3/bin/python
        Installing setuptools, pip, wheel...done.
        virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/predeactivate
        virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/postdeactivate
        virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/preactivate
        virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/postactivate
        virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/get_env_details

        (abjad3) ✔ ~/Desktop 
        12:56 $ python --version
        Python 3.5.3

7.  Reinstall Abjad from package root directory in the newly reestablished
    virtual environment:

        (abjad3) ✔ ~/abjad [trevor/dev|✔] 
        13:02 $ pip install -e .[development,ipython]
        Obtaining file:///Users/trevorbaca/abjad
        Collecting ply (from Abjad==2.20)
        Requirement already satisfied: six in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from Abjad==2.20)
        Collecting pytest>=3.0.0 (from Abjad==2.20)
        Using cached pytest-3.0.7-py2.py3-none-any.whl
        < ... snip ... >
        Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/d4/01/68/49055c80b9f01ccb49241e73c8019628605064730941d70b56
        Successfully built PyPDF2 simplegeneric MarkupSafe tornado pandocfilters
        Installing collected packages: ply, py, pytest, requests, MarkupSafe, Jinja2, pytz, babel, snowballstemmer, alabaster, imagesize, docutils, Pygments, sphinx, sphinx-rtd-theme, PyPDF2, wcwidth, prompt-toolkit, decorator, ipython-genutils, traitlets, ptyprocess, pexpect, appnope, simplegeneric, jedi, pickleshare, ipython, tornado, jupyter-core, python-dateutil, pyzmq, jupyter-client, ipykernel, jupyter-console, mistune, jsonschema, nbformat, entrypoints, webencodings, html5lib, bleach, testpath, pandocfilters, nbconvert, terminado, notebook, widgetsnbextension, ipywidgets, qtconsole, jupyter, Abjad
        Found existing installation: Abjad 2.20
            Not uninstalling abjad at /Users/trevorbaca/abjad, outside environment /Users/trevorbaca/.virtualenvs/abjad3/bin/..
        Running setup.py develop for Abjad
        Successfully installed Abjad Jinja2-2.9.6 MarkupSafe-1.0 PyPDF2-1.26.0 Pygments-2.2.0 alabaster-0.7.10 appnope-0.1.0 babel-2.4.0 bleach-2.0.0 decorator-4.0.11 docutils-0.13.1 entrypoints-0.2.2 html5lib-0.999999999 imagesize-0.7.1 ipykernel-4.6.1 ipython-6.0.0 ipython-genutils-0.2.0 ipywidgets-6.0.0 jedi-0.10.2 jsonschema-2.6.0 jupyter-1.0.0 jupyter-client-5.0.1 jupyter-console-5.1.0 jupyter-core-4.3.0 mistune-0.7.4 nbconvert-5.1.1 nbformat-4.3.0 notebook-5.0.0 pandocfilters-1.4.1 pexpect-4.2.1 pickleshare-0.7.4 ply-3.10 prompt-toolkit-1.0.14 ptyprocess-0.5.1 py-1.4.33 pytest-3.0.7 python-dateutil-2.6.0 pytz-2017.2 pyzmq-16.0.2 qtconsole-4.3.0 requests-2.13.0 simplegeneric-0.8.1 snowballstemmer-1.2.1 sphinx-1.5.5 sphinx-rtd-theme-0.2.4 terminado-0.6 testpath-0.3 tornado-4.5.1 traitlets-4.3.2 wcwidth-0.1.7 webencodings-0.5.1 widgetsnbextension-2.0.0

        (abjad3) ✔ ~/abjad [trevor/dev|✔] 
        13:03 $ 

8.  Use pip to install Bača-specific Python packages:

        (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
        13:06 $ pip install inflect
        Collecting inflect
        Downloading inflect-0.2.5-py2.py3-none-any.whl (58kB)
            100% |████████████████████████████████| 61kB 1.1MB/s 
        Installing collected packages: inflect
        Successfully installed inflect-0.2.5

    No list of these currently exists.

9.  Rebuild Bača API to test:

        make_baca_api.py
