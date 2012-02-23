from abjad.tools import iotools
from baca.scf.proxies.DirectoryProxy import DirectoryProxy
from baca.scf.proxies.InitializerFileProxy import InitializerFileProxy
from baca.scf.helpers import safe_import
import os
import sys


# TODO: find way to add 'list package directory' user command, somehow
class PackageProxy(DirectoryProxy):

    def __init__(self, package_importable_name=None, session=None):
        directory_name = self.package_importable_name_to_path_name(package_importable_name)
        DirectoryProxy.__init__(self, directory_name=directory_name, session=session)
        self._importable_name = package_importable_name

    ### OVERLOADS ###

    def __repr__(self):
        if self.importable_name is not None:
            return '{}({!r})'.format(self.class_name, self.importable_name)
        else:
            return '{}()'.format(self.class_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def directory_name(self):
        if self.importable_name is not None:
            return self.package_importable_name_to_path_name(self.importable_name)

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
    def has_parent_initializer(self):
        if self.parent_initializer_file_name is not None:
            return os.path.isfile(self.parent_initializer_file_name)

    @property
    def has_tags_file(self):
        return os.path.isfile(self.tags_file_name)

    @property
    def human_readable_name(self):
        return self.short_name.replace('_', ' ')

    @property
    def initializer_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, '__init__.py')

    # TODO: write test
    @property
    def initializer_file_proxy(self):
        if self.has_initializer:
            return InitializerFileProxy(self.initializer_file_name, session=self.session)

    @property
    def importable_name(self):
        return self._importable_name

    @property
    def package_root_name(self):
        return self.importable_name.split('.')[0]

    @property
    def parent_initializer_file_name(self):
        if self.parent_package_importable_name:
            parent_directory_name = self.package_importable_name_to_path_name(
                self.parent_package_importable_name)
            return os.path.join(parent_directory_name, '__init__.py')

    # TODO: write test
    @property
    def parent_initializer_file_proxy(self):
        if self.has_parent_initializer:
            return InitializerFileProxy(
                self.parent_initializer_file_name, session=self.session)

    @property
    def parent_package_importable_name(self):
        if self.importable_name is not None:
            result = self.dot_join(self.importable_name.split('.')[:-1])
            if result:
                return result

    # TODO: write test; or remove?
    @property
    def score(self):
        import baca
        if self.score_package_short_name is not None:
            return baca.scf.proxies.ScorePackageProxy(self.score_package_short_name)

    # TODO: write test; or remove?
    @property
    def score_package_short_name(self):
        if not self.importable_name.startswith(self.home_package_importable_name):
            return self.importable_name.split('.')[0]

    @property
    def tags_file_name(self):
        return os.path.join(self.directory_name, 'tags.py')

    @property
    def tags_file_proxy(self):
        if self.has_tags_file:
            return InitializerFileProxy(self.tags_file_name, session=self.session)


    ### PUBLIC METHODS ###

    def add_tag(self, tag_name, tag_value):
        tags = self.get_tags()
        tags[tag_name] = tag_value
        if self.has_tags_file:
            self.tags_file_proxy.write_tags_to_disk(tags)
        else:
            self.initializer_file_proxy.write_tags_to_disk(tags)

    def add_tag_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('tag name')
        getter.append_string('tag value')
        result = getter.run()
        if self.backtrack():
            return
        if result:
            tag_name, tag_value = result
            self.add_tag(tag_name, tag_value)

    def fix(self, is_interactive=True):
        self.print_implemented_on_child_classes()
        return True

    def remove_initializer(self, prompt=True):
        if self.has_initializer:
            os.remove(self.initializer_file_name)
            line = 'initializer deleted.'
            self.proceed(line, prompt=prompt)

    def remove_tag(self, tag_name):
        tags = self.get_tags()
        del(tags[tag_name])
        if self.has_tags_file:
            self.tags_file_proxy.write_tags_to_disk(tags)
        else:
            self.initializer_file_proxy.write_tags_to_disk(tags)

    def remove_tag_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('tag name')
        result = getter.run()
        if self.backtrack():
            return
        if result:
            tag_name = result
            self.remove_tag(tag_name)

    def get_tag(self, tag_name):
        tags = self.get_tags()
        tag = tags.get(tag_name, None)
        return tag

    def get_tag_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('tag name')
        result = getter.run()
        if self.backtrack():
            return
        tag = self.get_tag(result)
        line = '{!r}'.format(tag)
        self.proceed(line)

    def get_tags(self):
        import collections
        tags = self.read_tags_from_tags_file()
        if tags is None:
            tags = safe_import(locals(), self.short_name, 'tags', 
                source_parent_package_importable_name=self.parent_package_importable_name)
        if tags is None:
            tags = collections.OrderedDict([])
        #tags = self.read_tags_from_disk() or collections.OrderedDict([])
        return tags

    def handle_tags_menu_result(self, result):
        if result == 'add':
            self.add_tag_interactively()
        elif result == 'rm':
            self.remove_tag_interactively()
        elif result == 'get':
            self.get_tag_interactively()
        return False

    def has_tag(self, tag_name):
        tags = self.get_tags()
        return bool(tag_name in tags)

    def make_tags_menu(self):
        menu, section = self.make_menu(where=self.where(), is_keyed=False)
        section.tokens = self.formatted_tags
        section = menu.make_section()
        section.append(('add', 'add tag'))
        section.append(('rm', 'delete tag'))
        section.append(('get', 'get tag'))
        return menu

    def manage_tags(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb('tags')
            menu = self.make_tags_menu()
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            self.handle_tags_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    def profile(self):
        self.print_implemented_on_child_classes()

    def read_tags_from_tags_file(self):
        from collections import OrderedDict
        if not os.path.exists(self.tags_file_name):
            return
        file_pointer = open(self.tags_file_name, 'r')
        file_contents_string = file_pointer.read()
        file_pointer.close()
        exec(file_contents_string)
        result = locals().get('tags') or OrderedDict([])
        return result

    def remove(self):
        result = DirectoryProxy.remove(self)
        if result:
            line = 'package removed.'
            self.proceed(line)
        
    def set_package_importable_name_interactively(self):
        getter = self.make_getter(where=self.where())
        geter.append_underscore_delimited_lowercase_package_name('package importable name')
        result = getter.run()
        if self.backtrack():
            return
        self.importable_name = result

    def unimport_package(self):
        self.remove_package_importable_name_from_sys_modules(self.importable_name)
