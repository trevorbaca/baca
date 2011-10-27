from abjad.tools import iotools
from baca.scf.DirectoryProxy import DirectoryProxy
import os
import sys


class PackageProxy(DirectoryProxy):

    def __init__(self, package_importable_name=None):
        DirectoryProxy.__init__(self)
        self._package_short_name = None
        self.package_importable_name = package_importable_name
        self._purview = None

    ### OVERLOADS ###

    def __repr__(self):
        if self.package_importable_name is not None:
            return '%s(%r)' % (self.class_name, self.package_importable_name)
        else:
            return '%s()' % self.class_name

    ### PUBLIC ATTRIBUTES ###

    @property
    def creation_date(self):
        return self.get_tag('creation_date')

    @property
    def directory_name(self):
        if self.package_importable_name is not None:
            return self.package_importable_name_to_directory_name(self.package_importable_name)

    @property
    def has_initializer(self):
        if self.initializer_file_name is not None:
            return os.path.isfile(self.initializer_file_name)

    @property
    def initializer_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, '__init__.py')

    @apply
    def package_importable_name():
        def fget(self):
            return self._package_importable_name
        def fset(self, package_importable_name):
            assert isinstance(package_importable_name, (str, type(None)))
            if isinstance(package_importable_name, str):
                package_short_name = package_importable_name.split('.')[-1]
                self.package_short_name = package_short_name
            self._package_importable_name = package_importable_name
        return property(**locals())

    @apply
    def package_short_name():
        def fget(self):
            return self._package_short_name
        def fset(self, package_short_name):
            assert isinstance(package_short_name, (str, type(None)))
            self._package_short_name = package_short_name
        return property(**locals())

    @property
    def package_spaced_name(self):
        if self.package_short_name is not None:
            return self.package_short_name.replace('_', ' ')
        
    @property
    def parent_initializer_file_name(self):
        if self.parent_package_importable_name:
            parent_directory_name = self.package_importable_name_to_directory_name(
                self.parent_package_importable_name)
            return os.path.join(parent_directory_name, '__init__.py')

    @property
    def parent_package_importable_name(self):
        if self.package_importable_name is not None:
            result = '.'.join(self.package_importable_name.split('.')[:-1])
            if result:
                return result

    @apply
    def purview():
        def fget(self):
            if self._purview is not None:
                return self._purview
            else:
                return self.package_importable_name_to_purview(self.package_importable_name)
        def fset(self, purview):
            if self.package_importable_name is None:
                self._purview = purview
            else:
                raise ValueError('package importable name already assigned.')
        return property(**locals())

    @property
    def score(self):
        from baca.scf.ScoreProxy import ScoreProxy
        if isinstance(self.purview, ScoreProxy):
            return self.purview

    ### PRIVATE METHODS ###

    def _read_initializer_metadata(self, name):
        initializer = file(self.initializer_file_name, 'r')
        for line in initializer.readlines():
            if line.startswith(name):
                initializer.close()
                executable_line = line.replace(name, 'result')
                exec(executable_line)
                return result

    def _write_initializer_metadata(self, name, value):
        new_lines = []
        initializer = file(self.initializer_file_name, 'r')
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
        initializer = file(self.initializer_file_name, 'w')
        initializer.write(''.join(new_lines))
        initializer.close()

    ### PUBLIC METHODS ###

    def add_line_to_initializer(self, line):
        file_pointer = file(self.initializer_file_name, 'r')
        initializer_lines = set(file_pointer.readlines())
        file_pointer.close()
        initializer_lines.add(line)
        initializer_lines = list(initializer_lines)
        initializer_lines = [x for x in initializer_lines if not x == '\n']
        initializer_lines.sort()
        file_pointer = file(self.initializer_file_name, 'w')
        file_pointer.write(''.join(initializer_lines))
        file_pointer.close()

    def add_tag(self, tag_name, tag_value):
        tags = self.get_tags()
        tags[tag_name] = tag_value
        self.write_tags_to_initializer(tags)

    def add_tag_interactively(self, menu_header=None):
        getter = self.UserInputGetter()
        getter.menu_header = menu_header
        getter.menu_body = 'add tag'
        getter.prompts.append('Tag name> ')
        getter.prompts.append('Tag value> ')
        user_input = getter.run()
        if user_input:
            tag_name, tag_value = user_input
            self.add_tag(tag_name, tag_value)
            print 'Tag added.\n'
        self.proceed()

    def create_initializer(self):
        if self.has_initializer:
            raise OSError('package %r already has initializer.' % self)
        initializer = file(self.initializer_file_name, 'a')        
        initializer.write('')
        initializer.close()

    def delete_package(self):
        result = self.remove()
        if result:
            self.proceed()
        
    def delete_tag(self, tag_name):
        tags = self.get_tags()
        del(tags[tag_name])
        self.write_tags_to_initializer(tags)

    def delete_tag_interactively(self, menu_header=None):
        getter = self.UserInputGetter()
        getter.menu_header = menu_header
        getter.menu_body = 'delete tag'
        getter.prompts.append('Tag name> ')
        user_input = getter.run(clear_terminal=False)
        if user_input:
            tag_name = user_input[0]
            self.delete_tag(tag_name)
            print 'Tag deleted.\n'
        self.proceed()

    def edit_initializer(self):
        os.system('vi %s' % self.initializer_file_name)

    def edit_parent_initializer(self):
        os.system('vi %s' % self.parent_initializer_file_name)

    def import_attribute_from_initializer(self, attribute_name):
        try:
            exec('from %s import %s' % (self.package_importable_name, attribute_name))
            exec('result = %s' % attribute_name)
            return result
        except ImportError:
            return None

    def get_tag(self, tag_name):
        tags = self.get_tags()
        tag = tags.get(tag_name, None)
        return tag

    def get_tags(self):
        import collections
        try:
            exec('from %s import tags' % self.package_importable_name)
            return tags
        except ImportError:    
            return collections.OrderedDict([])

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
        while True:
            menu = self.Menu(client=self.where(), menu_header=menu_header)
            menu.menu_body = 'tags'
            section = self.MenuSection()
            section.lines_to_list = self.list_formatted_tags()
            menu.menu_sections.append(section)
            section = self.MenuSection()
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

#    def package_importable_name_to_purview(self, package_importable_name):
#        import baca
#        if package_importable_name is None:
#            return
#        elif package_importable_name.split('.')[0] == 'baca':
#            return baca.scf.GlobalProxy()
#        elif package_importable_name.split('.')[0] in os.listdir(os.environ.get('SCORES')):
#            return baca.scf.ScoreProxy(package_importable_name.split('.')[0])
#        else:
#            raise ValueError('Unknown package importable name %r.' % package_importable_name)

    def pprint_tags(self, tags):
        if tags:
            lines = []
            for key, value in sorted(tags.iteritems()):
                key = repr(key)
                if hasattr(value, '_get_multiline_repr'):
                    repr_lines = value._get_multiline_repr(include_tools_package=True)
                    value = '\n    '.join(repr_lines)
                    lines.append('({}, {})'.format(key, value))
                else:
                    value = getattr(value, '_repr_with_tools_package', repr(value))
                    lines.append('({}, {})'.format(key, value))
            lines = ',\n    '.join(lines)
            result = 'tags = OrderedDict([\n    {}])'.format(lines)
        else:
            result = 'tags = OrderedDict([])'
        return result

    def remove_package_importable_name_from_sys_modules(self, package_importable_name):
        '''Total hack. But works.
        '''
        command = "if '%s' in sys.modules: del(sys.modules['%s'])" % (
            package_importable_name, package_importable_name)
        exec(command)

    def set_package_importable_name_interactively(self):
        getter = self.UserInputGetter()
        getter.prompts.append('package importable name')
        getter.tests.append(iotools.is_underscore_delimited_lowercase_package_name)
        getter.helps.append('must be underscore-delimited lowercase package name.')
        self.package_importable_name = getter.run()

    def set_package_spaced_name_interactively(self, menu_header=None):
        getter = self.UserInputGetter(menu_header=menu_header)
        getter.menu_body = 'set package spaced name'
        getter.prompts.append('package spaced name')
        getter.tests.append(iotools.is_space_delimited_lowercase_string)
        getter.helps.append('must be space-delimited lowercase string.')
        self.package_spaced_name = getter.run()

    def set_purview_interactively(self, menu_header=None):
        from baca.scf.ScoreWrangler import ScoreWrangler
        menu = self.Menu(client=self.where(), menu_header=menu_header)
        menu.menu_body = 'select purview'
        score_wrangler = ScoreWrangler()
        menu.items_to_number = score_wrangler.list_score_titles_with_years()
        menu.named_pairs.append(('s', 'global to studio'))
        key, value = menu.display_menu()
        print key, value

    def unimport_baca_package(self):
        self.remove_package_importable_name_from_sys_modules('baca')

    def write_package_to_disk(self):
        self.print_not_implemented()

    def write_tags_to_initializer(self, tags):
        tags = self.pprint_tags(tags)
        lines = []
        fp = file(self.initializer_file_name, 'r')
        found_tags = False
        for line in fp.readlines():
            if found_tags:
                pass
            elif line.startswith('tags ='):
                found_tags = True
                lines.append(tags)
            else:
                lines.append(line)
        if not found_tags:
            lines.append(tags)
        fp.close()
        fp = file(self.initializer_file_name, 'w')
        fp.write(''.join(lines))
        fp.close()
