#! /usr/bin/env python
import argparse
import os
import pathlib

import baca

if __name__ == "__main__":
    directory = pathlib.Path(os.getcwd())
    parser = argparse.ArgumentParser(description="Activate tags in LilyPond files.")
    parser.add_argument("--undo", help="deactivate tags", action="store_true")
    arguments = parser.parse_args()
    for name in ("layout.ily", "music.ily", "music.ly"):
        file = directory / name
        if file.is_file():
            messages = baca.build.color_persistent_indicators(file, undo=arguments.undo)
            for message in messages:
                baca.build.print_tags(message)
