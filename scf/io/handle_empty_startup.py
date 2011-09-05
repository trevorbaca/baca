from print_scf_greeting import print_scf_greeting
from run_score_selection_menu import run_score_selection_menu
import os


def handle_empty_startup():

   print_scf_greeting()
   score_package_name = run_score_selection_menu()
   os.system('clear')

   return score_package_name
