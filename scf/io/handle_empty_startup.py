from abjad.tools import iotools
from print_scf_greeting import print_scf_greeting
from run_score_selection_menu import run_score_selection_menu


def handle_empty_startup():

    print_scf_greeting()
    score_package_name = run_score_selection_menu()
    iotools.clear_terminal()

    return score_package_name
