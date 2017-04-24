PyPy installation
=================

Objective: install PyPy; create a PyPy virtual environment; run Abjad.

1.  Installation: Go to http://pypy.org/download.html and click the link for
    Mac OS/X binary (64 bit). The pypy2-v5.7.1-osx64.zip archive will download.

2.  Double-click the archive to unzip. The directory pypy2-v5.7.1-osx64
    results. The PyPy binary is located at pypy2-v5.7.1-osx64/bin/pypy.

3.  Move the pypy2-v5.7.1-osx64 directory to ~/opt.

4.  Symlink the PyPy binary to /usr/local/bin

        ln -s ~/opt/pypy2-v5.7.1-osx64/bin/pypy /usr/local/bin/pypy

    Then check to make sure the symlink worked:

        which pypy

5.  Create a PyPy virtual environment:

        virtualenv -p pypy abjadpypy

6.  Work on the PyPy virtual environment:

        workon abjadpypy

7.  Use pip to install Abjad dependencies:

        cd ~/abjad
        pip install -e .[development,ipython]

8.  Start PyPy and import Abjad:

        pypy
        from abjad import *

9.  Run the Abjad tests to confirm installation.
