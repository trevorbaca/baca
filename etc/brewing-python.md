Brewing Python
==============

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
