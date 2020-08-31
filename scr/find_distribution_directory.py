import ide
import os
import sys



if __name__ == "__main__":
    directory = sys.argv[1]
    path = ide.Path(os.path.abspath(directory))
    string = str(path.distribution)
    print(string)
