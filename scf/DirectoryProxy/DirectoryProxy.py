from baca.scf.SCFObject import SCFObject
import os
import subprocess
import sys


class DirectoryProxy(SCFObject):

    def __init__(self, directory):
        SCFObject.__init__(self)
        self.directory = directory

    ### PUBLIC ATTRIBUTES ###

    @property
    def basename(self):
        return os.path.basename(self.directory)
   
    @property
    def is_in_repository(self):
        return self.path_is_in_repository(self.directory)
    
    @property
    def parent_directory(self):
        return os.path.dirname(self.directory)

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

    def svn_add(self):
        proc = subprocess.Popen('svn-add-all', shell=True, stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        if lines:
            print ''.join(lines)
        self.proceed()
 
    def svn_ci(self, commit_message=None, prompt_proceed=True):
        if commit_message is None:
            commit_message = raw_input('Commit message> ')
            print ''
            print 'Commit message will be: "%s"\n' % commit_message
            if not self.confirm():
                return
        print ''
        print self.directory
        command = 'svn commit -m "%s" %s' % (commit_message, self.directory)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        print ''.join(proc.stdout.readlines())
        if prompt_proceed:
            self.proceed()

    def svn_st(self, prompt_proceed=True):
        print self.directory
        command = 'svn st -u %s' % self.directory
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        print ''.join(proc.stdout.readlines())
        if prompt_proceed:
            self.proceed()
