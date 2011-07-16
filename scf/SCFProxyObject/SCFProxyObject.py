import os
import re


class SCFProxyObject(object):

   ## OVERLOADS ##

   def __repr__(self):
      return '%s( )' % self.__class__.__name__

   ## PUBLIC METHODS ##

   def clear_terminal(self):
      os.system('clear')

   def list_nearly_ubiquitous_menu_pairs(self):
      ubiquitous_menu_pairs = [
         ('q', 'quit'),
         ]
      return ubiquitous_menu_pairs

   def list_ubiquitous_menu_pairs(self):
      ubiquitous_menu_pairs = [
         ('b', 'back'),
         ('q', 'quit'),
         ]
      return ubiquitous_menu_pairs

   def matches_quit_regex(self, string):
      quit_regex = re.compile(r'quit\(\s*\)|[q]')
      return quit_regex.match(string)

   def present_menu(self, 
      values_to_number = None, named_pairs = None, indent_level = 0, is_nearly = False, show_options = True):
      if values_to_number is None:
         values_to_number = [ ]
      if named_pairs is None:
         named_pairs = [ ]
      if is_nearly:
         named_pairs += self.list_nearly_ubiquitous_menu_pairs( )
      else:
         named_pairs += self.list_ubiquitous_menu_pairs( )
      named_pairs.sort( )
      number_keys = range(1, len(values_to_number) + 1)
      number_keys = [str(x) for x in number_keys]
      numbered_pairs = zip(number_keys, values_to_number)
      if show_options:
         for number_key, value_to_number in numbered_pairs:
            self.print_tab(indent_level),
            print '%s: %s' % (number_key, value_to_number)
         print ''
      all_keys = number_keys[:]
      all_values = values_to_number[:]
      if named_pairs:
         self.print_tab(indent_level)
         for additional_key, additional_value in named_pairs:
            if show_options:
               print '%s: %s ' % (additional_key, additional_value),
            all_keys.append(additional_key)
            all_values.append(additional_value)
         if show_options:
            print '\n'
      while True:
         choice = raw_input('scf> ')
         print ''
         if choice in all_keys:
            break
      pair_dictionary = dict(zip(number_keys, values_to_number) + named_pairs)
      value = pair_dictionary[choice]
      return choice, value

   def print_menu_title(self, menu_title):
      self.clear_terminal( )
      print menu_title

   def print_not_implemented(self):
      print 'Not yet implemented.\n'

   def print_tab(self, n):
      if 0 < n:
         print self.tab(n),

   def run_go_on_menu(self):
      input = raw_input('Press any key to continue. ')
      print ''
      os.system('clear')

   def tab(self, n):
      return 3 * n * ' '
