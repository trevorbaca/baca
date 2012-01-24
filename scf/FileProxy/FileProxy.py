from baca.scf.SCFObject import SCFObject
import os
import shutil


# TODO: write all tests
class FileProxy(SCFObject):
    
    def __init__(self, full_file_name, session=None):
        assert isinstance(full_file_name, str), '{!r} is not a string.'.format(full_file_name)
        assert os.path.exists(full_file_name), 'Initializer {!r} does not exist.'.format(full_file_name)
        SCFObject.__init__(self, session=session)
        self._full_file_name = full_file_name
        self._encoding_directives = []
        self._docstring_lines = []
        self._setup_statements = []
        self._teardown_statements = []

    ### OVERLOADS ###

    def __repr__(self):
        return '{}({!r})'.format(self.class_name, self.full_file_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def docstring_lines(self):
        return self._docstring_lines

    @property
    def encoding_directives(self):
        return self._encoding_directives

    @property
    def format(self):
        return ''.join(self.formatted_lines)

    @property
    def formatted_lines(self):
        lines = []
        for content_collection, is_sorted in self.content_chunks:
            if content_collection:
                content_collection = content_collection[:]
                if is_sorted:
                    content_collection.sort()
                lines.extend(content_collection)
                lines.append('\n')
        if lines:
            lines.pop()
            lines[-1] = lines[-1].strip()
        return lines

    @property
    def full_file_name(self):
        return self._full_file_name

    @property
    def path_name(self):
        return os.path.dirname(self.full_file_name)

    @property
    def setup_statements(self):
        return self._setup_statements

    @property
    def short_file_name(self):
        return self.full_file_name.split(os.path.sep)[-1]

    @property
    def teardown_statements(self):
        return self._teardown_statements

    ### PUBLIC METHODS ###

    def clear(self):
        for content_chunk, is_sorted in self.content_chunks:
            content_chunk[:] = []

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

    def display(self):
        print self.format

    def rename_file(self, new_full_file_name):
        os.rename(self.full_file_name, new_full_file_name)
        self._full_file_name = new_full_file_name
        
    # TODO: extend for repository
    def remove(self):
        os.remove(self.full_file_name)

    def view(self):
        os.system('vi -R {}'.format(self.full_file_name))

    def write_to_disk(self):
        initializer = file(self.full_file_name, 'w')
        initializer.write(self.format)
