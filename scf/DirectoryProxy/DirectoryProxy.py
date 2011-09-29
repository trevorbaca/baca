from abjad.tools import iotools
from baca.scf.SCFObject import SCFObject
import os
import re
import subprocess
import sys


# TODO: implement new PackageProxy to inherit from this DirectoryProxy
class DirectoryProxy(SCFObject):

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

    def path_is_in_repository(self, path_name):
        command = 'svn st %s' % path_name
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        first_line = proc.stdout.readline()
        if not first_line.startswith('?'):
            return True
        else:
            return False

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
        command = "if '%s' in sys.modules: del(sys.modules['%s'])" % (module_name, module_name)
        exec(command)
