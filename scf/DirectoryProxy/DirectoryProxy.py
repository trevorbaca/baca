from baca.scf.SCFObject import SCFObject
import os
import subprocess
import sys


class DirectoryProxy(SCFObject):

    def __init__(self, directory_name, session=None):
        assert isinstance(directory_name, str)
        assert os.path.exists(directory_name)
        SCFObject.__init__(self, session=session)
        self._directory_name = directory_name

    ### OVERLOADS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.directory_name == other.directory_name:
                return True
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '{}({!r})'.format(self.class_name, self.directory_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def directory_name(self):
        return self._directory_name

    @property
    def is_in_repository(self):
        if self.directory_name is None:
            return False
        command = 'svn st {}'.format(self.directory_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        first_line = proc.stdout.readline()
        if first_line.startswith('?'):
            return False
        else:
            return True
    
    ### PUBLIC METHODS ###

    def create_directory(self):
        os.mkdir(self.directory_name)

    def get_directory_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('directory name')
        result = getter.run()
        if self.backtrack():
            return
        self.directory_name = result

    def list_directory(self):
        os.system('ls {}'.format(self.directory_name))
        self.conditionally_display_lines(lines=[''])
        self.session.hide_next_redraw = True

    def remove(self):
        if self.is_in_repository:
            result = self.remove_versioned_directory()
        else:
            result = self.remove_nonversioned_directory()    
        return result

    def remove_nonversioned_directory(self):
        line = '{} will be removed.\n'.format(self.directory_name)
        self.conditionally_display_lines([line])
        response = self.handle_raw_input("type 'remove' to proceed")
        if response == 'remove':
            command = 'rm -rf {}'.format(self.directory_name)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            first_line = proc.stdout.readline()
            line = 'Removed {}.\n'.format(self.directory_name)
            self.conditionally_display_lines([line])
            return True
        return False

    def remove_versioned_directory(self):
        line = '{} will be completely removed from the repository!\n'.format(self.directory_name)
        self.conditionally_display_lines([line])
        response = self.handle_raw_input("type 'remove' to proceed")
        if response == 'remove':
            command = 'svn --force rm {}'.format(self.directory_name)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            first_line = proc.stdout.readline()
            lines = []
            lines.append('Removed {}.\n'.format(self.directory_name))
            lines.append('(Subversion will cause empty package to remain visible until next commit.)')
            lines.append('')
            self.conditionally_display_lines(lines)
            return True
        return False

    def run_py_test(self, prompt=True):
        proc = subprocess.Popen('py.test {}'.format(self.directory_name), shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.conditionally_display_lines(lines)
        if prompt:
            line = 'tests run.'
            self.proceed(lines=[line])

    def svn_add(self, prompt=True):
        proc = subprocess.Popen('svn-add-all', shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.conditionally_display_lines(lines)
        if prompt:
            self.proceed()
 
    def svn_ci(self, commit_message=None, prompt=True):
        if commit_message is None:
            commit_message = self.handle_raw_input('commit message')
            line = 'commit message will be: "{}"\n'.format(commit_message)
            self.conditionally_display_lines([line])
            if not self.confirm():
                return
        lines = []
        lines.append('')
        lines.append(self.directory_name)
        command = 'svn commit -m "{}" {}'.format(commit_message, self.directory_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines.extend([line.strip() for line in proc.stdout.readlines()])
        self.conditionally_display_lines(lines)
        if prompt:
            self.proceed()

    def svn_st(self, prompt=True):
        line = self.directory_name
        self.conditionally_display_lines([line])
        command = 'svn st -u {}'.format(self.directory_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        self.conditionally_display_lines(lines)
        if prompt:
            self.proceed()

    def svn_up(self, prompt=True):
        line = self.directory_name
        self.conditionally_display_lines([line])
        command = 'svn up {}'.format(self.directory_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        self.conditionally_display_lines(lines)
        if prompt:
            self.proceed()
