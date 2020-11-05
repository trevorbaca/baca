Python 3 installation
=====================

OBJECTIVE. Install Python 3. Create a Python 3 virtualenv for Abjad development.

First make sure Python 3 is installed on your machine:

    $ which python3
    /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

    $ python3 --version
    Python 3.6.2

    $ ls -al /usr/local/bin/python3
    lrwxr-xr-x  1 root  wheel  69 Aug 24 16:06 /usr/local/bin/python3 -> ../../../Library/Frameworks/Python.framework/Versions/3.6/bin/python3

    $ /usr/local/bin/python3 --version
    Python 3.6.2

Then make sure the virtualenv and virtualenvwrapper packages are installed:

    $ virtualenv --version
    14.0.6

    $ which virtualenvwrapper.sh
    /usr/local/bin/virtualenvwrapper.sh

Upgrade virtualenv if necessary:

    $ sudo -H pip install --upgrade pip
    $ sudo -H pip install --upgrade virtualenv
    Collecting virtualenv
    Downloading virtualenv-15.1.0-py2.py3-none-any.whl (1.8MB)
        100% |████████████████████████████████| 1.8MB 738kB/s 
    Installing collected packages: virtualenv
    Found existing installation: virtualenv 14.0.6
        Uninstalling virtualenv-14.0.6:
        Successfully uninstalled virtualenv-14.0.6
    Successfully installed virtualenv-15.1.0
    
Deactivate any active virtual environment:

    09:45 $ deactivate
    ✔ ~/Desktop

Make a Python 3 virtual environment for Abjad:

    ✘-1 ~/Desktop 
    10:05 $ mkvirtualenv --python=/usr/local/bin/python3 abjad3
    Running virtualenv with interpreter /usr/local/bin/python3
    Using base prefix '/usr/local/Cellar/python3/3.5.1/Frameworks/Python.framework/Versions/3.5'
    New python executable in /Users/trevorbaca/Envs/abjad3/bin/python3
    Also creating executable in /Users/trevorbaca/Envs/abjad3/bin/python
    Installing setuptools, pip, wheel...done.
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/Envs/abjad3/bin/predeactivate
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/Envs/abjad3/bin/postdeactivate
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/Envs/abjad3/bin/preactivate
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/Envs/abjad3/bin/postactivate
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/Envs/abjad3/bin/get_env_details
    (abjad3) ✔ ~/Desktop 
    10:06 $ 

Reinstall Abjad under the Python 3 virtual environment:

    (abjad3) ✔ ~/Documents/abjad [master|✔] 
    10:32 $ pip install -e .[development,ipython]
    Obtaining file:///Users/trevorbaca/Documents/abjad
    Collecting ply (from Abjad==2.19)
    Downloading ply-3.9.tar.gz (150kB)
        100% |████████████████████████████████| 153kB 3.5MB/s 
    Collecting six (from Abjad==2.19)
    Downloading six-1.10.0-py2.py3-none-any.whl
    <SNIP>
    Running setup.py bdist_wheel for tornado ... done
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/b3/db/47/46e05d1ee3ecfba252fcab42f0a156dab0df0cddf99fa0827c
    Successfully built ply PyPDF2 simplegeneric MarkupSafe terminado tornado
    Installing collected packages: ply, six, py, pytest, docutils, imagesize, pytz, babel, MarkupSafe, Jinja2, alabaster, Pygments, snowballstemmer, sphinx, sphinx-rtd-theme, PyPDF2, appnope, decorator, ptyprocess, pexpect, wcwidth, prompt-toolkit, pickleshare, simplegeneric, ipython-genutils, traitlets, ipython, pyzmq, jupyter-core, jupyter-client, tornado, ipykernel, qtconsole, terminado, jsonschema, nbformat, entrypoints, mistune, nbconvert, notebook, jupyter-console, widgetsnbextension, ipywidgets, jupyter, Abjad
    Running setup.py develop for Abjad
    Successfully installed Abjad-2.19 Jinja2-2.8 MarkupSafe-0.23 PyPDF2-1.26.0 Pygments-2.1.3 alabaster-0.7.9 appnope-0.1.0 babel-2.3.4 decorator-4.0.10 docutils-0.12 entrypoints-0.2.2 imagesize-0.7.1 ipykernel-4.5.0 ipython-5.1.0 ipython-genutils-0.1.0 ipywidgets-5.2.2 jsonschema-2.5.1 jupyter-1.0.0 jupyter-client-4.4.0 jupyter-console-5.0.0 jupyter-core-4.2.0 mistune-0.7.3 nbconvert-4.2.0 nbformat-4.1.0 notebook-4.2.3 pexpect-4.2.1 pickleshare-0.7.4 ply-3.9 prompt-toolkit-1.0.7 ptyprocess-0.5.1 py-1.4.31 pytest-3.0.3 pytz-2016.7 pyzmq-15.4.0 qtconsole-4.2.1 simplegeneric-0.8.1 six-1.10.0 snowballstemmer-1.2.1 sphinx-1.4.8 sphinx-rtd-theme-0.1.9 terminado-0.6 tornado-4.4.2 traitlets-4.3.1 wcwidth-0.1.7 widgetsnbextension-1.2.6
    (abjad3) ✔ ~/Documents/abjad [master|✔] 

Import and test Abjad:

    (abjad3) ✔ ~/Documents/abjad [master|✔] 
    10:34 $ python
    Python 3.5.1 (default, Oct  6 2016, 09:12:24) 
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import abjad
    >>>

    (abjad3) ✔ ~/Documents/abjad [master|✔] 
    10:36 $ abjad
    Abjad 2.19 (development)
    >>> note = Note("c'4")
    >>> show(note)

Reinstall the IDE under the Python 3 virtual environment:

    (abjad3) ✔ ~/Documents/abjad-ide [master|✔] 
    11:14 $ pip install -e .
    Obtaining file:///Users/trevorbaca/Documents/abjad-ide
    Requirement already satisfied (use --upgrade to upgrade): abjad[development] in /Users/trevorbaca/Documents/abjad (from Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): ply in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): six in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): pytest>=3.0.0 in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): sphinx>=1.4 in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): sphinx-rtd-theme in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): PyPDF2 in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): py>=1.4.29 in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from pytest>=3.0.0->abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): Pygments>=2.0 in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): docutils>=0.11 in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): babel!=2.0,>=1.3 in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): snowballstemmer>=1.1 in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): alabaster<0.8,>=0.7 in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): imagesize in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): Jinja2>=2.3 in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): pytz>=0a in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from babel!=2.0,>=1.3->sphinx>=1.4->abjad[development]->Abjad-IDE==0.0.0)
    Requirement already satisfied (use --upgrade to upgrade): MarkupSafe in /Users/trevorbaca/Envs/abjad3/lib/python3.5/site-packages (from Jinja2>=2.3->sphinx>=1.4->abjad[development]->Abjad-IDE==0.0.0)
    Installing collected packages: Abjad-IDE
    Running setup.py develop for Abjad-IDE
    Successfully installed Abjad-IDE-0.0.0
    (abjad3) ✔ ~/Documents/abjad-ide [master|✔] 

Start the IDE to test.

All Abjad tests now pass and the API builds.

Build the Bača API:

    * Calling make_baca_api.py raises an import error because no inflect module.

    * Calling `pip install inflect` fixes the problem.

    * Calling make_baca_api.py now works.

Python 2 virtual environment installation
=========================================

Need to create a Python 2 virtual environment (November 2016).

First I deactivate my Python 3 virtual environment:

    (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
    11:44 $ deactivate

    ✔ ~/abjad/abjad [trevor/dev|✔] 
    11:44 $ 

Shell knows about Python 2:

    ✔ ~/abjad/abjad [trevor/dev|✔] 
    11:44 $ which python
    /usr/bin/python

    ✔ ~/abjad/abjad [trevor/dev|✔] 
    11:45 $ python --version
    Python 2.7.10

But Abjad startup fails:

    ✔ ~/abjad/abjad [trevor/dev|✔] 
    11:45 $ abjad
    Traceback (most recent call last):
    File "/Users/trevorbaca/abjad/abjad/scr/abjad", line 4, in <module>
        from abjad.tools.systemtools.run_abjad import run_abjad
    File "/Users/trevorbaca/abjad/abjad/__init__.py", line 31, in <module>
        from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration
    File "/Users/trevorbaca/abjad/abjad/tools/__init__.py", line 3, in <module>
        from abjad.tools import systemtools
    File "/Users/trevorbaca/abjad/abjad/tools/systemtools/__init__.py", line 2, in <module>
        from .AbjadConfiguration import AbjadConfiguration
    File "/Users/trevorbaca/abjad/abjad/tools/systemtools/AbjadConfiguration.py", line 6, in <module>
        from abjad.tools.systemtools.Configuration import Configuration
    File "/Users/trevorbaca/abjad/abjad/tools/systemtools/Configuration.py", line 9, in <module>
        from abjad.tools.abctools.AbjadObject import AbjadObject
    File "/Users/trevorbaca/abjad/abjad/tools/abctools/__init__.py", line 5, in <module>
        from .Parser import Parser
    File "/Users/trevorbaca/abjad/abjad/tools/abctools/Parser.py", line 6, in <module>
        import ply
    ImportError: No module named ply

Abjad is not installed under my non-virtual environment.

Will install Abjad under a Python 2 virtual environment.

Switch to desktop:

    ✔ ~/Desktop 
    11:50 $ 

Python 2 virtual environment doesn't exist yet:

    ✔ ~/Desktop 
    11:50 $ ls -a ~/.virtualenvs/
    .                initialize       postmkvirtualenv premkproject
    ..               postactivate     postrmvirtualenv premkvirtualenv
    abjad3           postdeactivate   preactivate      prermvirtualenv
    get_env_details  postmkproject    predeactivate

Creating Python 2 virtual environment:

    ✔ ~/Desktop 
    11:51 $ mkvirtualenv --python=/usr/bin/python abjad2
    Already using interpreter /usr/bin/python
    New python executable in /Users/trevorbaca/.virtualenvs/abjad2/bin/python
    Installing setuptools, pip, wheel...done.
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad2/bin/predeactivate
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad2/bin/postdeactivate
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad2/bin/preactivate
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad2/bin/postactivate
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad2/bin/get_env_details

    (abjad2) ✔ ~/Desktop 
    11:51 $ 

Switch to Abjad *root* directory:

    (abjad2) ✔ ~/Desktop 
    11:53 $ cd ~/abjad

    (abjad2) ✔ ~/abjad [trevor/dev|✔] 
    11:53 $ 

Abjad directory structure already exists:

    (abjad2) ✔ ~/abjad [trevor/dev|✔] 
    11:54 $ ls
    Abjad.egg-info   Makefile         pytest.ini       tox.ini
    Dockerfile       README.rst       requirements.txt
    LICENSE          abjad            setup.cfg
    MANIFEST.in      conftest.py      setup.py

Reinstall Abjad (for the benefit of Python 2):

    (abjad2) ✔ ~/abjad [trevor/dev|✔] 
    11:54 $ pip install  -e .[development,ipython]
    Obtaining file:///Users/trevorbaca/abjad
    Collecting ply (from Abjad==2.20)
    Downloading ply-3.9.tar.gz (150kB)
        100% |████████████████████████████████| 153kB 650kB/s 
    Collecting six (from Abjad==2.20)
    Downloading six-1.10.0-py2.py3-none-any.whl
    Collecting enum34 (from Abjad==2.20)
    Downloading enum34-1.1.6-py2-none-any.whl
    Collecting pathlib2 (from Abjad==2.20)
    Downloading pathlib2-2.1.0-py2.py3-none-any.whl
    Collecting funcsigs (from Abjad==2.20)
    Downloading funcsigs-1.0.2-py2.py3-none-any.whl
    Collecting mock (from Abjad==2.20)
    Downloading mock-2.0.0-py2.py3-none-any.whl (56kB)
        100% |████████████████████████████████| 61kB 832kB/s 
    Collecting pytest>=3.0.0 (from Abjad==2.20)
    Downloading pytest-3.0.4-py2.py3-none-any.whl (170kB)
        100% |████████████████████████████████| 174kB 613kB/s 
    Collecting sphinx>=1.4 (from Abjad==2.20)
    Downloading Sphinx-1.4.9-py2.py3-none-any.whl (1.6MB)
        100% |████████████████████████████████| 1.6MB 363kB/s 
    Collecting sphinx-rtd-theme (from Abjad==2.20)
    Downloading sphinx_rtd_theme-0.1.9-py2-none-any.whl (693kB)
        100% |████████████████████████████████| 696kB 514kB/s 
    Collecting PyPDF2 (from Abjad==2.20)
    Downloading PyPDF2-1.26.0.tar.gz (77kB)
        100% |████████████████████████████████| 81kB 744kB/s 
    Collecting ipython (from Abjad==2.20)
    Downloading ipython-5.1.0-py2-none-any.whl (747kB)
        100% |████████████████████████████████| 747kB 479kB/s 
    Collecting jupyter (from Abjad==2.20)
    Downloading jupyter-1.0.0-py2.py3-none-any.whl
    Collecting pbr>=0.11 (from mock->Abjad==2.20)
    Downloading pbr-1.10.0-py2.py3-none-any.whl (96kB)
        100% |████████████████████████████████| 102kB 613kB/s 
    Collecting py>=1.4.29 (from pytest>=3.0.0->Abjad==2.20)
    Downloading py-1.4.31-py2.py3-none-any.whl (81kB)
        100% |████████████████████████████████| 92kB 905kB/s 
    Collecting Jinja2>=2.3 (from sphinx>=1.4->Abjad==2.20)
    Downloading Jinja2-2.8-py2.py3-none-any.whl (263kB)
        100% |████████████████████████████████| 266kB 1.2MB/s 
    Collecting babel!=2.0,>=1.3 (from sphinx>=1.4->Abjad==2.20)
    Downloading Babel-2.3.4-py2.py3-none-any.whl (7.1MB)
        100% |████████████████████████████████| 7.1MB 147kB/s 
    Collecting docutils>=0.11 (from sphinx>=1.4->Abjad==2.20)
    Downloading docutils-0.12.tar.gz (1.6MB)
        100% |████████████████████████████████| 1.6MB 403kB/s 
    Collecting alabaster<0.8,>=0.7 (from sphinx>=1.4->Abjad==2.20)
    Downloading alabaster-0.7.9-py2.py3-none-any.whl
    Collecting snowballstemmer>=1.1 (from sphinx>=1.4->Abjad==2.20)
    Downloading snowballstemmer-1.2.1-py2.py3-none-any.whl (64kB)
        100% |████████████████████████████████| 71kB 659kB/s 
    Collecting Pygments>=2.0 (from sphinx>=1.4->Abjad==2.20)
    Downloading Pygments-2.1.3-py2.py3-none-any.whl (755kB)
        100% |████████████████████████████████| 757kB 511kB/s 
    Collecting imagesize (from sphinx>=1.4->Abjad==2.20)
    Downloading imagesize-0.7.1-py2.py3-none-any.whl
    Collecting decorator (from ipython->Abjad==2.20)
    Downloading decorator-4.0.10-py2.py3-none-any.whl
    Requirement already satisfied: setuptools>=18.5 in /Users/trevorbaca/.virtualenvs/abjad2/lib/python2.7/site-packages (from ipython->Abjad==2.20)
    Collecting pickleshare (from ipython->Abjad==2.20)
    Downloading pickleshare-0.7.4-py2.py3-none-any.whl
    Collecting backports.shutil-get-terminal-size; python_version == "2.7" (from ipython->Abjad==2.20)
    Downloading backports.shutil_get_terminal_size-1.0.0-py2.py3-none-any.whl
    Collecting pexpect; sys_platform != "win32" (from ipython->Abjad==2.20)
    Downloading pexpect-4.2.1-py2.py3-none-any.whl (55kB)
        100% |████████████████████████████████| 61kB 667kB/s 
    Collecting simplegeneric>0.8 (from ipython->Abjad==2.20)
    Downloading simplegeneric-0.8.1.zip
    Collecting prompt-toolkit<2.0.0,>=1.0.3 (from ipython->Abjad==2.20)
    Downloading prompt_toolkit-1.0.9-py2-none-any.whl (241kB)
        100% |████████████████████████████████| 245kB 575kB/s 
    Collecting traitlets>=4.2 (from ipython->Abjad==2.20)
    Downloading traitlets-4.3.1-py2.py3-none-any.whl (74kB)
        100% |████████████████████████████████| 81kB 787kB/s 
    Collecting appnope; sys_platform == "darwin" (from ipython->Abjad==2.20)
    Downloading appnope-0.1.0-py2.py3-none-any.whl
    Collecting ipywidgets (from jupyter->Abjad==2.20)
    Downloading ipywidgets-5.2.2-py2.py3-none-any.whl (43kB)
        100% |████████████████████████████████| 51kB 764kB/s 
    Collecting qtconsole (from jupyter->Abjad==2.20)
    Downloading qtconsole-4.2.1-py2.py3-none-any.whl (104kB)
        100% |████████████████████████████████| 112kB 646kB/s 
    Collecting nbconvert (from jupyter->Abjad==2.20)
    Downloading nbconvert-4.2.0-py2.py3-none-any.whl (319kB)
        100% |████████████████████████████████| 327kB 568kB/s 
    Collecting notebook (from jupyter->Abjad==2.20)
    Downloading notebook-4.2.3-py2.py3-none-any.whl (6.7MB)
        100% |████████████████████████████████| 6.7MB 153kB/s 
    Collecting jupyter-console (from jupyter->Abjad==2.20)
    Downloading jupyter_console-5.0.0-py2.py3-none-any.whl
    Collecting ipykernel (from jupyter->Abjad==2.20)
    Downloading ipykernel-4.5.1-py2.py3-none-any.whl (98kB)
        100% |████████████████████████████████| 102kB 594kB/s 
    Collecting MarkupSafe (from Jinja2>=2.3->sphinx>=1.4->Abjad==2.20)
    Downloading MarkupSafe-0.23.tar.gz
    Collecting pytz>=0a (from babel!=2.0,>=1.3->sphinx>=1.4->Abjad==2.20)
    Downloading pytz-2016.7-py2.py3-none-any.whl (480kB)
        100% |████████████████████████████████| 481kB 560kB/s 
    Collecting ptyprocess>=0.5 (from pexpect; sys_platform != "win32"->ipython->Abjad==2.20)
    Downloading ptyprocess-0.5.1-py2.py3-none-any.whl
    Collecting wcwidth (from prompt-toolkit<2.0.0,>=1.0.3->ipython->Abjad==2.20)
    Downloading wcwidth-0.1.7-py2.py3-none-any.whl
    Collecting ipython-genutils (from traitlets>=4.2->ipython->Abjad==2.20)
    Downloading ipython_genutils-0.1.0-py2.py3-none-any.whl
    Collecting widgetsnbextension>=1.2.6 (from ipywidgets->jupyter->Abjad==2.20)
    Downloading widgetsnbextension-1.2.6-py2.py3-none-any.whl (1.5MB)
        100% |████████████████████████████████| 1.5MB 366kB/s 
    Collecting jupyter-client>=4.1 (from qtconsole->jupyter->Abjad==2.20)
    Downloading jupyter_client-4.4.0-py2.py3-none-any.whl (76kB)
        100% |████████████████████████████████| 81kB 627kB/s 
    Collecting jupyter-core (from qtconsole->jupyter->Abjad==2.20)
    Downloading jupyter_core-4.2.0-py2.py3-none-any.whl (76kB)
        100% |████████████████████████████████| 81kB 630kB/s 
    Collecting entrypoints (from nbconvert->jupyter->Abjad==2.20)
    Downloading entrypoints-0.2.2-py2.py3-none-any.whl
    Collecting nbformat (from nbconvert->jupyter->Abjad==2.20)
    Downloading nbformat-4.1.0-py2.py3-none-any.whl (140kB)
        100% |████████████████████████████████| 143kB 142kB/s 
    Collecting mistune!=0.6 (from nbconvert->jupyter->Abjad==2.20)
    Downloading mistune-0.7.3-py2.py3-none-any.whl
    Collecting terminado>=0.3.3; sys_platform != "win32" (from notebook->jupyter->Abjad==2.20)
    Downloading terminado-0.6.tar.gz
    Collecting tornado>=4 (from notebook->jupyter->Abjad==2.20)
    Downloading tornado-4.4.2.tar.gz (460kB)
        100% |████████████████████████████████| 460kB 519kB/s 
    Collecting pyzmq>=13 (from jupyter-client>=4.1->qtconsole->jupyter->Abjad==2.20)
    Downloading pyzmq-16.0.2-cp27-cp27m-macosx_10_6_intel.whl (1.1MB)
        100% |████████████████████████████████| 1.1MB 445kB/s 
    Collecting configparser>=3.5; python_version == "2.7" (from entrypoints->nbconvert->jupyter->Abjad==2.20)
    Downloading configparser-3.5.0.tar.gz
    Collecting jsonschema!=2.5.0,>=2.0 (from nbformat->nbconvert->jupyter->Abjad==2.20)
    Downloading jsonschema-2.5.1-py2.py3-none-any.whl
    Collecting singledispatch (from tornado>=4->notebook->jupyter->Abjad==2.20)
    Downloading singledispatch-3.4.0.3-py2.py3-none-any.whl
    Collecting certifi (from tornado>=4->notebook->jupyter->Abjad==2.20)
    Downloading certifi-2016.9.26-py2.py3-none-any.whl (377kB)
        100% |████████████████████████████████| 378kB 525kB/s 
    Collecting backports_abc>=0.4 (from tornado>=4->notebook->jupyter->Abjad==2.20)
    Downloading backports_abc-0.5-py2.py3-none-any.whl
    Collecting functools32; python_version == "2.7" (from jsonschema!=2.5.0,>=2.0->nbformat->nbconvert->jupyter->Abjad==2.20)
    Downloading functools32-3.2.3-2.zip
    Building wheels for collected packages: ply, PyPDF2, docutils, simplegeneric, MarkupSafe, terminado, tornado, configparser, functools32
    Running setup.py bdist_wheel for ply ... done
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/c1/0c/bd/306a63396decbe8353a4a056fcba97a092be0e035522bc567d
    Running setup.py bdist_wheel for PyPDF2 ... done
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/86/6a/6a/1ce004a5996894d33d93e1fb1b67c30973dc945cc5875a1dd0
    Running setup.py bdist_wheel for docutils ... done
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/db/de/bd/b99b1e12d321fbc950766c58894c6576b1a73ae3131b29a151
    Running setup.py bdist_wheel for simplegeneric ... done
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/7b/31/08/c85e74c84188cbec6a6827beec4d640f2bd78ae003dc1ec09d
    Running setup.py bdist_wheel for MarkupSafe ... done
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/a3/fa/dc/0198eed9ad95489b8a4f45d14dd5d2aee3f8984e46862c5748
    Running setup.py bdist_wheel for terminado ... done
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/3b/c2/ea/af635ffb63857a8c2ddd22da6a4b52f5b7ea3065db94ef5d7c
    Running setup.py bdist_wheel for tornado ... done
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/b3/db/47/46e05d1ee3ecfba252fcab42f0a156dab0df0cddf99fa0827c
    Running setup.py bdist_wheel for configparser ... done
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/1c/bd/b4/277af3f6c40645661b4cd1c21df26aca0f2e1e9714a1d4cda8
    Running setup.py bdist_wheel for functools32 ... done
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/3c/d0/09/cd78d0ff4d6cfecfbd730782a7815a4571cd2cd4d2ed6e69d9
    Successfully built ply PyPDF2 docutils simplegeneric MarkupSafe terminado tornado configparser functools32
    Installing collected packages: ply, six, enum34, pathlib2, funcsigs, pbr, mock, py, pytest, MarkupSafe, Jinja2, pytz, babel, docutils, alabaster, snowballstemmer, Pygments, imagesize, sphinx, sphinx-rtd-theme, PyPDF2, decorator, pickleshare, backports.shutil-get-terminal-size, ptyprocess, pexpect, simplegeneric, wcwidth, prompt-toolkit, ipython-genutils, traitlets, appnope, ipython, configparser, entrypoints, functools32, jsonschema, jupyter-core, nbformat, mistune, nbconvert, singledispatch, certifi, backports-abc, tornado, terminado, pyzmq, jupyter-client, ipykernel, notebook, widgetsnbextension, ipywidgets, qtconsole, jupyter-console, jupyter, Abjad
    Found existing installation: Abjad 2.19
        Not uninstalling abjad at /Users/trevorbaca/abjad, outside environment /Users/trevorbaca/.virtualenvs/abjad2
    Running setup.py develop for Abjad
    Successfully installed Abjad Jinja2-2.8 MarkupSafe-0.23 PyPDF2-1.26.0 Pygments-2.1.3 alabaster-0.7.9 appnope-0.1.0 babel-2.3.4 backports-abc-0.5 backports.shutil-get-terminal-size-1.0.0 certifi-2016.9.26 configparser-3.5.0 decorator-4.0.10 docutils-0.12 entrypoints-0.2.2 enum34-1.1.6 funcsigs-1.0.2 functools32-3.2.3.post2 imagesize-0.7.1 ipykernel-4.5.1 ipython-5.1.0 ipython-genutils-0.1.0 ipywidgets-5.2.2 jsonschema-2.5.1 jupyter-1.0.0 jupyter-client-4.4.0 jupyter-console-5.0.0 jupyter-core-4.2.0 mistune-0.7.3 mock-2.0.0 nbconvert-4.2.0 nbformat-4.1.0 notebook-4.2.3 pathlib2-2.1.0 pbr-1.10.0 pexpect-4.2.1 pickleshare-0.7.4 ply-3.9 prompt-toolkit-1.0.9 ptyprocess-0.5.1 py-1.4.31 pytest-3.0.4 pytz-2016.7 pyzmq-16.0.2 qtconsole-4.2.1 simplegeneric-0.8.1 singledispatch-3.4.0.3 six-1.10.0 snowballstemmer-1.2.1 sphinx-1.4.9 sphinx-rtd-theme-0.1.9 terminado-0.6 tornado-4.4.2 traitlets-4.3.1 wcwidth-0.1.7 widgetsnbextension-1.2.6

Import Abjad:

    (abjad2) ✔ ~/abjad [trevor/dev|✔] 
    11:57 $ python
    Python 2.7.10 (default, Jul 30 2016, 18:31:42) 
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import abjad
    >>> 

Start Abjad:

    (abjad2) ✔ ~/abjad/abjad [trevor/dev|✔] 
    11:59 $ abjad
    Abjad 2.20 (development)
    >>> 

Run tests.

Python's inflect module is not yet installed:

    (abjad2) ✔ ~/baca/baca [master|✔] 
    15:51 $ python
    Python 2.7.10 (default, Jul 30 2016, 18:31:42) 
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import inflect
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ImportError: No module named inflect

Install inflect:

    (abjad2) ✔ ~/baca/baca [master|✚ 1] 
    15:51 $ pip install inflect
    Collecting inflect
    Downloading inflect-0.2.5-py2.py3-none-any.whl (58kB)
        100% |████████████████████████████████| 61kB 997kB/s 
    Installing collected packages: inflect
    Successfully installed inflect-0.2.5

Run make_baca_api.py.

Abjad is now broken under the Python 3 virtual environment:

    (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
    17:35 $ abjad
    Traceback (most recent call last):
    File "/Users/trevorbaca/.virtualenvs/abjad3/bin/abjad", line 6, in <module>
        from pkg_resources import load_entry_point
    File "/Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages/pkg_resources/__init__.py", line 2991, in <module>
        @_call_aside
    File "/Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages/pkg_resources/__init__.py", line 2977, in _call_aside
        f(*args, **keywords)
    File "/Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages/pkg_resources/__init__.py", line 3004, in _initialize_master_working_set
        working_set = WorkingSet._build_master()
    File "/Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages/pkg_resources/__init__.py", line 662, in _build_master
        ws.require(__requires__)
    File "/Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages/pkg_resources/__init__.py", line 970, in require
        needed = self.resolve(parse_requirements(requirements))
    File "/Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages/pkg_resources/__init__.py", line 856, in resolve
        raise DistributionNotFound(req, requirers)
    pkg_resources.DistributionNotFound: The 'mock' distribution was not found and is required by Abjad

And indeed the 'mock' module appears to be missing under the Python 3 virtual
environment:

    (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
    17:35 $ python
    Python 3.5.1 (default, Oct  6 2016, 09:12:24) 
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import mock
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ImportError: No module named 'mock'

Even though it is present under the Python 2 virtual environment:

    (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
    17:36 $ workon abjad2

    (abjad2) ✔ ~/abjad/abjad [trevor/dev|✔] 
    17:36 $ python
    Python 2.7.10 (default, Jul 30 2016, 18:31:42) 
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import mock
    >>> 

So what does this mean?

"Reinstalling" Abjad under Python 3 appears to hurt more than help:

    (abjad3) ✔ ~/abjad [trevor/dev|✔] 
    17:38 $ cd ~/abjad

    (abjad3) ✔ ~/abjad [trevor/dev|✔] 
    17:38 $ pip install -e .[development,ipython]
    Obtaining file:///Users/trevorbaca/abjad
    Requirement already satisfied: ply in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from Abjad==2.20)
    Requirement already satisfied: six in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from Abjad==2.20)
    Requirement already satisfied: pytest>=3.0.0 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from Abjad==2.20)
    Requirement already satisfied: sphinx>=1.4 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from Abjad==2.20)
    Requirement already satisfied: sphinx-rtd-theme in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from Abjad==2.20)
    Requirement already satisfied: PyPDF2 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from Abjad==2.20)
    Requirement already satisfied: ipython in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from Abjad==2.20)
    Requirement already satisfied: jupyter in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from Abjad==2.20)
    Requirement already satisfied: py>=1.4.29 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from pytest>=3.0.0->Abjad==2.20)
    Requirement already satisfied: snowballstemmer>=1.1 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->Abjad==2.20)
    Requirement already satisfied: docutils>=0.11 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->Abjad==2.20)
    Requirement already satisfied: imagesize in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->Abjad==2.20)
    Requirement already satisfied: alabaster<0.8,>=0.7 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->Abjad==2.20)
    Requirement already satisfied: Pygments>=2.0 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->Abjad==2.20)
    Requirement already satisfied: Jinja2>=2.3 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->Abjad==2.20)
    Requirement already satisfied: babel!=2.0,>=1.3 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from sphinx>=1.4->Abjad==2.20)
    Requirement already satisfied: simplegeneric>0.8 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from ipython->Abjad==2.20)
    Requirement already satisfied: traitlets>=4.2 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from ipython->Abjad==2.20)
    Requirement already satisfied: pexpect; sys_platform != "win32" in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from ipython->Abjad==2.20)
    Requirement already satisfied: setuptools>=18.5 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from ipython->Abjad==2.20)
    Requirement already satisfied: prompt-toolkit<2.0.0,>=1.0.3 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from ipython->Abjad==2.20)
    Requirement already satisfied: pickleshare in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from ipython->Abjad==2.20)
    Requirement already satisfied: appnope; sys_platform == "darwin" in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from ipython->Abjad==2.20)
    Requirement already satisfied: decorator in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from ipython->Abjad==2.20)
    Requirement already satisfied: nbconvert in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from jupyter->Abjad==2.20)
    Requirement already satisfied: ipykernel in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from jupyter->Abjad==2.20)
    Requirement already satisfied: ipywidgets in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from jupyter->Abjad==2.20)
    Requirement already satisfied: jupyter-console in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from jupyter->Abjad==2.20)
    Requirement already satisfied: qtconsole in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from jupyter->Abjad==2.20)
    Requirement already satisfied: notebook in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from jupyter->Abjad==2.20)
    Requirement already satisfied: MarkupSafe in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from Jinja2>=2.3->sphinx>=1.4->Abjad==2.20)
    Requirement already satisfied: pytz>=0a in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from babel!=2.0,>=1.3->sphinx>=1.4->Abjad==2.20)
    Requirement already satisfied: ipython-genutils in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from traitlets>=4.2->ipython->Abjad==2.20)
    Requirement already satisfied: ptyprocess>=0.5 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from pexpect; sys_platform != "win32"->ipython->Abjad==2.20)
    Requirement already satisfied: wcwidth in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from prompt-toolkit<2.0.0,>=1.0.3->ipython->Abjad==2.20)
    Requirement already satisfied: mistune!=0.6 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from nbconvert->jupyter->Abjad==2.20)
    Requirement already satisfied: nbformat in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from nbconvert->jupyter->Abjad==2.20)
    Requirement already satisfied: jupyter-core in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from nbconvert->jupyter->Abjad==2.20)
    Requirement already satisfied: entrypoints in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from nbconvert->jupyter->Abjad==2.20)
    Requirement already satisfied: jupyter-client in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from ipykernel->jupyter->Abjad==2.20)
    Requirement already satisfied: tornado>=4.0 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from ipykernel->jupyter->Abjad==2.20)
    Requirement already satisfied: widgetsnbextension>=1.2.6 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from ipywidgets->jupyter->Abjad==2.20)
    Requirement already satisfied: terminado>=0.3.3; sys_platform != "win32" in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from notebook->jupyter->Abjad==2.20)
    Requirement already satisfied: jsonschema!=2.5.0,>=2.0 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from nbformat->nbconvert->jupyter->Abjad==2.20)
    Requirement already satisfied: pyzmq>=13 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages (from jupyter-client->ipykernel->jupyter->Abjad==2.20)
    Installing collected packages: Abjad
    Found existing installation: Abjad 2.20
    Exception:
    Traceback (most recent call last):
    File "/Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages/pip/basecommand.py", line 215, in main
        status = self.run(options, args)
    File "/Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages/pip/commands/install.py", line 342, in run
        prefix=options.prefix_path,
    File "/Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages/pip/req/req_set.py", line 778, in install
        requirement.uninstall(auto_confirm=True)
    File "/Users/trevorbaca/.virtualenvs/abjad3/lib/python3.5/site-packages/pip/req/req_install.py", line 703, in uninstall
        '(at %s)' % (link_pointer, self.name, dist.location)
    AssertionError: Egg-link /Users/trevorbaca/Documents/abjad does not match installed location of Abjad (at /Users/trevorbaca/abjad)

Although now, magically, Abjad works:

    (abjad3) ✔ ~/abjad/abjad [trevor/dev|✔] 
    17:40 $ abjad
    Abjad 2.20 (development)
    >>> 
