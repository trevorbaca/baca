from abjad.tools import iotools
from handle_empty_startup import handle_empty_startup


def handle_startup(argv):

    iotools.clear_terminal()

    print 'argv %r' % argv
    if len(argv) == 1:
        score_package_name = handle_empty_startup()
        command_string = None
    elif len(argv) == 2:
        score_package_name = argv[1]
        command_string = None
    elif len(argv) == 3:
        score_package_name = argv[1]
        command_string = argv[2]
    else:
        raise Exception('\nUsage: scf[, score[, command_string]]')

    return score_package_name, command_string
