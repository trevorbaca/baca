from abjad.tools import iotools
from baca.scf.PackageProxy import PackageProxy
import os


class MakerProxy(PackageProxy):

    def __init__(self, maker_class_name=None, session=None):
        self.maker_class_name = maker_class_name
        if maker_class_name is not None:
            package_importable_name = 'baca.scf.makers.{}'.format(maker_class_name)
        else:
            package_importable_name = None
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)

    ### OVERLOADS ###

    def __repr__(self):
        if self.maker_class_name is None:
            return '{}()'.format(self.class_name)
        else:
            return '{}({!r})'.format(self.class_name, self.maker_class_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###
    
    @property
    def breadcrumb(self):
        return self.maker_name

    ### READ / WRITE PUBLIC ATTRIBUTES ###

    # TODO: Maybe this can't be set here? Must be derived from hardcoded maker classfile?
    @apply
    def generic_output_name():
        def fget(self):
            return self._generic_output_name
        def fset(self, generic_output_name):
            assert isinstance(generic_output_name, (str, type(None)))
            if isinstance(generic_output_name):
                assert iotools.is_underscore_delimited_lowercase_string(generic_output_name)
            self._generic_output_name = generic_output_name
        return property(**locals())

    @apply
    def maker_class_name():
        def fget(self):
            return self._maker_class_name
        def fset(self, maker_class_name):
            assert isinstance(maker_class_name, (str, type(None)))
            if isinstance(maker_class_name, str):
                assert iotools.is_uppercamelcase_string(maker_class_name)
            self._maker_class_name = maker_class_name
        return property(**locals())

    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, key):
        if key == 'del':
            self.delete_package()
            return False
        elif key == 'new':
            self.run()
        elif key == 'ren':
            self.print_not_implemented()
        elif key == 'src':
            self.edit_source_file()
        else:
            material_proxy = value
            material_proxy.run()
    
    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.section_title = 'existing {}'.format(self.generic_output_name)
        section.tokens = list(self.iterate_materials_based_on_maker())
        section = menu.make_new_section()
        section.append(('del', 'delete {}'.format(self.spaced_class_name)))
        section.append(('new', 'create {}'.format(self.generic_output_name)))
        section.append(('ren', 'rename {}'.format(self.spaced_class_name)))
        section.append(('src', 'edit {} source'.format(self.spaced_class_name)))
        return menu

    def make_tags_dictionary(self):
        tags = {}
        tags['creation_date'] = self.helpers.get_current_date()
        tags['maker'] = self.class_name
        return tags

    def run(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        while True:
            self.append_breadcrumb()
            menu = self.make_main_menu()
            result = menu.run()
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()

    def write_stub_initializer_to_disk(self):
        initializer = file(os.path.join(self.material_package_directory, '__init__.py'), 'w')
        initializer.write('from output import *\n')
        initializer.write('import datetime\n')
        initializer.write('\n\n')
        tags_dictionary = self.make_tags_dictionary()
        initializer.write('tags = {!r}\n'.format(tags_dictionary))
        initializer.close()
