from baca.scf._SCFObject import _SCFObject
import os
import subprocess
import sys


class DirectoryProxy(_SCFObject):

    def __init__(self, directory):
        _SCFObject.__init__(self)
        self.directory = directory

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%r)' % (self.class_name, self.directory)

    ### PUBLIC ATTRIBUTES ###

    @property
    def base_name(self):
        return os.path.basename(self.directory)

    @apply
    def directory():
        def fget(self):
            return self._directory
        def fset(self, directory):
            assert isinstance(directory, str)
            self._directory = directory
        return property(**locals())
   
    @property
    def is_in_repository(self):
        command = 'svn st %s' % self.directory
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        first_line = proc.stdout.readline()
        if first_line.startswith('?'):
            return False
        else:
            return True
    
    @property
    def parent_directory(self):
        return os.path.dirname(self.directory)

    ### PRIVATE METHODS ###

    def _remove_nonversioned_directory(self):
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

    def _remove_versioned_directory(self):
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

    ### PUBLIC METHODS ###

    def remove_directory(self):
        if self.is_in_repository:
            result = self._remove_versioned_directory()
        else:
            result = self._remove_nonversioned_directory()    
        return result

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
