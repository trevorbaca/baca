from abjad.tools import iotools
from baca.scf.PackageWrangler import PackageWrangler
import collections
import os


class MaterialPackageWrangler(PackageWrangler):

    def __init__(self, session=None):
        import baca
        PackageWrangler.__init__(self, 
            self.studio_materials_package_importable_name, 'mus.materials', session=session)
        self._material_package_maker_wrangler = baca.scf.MaterialPackageMakerWrangler(session=self.session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'materials'

    @property
    def material_package_maker_wrangler(self):
        return self._material_package_maker_wrangler
    
    ### PUBLIC METHODS ###

    # TODO: write test
    def get_new_material_package_importable_name_interactively(self):
        import baca
        getter = self.make_new_getter(where=self.where())
        getter.append_underscore_delimited_lowercase_package_name('material name')
        self.push_backtrack()
        material_name = getter.run()
        self.pop_backtrack()
        if self.backtrack():
            return
        material_package_short_name = iotools.string_to_strict_directory_name(material_name)
        studio = baca.scf.Studio(session=self.session)
        self.push_backtrack()
        package_root_name = studio.get_package_root_name_interactively(clear=False)
        self.pop_backtrack()
        if self.backtrack():
            return
        materials_package_importable_name = \
            self.package_root_name_to_materials_package_importable_name(package_root_name)
        material_package_importable_name = '{}.{}'.format(
            materials_package_importable_name, material_package_short_name)
        if self.package_exists(material_package_importable_name):
            line = 'Material package {!r} already exists.'.format(material_package_importable_name)
            self.proceed(line)
            return
        return material_package_importable_name

    def get_package_proxy(self, package_importable_name):
        return self.material_package_maker_wrangler.get_package_proxy(package_importable_name)

    def handle_main_menu_result(self, result):
        if result == 'd':
            self.make_data_package_interactively()
        elif result == 'h':
            self.make_handmade_material_package_interactively()
        elif result == 'm':
            self.make_editable_material_package_interactively()
        else:
            material_proxy = self.get_package_proxy(result)
            material_proxy.run()
        
    # TODO: write test
    def make_data_package_interactively(self):
        self.push_backtrack()
        material_package_importable_name = self.get_new_material_package_importable_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        material_package_maker_class_name = None
        should_have_illustration = False
        self.make_material_package(
            material_package_importable_name, material_package_maker_class_name, should_have_illustration)

    # TODO: write test
    def make_editable_material_package_interactively(self):
        self.push_backtrack()
        material_package_importable_name = self.get_new_material_package_importable_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.push_backtrack()
        material_package_maker_class_name = \
            self.material_package_maker_wrangler.select_material_proxy_class_name_interactively(
                clear=False, cache=True)
        self.pop_backtrack()
        if self.backtrack():
            return
        # TODO: set following attribute by editor automatically
        should_have_illustration = True
        self.make_material_package(
            material_package_importable_name, material_package_maker_class_name, should_have_illustration)

    # TODO: write test
    def make_handmade_material_package_interactively(self):
        material_package_importable_name = self.get_new_material_package_importable_name_interactively()
        material_package_maker_class_name = None
        should_have_illustration = True
        self.make_material_package(
            material_package_importable_name, material_package_maker_class_name, should_have_illustration)

    def make_main_menu(self, head=None):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True, is_keyed=False)
        section.tokens = self.list_wrangled_package_menuing_pairs(head=head)
        section = menu.make_new_section()
        section.append(('d', 'make data'))
        section.append(('h', 'make material by hand'))
        section.append(('m', 'make material with maker'))
        return menu

    # TODO: write test
    def make_material_package(self, material_package_importable_name, material_package_maker_class_name, 
        should_have_illustration, prompt=True):
        '''True on success.'''
        import baca
        assert iotools.is_underscore_delimited_lowercase_package_name(material_package_importable_name)
        assert material_package_maker_class_name is None or iotools.is_uppercamelcase_string(
            material_package_maker_class_name)
        assert isinstance(should_have_illustration, bool)
        directory_name = self.package_importable_name_to_directory_name(material_package_importable_name)
        if os.path.exists(directory_name):
            line = 'package {!r} already exists.'.format(material_name)
            self.proceed(line, prompt=prompt)
            return False
        os.mkdir(directory_name)
        file(os.path.join(directory_name, '__init__.py'), 'w').write('')
        if material_package_maker_class_name is None: 
            material_proxy = baca.scf.MaterialPackageProxy(
                material_package_importable_name, session=self.session)
        else:
            command = 'material_proxy = baca.scf.materialpackagemakers.{}(material_package_importable_name, session=self.session)'.format(material_package_maker_class_name)
            exec(command)
        tags = collections.OrderedDict([])
        tags['material_package_maker_class_name'] = material_package_maker_class_name
        tags['should_have_illustration'] = should_have_illustration
        material_proxy.initializer_file_proxy.write_stub_to_disk(tags=tags)
        if material_package_maker_class_name is None:
            file(os.path.join(directory_name, 'material_definition.py'), 'w').write('')
            is_data_only = not should_have_illustration
            material_proxy.material_definition_module_proxy.write_stub_to_disk(is_data_only, prompt=False)
        else:
            material_proxy.write_stub_user_input_module_to_disk(prompt=False)
        line = 'material package {!r} created.'.format(material_package_importable_name)
        self.proceed(line, prompt=prompt)
        return True

    # TODO: write tests
    def package_root_name_to_materials_package_importable_name(self, package_root_name):
        assert isinstance(package_root_name, str)
        result = []
        result.append(package_root_name)
        if not package_root_name == self.studio_package_importable_name:
            result.append('mus')
        result.append('materials')
        result = '.'.join(result)
        return result

    def run(self, user_input=None, head=None, clear=True, cache=False):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu(head=head)
            result = menu.run(clear=clear)
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
        self.restore_breadcrumbs(cache=cache)
