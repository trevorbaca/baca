from baca.scf.proxies.AssetProxy import AssetProxy
import os
import shutil


# TODO: write all tests
class FileProxy(AssetProxy):
    
    ### OVERLOADS ###

    def __repr__(self):
        return '{}({!r})'.format(self.class_name, self.path_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def file_lines(self):
        file_pointer = file(self.path_name)
        file_lines = file_pointer.readlines()
        file_pointer.close()
        return file_lines

    @property
    def is_exceptionless(self):
        try:
            self.execute_file_lines()
            return True
        except:
            return False

    @property
    def parent_directory_name(self):
        return os.path.dirname(self.path_name)

    @property
    def path_name(self):
        return self._path_name

    @property
    def sections(self):
        return ()

    @property
    def short_name(self):
        return self.path_name.split(os.path.sep)[-1]

    @property
    def short_name_without_extension(self):
        if '.' in self.short_name:
            return self.short_name[:self.short_name.rdindex('.')]
        else:
            return self.short_name

    ### PUBLIC METHODS ###

    def clear(self):
        for section, is_sorted, blank_line_count  in self.sections:
            section[:] = []

    def conditionally_make_file(self):
        if not os.path.exists(self.path_name):
            file_reference = file(self.path_name, 'w')
            file_reference.write('')
            file_reference.close()
        
    def copy_file(self, new_path_name):
        shutil.copyfile(self.path_name, new_path_name)

    def copy_file_interactively(self, prompt=True):
        getter = self.make_getter()
        getter.append_string('new file name')
        new_short_name = getter.run()
        if self.backtrack():
            return
        new_path_name = os.path.join(self.parent_directory_name, new_short_name)
        self.copy_file(new_path_name)
        line = 'file copied.'
        self.proceed(line, prompt=prompt)

    def edit(self):
        os.system('vi + {}'.format(self.path_name))

    def execute_file_lines(self):
        file_pointer = open(self.path_name, 'r')
        file_contents_string = file_pointer.read()
        file_pointer.close()
        exec(file_contents_string)

    def fix(self):
        self.print_implemented_on_child_classes()

    def has_line(self, line):
        file_reference = open(self.path_name, 'r')
        for file_line in file_reference.readlines():
            if file_line == line:
                file_reference.close()
                return True
        file_reference.close()
        return False

    # TODO: extend for repository
    def remove(self, prompt=False):
        os.remove(self.path_name)
        self.proceed('file deleted.', prompt=prompt)

    def rename_file(self, new_path_name):
        os.rename(self.path_name, new_path_name)
        self._path_name = new_path_name
        
    def touch(self):
        os.system('touch {}'.format(self.path_name))

    def view(self):
        os.system('vi -R {}'.format(self.path_name))

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
            canned_file_name = os.path.join(self.boilerplate_directory, canned_file_name)
        if not os.path.exists(canned_file_name):
            self.proceed('canned file {!r} does not exist.'.format(canned_file_name), prompt=prompt)
        else:
            shutil.copyfile(canned_file_name, self.path_name)
            self.proceed('canned file copied.', prompt=prompt)
