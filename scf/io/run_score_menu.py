from print_not_implemented import print_not_implemented
from regexes import *
from run_chordal_sequences_menu import run_chordal_sequences_menu



def run_score_menu(score_package_name):

   try:
      while True:
         print 'Main menu'
         print ''
         print '  [1: score overview ...]'
         print '  2: chordal sequences ...'
         print ''
         print '  q: quit'
         print ''
         input = raw_input('scf> ')
         print ''
         if quit_regex.match(input):
            break
         elif input == '1':
            print_not_implemented( )
         elif input == '2':
            run_chordal_sequences_menu(score_package_name)
         elif input.lower( ) == 'q':
            break
         else:
            pass
   except EOFError:
      print ''
      print ''
