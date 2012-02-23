from abjad.tools import iotools
from baca.scf.wranglers.PackageWrangler import PackageWrangler
import collections
import os


class MaterialPackageWrangler(PackageWrangler):

    def __init__(self, session=None):
        from baca.scf.wranglers.MaterialPackageMakerWrangler import MaterialPackageMakerWrangler
        PackageWrangler.__init__(self, 
            score_external_asset_container_importable_names= \
                [self.score_external_materials_package_importable_name], 
            score_internal_asset_container_importable_name_infix= \
                self.score_internal_materials_package_importable_name_infix,
            session=session)
        self._material_package_maker_wrangler = MaterialPackageMakerWrangler(session=self.session)

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
        while True:
            getter = self.make_getter(where=self.where())
            getter.append_space_delimited_lowercase_string('material name')
            self.push_backtrack()
            material_name = getter.run()
            self.pop_backtrack()
            if self.backtrack():
                return
            material_package_short_name = iotools.string_to_strict_directory_name(material_name)
            material_package_importable_name = self.dot_join([
                self.current_asset_container_importable_name, material_package_short_name])
            if self.package_exists(material_package_importable_name):
                line = 'Material package {!r} already exists.'.format(material_package_importable_name)
                self.display([line, ''])
            else:
                return material_package_importable_name

    def get_asset_proxy(self, package_importable_name):
        return self.material_package_maker_wrangler.get_asset_proxy(package_importable_name)

    def handle_main_menu_result(self, result):
        if result == 'd':
            self.make_data_package_interactively()
        elif result == 'h':
            self.make_handmade_material_package_interactively()
        elif result == 'm':
            self.make_makermade_material_package_interactively()
        elif result == 'missing':
            self.conditionally_make_asset_container_packages(is_interactive=True)
        elif result == 'profile':
            self.profile_visible_assets()
        else:
            material_package_proxy = self.get_asset_proxy(result)
            material_package_proxy.run()
        
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
    def make_handmade_material_package_interactively(self):
        material_package_importable_name = self.get_new_material_package_importable_name_interactively()
        material_package_maker_class_name = None
        should_have_illustration = True
        self.make_material_package(
            material_package_importable_name, material_package_maker_class_name, should_have_illustration)

    # TODO: write test
    def make_makermade_material_package_interactively(self):
        self.push_backtrack()
        result = self.material_package_maker_wrangler.select_asset_importable_name_interactively(
            clear=False, cache=True)
        material_package_maker_importable_name = result
        material_package_maker_class_name = material_package_maker_importable_name.split('.')[-1]
        self.pop_backtrack()
        if self.backtrack():
            return
        self.push_backtrack()
        material_package_importable_name = self.get_new_material_package_importable_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        # TODO: set following attribute by editor automatically
        should_have_illustration = True
        self.make_material_package(
            material_package_importable_name, material_package_maker_class_name, should_have_illustration)

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_numbered=True, is_keyed=False)
        section.tokens = self.make_visible_asset_menu_tokens(head=head)
        section = menu.make_section()
        section.append(('d', 'data-only'))
        section.append(('h', 'handmade'))
        section.append(('m', 'maker-made'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('missing', 'create missing packages'))
        hidden_section.append(('profile', 'profile packages'))
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
        directory_name = self.package_importable_name_to_path_name(material_package_importable_name)
        if os.path.exists(directory_name):
            line = 'package {!r} already exists.'.format(material_name)
            self.proceed(line, prompt=prompt)
            return False
        os.mkdir(directory_name)
        file(os.path.join(directory_name, '__init__.py'), 'w').write('')
        if material_package_maker_class_name is None: 
            material_package_proxy = baca.scf.proxies.MaterialPackageProxy(
                material_package_importable_name, session=self.session)
        else:
            command = 'material_package_proxy = baca.scf.makers.{}(material_package_importable_name, session=self.session)'.format(material_package_maker_class_name)
            exec(command)
        tags = collections.OrderedDict([])
        tags['material_package_maker_class_name'] = material_package_maker_class_name
        tags['should_have_illustration'] = should_have_illustration
        material_package_proxy.initializer_file_proxy.write_stub_to_disk(tags=tags)
        if material_package_maker_class_name is None:
            file(os.path.join(directory_name, 'material_definition.py'), 'w').write('')
            is_data_only = not should_have_illustration
            material_package_proxy.material_definition_module_proxy.write_stub_to_disk(is_data_only, prompt=False)
        else:
            material_package_proxy.write_stub_user_input_module_to_disk(prompt=False)
        line = 'material package {!r} created.'.format(material_package_importable_name)
        self.proceed(line, prompt=prompt)
        return True

    # TODO: write tests
    def package_root_name_to_materials_package_importable_name(self, package_root_name):
        assert isinstance(package_root_name, str)
        result = []
        result.append(package_root_name)
        if not package_root_name == self.home_package_importable_name:
            result.append('mus')
        result.append('materials')
        result = self.dot_join(result)
        return result
