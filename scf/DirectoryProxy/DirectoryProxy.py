from baca.scf._SCFObject import _SCFObject
import os
import subprocess
import sys


class DirectoryProxy(_SCFObject):

    def __init__(self, directory_name):
        _SCFObject.__init__(self)
        self.directory_name = directory_name

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%r)' % (self.class_name, self.directory_name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def base_name(self):
        return os.path.basename(self.directory_name)

    @apply
    def directory_name():
        def fget(self):
            return self._directory_name
        def fset(self, directory_name):
            assert isinstance(directory_name, str)
            self._directory_name = directory_name
        return property(**locals())

    @property
    def is_in_repository(self):
        command = 'svn st %s' % self.directory_name
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        first_line = proc.stdout.readline()
        if first_line.startswith('?'):
            return False
        else:
            return True
    
    @property
    def parent_directory_name(self):
        return os.path.dirname(self.directory_name)

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
