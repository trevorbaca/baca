from abjad.tools import iotools
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from baca.scf.wranglers.PackageWrangler import PackageWrangler
import os


class MaterialPackageMakerWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self, 
            score_external_asset_container_importable_name= \
                self.makers_package_importable_name, 
            score_internal_asset_container_importable_name_infix=None,
            session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def base_class_name(self):
        return self.dot_join(['baca.scf.makers', 'MaterialPackageMaker'])

    @property
    def breadcrumb(self):
        return 'material package makers'

    @property
    def score_external_wrangled_asset_importable_names(self):
        result = PackageWrangler.score_external_wrangled_asset_importable_names.fget(self)
        result.remove(self.base_class_name)
        return result

    ### PUBLIC METHODS ###

    def get_wrangled_asset_proxy(self, package_importable_name):
        from baca.scf.proxies.MaterialPackageProxy import MaterialPackageProxy
        material_package_proxy = MaterialPackageProxy(package_importable_name, session=self.session)
        material_package_maker_class_name = material_package_proxy.material_package_maker_class_name
        if material_package_maker_class_name is not None:
            material_package_maker_class = None
            command = 'from baca.scf.makers import {} as material_package_maker_class'
            command = command.format(material_package_maker_class_name)
            exec(command)
            material_package_proxy = material_package_maker_class(
                package_importable_name, session=self.session)
        return material_package_proxy
            
    def handle_main_menu_result(self, result):
        if result == 'new':
            self.make_wrangled_asset_interactively()
        else:
            raise ValueError

    def list_score_internal_asset_container_importable_names(self, head=None):
        return []

    def list_wrangled_asset_human_readable_names(self, head=None):
        result = []
        for name in self.list_wrangled_asset_short_names(head=head):
            spaced_class_name = iotools.uppercamelcase_to_space_delimited_lowercase(name)
            result.append(spaced_class_name)
        return result

    def list_wrangled_asset_menuing_pairs(self, head=None):
        keys = self.list_wrangled_asset_short_names(head=head)
        bodies = self.list_wrangled_asset_human_readable_names(head=head)
        return zip(keys, bodies)
        
    def make_class_selection_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_keyed=False, is_numbered=True)
        section.tokens = self.list_wrangled_asset_menuing_pairs(head=self.home_package_importable_name)
        section.return_value_attribute = 'key'
        return menu

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_numbered=True)
        section.tokens = self.list_wrangled_asset_human_readable_names(head=head)
        section = menu.make_section()
        section.append(('new', 'new material package maker'))
        return menu

    # TODO: implement MaterialPackageProxyClassFile object to model and customize these settings
    def make_wrangled_asset_class_file(self, package_short_name, generic_output_name):
        class_file_name = os.path.join(
            self.score_external_asset_container_importable_name, 
            package_short_name, package_short_name + '.py')
        class_file = file(class_file_name, 'w')
        lines = []
        lines.append('from baca.music.foo import foo')
        lines.append('from baca.music.foo import make_illustration_from_output_material')
        lines.append('from baca.scf.makers.MaterialPackageMaker import MaterialPackageMaker')
        lines.append('from baca.scf.editors.UserInputWrapper import UserInputWrapper')
        lines.append('import baca')
        lines.append('')
        lines.append('')
        lines.append('class {}(MaterialPackageMaker):'.format(package_short_name))
        lines.append('')
        lines.append('    def __init__(self, package_importable_name=None, session=None):')
        lines.append('        MaterialPackageMaker.__init__(')
        lines.append('            self, package_importable_name=package_importable_name, session=seession')
        lines.append('')
        lines.append('    ### READ-ONLY PUBLIC ATTRIBUTES ###')
        lines.append('')
        lines.append('    generic_output_name = {!r}'.format(generic_output_name))
        lines.append('')
        lines.append('    illustration_maker = staticmethod(make_illustration_from_output_material)')
        lines.append('')
        lines.append('    output_material_checker = staticmethod(componenttools.all_are_components)')
        lines.append('')
        lines.append('    output_material_maker = staticmethod(baca.music.foo)')
        lines.append('')
        lines.append('    output_material_module_import_statements = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_demo_values = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_module_import_statements = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    user_input_tests = [')
        lines.append('        ]')
        lines.append('')
        lines.append('    ### PUBLIC METHODS ###')
        lines.append('')
        lines.append('    @property')
        lines.append('    def output_material_module_body_lines(self):')
        lines.append('        lines = []')
        lines.append('        output_material = self.output_material')
        lines.append("        lines.append('{} = {!r}'.format(self.material_underscored_name, output_material)")
        class_file.write('\n'.join(lines))
        class_file.close()

    # TODO: change to boilerplate file stored in material_package_maker package
    def make_wrangled_asset_initializer(self, package_short_name):
        initializer_file_name = os.path.join(
            self.score_external_asset_container_importable_name, 
            package_short_name, '__init__.py')
        initializer = file(initializer_file_name, 'w')
        line = 'from abjad.tools.importtools._import_structured_package import _import_structured_package\n'
        initializer.write(line)
        initializer.write('\n')
        initializer.write("_import_structured_package(__path__[0], globals(), 'baca')\n")
        initializer.close() 

    def make_wrangled_asset_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_material_package_maker_class_name('material proxy name')
        getter.append_space_delimited_lowercase_string('generic output product')
        result = getter.run()
        if self.backtrack():
            return
        material_package_maker_class_name, generic_output_product_name = result
        material_package_maker_directory = os.path.join(
            self.score_external_asset_container_importable_name, material_package_maker_class_name)
        os.mkdir(material_package_maker_directory)
        self.make_wrangled_asset_initializer(material_package_maker_class_name)
        self.make_wrangled_asset_class_file(
            material_package_maker_class_name, generic_output_product_name)
        self.make_wrangled_asset_stylesheet(material_package_maker_class_name)

    # TODO: change to boilerplate file stored somewhere
    def make_wrangled_asset_stylesheet(self, package_short_name):
        stylesheet = lilypondfiletools.make_basic_lilypond_file()
        stylesheet.pop()
        stylesheet.file_initial_system_comments = []
        stylesheet.default_paper_size = 'letter', 'portrait'
        stylesheet.global_staff_size = 14
        stylesheet.layout_block.indent = 0
        stylesheet.layout_block.ragged_right = True
        stylesheet.paper_block.makup_system_spacing = layouttools.make_spacing_vector(0, 0, 12, 0)
        stylesheet.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 10, 0)
        stylesheet_file_name = os.path.join(
            self.score_external_asset_container_importable_name, 
            package_short_name, 'stylesheet.ly')
        stylesheet_file_pointer = file(stylesheet_file_name, 'w')
        stylesheet_file_pointer.write(stylesheet.format)
        stylesheet_file_pointer.close()

    def run(self, cache=False, clear=True, head=None, user_input=None):
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

    # TODO: write test
    def select_wrangled_package_class_name_interactively(
        self, clear=True, cache=False, head=None, user_input=None):
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb('select material proxy:')
            menu = self.make_class_selection_menu(head=head)
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue 
            else:
                break
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        return result
