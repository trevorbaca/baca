#! /usr/bin/env python
import argparse
import os
import pathlib

import baca


def main():
    directory = pathlib.Path(os.getcwd())
    parser = argparse.ArgumentParser(description="Activate tags in LilyPond files.")
    parser.add_argument("--undo", help="deactivate tags", action="store_true")
    arguments = parser.parse_args()
    for name in ("layout.ily", "music.ily", "music.ly"):
        file = directory / name
        if file.is_file():
            messages = baca.build.show_annotations(file, undo=arguments.undo)
            for message in messages:
                baca.build.print_tags(message)


if __name__ == "__main__":
    main()
