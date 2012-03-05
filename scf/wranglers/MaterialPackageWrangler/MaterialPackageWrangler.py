from abjad.tools import iotools
from scf import predicates
from scf.wranglers.PackageWrangler import PackageWrangler
import collections
import os


# TODO: write all iteration tests
class MaterialPackageWrangler(PackageWrangler):

    def __init__(self, session=None):
        from scf.wranglers.MaterialPackageMakerWrangler import MaterialPackageMakerWrangler
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

    def get_asset_proxy(self, package_importable_name):
        return self.material_package_maker_wrangler.get_asset_proxy(package_importable_name)

    def get_appropriate_material_package_proxy(self, 
        material_package_maker_class_name, material_package_importable_name):
        import scf
        if material_package_maker_class_name is None: 
            material_package_proxy = scf.proxies.MaterialPackageProxy(
                material_package_importable_name, session=self.session)
        else:
            command = 'material_package_proxy = '
            command += 'scf.makers.{}(material_package_importable_name, session=self.session)'
            command = command.format(material_package_maker_class_name)
            exec(command)
        return material_package_proxy

    def get_available_material_package_importable_name_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
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

    def handle_main_menu_result(self, result):
        if result == 'd':
            self.make_data_package_interactively()
        elif result == 's':
            self.make_numeric_sequence_package_interactively()
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
        
    def make_asset_interactively(self):
        return NotImplemented

    def make_data_package(self, material_package_importable_name, tags=None):
        material_package_maker_class_name = None
        should_have_illustration = False
        should_have_user_input_module = False
        self.make_material_package(material_package_importable_name, 
            material_package_maker_class_name, 
            should_have_illustration, 
            should_have_user_input_module,
            tags=tags)

    def make_data_package_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.push_backtrack()
        material_package_importable_name = self.get_available_material_package_importable_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.make_data_package(material_package_importable_name)

    # TODO: write test
    def make_handmade_material_package(self, material_package_importable_name, tags=None):
        material_package_maker_class_name = None
        should_have_illustration = True
        should_have_user_input_module = False
        self.make_material_package(material_package_importable_name, 
            material_package_maker_class_name, 
            should_have_illustration, 
            should_have_user_input_module,
            tags=tags)

    # TODO: write test
    def make_handmade_material_package_interactively(self):
        self.push_backtrack()
        material_package_importable_name = self.get_available_material_package_importable_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.make_handmade_material_package(material_package_importable_name)

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_numbered=True, is_keyed=False)
        section.tokens = self.make_visible_asset_menu_tokens(head=head)
        section = menu.make_section()
        section.append(('d', 'data-only'))
        section.append(('s', 'numeric sequence'))
        section.append(('h', 'handmade'))
        section.append(('m', 'maker-made'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('missing', 'create missing packages'))
        hidden_section.append(('profile', 'profile packages'))
        return menu

    # TODO: write test
    def make_makermade_material_package(self, 
        material_package_importable_name, material_package_maker_class_name, tags=None):
        command = 'from scf.makers import {} as material_package_maker_class'.format(
            material_package_maker_class_name)
        exec(command)
        should_have_user_input_module = getattr(
            material_package_maker_class, 'should_have_user_input_module', True)
        should_have_illustration = hasattr(material_package_maker_class, 'illustration_maker')
        self.make_material_package(material_package_importable_name, 
            material_package_maker_class_name, 
            should_have_illustration, 
            should_have_user_input_module,
            tags=tags)

    # TODO: write test
    def make_makermade_material_package_interactively(self):
        self.push_backtrack()
        result = self.material_package_maker_wrangler.select_asset_importable_name_interactively(
            cache=True, clear=False)
        self.pop_backtrack()
        if self.backtrack():
            return
        material_package_maker_importable_name = result
        material_package_maker_class_name = material_package_maker_importable_name.split('.')[-1]
        self.push_backtrack()
        material_package_importable_name = self.get_available_material_package_importable_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.make_makermade_material_package(
            material_package_importable_name, material_package_maker_class_name)

    # TODO: write test
    def make_material_package(self, material_package_importable_name, material_package_maker_class_name, 
        should_have_illustration, should_have_user_input_module, is_interactive=False, tags=None):
        assert iotools.is_underscore_delimited_lowercase_package_name(material_package_importable_name)
        assert predicates.is_class_name_or_none(material_package_maker_class_name)
        assert isinstance(should_have_illustration, bool)
        assert isinstance(should_have_user_input_module, bool)
        path_name = self.package_importable_name_to_path_name(material_package_importable_name)
        assert not os.path.exists(path_name)
        os.mkdir(path_name)
        file(os.path.join(path_name, '__init__.py'), 'w').write('')
        material_package_proxy = self.get_appropriate_material_package_proxy(
            material_package_maker_class_name, material_package_importable_name)
        tags = tags or {}
        tags = collections.OrderedDict(tags)
        tags['material_package_maker_class_name'] = material_package_maker_class_name
        tags['should_have_illustration'] = should_have_illustration
        tags['should_have_user_input_module'] = should_have_user_input_module
        #material_package_proxy.initializer_file_proxy.write_stub_to_disk(tags=tags)
        material_package_proxy.initializer_file_proxy.write_stub_to_disk()
        material_package_proxy.tags_file_proxy.write_tags_to_disk(tags)
        if material_package_maker_class_name is None:
            file(os.path.join(path_name, 'material_definition.py'), 'w').write('')
            is_data_only = not should_have_illustration
            material_package_proxy.material_definition_module_proxy.write_stub_to_disk(
                is_data_only, prompt=False)
        if should_have_user_input_module:
            material_package_proxy.write_stub_user_input_module_to_disk(prompt=False)
        line = 'material package {!r} created.'.format(material_package_importable_name)
        self.proceed(line, is_interactive=is_interactive)
