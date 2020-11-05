Upgrading Python
================

OBJECTIVE: 3.7.4 to Python 3.9.0 under OSX. Then reestablish virtualenvs.

1.  Make sure no virtual environment is running. (Run "deactivate" if necessary).
    Then note the current version of Python 2 on the laptop:

    $ python --version
    Python 2.7.16

2.  Work on abjad3. Then note version of Python 3 used to created abjad3:

    $ workon abjad3
    $ python --version
    Python 3.7.4

3.  Download the new Python installer and install:

    https://www.python.org/downloads/mac-osx/

4.  Double-click the installer and install.

5.  Note that the version of Python 2 has not changed:

    $ python --version
    Python 2.7.16

6.  And note that the version of Python powering abjad3 hasn't changed either:

    $ workon abjad3
    $ python --version
    Python 3.7.4

7.  Note that the location of the new version:

    $ ls /Library/Frameworks/Python.framework/Versions/
    3.6     3.7     3.9     Current

8.  Edit ~/.profile. Make sure the Python package installer added these lines:

    PATH="/Library/Frameworks/Python.framework/Versions/3.9/bin:${PATH}"
    export PATH

9.  Restart the terminal.

10. Confirm that python3 now points to 3.9:

    $ python3 --version
    Python 3.9.0

11. Note installed versions of pip and pip3:

    $ pip --version
    pip 10.0.1 from /Library/Python/2.7/site-packages/pip-10.0.1-py2.7.egg/pip (python 2.7)
    $ pip3 --version
    pip 20.2.3 from /Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/pip (python 3.9)

12. Note installed version of virtualenv:

    $ virtualenv --version
    16.0.0

    $ which virtualenvwrapper.sh
    /usr/local/bin/virtualenvwrapper.sh

13. Trash the old version of abjad3:

    $ trash ~/.virtualenvs/abjad3/
    Moving '/Users/trevorbaca/.virtualenvs/abjad3/' to '/Users/trevorbaca/.Trash'

    $ deactivate

    $ python --version
    2.7.16

14. Attempting to remake abjad3 can error:

    $ mkvirtualenv -p python3 abjad3
    Running virtualenv with interpreter /usr/local/bin/python3
    Using base prefix '/Library/Frameworks/Python.framework/Versions/3.9'
    /Library/Python/2.7/site-packages/virtualenv.py:1041: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
    import imp
    New python executable in /Users/trevorbaca/.virtualenvs/abjad3/bin/python3
    Not overwriting existing python script /Users/trevorbaca/.virtualenvs/abjad3/bin/python (you must use /Users/trevorbaca/.virtualenvs/abjad3/bin/python3)
    ERROR: The executable /Users/trevorbaca/.virtualenvs/abjad3/bin/python3 is not functioning
    ERROR: It thinks sys.prefix is '/Library/Frameworks/Python.framework/Versions/3.9' (should be '/Users/trevorbaca/.virtualenvs/abjad3')
    ERROR: virtualenv is not compatible with this system or executable

15. Upgrade pip under Python 2:

    $ sudo -H pip install --upgrade pip
    Password:
    Collecting pip
    Downloading https://files.pythonhosted.org/packages/cb/28/91f26bd088ce8e22169032100d4260614fc3da435025ff389ef1d396a433/pip-20.2.4-py2.py3-none-any.whl (1.5MB)
        100% |████████████████████████████████| 1.5MB 9.8MB/s 
    matplotlib 1.3.1 requires nose, which is not installed.
    matplotlib 1.3.1 requires tornado, which is not installed.
    Installing collected packages: pip
    Found existing installation: pip 10.0.1
        Uninstalling pip-10.0.1:
        Successfully uninstalled pip-10.0.1
    Successfully installed pip-20.2.4
    You are using pip version 20.2.4, however version 20.3b1 is available.
    You should consider upgrading via the 'pip install --upgrade pip' command.

16. Upgrade virtualenv:

    $ sudo -H pip install --upgrade virtualenv
    DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. pip 21.0 will drop support for Python 2.7 in January 2021. More details about Python 2 support in pip can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support pip 21.0 will remove support for this functionality.
    Collecting virtualenv
    Downloading virtualenv-20.1.0-py2.py3-none-any.whl (4.9 MB)
        |████████████████████████████████| 4.9 MB 3.0 MB/s 
    Collecting distlib<1,>=0.3.1
    Downloading distlib-0.3.1-py2.py3-none-any.whl (335 kB)
        |████████████████████████████████| 335 kB 15.7 MB/s 
    Collecting appdirs<2,>=1.4.3
    Downloading appdirs-1.4.4-py2.py3-none-any.whl (9.6 kB)
    Collecting pathlib2<3,>=2.3.3; python_version < "3.4" and sys_platform != "win32"
    Downloading pathlib2-2.3.5-py2.py3-none-any.whl (18 kB)
    Collecting filelock<4,>=3.0.0
    Downloading filelock-3.0.12.tar.gz (8.5 kB)
    Collecting importlib-metadata<3,>=0.12; python_version < "3.8"
    Downloading importlib_metadata-2.0.0-py2.py3-none-any.whl (31 kB)
    Collecting importlib-resources>=1.0; python_version < "3.7"
    Downloading importlib_resources-3.3.0-py2.py3-none-any.whl (26 kB)
    Requirement already satisfied, skipping upgrade: six<2,>=1.9.0 in /Library/Python/2.7/site-packages (from virtualenv) (1.11.0)
    Collecting scandir; python_version < "3.5"
    Downloading scandir-1.10.0.tar.gz (33 kB)
    Collecting configparser>=3.5; python_version < "3"
    Downloading configparser-4.0.2-py2.py3-none-any.whl (22 kB)
    Collecting zipp>=0.5
    Downloading zipp-1.2.0-py2.py3-none-any.whl (4.8 kB)
    Collecting contextlib2; python_version < "3"
    Downloading contextlib2-0.6.0.post1-py2.py3-none-any.whl (9.8 kB)
    Collecting singledispatch; python_version < "3.4"
    Downloading singledispatch-3.4.0.3-py2.py3-none-any.whl (12 kB)
    Collecting typing; python_version < "3.5"
    Downloading typing-3.7.4.3-py2-none-any.whl (26 kB)
    Using legacy 'setup.py install' for filelock, since package 'wheel' is not installed.
    Using legacy 'setup.py install' for scandir, since package 'wheel' is not installed.
    Installing collected packages: distlib, appdirs, scandir, pathlib2, filelock, configparser, contextlib2, zipp, importlib-metadata, singledispatch, typing, importlib-resources, virtualenv
        Running setup.py install for scandir ... done
        Running setup.py install for filelock ... done
    Attempting uninstall: virtualenv
        Found existing installation: virtualenv 16.0.0
        Uninstalling virtualenv-16.0.0:
        Successfully uninstalled virtualenv-16.0.0
    Successfully installed appdirs-1.4.4 configparser-4.0.2 contextlib2-0.6.0.post1 distlib-0.3.1 filelock-3.0.12 importlib-metadata-2.0.0 importlib-resources-3.3.0 pathlib2-2.3.5 scandir-1.10.0 singledispatch-3.4.0.3 typing-3.7.4.3 virtualenv-20.1.0 zipp-1.2.0

    $ virtualenv --version
    virtualenv 20.1.0 from /Library/Python/2.7/site-packages/virtualenv/__init__.pyc

17. Remake the abjad3 virtualenv:

    $ mkvirtualenv -p python3 abjad3
    created virtual environment CPython3.9.0.final.0-64 in 4748ms
    creator CPython3Posix(dest=/Users/trevorbaca/.virtualenvs/abjad3, clear=False, global=False)
    seeder FromAppData(download=False, pip=bundle, wheel=bundle, setuptools=bundle, via=copy, app_data_dir=/Users/trevorbaca/Library/Application Support/virtualenv)
        added seed packages: pip==20.2.4, setuptools==50.3.2, wheel==0.35.1
    activators PythonActivator,FishActivator,XonshActivator,CShellActivator,PowerShellActivator,BashActivator
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/predeactivate
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/postdeactivate
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/preactivate
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/postactivate
    virtualenvwrapper.user_scripts creating /Users/trevorbaca/.virtualenvs/abjad3/bin/get_env_details

    $ python --version
    Python 3.9.0

18. Install mypy:

    $ pip install mypy
    Collecting mypy
    Downloading mypy-0.790-py3-none-any.whl (2.4 MB)
        |████████████████████████████████| 2.4 MB 3.1 MB/s 
    Collecting typing-extensions>=3.7.4
    Downloading typing_extensions-3.7.4.3-py3-none-any.whl (22 kB)
    Collecting typed-ast<1.5.0,>=1.4.0
    Downloading typed_ast-1.4.1-cp39-cp39-macosx_10_9_x86_64.whl (225 kB)
        |████████████████████████████████| 225 kB 12.1 MB/s 
    Collecting mypy-extensions<0.5.0,>=0.4.3
    Using cached mypy_extensions-0.4.3-py2.py3-none-any.whl (4.5 kB)
    Installing collected packages: typing-extensions, typed-ast, mypy-extensions, mypy
    ERROR: After October 2020 you may experience errors when installing or updating packages. This is because pip will change the way that it resolves dependency conflicts.

    We recommend you use --use-feature=2020-resolver to test your packages with the new resolver before it becomes the default.

    abjad-ide 0.0.0 requires abjad, which is not installed.
    abjad-ide 0.0.0 requires roman, which is not installed.
    abjad-ide 0.0.0 requires sphinx, which is not installed.
    abjad-ide 0.0.0 requires sphinx-rtd-theme, which is not installed.
    abjad-ide 0.0.0 requires uqbar>=0.2.13, which is not installed.
    Successfully installed mypy-0.790 mypy-extensions-0.4.3 typed-ast-1.4.1 typing-extensions-3.7.4.3

19. Reinstall Abjad in the newly reestablished virtual environment. The [test]
    option includes black, flake8, isort, mypy and pytest will be included:

    (abjad3) ✔ ~/abjad [trevor/dev|✔] 
    13:02 $ pip install -e .[test]
    Obtaining file:///Users/trevorbaca/abjad
    Collecting ply
    Using cached ply-3.11-py2.py3-none-any.whl (49 kB)
    Collecting quicktions>=1.3
    Using cached quicktions-1.11.tar.gz (218 kB)
    Collecting roman
    Downloading roman-3.3-py2.py3-none-any.whl (3.9 kB)
    Collecting uqbar<0.5.0,>=0.4.4
    Downloading uqbar-0.4.8.tar.gz (56 kB)
        |████████████████████████████████| 56 kB 2.2 MB/s 
    Collecting black==20.8b1
    Downloading black-20.8b1.tar.gz (1.1 MB)
        |████████████████████████████████| 1.1 MB 6.1 MB/s 
    Installing build dependencies ... done
    Getting requirements to build wheel ... done
        Preparing wheel metadata ... done
    Collecting flake8
    Downloading flake8-3.8.4-py2.py3-none-any.whl (72 kB)
        |████████████████████████████████| 72 kB 2.4 MB/s 
    Collecting isort
    Downloading isort-5.6.4-py3-none-any.whl (98 kB)
        |████████████████████████████████| 98 kB 7.9 MB/s 
    < ... snip ... >
    Building wheels for collected packages: quicktions, uqbar, black, MarkupSafe
    Building wheel for quicktions (setup.py) ... done
    Created wheel for quicktions: filename=quicktions-1.11-cp39-cp39-macosx_10_9_x86_64.whl size=75881 sha256=149037017181b294858aef373e859d047de2d8c2856ecbe5e99f1dde1f75f511
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/89/f7/7d/4abee593ca1642f3b6f43754692825b63df78b6c654d404e10
    Building wheel for uqbar (setup.py) ... done
    Created wheel for uqbar: filename=uqbar-0.4.8-py3-none-any.whl size=82602 sha256=e0fab04482c1e05e7f46d6a9e1255b76b60ec46b64416bfd10911bb27e787117
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/63/d7/aa/22fbc4783d140f094142f55b09a8f3438124ce84e14efde769
    Building wheel for black (PEP 517) ... done
    Created wheel for black: filename=black-20.8b1-py3-none-any.whl size=124186 sha256=b672033f3c9440f347425f773324193d6b7e537ce604bbf02c1b6785dbc5808a
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/4e/57/9a/e704bdd859ee892dc46fff03fd499422dc9e99fd9bd5c446d3
    Building wheel for MarkupSafe (setup.py) ... done
    Created wheel for MarkupSafe: filename=MarkupSafe-1.1.1-cp39-cp39-macosx_10_9_x86_64.whl size=16382 sha256=188a97cbeea5fd4f324d1dbfc64373b55e33fa2e287d2805ec1d86a926cb6b1f
    Stored in directory: /Users/trevorbaca/Library/Caches/pip/wheels/e0/19/6f/6ba857621f50dc08e084312746ed3ebc14211ba30037d5e44e
    Successfully built quicktions uqbar black MarkupSafe
    Installing collected packages: ply, quicktions, roman, idna, certifi, chardet, urllib3, requests, pytz, babel, sphinxcontrib-applehelp, six, pyparsing, packaging, Pygments, snowballstemmer, MarkupSafe, Jinja2, alabaster, imagesize, sphinxcontrib-devhelp, sphinxcontrib-qthelp, docutils, sphinxcontrib-serializinghtml, sphinxcontrib-jsmath, sphinxcontrib-htmlhelp, Sphinx, Unidecode, regex, toml, click, appdirs, pathspec, black, sphinx-rtd-theme, uqbar, pyflakes, pycodestyle, mccabe, flake8, isort, pluggy, attrs, iniconfig, py, pytest, coverage, pytest-cov, sphinx-autodoc-typehints, Abjad
    Attempting uninstall: Abjad
        Found existing installation: Abjad 3.1
        Not uninstalling abjad at /Users/trevorbaca/abjad, outside environment /Users/trevorbaca/.virtualenvs/abjad3
        Can't uninstall 'Abjad'. No files were found to uninstall.
    Running setup.py develop for Abjad
    Successfully installed Abjad Jinja2-2.11.2 MarkupSafe-1.1.1 Pygments-2.7.2 Sphinx-3.3.0 Unidecode-1.1.1 alabaster-0.7.12 appdirs-1.4.4 attrs-20.3.0 babel-2.8.0 black-20.8b1 certifi-2020.6.20 chardet-3.0.4 click-7.1.2 coverage-5.3 docutils-0.16 flake8-3.8.4 idna-2.10 imagesize-1.2.0 iniconfig-1.1.1 isort-5.6.4 mccabe-0.6.1 packaging-20.4 pathspec-0.8.0 pluggy-0.13.1 ply-3.11 py-1.9.0 pycodestyle-2.6.0 pyflakes-2.2.0 pyparsing-2.4.7 pytest-6.1.2 pytest-cov-2.10.1 pytz-2020.4 quicktions-1.11 regex-2020.10.28 requests-2.24.0 roman-3.3 six-1.15.0 snowballstemmer-2.0.0 sphinx-autodoc-typehints-1.11.1 sphinx-rtd-theme-0.5.0 sphinxcontrib-applehelp-1.0.2 sphinxcontrib-devhelp-1.0.2 sphinxcontrib-htmlhelp-1.0.3 sphinxcontrib-jsmath-1.0.1 sphinxcontrib-qthelp-1.0.3 sphinxcontrib-serializinghtml-1.1.4 toml-0.10.2 uqbar-0.4.8 urllib3-1.25.11

    (abjad3) ✔ ~/abjad [trevor/dev|✔] 
    13:03 $ 

20. Visit and reinstall Abjad extensions in abjad3:

    cd ~/abjad-ext-ipython
    pip install -e .

    cd ~/abjad-ext-rmakers
    pip install -e .

    cd ~/abjad-ext-tonality
    pip install -e .

    Confirmation messaging will look like this in each clone:

    Obtaining file:///Users/trevorbaca/abjad-ext-tonality
    < ... snip ... >
    Successfully installed abjad-ext-tonality

21. Reinstall Bača in abjad3:

    ✔ ~/baca [master|✚ 2] 
    17:07 $ pip install -e .
    Obtaining file:///Users/trevorbaca/baca
    Requirement already satisfied: abjad in /Users/trevorbaca/abjad (from Ba-a-Composition-API==0.0.0) (3.1)
    Requirement already satisfied: mypy in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from Ba-a-Composition-API==0.0.0) (0.790)
    Requirement already satisfied: roman in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from Ba-a-Composition-API==0.0.0) (3.3)
    Requirement already satisfied: sphinx in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from Ba-a-Composition-API==0.0.0) (3.3.0)
    Requirement already satisfied: sphinx-rtd-theme in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from Ba-a-Composition-API==0.0.0) (0.5.0)
    Requirement already satisfied: uqbar>=0.2.13 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from Ba-a-Composition-API==0.0.0) (0.4.8)
    Requirement already satisfied: ply in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from abjad->Ba-a-Composition-API==0.0.0) (3.11)
    Requirement already satisfied: quicktions>=1.3 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from abjad->Ba-a-Composition-API==0.0.0) (1.11)
    Requirement already satisfied: typed-ast<1.5.0,>=1.4.0 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from mypy->Ba-a-Composition-API==0.0.0) (1.4.1)
    Requirement already satisfied: typing-extensions>=3.7.4 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from mypy->Ba-a-Composition-API==0.0.0) (3.7.4.3)
    Requirement already satisfied: mypy-extensions<0.5.0,>=0.4.3 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from mypy->Ba-a-Composition-API==0.0.0) (0.4.3)
    Requirement already satisfied: babel>=1.3 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (2.8.0)
    Requirement already satisfied: alabaster<0.8,>=0.7 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (0.7.12)
    Requirement already satisfied: docutils>=0.12 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (0.16)
    Requirement already satisfied: requests>=2.5.0 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (2.24.0)
    Requirement already satisfied: sphinxcontrib-serializinghtml in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (1.1.4)
    Requirement already satisfied: sphinxcontrib-applehelp in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (1.0.2)
    Requirement already satisfied: imagesize in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (1.2.0)
    Requirement already satisfied: setuptools in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (50.3.2)
    Requirement already satisfied: snowballstemmer>=1.1 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (2.0.0)
    Requirement already satisfied: Jinja2>=2.3 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (2.11.2)
    Requirement already satisfied: sphinxcontrib-qthelp in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (1.0.3)
    Requirement already satisfied: sphinxcontrib-htmlhelp in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (1.0.3)
    Requirement already satisfied: sphinxcontrib-devhelp in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (1.0.2)
    Requirement already satisfied: sphinxcontrib-jsmath in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (1.0.1)
    Requirement already satisfied: packaging in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (20.4)
    Requirement already satisfied: Pygments>=2.0 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from sphinx->Ba-a-Composition-API==0.0.0) (2.7.2)
    Requirement already satisfied: black>=19.10b0 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from uqbar>=0.2.13->Ba-a-Composition-API==0.0.0) (20.8b1)
    Requirement already satisfied: Unidecode>=1.0.0 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from uqbar>=0.2.13->Ba-a-Composition-API==0.0.0) (1.1.1)
    Requirement already satisfied: pytz>=2015.7 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from babel>=1.3->sphinx->Ba-a-Composition-API==0.0.0) (2020.4)
    Requirement already satisfied: chardet<4,>=3.0.2 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from requests>=2.5.0->sphinx->Ba-a-Composition-API==0.0.0) (3.0.4)
    Requirement already satisfied: certifi>=2017.4.17 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from requests>=2.5.0->sphinx->Ba-a-Composition-API==0.0.0) (2020.6.20)
    Requirement already satisfied: urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from requests>=2.5.0->sphinx->Ba-a-Composition-API==0.0.0) (1.25.11)
    Requirement already satisfied: idna<3,>=2.5 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from requests>=2.5.0->sphinx->Ba-a-Composition-API==0.0.0) (2.10)
    Requirement already satisfied: MarkupSafe>=0.23 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from Jinja2>=2.3->sphinx->Ba-a-Composition-API==0.0.0) (1.1.1)
    Requirement already satisfied: six in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from packaging->sphinx->Ba-a-Composition-API==0.0.0) (1.15.0)
    Requirement already satisfied: pyparsing>=2.0.2 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from packaging->sphinx->Ba-a-Composition-API==0.0.0) (2.4.7)
    Requirement already satisfied: regex>=2020.1.8 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from black>=19.10b0->uqbar>=0.2.13->Ba-a-Composition-API==0.0.0) (2020.10.28)
    Requirement already satisfied: toml>=0.10.1 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from black>=19.10b0->uqbar>=0.2.13->Ba-a-Composition-API==0.0.0) (0.10.2)
    Requirement already satisfied: pathspec<1,>=0.6 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from black>=19.10b0->uqbar>=0.2.13->Ba-a-Composition-API==0.0.0) (0.8.0)
    Requirement already satisfied: click>=7.1.2 in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from black>=19.10b0->uqbar>=0.2.13->Ba-a-Composition-API==0.0.0) (7.1.2)
    Requirement already satisfied: appdirs in /Users/trevorbaca/.virtualenvs/abjad3/lib/python3.9/site-packages (from black>=19.10b0->uqbar>=0.2.13->Ba-a-Composition-API==0.0.0) (1.4.4)
    Installing collected packages: Ba-a-Composition-API
    Running setup.py develop for Ba-a-Composition-API
    Successfully installed Ba-a-Composition-API

22. Run tests:

    cdj
    ..
    make check
    make pytest

    cdb
    ..
    make check
    make pytest

    cdi
    ..
    make check
    make pytest

23. Rebuild APIs:

    apim; apib; apis; apii


### OLDER ###



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
