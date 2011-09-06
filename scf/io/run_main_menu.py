#from get_score_title import get_score_title
#from print_not_implemented import print_not_implemented
#from regexes import quit_regex
#from run_chordal_sequences_menu import run_chordal_sequences_menu
#from run_go_on_menu import run_go_on_menu
#import os
#
#
#def run_main_menu(score_package_name):
#
#   score_title = get_score_title(score_package_name)
#   try:
#      while True:
#         print '%s - main menu' % score_title
#         print ''
#         print '  1: score overview'
#         print '  2: chordal sequences'
#         print ''
#         response = raw_input('scf> ')
#         print ''
#         if quit_regex.match(response):
#            break
#         elif response == '1':
#            print_not_implemented()
#            run_go_on_menu()
#         elif response == '2':
#            try:
#               run_chordal_sequences_menu(score_package_name)
#            except KeyboardInterrupt:
#               os.system('clear')
#         elif response.lower() == 'q':
#            break
#         else:
#            pass
#   except EOFError:
#      print ''
#      print ''
#   except (SystemExit, KeyboardInterrupt):
#      print ''
