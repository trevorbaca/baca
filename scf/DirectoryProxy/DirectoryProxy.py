from baca.scf._SCFObject import _SCFObject
import os
import subprocess
import sys


class DirectoryProxy(_SCFObject):

    def __init__(self, directory_name=None):
        _SCFObject.__init__(self)
        if directory_name is not None:
            self.directory_name = directory_name
        else:
            self._directory_name = None

    ### OVERLOADS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.directory_name == other.directory_name:
                return True
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        if self.directory_name is not None:
            return '%s(%r)' % (self.class_name, self.directory_name)
        else:
            return '%s()' % self.class_name

    ### PUBLIC ATTRIBUTES ###

    @apply
    def directory_name():
        def fget(self):
            return self._directory_name
        def fset(self, directory_name):
            assert isinstance(directory_name, (str, type(None)))
            self._directory_name = directory_name
        return property(**locals())

    @property
    def has_directory(self):
        if self.directory_name is not None:
            return os.path.exists(self.directory_name)
        else:
            return False

    @property
    def is_in_repository(self):
        if self.directory_name is None:
            return False
        if not self.has_directory:
            return False
        command = 'svn st %s' % self.directory_name
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        first_line = proc.stdout.readline()
        if first_line.startswith('?'):
            return False
        else:
            return True
    
    ### PRIVATE METHODS ###

    def _remove_nonversioned_directory(self):
        print '%s will be removed.\n' % self.directory_name
        response = raw_input("Type 'remove' to proceed: ")
        print ''
        if response == 'remove':
            command = 'rm -rf %s' % self.directory_name
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            first_line = proc.stdout.readline()
            print 'Removed %s.\n' % self.directory_name
            return True
        return False

    def _remove_versioned_directory(self):
        print '%s will be completely removed from the repository!\n' % self.directory_name
        response = raw_input("Type 'remove' to proceed: ")
        print ''
        if response == 'remove':
            command = 'svn rm %s' % self.directory_name
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            first_line = proc.stdout.readline()
            print 'Removed %s.\n' % self.directory_name
            print '(Subversion will cause empty package to remain visible until next commit.)\n'
            return True
        return False

    ### PUBLIC METHODS ###

    def create_directory(self):
        os.mkdir(self.directory_name)

    def get_directory_name_interactively(self):
        getter = self.UserInputGetter()
        getter.prompts.append('directory name')
        self.directory_name = getter.run()

    def remove(self):
        if self.is_in_repository:
            result = self._remove_versioned_directory()
        else:
            result = self._remove_nonversioned_directory()    
        return result

    def run_py_test(self, prompt_proceed=True):
        proc = subprocess.Popen('py.test %s' % self.directory_name, shell=True, stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        if lines:
            print ''.join(lines)
        if prompt_proceed:
            self.proceed()

    def svn_add(self, prompt_proceed=True):
        proc = subprocess.Popen('svn-add-all', shell=True, stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        if lines:
            print ''.join(lines)
        if prompt_proceed:
            self.proceed()
 
    def svn_ci(self, commit_message=None, prompt_proceed=True):
        if commit_message is None:
            commit_message = raw_input('Commit message> ')
            print ''
            print 'Commit message will be: "%s"\n' % commit_message
            if not self.confirm():
                return
        print ''
        print self.directory_name
        command = 'svn commit -m "%s" %s' % (commit_message, self.directory_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        print ''.join(proc.stdout.readlines())
        if prompt_proceed:
            self.proceed()

    def svn_st(self, prompt_proceed=True):
        print self.directory_name
        command = 'svn st -u %s' % self.directory_name
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        print ''.join(proc.stdout.readlines())
        if prompt_proceed:
            self.proceed()

    def svn_up(self, prompt_proceed=True):
        print self.directory_name
        command = 'svn up %s' % self.directory_name
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        print ''.join(proc.stdout.readlines())
        if prompt_proceed:
            self.proceed()
