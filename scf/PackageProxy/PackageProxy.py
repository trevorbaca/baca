from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.menuing import UserInputGetter
import os


class PackageProxy(DirectoryProxy):

    def __init__(self, importable_package_name):
        directory = self.importable_package_name_to_directory(importable_package_name)
        DirectoryProxy.__init__(self, directory)
        self._importable_package_name = importable_package_name

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%r)' % (self.class_name, self.importable_package_name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def creation_date(self):
        return self.get_tag('creation_date')
        
    @property
    def importable_package_name(self):
        return self._importable_package_name

    @property
    def importable_parent_package_name(self):
        return '.'.join(self.importable_package_name.split('.')[:-1])

    @property
    def initializer(self):
        return os.path.join(self.directory, '__init__.py')

    @property
    def module_name(self):
        return self.importable_package_name.split('.')[-1]

    @property
    def parent_initializer(self):
        return os.path.join(self.parent_directory, '__init__.py')

    @property
    def short_package_name(self):
        return self.base_name
        
    ### PRIVATE METHODS ###

    def _read_initializer_metadata(self, name):
        initializer = file(self.initializer, 'r')
        for line in initializer.readlines():
            if line.startswith(name):
                initializer.close()
                executable_line = line.replace(name, 'result')
                exec(executable_line)
                return result

    def _write_initializer_metadata(self, name, value):
        new_lines = []
        initializer = file(self.initializer, 'r')
        found_existing_line = False
        for line in initializer.readlines():
            if line.startswith(name):
                found_existing_line = True
                new_line = '%s = %r\n' % (name, value)
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        if not found_existing_line:
            new_line = '%s = %r\n' % (name, value)
            new_lines.append(new_line)
        initializer.close()
        initializer = file(self.initializer, 'w')
        initializer.write(''.join(new_lines))
        initializer.close()

    ### PUBLIC METHODS ###

    def add_line_to_initializer(self, line):
        file_pointer = file(self.initializer, 'r')
        initializer_lines = set(file_pointer.readlines())
        file_pointer.close()
        initializer_lines.add(line)
        initializer_lines = list(initializer_lines)
        initializer_lines = [x for x in initializer_lines if not x == '\n']
        initializer_lines.sort()
        file_pointer = file(self.initializer, 'w')
        file_pointer.write(''.join(initializer_lines))
        file_pointer.close()

    def add_tag(self, tag_name, tag_value):
        tags = self.get_tags()
        tags[tag_name] = tag_value
        self.write_tags_to_initializer(tags)

    def add_tag_interactively(self, menu_header=None):
        user_input_getter = UserInputGetter()
        user_input_getter.menu_header = menu_header
        user_input_getter.menu_body = 'add tag'
        user_input_getter.prompts.append('Tag name> ')
        user_input_getter.prompts.append('Tag value> ')
        user_input = user_input_getter.get_user_input()
        if user_input:
            tag_name, tag_value = user_input
            self.add_tag(tag_name, tag_value)
            print 'Tag added.\n'
        self.proceed()

    def delete_tag(self, tag_name):
        tags = self.get_tags()
        del(tags[tag_name])
        self.write_tags_to_initializer(tags)

    def delete_tag_interactively(self, menu_header=None):
        user_input_getter = UserInputGetter()
        user_input_getter.menu_header = menu_header
        user_input_getter.menu_body = 'delete tag'
        user_input_getter.prompts.append('Tag name> ')
        user_input = user_input_getter.get_user_input(clear_terminal=False)
        if user_input:
            tag_name = user_input[0]
            self.delete_tag(tag_name)
            print 'Tag deleted.\n'
        self.proceed()

    def edit_initializer(self):
        os.system('vi %s' % self.initializer)

    def edit_parent_initializer(self):
        os.system('vi %s' % self.parent_initializer)

    def import_attribute_from_initializer(self, attribute_name):
        try:
            exec('from %s import %s' % (self.importable_package_name, attribute_name))
            exec('result = %s' % attribute_name)
            return result
        except ImportError:
            return None

    def get_tag(self, tag_name):
        tags = self.get_tags()
        tag = tags.get(tag_name, None)
        return tag

    def get_tags(self):
        try:
            exec('from %s import tags' % self.importable_package_name)
            return tags
        except ImportError:    
            return {}

    def has_tag(self, tag_name):
        tags = self.get_tags()
        return bool(tag_name in tags)

    def list_formatted_tags(self):
        formatted_tags = []
        tags = self.get_tags()
        for key in sorted(tags):
            formatted_tag = '%r: %r' % (key, tags[key])
            formatted_tags.append(formatted_tag)
        return formatted_tags

    def manage_tags(self, menu_header=None):
        from baca.scf.menuing import MenuSection
        from baca.scf.menuing import Menu
        while True:
            menu = Menu(client=self, menu_header=menu_header)
            menu.menu_body = 'tags'
            section = MenuSection()
            section.lines_to_list = self.list_formatted_tags()
            menu.menu_sections.append(section)
            section = MenuSection()
            section.sentence_length_items.append(('add', 'add tag'))
            section.sentence_length_items.append(('del', 'delete tag'))
            menu.menu_sections.append(section)
            key, value = menu.display_menu()
            if key == 'b':
                return key, None
            elif key == 'add':
                self.add_tag_interactively(menu_header=menu.menu_title)
            elif key == 'del':
                self.delete_tag_interactively(menu_header=menu.menu_title)

    @staticmethod
    def remove_module_name_from_sys_modules(self, module_name):
        '''Total hack. But works.
        '''
        command = "if '%s' in sys.modules: del(sys.modules['%s'])" % (module_name, module_name)
        exec(command)

    def write_tags_to_initializer(self, tags):
        lines = []
        fp = file(self.initializer, 'r')
        found_tags = False
        for line in fp.readlines():
            if line.startswith('tags ='):
                found_tags = True
                lines.append('tags = %s\n' % tags)
            else:
                lines.append(line)
        if not found_tags:
            lines.append('tags = %s\n' % tags)
        fp.close()
        fp = file(self.initializer, 'w')
        fp.write(''.join(lines))
        fp.close()
