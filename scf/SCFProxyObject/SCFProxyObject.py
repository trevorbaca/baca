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

#    def clear_terminal(self):
#        iotools.clear_terminal()
#
#    def confirm(self):
#        response = raw_input('Ok? ')
#        if not response.lower() == 'y':
#            print ''
#            return False
#        return True

    def exec_statement(self):
        statement = raw_input('xcf> ')
        exec('from abjad import *')
        exec('result = %s' % statement)
        print repr(result) + '\n'

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

#    def go_on(self):
#        response = raw_input('Press return to continue.')
#        print ''
#        self.clear_terminal()

    def path_is_in_repository(self, path_name):
        command = 'svn st %s' % path_name
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        first_line = proc.stdout.readline()
        if not first_line.startswith('?'):
            return True
        else:
            return False

    def print_not_implemented(self):
        print 'Not yet implemented.\n'

#    def print_tab(self, n):
#        if 0 < n:
#            print self.tab(n),
#
#    def query(self, prompt):
#        response = raw_input(prompt)
#        return response.lower().startswith('y')

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
            print '(Subversion will cause empty package to remain visible until next commit.)\n'
            return True
        return False

    def remove_module_name_from_sys_modules(self, module_name):
        '''Total hack. But works.
        '''
        #exec("print ('%s', '%s' in sys.modules)" % (module_name, module_name))
        command = "if '%s' in sys.modules: del(sys.modules['%s'])" % (module_name, module_name)
        exec(command)
        
#    def tab(self, n):
#        return 4 * n * ' '
