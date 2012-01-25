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
        self.encoding_directives = []
        self.docstring_lines = []
        self.setup_statements = []
        self.teardown_statements = []

    ### OVERLOADS ###

    def __repr__(self):
        return '{}({!r})'.format(self.class_name, self.full_file_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        return ''.join(self.formatted_lines)

    @property
    def formatted_lines(self):
        lines = []
        for section, is_sorted, blank_line_count in self.sections:
            if section:
                section = section[:]
                if is_sorted:
                    section.sort()
                lines.extend(section)
                for x in range(blank_line_count):
                    lines.append('\n')
        if lines:
            lines[-1] = lines[-1].strip('\n')
        return lines

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

    def clear(self):
        for content_chunk, is_sorted in self.sections:
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
