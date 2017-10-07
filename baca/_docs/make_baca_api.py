#! /usr/bin/env python
import os
import pathlib


if __name__ == '__main__':
    docs = pathlib.Path(__file__).parent
    command = f"ajv api -S --api-title='Bača API'"
    command += f' --docs-directory={docs}'
    command += f' --packages-to-document=baca.tools'
    os.system(command)
