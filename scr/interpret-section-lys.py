#! /usr/bin/env python
import os
import pathlib

import baca


def main():
    current_directory = pathlib.Path(os.getcwd())
    contents_directory = baca.path.get_contents_directory(current_directory)
    sections_directory = contents_directory / "sections"
    for path in sorted(sections_directory.glob("[0-9]*")):
        if not path.is_dir():
            continue
        os.chdir(path)
        os.system("mylily music.ly")
        print()


if __name__ == "__main__":
    main()
