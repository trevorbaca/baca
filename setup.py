#!/usr/bin/env python
import os
import setuptools


def read_version():
    version_file_path = os.path.join(os.path.dirname(__file__), "baca", "_version.py")
    with open(version_file_path, "r") as file_pointer:
        file_contents_string = file_pointer.read()
    local_dict: dict = {}
    exec(file_contents_string, None, local_dict)
    __version__ = local_dict["__version__"]
    return __version__


if __name__ == "__main__":
    setuptools.setup(
        author="Trevor Bača",
        author_email="trevor.baca@gmail.com",
        description="Trevor Bača's Abjad library.",
        install_requires=["abjad>=3.19"],
        keywords="abjad, lilypond, music composition, music notation",
        license="MIT",
        name="baca",
        packages=["baca"],
        platforms="Any",
        python_requires=">=3.12",
        url="https://github.com/trevorbaca/baca",
        version=read_version(),
    )
