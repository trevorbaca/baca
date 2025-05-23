#! /usr/bin/env python
import argparse
import os
import pathlib

import baca


def main():
    parser = argparse.ArgumentParser(description="Activate tags in LilyPond files.")
    parser.add_argument(
        "--keep-temporary-files", help="keep .[i]ly files", action="store_true"
    )
    parser.add_argument(
        "--skip-temporary-files", help="skip .[i]ly files", action="store_true"
    )
    arguments = parser.parse_args()
    directory = os.getcwd()
    directory = pathlib.Path(directory)
    baca.build.interpret_build_music(
        directory,
        keep_temporary_files=arguments.keep_temporary_files,
        skip_temporary_files=arguments.skip_temporary_files,
    )


if __name__ == "__main__":
    main()
