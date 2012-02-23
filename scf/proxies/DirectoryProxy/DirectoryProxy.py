from baca.scf.proxies.AssetProxy import AssetProxy
import os
import subprocess


class DirectoryProxy(AssetProxy):

    ### OVERLOADS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.path_name == other.path_name:
                return True
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '{}({!r})'.format(self.class_name, self.path_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def directory_contents(self):
        for file_name in os.listdir(self.path_name):
            if file_name.endswith('.pyc'):
                path_name = os.path.join(self.path_name, file_name)
                os.remove(path_name)
        return os.listdir(self.path_name)

    @property
    def directory_name(self):
        return self._path_name

    @property
    def svn_add_command(self):
        return 'cd {} && svn-add-all'.format(self.path_name)
    
    ### PUBLIC METHODS ###

    def get_directory_name_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('directory name')
        result = getter.run()
        if self.backtrack():
            return
        self.path_name = result

    def make_directory(self):
        os.mkdir(self.path_name)

    def print_directory_contents(self):
        self.display(self.directory_contents, capitalize_first_character=False)
        self.display('')
        self.session.hide_next_redraw = True
