from abjad.tools import iotools
from baca.scf.DirectoryProxy import DirectoryProxy
import os
import sys


class PackageProxy(DirectoryProxy):

    def __init__(self, package_importable_name=None, session=None):
        directory_name = self._package_importable_name_to_directory_name(package_importable_name)
        DirectoryProxy.__init__(self, directory_name=directory_name, session=session)
        self._package_short_name = None
        self.package_importable_name = package_importable_name
        self._purview = None

    ### OVERLOADS ###

    def __repr__(self):
        if self.package_importable_name is not None:
            return '{}({!r})'.format(self.class_name, self.package_importable_name)
        else:
            return '{}()'.format(self.class_name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def directory_name(self):
        if self.package_importable_name is not None:
            return self._package_importable_name_to_directory_name(self.package_importable_name)

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
            parent_directory_name = self._package_importable_name_to_directory_name(
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
                return self._package_importable_name_to_purview(self.package_importable_name)
        def fset(self, purview):
            if self.package_importable_name is None:
                self._purview = purview
            else:
                raise ValueError('package importable name already assigned.')
        return property(**locals())

    @property
    def purview_name(self):
        if self.score is not None:
            return self.score.title
        else:
            return 'studio'

    @property
    def score(self):
        import baca
        if isinstance(self.purview, baca.scf.ScoreProxy):
            return self.purview

    ### PRIVATE METHODS ###

    def _package_importable_name_to_directory_name(self, package_importable_name):
        if package_importable_name is None:
            return
        package_importable_name_parts = package_importable_name.split('.')
        if package_importable_name_parts[0] == 'baca':
            directory_parts = [os.environ.get('BACA')] + package_importable_name_parts[1:]
        elif package_importable_name_parts[0] in os.listdir(os.environ.get('SCORES')):
            directory_parts = [os.environ.get('SCORES')] + package_importable_name_parts[:]
        else:
            raise ValueError('Unknown package importable name {!r}.'.format(package_importable_name))
        directory = os.path.join(*directory_parts)
        return directory

    def _package_importable_name_to_purview(self, package_importable_name):
        import baca
        if package_importable_name is None:
            return
        elif package_importable_name.split('.')[0] == 'baca':
            return baca.scf.GlobalProxy()
        elif package_importable_name.split('.')[0] in os.listdir(os.environ.get('SCORES')):
            return baca.scf.ScoreProxy(package_importable_name.split('.')[0])
        else:
            raise ValueError('Unknown package importable name {!r}.'.format(package_importable_name))

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
                new_line = '{} = {!r}\n'.format(name, value)
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        if not found_existing_line:
            new_line = '{} = {!r}\n'.format(name, value)
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

    def add_tag_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.prompts.append('Tag name')
        getter.prompts.append('Tag value')
        getter.should_clear_terminal = False
        user_input = getter.run()
        if user_input:
            tag_name, tag_value = user_input
            self.add_tag(tag_name, tag_value)
            confirm_line = 'Tag added.\n'
            self.display_lines([confirm_line])
        if self.session.user_input is None:
            self.proceed()

    def create_initializer(self):
        if self.has_initializer:
            raise OSError('package {!r} already has initializer.'.format(self))
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

    def delete_tag_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.prompts.append('Tag name')
        getter.should_clear_terminal = False
        user_input = getter.run()
        if user_input:
            tag_name = user_input
            self.delete_tag(tag_name)
            confirm_line = 'tag deleted.\n'
            self.display_lines([confirm_line])
        if self.session.user_input is None:
            self.proceed()

    def edit_initializer(self):
        os.system('vi {}'.format(self.initializer_file_name))

    def edit_parent_initializer(self):
        os.system('vi {}'.format(self.parent_initializer_file_name))

    def import_attribute_from_initializer(self, attribute_name):
        try:
            exec('from {} import {}'.format(self.package_importable_name, attribute_name))
            exec('result = {}'.format(attribute_name))
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
            exec('from {} import tags'.format(self.package_importable_name))
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
            formatted_tag = '{!r}: {!r}'.format(key, tags[key])
            formatted_tags.append(formatted_tag)
        return formatted_tags

    def manage_tags(self):
        self.session.menu_pieces.append('tags')
        while True:
            menu = self.make_new_menu(where=self.where())
            section = self.MenuSection()
            section.lines_to_list = self.list_formatted_tags()
            menu.menu_sections.append(section)
            section = self.MenuSection()
            section.sentence_length_items.append(('add', 'add tag'))
            section.sentence_length_items.append(('del', 'delete tag'))
            menu.menu_sections.append(section)
            key, value = menu.run()
            if self.session.session_is_complete:
                return True
            if key == 'b':
                break
            elif key == 'add':
                self.add_tag_interactively()
            elif key == 'del':
                self.delete_tag_interactively()
        self.session.menu_pieces.pop()

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
        command = "if '{}' in sys.modules: del(sys.modules['{}'])".format(
            package_importable_name, package_importable_name)
        exec(command)

    def set_package_importable_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.prompts.append('package importable name')
        getter.tests.append(iotools.is_underscore_delimited_lowercase_package_name)
        getter.helps.append('must be underscore-delimited lowercase package name.')
        self.package_importable_name = getter.run()

    def set_package_spaced_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.prompts.append('package spaced name')
        getter.tests.append(iotools.is_space_delimited_lowercase_string)
        getter.helps.append('must be space-delimited lowercase string.')
        self.package_spaced_name = getter.run()

    def set_purview_interactively(self):
        from baca.scf.ScoreWrangler import ScoreWrangler
        menu = self.make_new_menu(where=self.where())
        score_wrangler = ScoreWrangler()
        menu.items_to_number = score_wrangler.iterate_score_titles_with_years()
        menu.named_pairs.append(('s', 'global to studio'))
        key, value = menu.run()
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
