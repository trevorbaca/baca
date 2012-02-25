from scf.proxies.AssetProxy import AssetProxy
import os
import shutil


# TODO: write all tests
class FileProxy(AssetProxy):
    
    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def file_lines(self):
        result = []
        if self.path_name:
            file_pointer = file(self.path_name)
            result.extend(file_pointer.readlines())
            file_pointer.close()
        return result

    @property
    def format(self):
        return ''.join(self.formatted_lines)

    @property
    def formatted_lines(self):
        return self.file_lines

    ### PUBLIC METHODS ###

    # TODO: write test
    def conditionally_make_empty_asset(self, is_interactive=False):
        if not os.path.exists(self.path_name):
            file_reference = file(self.path_name, 'w')
            file_reference.write('')
            file_reference.close()
        self.proceed(prompt=is_interactive)
        
    # TODO: move up to AssetProxy.copy()
    def copy_file(self, new_path_name):
        shutil.copyfile(self.path_name, new_path_name)

    # TODO: move up to AssetProxy.copy_interactively()
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

    # TODO: move up to AssetProxy
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

    def print_to_screen(self):
        # TODO: reimplement with self.display()
        print self.format

    # TODO: move up to asset proxy
    def touch(self):
        os.system('touch {}'.format(self.path_name))

    def view(self):
        os.system('vi -R {}'.format(self.path_name))

    # TODO: write test
    # TODO: rename to write_canned_asset_to_disk_interactively
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
