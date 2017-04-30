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

5.  Reestablish the abjad3 virtual environment:

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
