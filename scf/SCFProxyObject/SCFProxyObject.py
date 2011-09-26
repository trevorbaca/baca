from abjad.tools import iotools
import os
import re
import subprocess
import sys


class SCFProxyObject(object):

    def __init__(self):
        self.baca_directory = os.environ.get('BACA')
        self.shared_materials_directory = os.path.join(self.baca_directory, 'materials')

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PUBLIC ATTRIBUTES ###

    @property
    def initializer(self):
        return os.path.join(self.directory, '__init__.py')

    @property
    def is_in_repository(self):
        return self.path_is_in_repository(self.directory)
    
    @property
    def parent_directory(self):
        return os.path.dirname(self.directory)

    @property
    def parent_initializer(self):
        return os.path.join(self.parent_directory, '__init__.py')

    ### PUBLIC METHODS ###

    def clear_terminal(self):
        iotools.clear_terminal()

    def confirm(self):
        response = raw_input('ok? ')
        if not response.lower() == 'y':
            print ''
            return False
        return True

    def display_menu(self, values_to_number=None, named_pairs=None, 
        secondary_named_pairs=None, indent_level=0, is_nearly=True, show_options=True,
        item_width = 11):
        if values_to_number is None:
            values_to_number = []
        if named_pairs is None:
            named_pairs = []
        named_pairs.sort()
        if secondary_named_pairs is None:
            secondary_named_pairs = []
        secondary_named_pairs.sort()
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
            if show_options:
                self.print_tab(indent_level)
            for additional_key, additional_value in named_pairs:
                if show_options:
                    print '%s: %s ' % (additional_key, additional_value.ljust(item_width)),
                all_keys.append(additional_key)
                all_values.append(additional_value)
            if show_options:
                print ''
        if secondary_named_pairs:
            if show_options:
                self.print_tab(indent_level)
            for key, value in secondary_named_pairs:
                if show_options:
                    print '%s: %s ' % (key, value.ljust(item_width)),
                all_keys.append(key)
                all_values.append(value)
            if show_options:
                print ''
        if is_nearly:
            ubiquitous_pairs = self.list_nearly_ubiquitous_menu_pairs()
        else:
            ubiquitous_pairs = self.list_ubiquitous_menu_pairs()
        if show_options:
            self.print_tab(indent_level)
        for key, value in ubiquitous_pairs:
            if show_options:
                print '%s: %s ' % (key, value.ljust(item_width)),
            all_keys.append(key)
            all_values.append(value)
        if show_options:
            print '\n'
        while True:
            response = raw_input('scf> ')
            print ''
            if response[0] in all_keys:
                break
        pair_dictionary = dict(zip(number_keys, values_to_number) + 
            named_pairs + secondary_named_pairs + ubiquitous_pairs)
        value = pair_dictionary[response[0]]
        return response, value

    def globally_replace_in_file(self, file_name, old, new):
        file_pointer = file(file_name, 'r')
        new_file_lines = []
        for line in file_pointer.readlines():
            line = line.replace(old, new)
            new_file_lines.append(line)
        file_pointer.close()
        file_pointer = file(file_name, 'w')
        file_pointer.write('\n'.join(new_file_lines))
        file_pointer.close()

    def exec_statement(self):
        statement = raw_input('xcf> ')
        exec('from abjad import *')
        exec('result = %s' % statement)
        print repr(result) + '\n'

    def list_nearly_ubiquitous_menu_pairs(self):
        pairs = self.list_ubiquitous_menu_pairs()
        pairs.extend([
            ('b', 'back'),
            ])
        pairs.sort()
        return pairs

    def list_ubiquitous_menu_pairs(self):
        pairs = [
            ('q', 'quit'),
            ('w', 'redraw'),
            ('x', 'exec'),
            ]
        pairs.sort()
        return pairs

#    def matches_quit_regex(self, string):
#        quit_regex = re.compile(r'quit\(\s*\)|[q]')
#        return quit_regex.match(string)

    def path_is_in_repository(self, path_name):
        command = 'svn st %s' % path_name
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        first_line = proc.stdout.readline()
        if not first_line.startswith('?'):
            return True
        else:
            return False

    def print_menu_title(self, menu_title):
        self.clear_terminal()
        print menu_title

    def print_not_implemented(self):
        print 'Not yet implemented.\n'

    def print_tab(self, n):
        if 0 < n:
            print self.tab(n),

    def query(self, prompt):
        response = raw_input(prompt)
        return response.lower().startswith('y')

    def remove_directory(self):
        if self.is_in_repository:
            result = self.remove_versioned_directory()
        else:
            result = self.remove_nonversioned_directory()    
        return result

    def remove_nonversioned_directory(self):
        print '%s will be removed.\n' % self.directory
        response = raw_input("Type 'remove' to proceed: ")
        print ''
        if response == 'remove':
            command = 'rm -rf %s' % self.directory
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            first_line = proc.stdout.readline()
            print 'Removed %s ...\n' % self.directory
            return True
        return False

    def remove_versioned_directory(self):
        print '%s will be completely removed from the repository!\n' % self.directory
        response = raw_input("Type 'remove' to proceed: ")
        print ''
        if response == 'remove':
            command = 'svn rm %s' % self.directory
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            first_line = proc.stdout.readline()
            print 'Removed %s ...\n' % self.directory
            return True
        return False

    def remove_module_name_from_sys_modules(self, module_name):
        '''Total hack. But works.
        '''
        #exec("print ('%s', '%s' in sys.modules)" % (module_name, module_name))
        command = "if '%s' in sys.modules: del(sys.modules['%s'])" % (module_name, module_name)
        exec(command)
        
        
    def run_go_on_menu(self):
        response = raw_input('Press any key to continue. ')
        print ''
        self.clear_terminal()

    def tab(self, n):
        return 4 * n * ' '
