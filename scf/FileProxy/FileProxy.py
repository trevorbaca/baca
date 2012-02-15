from baca.scf.SCFObject import SCFObject
import os
import shutil


# TODO: write all tests
class FileProxy(SCFObject):
    
    def __init__(self, full_file_name, session=None):
        assert isinstance(full_file_name, str), '{!r} is not a string.'.format(full_file_name)
        #assert os.path.exists(full_file_name), 'Initializer {!r} does not exist.'.format(full_file_name)
        SCFObject.__init__(self, session=session)
        self._full_file_name = full_file_name

    ### OVERLOADS ###

    def __repr__(self):
        return '{}({!r})'.format(self.class_name, self.full_file_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def file_lines(self):
        file_pointer = file(self.full_file_name)
        file_lines = file_pointer.readlines()
        file_pointer.close()
        return file_lines

    @property
    def full_file_name(self):
        return self._full_file_name

    @property
    def is_exceptionless(self):
        try:
            self.execute_file_lines()
            return True
        except:
            return False

    @property
    def path_name(self):
        return os.path.dirname(self.full_file_name)

    @property
    def short_file_name(self):
        return self.full_file_name.split(os.path.sep)[-1]

    ### PUBLIC METHODS ###

    def clear(self):
        for section, is_sorted, blank_line_count  in self.sections:
            section[:] = []

    def conditionally_make_file(self):
        if not os.path.exists(self.full_file_name):
            file_reference = open(self.full_file_name, 'w')
            file_reference.write('')
            file_reference.close()
        
    def copy_file(self, new_full_file_name):
        shutil.copyfile(self.full_file_name, new_full_file_name)

    def copy_file_interactively(self, prompt=True):
        getter = self.make_getter()
        getter.append_string('new file name')
        new_short_file_name = getter.run()
        if self.backtrack():
            return
        new_full_file_name = os.path.join(self.path_name, new_short_file_name)
        self.copy_file(new_full_file_name)
        line = 'file copied.'
        self.proceed(line, prompt=prompt)

    def edit(self):
        os.system('vi + {}'.format(self.full_file_name))

    def execute_file_lines(self):
        file_pointer = open(self.full_file_name, 'r')
        file_contents_string = file_pointer.read()
        file_pointer.close()
        exec(file_contents_string)

    def has_line(self, line):
        file_reference = open(self.full_file_name, 'r')
        for file_line in file_reference.readlines():
            if file_line == line:
                file_reference.close()
                return True
        file_reference.close()
        return False

    # TODO: extend for repository
    def remove(self, prompt=False):
        os.remove(self.full_file_name)
        self.proceed('file deleted.', prompt=prompt)

    def rename_file(self, new_full_file_name):
        os.rename(self.full_file_name, new_full_file_name)
        self._full_file_name = new_full_file_name
        
    def short_file_name(self):
        return os.path.sep.split(self.full_file_name)[-1]

    def touch(self):
        os.system('touch {}'.format(self.full_file_name))

    def view(self):
        os.system('vi -R {}'.format(self.full_file_name))

    # TODO: write test
    def write_canned_file_to_disk(self, prompt=True):
        getter = self.make_getter(where=self.where())
        getter.append_string('name of canned file')
        self.push_backtrack()
        canned_file_name = getter.run()
        self.pop_backtrack()
        if self.backtrack():
            return
        if not os.path.exists(canned_file_name):
            canned_file_name = os.path.join(self.assets_directory, canned_file_name)
        if not os.path.exists(canned_file_name):
            self.proceed('canned file {!r} does not exist.'.format(canned_file_name), prompt=prompt)
        else:
            shutil.copyfile(canned_file_name, self.full_file_name)
            self.proceed('canned file copied.', prompt=prompt)
