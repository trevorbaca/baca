#! /usr/bin/env python
import argparse
import os
import pathlib

import abjad
import baca


def main():
    directory = os.getcwd()
    parser = argparse.ArgumentParser(description="Activate tags in LilyPond files.")
    parser.add_argument("name", help="name of tag to activate")
    parser.add_argument("--undo", help="deactivate tags", action="store_true")
    arguments = parser.parse_args()
    tag = abjad.Tag(arguments.name)
    for file in sorted(pathlib.Path(directory).glob("**/*")):
        if file.suffix in (".ily", ".ly"):
            text, messages = file.read_text(), []
            text_ = baca.build.show_tag(text, tag, messages, undo=arguments.undo)
            if text_ != text:
                file.write_text(text_)
            if messages:
                print(file)
                for message in messages:
                    baca.build.print_tags(message)


if __name__ == "__main__":
    main()
