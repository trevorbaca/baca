from baca.scf.SCFObject import SCFObject
import os
import shutil


# TODO: write all tests
class FileProxy(SCFObject):
    
    def __init__(self, full_file_name, session=None):
        assert isinstance(full_file_name, str)
        assert os.path.exists(full_file_name)
        SCFObject.__init__(self, session=session)
        self._full_file_name = full_file_name

    ### OVERLOADS ###

    def __repr__(self):
        return '{}({!r})'.format(self.class_name, self.full_file_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def full_file_name(self):
        return self._full_file_name

    @property
    def path_name(self):
        return os.path.dirname(self.full_file_name)

    @property
    def short_file_name(self):
        return self.full_file_name.split(os.path.sep)[-1]

    ### PUBLIC METHODS ###

    def copy_file(self, new_full_file_name):
        shutil.copyfile(self.full_file_name, new_full_file_name)

    def copy_file_interactively(self, prompt=True):
        getter = self.make_new_getter()
        getter.append_string('new file name')
        new_short_file_name = getter.run()
        if self.backtrack():
            return
        new_full_file_name = os.path.join(self.path_name, new_short_file_name)
        self.copy_file(new_full_file_name)
        line = 'file copied.'
        self.proceed(line, prompt=prompt)

    def rename_file(self, new_full_file_name):
        os.rename(self.full_file_name, new_full_file_name)
        self._full_file_name = new_full_file_name
        
    # TODO: extend for repository
    def remove(self):
        os.remove(self.full_file_name)
