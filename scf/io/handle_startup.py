from abjad.tools import iotools
from handle_empty_startup import handle_empty_startup


def handle_startup(argv):

    iotools.clear_terminal()
    
    if len(argv) == 1:
        score_package_name = handle_empty_startup()
    else:
        score_package_name = argv[1]

    return score_package_name
