from abjad.tools import iotools
from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.InitializerFileProxy import InitializerFileProxy
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

    # TODO: write test
    @property
    def initializer_file_proxy(self):
        return InitializerFileProxy(self.initializer_file_name, session=self.session)

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

    # TODO: write test; collapse with purview_name
    @property
    def purview(self):
        import baca
        if self.score_package_short_name is None:
            return baca.scf.HomePackageProxy()
        else:
            return baca.scf.ScorePackageProxy(self.score_package_short_name)

    # TODO: write test; collapse with purview
    @property
    def purview_name(self):
        if self.score_package_short_name is None:
            return self.studio_package_importable_name
        else:
            return self.score_package_short_name

    # TODO: write test; or remove?
    @property
    def score(self):
        import baca
        if self.score_package_short_name is not None:
            return baca.scf.ScorePackageProxy(self.score_package_short_name)

    # TODO: write test; or remove?
    @property
    def score_package_short_name(self):
        if not self.package_importable_name.startswith(self.studio_package_importable_name):
            return self.package_importable_name.split('.')[0]

    ### PUBLIC METHODS ###

    def add_tag(self, tag_name, tag_value):
        tags = self.get_tags()
        tags[tag_name] = tag_value
        self.initializer_file_proxy.write_tags_to_disk(tags)

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

    def delete_initializer(self, prompt=True):
        if self.has_initializer:
            os.remove(self.initializer_file_name)
            line = 'initializer deleted.'
            self.proceed(line, prompt=prompt)

    def delete_tag(self, tag_name):
        tags = self.get_tags()
        del(tags[tag_name])
        self.initializer_file_proxy.write_tags_to_disk(tags)

    def delete_tag_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('tag name')
        result = getter.run()
        if self.backtrack():
            return
        if result:
            tag_name = result
            self.delete_tag(tag_name)

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
        self.proceed(line)

    # TODO: try reimplementing with safe_import()
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

    # TODO: write tests
    def package_importable_name_to_purview(self, package_importable_name):
        import baca
        if package_importable_name is None:
            return
        elif package_importable_name.split('.')[0] == self.studio_package_importable_name:
            return baca.scf.HomePackageProxy()
        elif package_importable_name.split('.')[0] in os.listdir(os.environ.get('SCORES')):
            return baca.scf.ScorePackageProxy(package_importable_name.split('.')[0])
        else:
            raise ValueError('Unknown package importable name {!r}.'.format(package_importable_name))

    def remove(self):
        result = DirectoryProxy.remove(self)
        if result:
            line = 'package deleted.'
            self.proceed(line)
        
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

    # TODO: rename without hardcoding
    def unimport_baca_package(self):
        self.remove_package_importable_name_from_sys_modules(self.studio_package_importable_name)

    def unimport_package(self):
        self.remove_package_importable_name_from_sys_modules(self.package_importable_name)
