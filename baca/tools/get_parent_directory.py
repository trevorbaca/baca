# -*- coding: utf-8 -*-
import os


def get_parent_directory(location):
    '''Gets parent directory.

    Pass `location` as a ``__file__`` instance.

    Returns absolute path of parent directory of `location`.
    '''

    location = os.path.abspath(location)
    dirname = os.path.dirname(location)
    dirpath = dirname.split(os.sep)
    parent_directory = dirpath[:-1]
    parent_directory.insert(0, '/')
    parent_directory = os.path.join(*parent_directory)
    return parent_directory