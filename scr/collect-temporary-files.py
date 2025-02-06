#! /usr/bin/env python
import os
import pathlib

import baca


def main():
    directory = os.getcwd()
    directory = pathlib.Path(directory)
    assert "builds" in directory.parts, repr(directory)
    _sections_directory = directory / "_sections"
    baca.build.collect_temporary_files(_sections_directory)


if __name__ == "__main__":
    main()
