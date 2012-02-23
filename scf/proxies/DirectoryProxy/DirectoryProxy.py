from baca.scf.proxies.AssetProxy import AssetProxy
import os
import subprocess


class DirectoryProxy(AssetProxy):

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
    def directory_contents(self):
        for file_name in os.listdir(self.directory_name):
            if file_name.endswith('.pyc'):
                path_name = os.path.join(self.directory_name, file_name)
                os.remove(path_name)
        return os.listdir(self.directory_name)

    @property
    def directory_name(self):
        #return self._directory_name
        return self._path_name

    @property
    def is_in_repository(self):
        if self.directory_name is None:
            return False
        command = 'svn st {}'.format(self.directory_name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        first_line = proc.stdout.readline()
        if first_line.startswith(('?', 'svn: warning:')):
            return False
        else:
            return True

    @property
    def path_name(self):
        return self.directory_name

    @property
    def svn_add_command(self):
        return 'cd {} && svn-add-all'.format(self.directory_name)
    
    ### PUBLIC METHODS ###

    def get_directory_name_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('directory name')
        result = getter.run()
        if self.backtrack():
            return
        self.directory_name = result

    def make_directory(self):
        os.mkdir(self.directory_name)

    def print_directory_contents(self):
        self.display(self.directory_contents, capitalize_first_character=False)
        self.display('')
        self.session.hide_next_redraw = True

    def remove(self):
        if self.is_in_repository:
            result = self.remove_versioned_directory()
        else:
            result = self.remove_nonversioned_directory()    
        return result

    def remove_nonversioned_directory(self):
        line = '{} will be removed.\n'.format(self.directory_name)
        self.display(line)
        getter = self.make_getter(where=self.where())
        getter.append_string("type 'remove' to proceed")
        response = getter.run()
        if self.backtrack():
            return
        if response == 'remove':
            command = 'rm -rf {}'.format(self.directory_name)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            proc.stdout.readline()
            line = 'removed {}.\n'.format(self.directory_name)
            self.display(line)
            return True
        return False

    def remove_versioned_directory(self):
        line = '{} will be completely removed from the repository!\n'.format(self.directory_name)
        self.display(line)
        getter = self.make_getter(where=self.where())
        getter.append_string("type 'remove' to proceed")
        response = getter.run()
        if self.backtrack():
            return
        if response == 'remove':
            command = 'svn --force rm {}'.format(self.directory_name)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            proc.stdout.readline()
            lines = []
            lines.append('Removed {}.\n'.format(self.directory_name))
            lines.append('(Subversion will cause empty package to remain visible until next commit.)')
            lines.append('')
            self.display(lines)
            return True
        return False

    def run_py_test(self, prompt=True):
        proc = subprocess.Popen('py.test {}'.format(self.directory_name), shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.display(lines)
        line = 'tests run.'
        self.proceed(line, prompt=prompt)
