from abjad.tools import iotools
from baca.scf.DirectoryProxy import DirectoryProxy
import os
import sys


# TODO: find way to add 'list package directory' user command, somehow
class PackageProxy(DirectoryProxy):

    def __init__(self, package_importable_name=None, session=None):
        directory_name = self.package_importable_name_to_directory_name(package_importable_name)
        DirectoryProxy.__init__(self, directory_name=directory_name, session=session)
        self._package_short_name = None
        self._package_importable_name = package_importable_name

    ### OVERLOADS ###

    def __repr__(self):
        if self.package_importable_name is not None:
            return '{}({!r})'.format(self.class_name, self.package_importable_name)
        else:
            return '{}()'.format(self.class_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def directory_name(self):
        if self.package_importable_name is not None:
            return self.package_importable_name_to_directory_name(self.package_importable_name)

    @property
    def formatted_tags(self):
        formatted_tags = []
        tags = self.get_tags()
        for key in sorted(tags):
            formatted_tag = '{!r}: {!r}'.format(key, tags[key])
            formatted_tags.append(formatted_tag)
        return formatted_tags

    @property
    def has_initializer(self):
        if self.initializer_file_name is not None:
            return os.path.isfile(self.initializer_file_name)

    @property
    def initializer_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, '__init__.py')

    @property
    def package_importable_name(self):
        return self._package_importable_name

    @property
    def package_short_name(self):
        return self.package_importable_name.split('.')[-1]

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

    # TODO: write test
    @property
    def purview(self):
        import baca
        if self.score_package_short_name is None:
            return baca.scf.GlobalProxy()
        else:
            return baca.scf.ScoreProxy(self.score_package_short_name)

    # TODO: write test
    @property
    def purview_name(self):
        if self.score_package_short_name is None:
            return 'baca'
        else:
            return self.score_package_short_name

    # TODO: write test
    @property
    def score(self):
        import baca
        if self.score_package_short_name is not None:
            return baca.scf.ScoreProxy(self.score_package_short_name)

    # TODO: write test
    @property
    def score_package_short_name(self):
        if not self.package_importable_name.startswith('baca'):
            return self.package_importable_name.split('.')[0]

    ### PUBLIC METHODS ###

    def add_import_statement_to_initializer(self, import_statement):
        initializer_import_statements, initializer_tag_lines = self.parse_initializer()
        initializer_import_statements = set(initializer_import_statements)
        initializer_import_statements.add(import_statement)
        initializer_import_statements = list(initializer_import_statements)
        initializer_import_statements.sort()
        self.write_initializer_to_disk(initializer_import_statements, initializer_tag_lines)

    def add_tag(self, tag_name, tag_value):
        tags = self.get_tags()
        tags[tag_name] = tag_value
        self.write_tags_to_initializer(tags)

    def add_tag_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('tag name')
        getter.append_string('tag value')
        result = getter.run()
        if self.backtrack():
            return
        if result:
            tag_name, tag_value = result
            self.add_tag(tag_name, tag_value)

    def delete_package(self):
        result = self.remove()
        if result:
            line = 'package deleted.'
            self.proceed(lines=[line])
        
    def delete_tag(self, tag_name):
        tags = self.get_tags()
        del(tags[tag_name])
        self.write_tags_to_initializer(tags)

    def delete_tag_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('tag name')
        result = getter.run()
        if self.backtrack():
            return
        if result:
            tag_name = result
            self.delete_tag(tag_name)

    def edit_initializer(self):
        os.system('vi {}'.format(self.initializer_file_name))

    def edit_parent_initializer(self):
        os.system('vi {}'.format(self.parent_initializer_file_name))

    def get_tag(self, tag_name):
        tags = self.get_tags()
        tag = tags.get(tag_name, None)
        return tag

    def get_tag_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('tag name')
        result = getter.run()
        if self.backtrack():
            return
        tag = self.get_tag(result)
        line = '{!r}'.format(tag)
        self.proceed(lines=[line])

    def get_tags(self):
        import collections
        try:
            command = 'from {} import tags'.format(self.package_importable_name)
            exec(command)
        except ImportError:    
            tags = collections.OrderedDict([])
        return tags

    def handle_tags_menu_result(self, result):
        if result == 'add':
            self.add_tag_interactively()
        elif result == 'del':
            self.delete_tag_interactively()
        elif result == 'get':
            self.get_tag_interactively()
        return False

    def has_tag(self, tag_name):
        tags = self.get_tags()
        return bool(tag_name in tags)

    def make_tags_menu(self):
        menu, section = self.make_new_menu(where=self.where(), is_keyed=False)
        section.tokens = self.formatted_tags
        section = menu.make_new_section()
        section.append(('add', 'add tag'))
        section.append(('del', 'delete tag'))
        section.append(('get', 'get tag'))
        return menu

    def manage_tags(self):
        while True:
            self.append_breadcrumb('tags')
            menu = self.make_tags_menu()
            result = menu.run()
            if self.backtrack():
                break
            self.handle_tags_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()

    # TODO: write tests
    def package_importable_name_to_purview(self, package_importable_name):
        import baca
        if package_importable_name is None:
            return
        elif package_importable_name.split('.')[0] == 'baca':
            return baca.scf.GlobalProxy()
        elif package_importable_name.split('.')[0] in os.listdir(os.environ.get('SCORES')):
            return baca.scf.ScoreProxy(package_importable_name.split('.')[0])
        else:
            raise ValueError('Unknown package importable name {!r}.'.format(package_importable_name))

    # TODO: write test
    def parse_initializer(self, initializer_file_name=None):
        if initializer_file_name is None:
            initializer_file_name = self.initializer_file_name
        initializer = file(initializer_file_name, 'r')
        initializer_import_statements = []
        initializer_tag_lines = []
        found_tags = False
        for line in initializer.readlines():
            if line == '\n':
                pass
            elif line.startswith('tags ='):
                found_tags = True
                initializer_tag_lines.append(line)
            elif not found_tags:
                initializer_import_statements.append(line)
            else:
                initializer_tag_lines.append(line)
        initializer.close()
        return initializer_import_statements, initializer_tag_lines

    # TODO: write test
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

    # TODO: write test
    def remove_import_statement_from_initializer(self, import_statement, initializer_file_name):
        initializer_import_statements, initializer_tag_lines = self.parse_initializer(initializer_file_name)
        initializer_import_statements = [x for x in initializer_import_statements if x != import_statement] 
        self.write_initializer_to_disk(
            initializer_import_statements, initializer_tag_lines, initializer_file_name)

    def remove_package_importable_name_from_sys_modules(self, package_importable_name):
        '''Total hack. But works.'''
        command = "if '{}' in sys.modules: del(sys.modules['{}'])".format(
            package_importable_name, package_importable_name)
        exec(command)

    def set_package_importable_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        # TODO: implement getter.append_package_name
        getter.prompts.append('package importable name')
        getter.tests.append(iotools.is_underscore_delimited_lowercase_package_name)
        getter.helps.append('must be underscore-delimited lowercase package name.')
        result = getter.run()
        if self.backtrack():
            return
        self.package_importable_name = result

    def set_package_spaced_name_interactively(self):
        getter = self.make_new_getter(where=self.where())
        # TODO: implement package spaced name
        getter.prompts.append('package spaced name')
        getter.tests.append(iotools.is_space_delimited_lowercase_string)
        getter.helps.append('must be space-delimited lowercase string.')
        result = getter.run()
        if self.backtrack():
            return
        self.package_spaced_name = result

    def unimport_baca_package(self):
        self.remove_package_importable_name_from_sys_modules('baca')

    def unimport_package(self):
        self.remove_package_importable_name_from_sys_modules(self.package_importable_name)

    # TODO: write test
    def write_initializer_to_disk(self, 
        initializer_import_statements, initializer_tag_lines, initializer_file_name=None):
        if initializer_file_name is None:
            initializer_file_name = self.initializer_file_name
        initializer_lines = []
        initializer_lines.extend(initializer_import_statements)
        if initializer_import_statements and initializer_tag_lines:
            initializer_lines.extend(['\n', '\n'])
        initializer_lines.extend(initializer_tag_lines)
        initializer = file(initializer_file_name, 'w')
        initializer.write(''.join(initializer_lines))
        initializer.close()

    # TODO: write test
    def write_stub_initializer_to_disk(self, tags=None):
        initializer_import_statements = ['from collections import OrderedDict\n']
        initializer_tag_lines = self.pprint_tags(tags)
        self.write_initializer_to_disk(initializer_import_statements, initializer_tag_lines)

    # TODO: write test
    def write_tags_to_initializer(self, tags):
        import_statement = 'from collections import OrderedDict\n'
        self.add_import_statement_to_initializer(import_statement)
        initializer_import_statements, initializer_tag_lines = self.parse_initializer()
        initializer_tag_lines = self.pprint_tags(tags)
        self.write_initializer_to_disk(initializer_import_statements, initializer_tag_lines)
