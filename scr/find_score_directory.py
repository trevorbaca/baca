import os
import sys

import ide

if __name__ == "__main__":
    directory = sys.argv[1]
    subdirectory = sys.argv[2]
    path = ide.Path(os.path.abspath(directory))
    subpath = getattr(path, subdirectory)
    string = str(subpath)
    print(string)
