Python 3 installation
=====================

OBJECTIVE. Install Python 3. Create a Python 3 virtualenv for Abjad development.

Starting with ...

    brew install python3

... which builds things for six or seven minutes and then ends with ...

    <SNIP>
    ==> ./configure --prefix=/usr/local/Cellar/python3/3.5.1 --enable-ipv6 --dataroo
    ==> make
    ==> make install PYTHONAPPSDIR=/usr/local/Cellar/python3/3.5.1
    ==> make frameworkinstallextras PYTHONAPPSDIR=/usr/local/Cellar/python3/3.5.1/sh
    ==> Downloading https://pypi.python.org/packages/source/s/setuptools/setuptools-
    ######################################################################## 100.0%
    ==> Downloading https://pypi.python.org/packages/source/p/pip/pip-8.0.2.tar.gz
    ######################################################################## 100.0%
    ==> Downloading https://pypi.python.org/packages/source/w/wheel/wheel-0.26.0.tar
    ######################################################################## 100.0%
    Error: An unexpected error occurred during the `brew link` step
    The formula built, but is not symlinked into /usr/local
    Permission denied - /usr/local/Frameworks
    Error: Permission denied - /usr/local/Frameworks

... which makes me try ...

    09:13 $ sudo brew install python3
    Password:
    Error: Cowardly refusing to 'sudo brew install'
    You can use brew with sudo, but only if the brew executable is owned by root.
    However, this is both not recommended and completely unsupported so do so at
    your own risk.

... which apparently isn't the recommended way to go.

So Stackoverflow leads me to ...

    http://stackoverflow.com/questions/16432071/how-to-fix-homebrew-permissions

... which suggests:

    sudo chown -R "$USER":admin /usr/local
    sudo chown -R "$USER":admin /Library/Caches/Homebrew

Ownership of /usr/local is currently root:

    09:24 $ ls -l /usr
    total 0
    drwxr-xr-x     3 root  wheel    102 Aug 29 21:10 adic
    drwxr-xr-x  1057 root  wheel  35938 Oct  3 13:35 bin
    drwxr-xr-x   275 root  wheel   9350 Oct  3 13:40 lib
    drwxr-xr-x   197 root  wheel   6698 Oct  3 13:35 libexec
    drwxr-xr-x    19 root  wheel    646 Oct  3 13:40 local
    drwxr-xr-x   245 root  wheel   8330 Oct  3 13:35 sbin
    drwxr-xr-x    46 root  wheel   1564 Oct  3 13:35 share
    drwxr-xr-x     4 root  wheel    136 Sep 13 19:51 standalone

So ...

    09:24 $ sudo chown -R "$USER":admin /usr/local
    Password:
    
... which takes a few seconds to recurse and completes without error.

My /Library/Caches has no Homebrew subdirectory. So I ignore the second step
recommended at Stackoverflow.

Rebrewing Python 3 gives ...

    09:32 $ brew install python3
    Warning: python3-3.5.1 already installed, it's just not linked
    Warning: You are using OS X 10.12.
    We do not provide support for this pre-release version.
    You may encounter build failures or other breakages.

... which makes sense because the previous brew probably completed but just
couldn't link.

So on a hunch I try ...

    09:32 $ brew link python3
    Linking /usr/local/Cellar/python3/3.5.1... 19 symlinks created

... which completes without error.

Python 3 is now resident on my machine ...

    09:35 $ which python3
    /usr/local/bin/python3

... and starts correctly:

    09:35 $ python3
    Python 3.5.1 (default, Oct  6 2016, 09:12:24) 
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.

Importing Abjad fails ...

    09:35 $ python3
    Python 3.5.1 (default, Oct  6 2016, 09:12:24) 
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> 2 ** 38
    274877906944
    >>> import abjad
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/Users/trevorbaca/Documents/abjad/abjad/__init__.py", line 31, in <module>
        from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/__init__.py", line 2, in <module>
        import six
    ImportError: No module named 'six'

... but will have to be debugged later. (Probably just need to "reinstall"
Abjad under Python 3. Will do later.)

Next up is running the Abjad tests under Python 2.7.10 to make sure that
Python 3 installation didn't break Abjad under Python 2.7.10.

All Abjad tests continue to pass under Python 2.7.10 after brewing Python 3.

So back to debugging Abjad under Python 3.

Maybe just need to install Abjad under Python 3? Abjad's dependency tree should
take care of things like the six module.

So that raises the question of how to install Abjad under Python 3.

Don't wanna get conflicting Abjad installs. So trying under a virtualenv:

    09:45 $ deactivate
    ✔ ~/Documents/abjad/abjad [trevor/dev|✔] 
    09:50 $ virtualenv -p python3 abjad3
    Running virtualenv with interpreter /usr/local/Cellar/python3
    Traceback (most recent call last):
    File "/usr/local/bin/virtualenv", line 11, in <module>
        sys.exit(main())
    File "/Library/Python/2.7/site-packages/virtualenv.py", line 667, in main
        popen = subprocess.Popen([interpreter, file] + sys.argv[1:], env=env)
    File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 710, in __init__
        errread, errwrite)
    File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 1335, in _execute_child
        raise child_exception
    OSError: [Errno 13] Permission denied

Hmmm ... I'm not so sure about /usr/local/Cellar/python3. Because ...

    09:52 $ which python3
    /usr/local/bin/python3

... suggests that "my" Python 3 is /usr/local/bin/python3 instead of
/usr/local/Cellar/python3. Although /usr/local/Cellar/python3 does, in fact,
exist:

    09:52 $ ls /usr/local/Cellar
    ack             gdbm            libogg          makedepend      speex
    bash-completion graphviz        libpng          openssl         sqlite
    bash-git-prompt imagemagick     libtiff         pkg-config      timidity
    flac            jpeg            libtool         python3         xz
    freetype        libao           libvorbis       readline

On a hunch ...

    ✔ ~/Documents/abjad/abjad [trevor/dev|✔] 
    09:53 $ virtualenv --python=/usr/local/bin/python3 abjad3
    Running virtualenv with interpreter /usr/local/bin/python3
    Using base prefix '/usr/local/Cellar/python3/3.5.1/Frameworks/Python.framework/Versions/3.5'
    New python executable in /Users/trevorbaca/Documents/abjad/abjad/abjad3/bin/python3
    Also creating executable in /Users/trevorbaca/Documents/abjad/abjad/abjad3/bin/python
    Installing setuptools, pip, wheel...done.

... which creates the abjad3 virtualenv not in ~/Envs but in
~/Documents/abjad/abjad! Gargh.

I trash the spurious abjad3 virtualenv.

Maybe used the wrong virtualenv command? Should've used "mkvirtualenv" instead
of "virtualenv"?

Starting with ...

    ✔ ~/Desktop 
    10:05 $ mkvirtualenv -p python3 abjad3
    Running virtualenv with interpreter /usr/local/Cellar/python3
    Traceback (most recent call last):
    File "/usr/local/bin/virtualenv", line 11, in <module>
        sys.exit(main())
    File "/Library/Python/2.7/site-packages/virtualenv.py", line 667, in main
        popen = subprocess.Popen([interpreter, file] + sys.argv[1:], env=env)
    File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 710, in __init__
        errread, errwrite)
    File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 1335, in _execute_child
        raise child_exception
    OSError: [Errno 13] Permission denied

... and then switching, again, to ...

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

... which appears to work.

Attempting to import Abjad in the abjad3 virtualenv ...

    (abjad3) ✔ ~/Desktop 
    10:07 $ python
    Python 3.5.1 (default, Oct  6 2016, 09:12:24) 
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import abjad
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/Users/trevorbaca/Documents/abjad/abjad/__init__.py", line 31, in <module>
        from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/__init__.py", line 2, in <module>
        import six
    ImportError: No module named 'six'

... gives the same import error.

Which probably means I just need to install Abjad "fresh" in the abjad3
virtualenv.

Our install instructions at ...

    https://github.com/Abjad/abjad

... summary like this:

    To recap, a complete development installation of Abjad within a virtual
    environment requires the following steps:

    * Create and activate a new virtual environment
    * Clone Abjad somewhere and cd into the root of the cloned repository
    * Install Abjad and its development / IPython dependencies

Ok, now a challenge. Because I have a clone of the Abjad repository that's been
sitting around for years:

    (abjad3) ✔ ~/Documents/abjad [trevor/dev|✔] 
    10:29 $ git st
    On branch trevor/dev
    Your branch is up-to-date with 'origin/trevor/dev'.
    nothing to commit, working directory clean

So do I clone the Abjad repo again? Or will my existing clone work?

Looking at our development install instructions again, I get confused about the
difference between cloning and installing, steps 2 and 3:

    * Create and activate a new virtual environment
    * Clone Abjad somewhere and cd into the root of the cloned repository
    * Install Abjad and its development / IPython dependencies

I'm gonna go with the idea that (perhaps) my years-old clone of the Abjad repo
is fine for my abjad3 virtualenv. And that all I need to do (hopefully) is
"install" Abjad in my existing clone. So ...

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

... which does a ton of stuff without error, and appears to work.

Trying Abjad import again:

    (abjad3) ✔ ~/Documents/abjad [master|✔] 
    10:34 $ python
    Python 3.5.1 (default, Oct  6 2016, 09:12:24) 
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import abjad
    >>>

Unbelievable. Works!

And ...

    (abjad3) ✔ ~/Documents/abjad [master|✔] 
    10:36 $ abjad
    Abjad 2.19 (development)
    >>> note = Note("c'4")
    >>> show(note)

... WORKS!

What about the tests?

Running ...

    (abjad3) ✔ ~/Documents/abjad/abjad [master|✔] 
    10:40 $ py.test -rf

... works but shows that four tests fail, at least one or two of which look to
be IDE-related ...

        @staticmethod
        def _get_public_function_names_in_module(module_file):
            r'''Collects and returns all public functions defined in
                module_file.
                '''
            result = []
            module_file = module_file.replace(os.sep, '.')
    >       mod = __import__(module_file, fromlist=['*'])
    E         File "/Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/AbjadIDE.py", line 575
    E           except NameError, e:
    E                           ^
    E       SyntaxError: invalid syntax

    tools/systemtools/ImportManager.py:25: SyntaxError
    ============ 4 failed, 10181 passed, 526 skipped in 245.66 seconds =============

... which probably means I need to "reinstall" the IDE in my abjad3 virtualenv,
similarly to how I "reinstalled" Abjad in my abjad3 virtualenv.

Note, too, that using ajv (to build the API or run the doctests) errors at the
same line (575) in the IDE:

    10:42 $ ajv doctest
    Traceback (most recent call last):
    File "/Users/trevorbaca/Envs/abjad3/bin/ajv", line 11, in <module>
        load_entry_point('Abjad', 'console_scripts', 'ajv')()
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/commandlinetools/run_ajv.py", line 11, in run_ajv
        commandlinetools.AbjDevScript()()
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/commandlinetools/AbjDevScript.py", line 43, in __call__
        self._process_args(args)
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/commandlinetools/AbjDevScript.py", line 116, in _process_args
        instance(unknown_args)
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/commandlinetools/CommandlineScript.py", line 72, in __call__
        self._process_args(args)
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/commandlinetools/DoctestScript.py", line 97, in _process_args
        globs = self._get_namespace()
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/commandlinetools/DoctestScript.py", line 71, in _get_namespace
        ide_module = importlib.import_module('ide')
    File "/Users/trevorbaca/Envs/abjad3/lib/python3.5/importlib/__init__.py", line 126, in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
    File "<frozen importlib._bootstrap>", line 986, in _gcd_import
    File "<frozen importlib._bootstrap>", line 969, in _find_and_load
    File "<frozen importlib._bootstrap>", line 958, in _find_and_load_unlocked
    File "<frozen importlib._bootstrap>", line 673, in _load_unlocked
    File "<frozen importlib._bootstrap_external>", line 662, in exec_module
    File "<frozen importlib._bootstrap>", line 222, in _call_with_frames_removed
    File "/Users/trevorbaca/Documents/abjad-ide/ide/__init__.py", line 70, in <module>
        from ide.tools import idetools
    File "/Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/__init__.py", line 7, in <module>
        globals(),
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/systemtools/ImportManager.py", line 245, in import_structured_package
        ignored_names=ignored_names,
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/systemtools/ImportManager.py", line 190, in import_public_names_from_path_into_namespace
        submodule_name)
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/systemtools/ImportManager.py", line 25, in _get_public_function_names_in_module
        mod = __import__(module_file, fromlist=['*'])
    File "/Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/AbjadIDE.py", line 575
        except NameError, e:
                        ^
    SyntaxError: invalid syntax

Ok so how to "reinstall" the IDE repo in my abjad3 virtualenv?

A clone of the repo already exists (just like a clone of the Abjad repo already
existed). So perhaps reinstalling with pip will work for the IDE the same it
seems to have for Abjad.

Actually, I have drama with the master branching of my existing IDE clone:

    g(abjad3) ✔ ~/Documents/abjad-ide [master|●1] 
    10:54 $ git st
    On branch master
    Your branch is up-to-date with 'origin/master'.
    Changes not staged for commit:
    (use "git add/rm <file>..." to update what will be committed)
    (use "git checkout -- <file>..." to discard changes in working directory)

        deleted:    ide/scores/red_example_score/red_example_score/segments/segment_01/illustration.pdf

    no changes added to commit (use "git add" and/or "git commit -a")
    (abjad3) ✔ ~/Documents/abjad-ide [master|●1] 
    10:54 $ git checkout ide/scores/red_example_score/red_example_score/segments/segment_01/illustration.pdf
    error: unable to read sha1 file of ide/scores/red_example_score/red_example_score/segments/segment_01/illustration.pdf (fb9ef6e54c6a31e9a87a4f8b8070e8cbd48d24f2)
    (abjad3) ✘-255 ~/Documents/abjad-ide [master|●1] 
    10:54 $ git checkout ide/scores/red_example_score/red_example_score/segments/segment_01/illustration.pdf
    error: unable to read sha1 file of ide/scores/red_example_score/red_example_score/segments/segment_01/illustration.pdf (fb9ef6e54c6a31e9a87a4f8b8070e8cbd48d24f2)
    (abjad3) ✘-255 ~/Documents/abjad-ide [master|●1] 
    10:54 $ git st
    On branch master
    Your branch is up-to-date with 'origin/master'.
    Changes not staged for commit:
    (use "git add/rm <file>..." to update what will be committed)
    (use "git checkout -- <file>..." to discard changes in working directory)

        deleted:    ide/scores/red_example_score/red_example_score/segments/segment_01/illustration.pdf

    no changes added to commit (use "git add" and/or "git commit -a")
    (abjad3) ✔ ~/Documents/abjad-ide [master|●1] 
    10:55 $ git reset --hard HEAD
    error: unable to read sha1 file of ide/scores/red_example_score/red_example_score/segments/segment_01/illustration.pdf (fb9ef6e54c6a31e9a87a4f8b8070e8cbd48d24f2)
    fatal: Could not reset index file to revision 'HEAD'.

This is frustrating.

Looks like the same problem with macOS 10.12 install I had with all the other
repos cloned into ~/Documents.

So I have two branches checked out: master and spiel-der-dornen-cleanup. The
cleanup branch (which is really a development branch) is up to date with
GitHub's servers. So I feel like just blowing away my IDE repo and recloning.
Only hesitation would be losing any commits in the cleanup branch. But the
cleanup branch should be re-checkout-able. So I trash my IDE repo and reclone.
Which works fine:

    (abjad3) ✔ ~/Documents/abjad-ide [master|✔] 
    11:06 $ git branch
    * master

And checking out the cleanup branch works fine:

    (abjad3) ✔ ~/Documents/abjad-ide [master|✔] 
    11:07 $ git checkout spiel-der-dornen-cleanup
    Branch spiel-der-dornen-cleanup set up to track remote branch spiel-der-dornen-cleanup from origin.
    Switched to a new branch 'spiel-der-dornen-cleanup'
    (abjad3) ✔ ~/Documents/abjad-ide [spiel-der-dornen-cleanup|✔] 

The reclone by itself isn't enough to successfully import the IDE:

    (abjad3) ✔ ~/Desktop 
    11:08 $ start-abjad-ide 
    Traceback (most recent call last):
    File "/Users/trevorbaca/Documents/abjad-ide/ide/scr/start-abjad-ide", line 3, in <module>
        import ide
    File "/Users/trevorbaca/Documents/abjad-ide/ide/__init__.py", line 70, in <module>
        from ide.tools import idetools
    File "/Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/__init__.py", line 7, in <module>
        globals(),
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/systemtools/ImportManager.py", line 245, in import_structured_package
        ignored_names=ignored_names,
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/systemtools/ImportManager.py", line 190, in import_public_names_from_path_into_namespace
        submodule_name)
    File "/Users/trevorbaca/Documents/abjad/abjad/tools/systemtools/ImportManager.py", line 25, in _get_public_function_names_in_module
        mod = __import__(module_file, fromlist=['*'])
    File "/Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/AbjadIDE.py", line 575
        except NameError, e:
                        ^
    SyntaxError: invalid syntax

Certainly looks like a straight-up syntax incompability with Python 3.

But before changing the source, an attempt at "reinstallation" with pip:

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

... which looks like it did nothing. But which does, in fact, allow the IDE to
start.

All Abjad tests now pass and the API builds.

The IDE starts; the IDE API builds; all IDE doctests pass; but two IDE pytests
fail because of pytest.skip usage:

    (abjad3) ✔ ~/Documents/abjad-ide/ide [master|✔] 
    11:29 $ py.test -rf
    ============================= test session starts ==============================
    platform darwin -- Python 3.5.1, pytest-3.0.3, py-1.4.31, pluggy-0.4.0
    rootdir: /Users/trevorbaca/Documents/abjad-ide, inifile: 
    collected 268 items / 2 errors 

    ==================================== ERRORS ====================================
    ____ ERROR collecting ide/tools/idetools/test/test_AbjadIDE_build_score.py _____
    Using @pytest.skip outside of a test (e.g. as a test function decorator) is not allowed. Use @pytest.mark.skip or @pytest.mark.skipif instead.
    ____ ERROR collecting ide/tools/idetools/test/test_AbjadIDE_run_doctest.py _____
    Using @pytest.skip outside of a test (e.g. as a test function decorator) is not allowed. Use @pytest.mark.skip or @pytest.mark.skipif instead.
    !!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
    =========================== 2 error in 1.41 seconds ============================
    (abjad3) ✘-2 ~/Documents/abjad-ide/ide [master|✔] 

So I change pytest.skip() to pytest.mark.skip() in those two files.

This allows the IDE pytests to run.

But 64 tests fail. The 64 failing tests look like they are all the tests that
touch the filesystem. All raise the same NameError in the IDE IOManager at line
401. For example:

    __________________________ test_Session_is_example_01 __________________________

        def test_Session_is_example_01():
            r'''In scores directory.
            '''
        
            lines = [
                'Abjad IDE - all score directories',
                '',
                '   1: __metadata__.py',
                '   2: Blue Example Score (2013)',
                '   3: Red Example Score (2013)',
                '',
                '      copy (cp)',
                '      new (new)',
                '      remove (rm)',
                '      rename (ren)',
                '',
                '>',
                ]
        
            input_ = 'q'
    >       abjad_ide._start(input_=input_)

    /Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/test/test_Session_is_example.py:27: 
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
    /Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/AbjadIDE.py:2018: in _start
        self._manage_directory(directory)
    /Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/AbjadIDE.py:1609: in _manage_directory
        menu = self._make_main_menu(directory, menu_header)
    /Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/AbjadIDE.py:1127: in _make_main_menu
        paths = self._list_visible_paths(directory)
    /Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/AbjadIDE.py:1025: in _list_visible_paths
        entries = self._filter_by_view(directory, entries)
    /Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/AbjadIDE.py:298: in _filter_by_view
        view = self._read_view(directory)
    /Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/AbjadIDE.py:1804: in _read_view
        view_name = self._get_metadatum(directory, 'view_name')
    /Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/AbjadIDE.py:519: in _get_metadatum
        metadata = self._get_metadata(directory)
    /Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/AbjadIDE.py:507: in _get_metadata
        attribute_names=('metadata',),
    /Users/trevorbaca/Documents/abjad-ide/ide/tools/idetools/IOManager.py:401: in execute_string
        exec(string, local_namespace, local_namespace)
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    >   ???
    E   NameError: name 'abjad' is not defined

    <string>:5: NameError

IDE IOManager.execute_string(string, ...) is raising the NameError. In each
case, the line causing the error is just the 'import abjad' at the top of a
file being reading from the filesystem.

2016-10-11:

Calling make_baca_api.py raises an import error because no inflect module.
Calling `pip install inflect` fixes the problem.
Calling make_baca_api.py now works.
Calling py.test in ~/Documents/baca/baca passes all 56 tests.
Calling `ajv doctest` in ~/Documents/baca/baca gives 128 failures:
    2862 passed, 128 failed out of 2990 tests in 112 modules.
Will back up and fix IDE failures first.

IDE failures now fixed: all tests pass.
Explanation: not sure how I fixed everything. But it all fixed when I created a
PR from my spiel-der-dornen-cleanup development branch and merged everything
from that development branch into master. Took only minimal futzing to do so.
Didn't transcribe into this file. But now all IDE tests pass under my Python 3
virutal environment (abjad3).

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
    Abjad.egg-info   MANIFEST.in      experimental     setup.cfg
    Dockerfile       README.rst       pytest.ini       setup.py
    LICENSE          abjad            requirements.txt tox.ini

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

Some tests fail. But I think everything is working fine.

29 doctests fail:    

    FAILED: tools/datastructuretools/CyclicTuple.py
    FAILED: tools/pitchtools/PitchClassSegment.py
    FAILED: tools/pitchtools/TwelveToneRow.py
    FAILED: tools/rhythmmakertools/EvenDivisionRhythmMaker.py
    FAILED: tools/rhythmmakertools/InciseSpecifier.py
    FAILED: tools/rhythmmakertools/IncisedRhythmMaker.py
    FAILED: tools/rhythmmakertools/TaleaRhythmMaker.py
    12634 passed, 29 failed out of 12663 tests in 898 modules.

22 pytests fail:

    ========= 22 failed, 10165 passed, 528 skipped in 256.44 seconds ==========

I think the failing tests have to do with a recent change to CyclicTuple.
