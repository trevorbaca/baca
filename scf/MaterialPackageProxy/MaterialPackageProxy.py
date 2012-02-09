from abjad.tools import iotools
from abjad.tools import markuptools
from abjad.tools import mathtools
from baca.scf.IllustrationBuilderModuleProxy import IllustrationBuilderModuleProxy
from baca.scf.IllustrationLyFileProxy import IllustrationLyFileProxy
from baca.scf.IllustrationPdfFileProxy import IllustrationPdfFileProxy
from baca.scf.MaterialDefinitionModuleProxy import MaterialDefinitionModuleProxy
from baca.scf.MaterialPackageMakerWrangler import MaterialPackageMakerWrangler
from baca.scf.OutputMaterialModuleProxy import OutputMaterialModuleProxy
from baca.scf.PackageProxy import PackageProxy
from baca.scf.StylesheetFileProxy import StylesheetFileProxy
from baca.scf.StylesheetWrangler import StylesheetWrangler
from baca.scf.UserInputModuleProxy import UserInputModuleProxy
from baca.scf.helpers import safe_import
import os


class MaterialPackageProxy(PackageProxy):

    def __init__(self, package_importable_name=None, session=None):
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        self._generic_output_name = None

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.package_spaced_name

    @property
    def has_complete_user_input_wrapper_in_memory(self):
        if self.has_user_input_wrapper_in_memory:
            return self.user_input_wrapper_in_memory.is_complete
        return False

    @property
    def has_complete_user_input_wrapper_on_disk(self):
        if self.has_user_input_wrapper_on_disk:
            return self.user_input_wrapper_on_disk.is_complete

    @property
    def has_illustration_builder_module(self):
        if self.should_have_illustration_builder_module:
            return os.path.exists(self.illustration_builder_module_file_name)
        return False

    @property
    def has_illustration_ly(self):
        if self.should_have_illustration_ly:
            return os.path.exists(self.illustration_ly_file_name)
        return False

    @property
    def has_illustration_pdf(self):
        if self.should_have_illustration_pdf:
            return os.path.exists(self.illustration_pdf_file_name)
        return False

    @property
    def has_initializer(self):
        if self.should_have_initializer:
            return os.path.exists(self.initializer_file_name)
        return False

    @property
    def has_material_definition(self):
        if self.should_have_material_definition_module:
            if self.has_material_definition_module:
                return bool(self.material_definition)
        return False

    @property
    def has_material_definition_module(self):
        if self.should_have_material_definition_module:
            return os.path.exists(self.material_definition_module_file_name)
        return False

    @property
    def has_material_package_maker(self):
        return bool(self.material_package_maker_class_name)

    @property
    def has_output_material(self):
        if self.should_have_output_material_module:
            if self.has_output_material_module:
                return bool(self.output_material_module_proxy.import_output_material_safely())
        return False

    @property
    def has_output_material_editor(self):
        return hasattr(self, 'output_material_editor')

    @property
    def has_output_material_module(self):
        if self.should_have_output_material_module:
            return os.path.exists(self.output_material_module_file_name)
        return False

    # TODO: impelement
    @property
    def has_stylesheet(self):
        return False

    @property
    def has_user_input_module(self):
        if self.should_have_user_input_module:
            return os.path.exists(self.user_input_module_file_name)
        return False

    @property
    def has_user_input_wrapper_on_disk(self):
        if self.should_have_user_input_module:
            return bool(self.user_input_module_proxy.read_user_input_wrapper_from_disk())
        return False

    @property
    def has_user_input_wrapper_in_memory(self):
        if self.should_have_user_input_module:
            return bool(self.user_input_wrapper_in_memory)
        return False

    @property
    def has_readable_illustration_builder_module(self):
        if self.has_illustration_builder_module:
            return self.illustration_builder_module_proxy.is_readable
        return False

    @property
    def has_readable_initializer(self):
        if self.has_initializer:
            return self.initializer_file_proxy.is_readable
        return False

    @property
    def has_readable_material_definition_module(self):
        if self.has_material_definition_module:
            return self.material_definition_module_proxy.is_readable
        return False

    @property
    def has_readable_output_material_module(self):
        if self.has_output_material_module:
            return self.output_material_module_proxy.is_readable
        return False

    @property
    def has_readable_user_input_module(self):
        if self.has_user_input_module:
            return self.user_input_module_proxy.is_readable
        return False

    @property
    def has_user_finalized_illustration_builder_module(self):
        if self.has_readable_illustration_builder_module:
            return self.illustration_builder_module_proxy.is_user_finalized

    @property
    def has_user_finalized_material_definition_module(self):
        if self.has_material_definition_module:
            return self.material_definition_module_proxy.is_user_finalized
        return False

    @property
    def illustration(self):
        if self.has_illustration_builder_module:
            return self.illustration_builder_module_proxy.import_illustration()

    @property
    def illustration_builder_module_file_name(self):
        if self.should_have_illustration_builder_module:
            return os.path.join(self.directory_name, 'illustration_builder.py')

    @property
    def illustration_builder_module_importable_name(self):
        if self.should_have_illustration_builder_module:
            return '.'.join([self.package_importable_name, 'illustration_builder'])

    @property
    def illustration_builder_module_proxy(self):
        if self.should_have_illustration_builder_module:
            if not self.has_illustration_builder_module:
                file(self.illustration_builder_module_file_name, 'w').write('')
            return IllustrationBuilderModuleProxy(
                self.illustration_builder_module_importable_name, session=self.session)

    @property
    def illustration_ly_file_name(self):
        if self.should_have_illustration_ly:
            return os.path.join(self.directory_name, 'illustration.ly')

    @property
    def illustration_ly_file_proxy(self):
        if self.should_have_illustration_ly:
            if not self.has_illustration_ly:
                file(self.illustration_ly_file_name, 'w').write('')
            return IllustrationLyFileProxy(self.illustration_ly_file_name, session=self.session)

    @property
    def illustration_pdf_file_name(self):
        if self.should_have_illustration_pdf:
            return os.path.join(self.directory_name, 'illustration.pdf')

    @property
    def illustration_pdf_file_proxy(self):
        if self.should_have_illustration_pdf:
            if not self.has_illustration_pdf:
                file(self.illustration_pdf_file_name, 'w').write('')
            return IllustrationPdfFileProxy(self.illustration_pdf_file_name, session=self.session)

    @property
    def initializer_has_output_material_safe_import_statement(self):
        if self.has_initializer:
            return self.initializer_file_proxy.has_safe_import_statement(
                'output_material', self.material_underscored_name)

    # TODO: port
    @property
    def is_changed(self):
        self.print_not_implemented()
        material_definition = self.material_definition_module_proxy.import_material_definition()
        output_material = self.output_material_module_proxy.import_output_material_safely()
        return material_definition != output_material

    @property
    def is_data_only(self):
        return not self.should_have_illustration

    @property
    def is_handmade(self):
        return not(self.has_material_package_maker)

    @property
    def is_makermade(self):
        return self.has_material_package_maker

    # TODO: replace with self.material_definition_module_proxy.material_definition
    @property
    def material_definition(self):
        if self.has_readable_material_definition_module:
            pair = self.output_material_module_import_statements_and_material_definition
            material_definition = pair[1]
            return material_definition

    @property
    def output_material(self):
        if self.has_readable_output_material_module:
            return self.output_material_module_proxy.import_output_material()
    
    @property
    def output_material_module_import_statements_and_material_definition(self):
        if self.should_have_material_definition_module:
            tmp = self.material_definition_module_proxy
            return tmp.import_output_material_module_import_statements_and_material_definition()

    @property
    def material_definition_module_file_name(self):
        if self.should_have_material_definition_module:
            return os.path.join(self.directory_name, 'material_definition.py')

    @property
    def material_definition_module_importable_name(self):
        if self.should_have_material_definition_module:
            return '.'.join([self.package_importable_name, 'material_definition'])

    @property
    def material_definition_module_proxy(self):
        if self.should_have_material_definition_module:
            if self.has_material_definition_module:
                return MaterialDefinitionModuleProxy(
                    self.material_definition_module_importable_name, session=self.session)

    @property
    def material_package_directory(self):
        if self.materials_directory_name:
            if self.material_package_short_name:
                return os.path.join(self.materials_directory_name, self.material_package_short_name)

    @property
    def material_package_maker(self):
        if self.material_package_maker_class_name is not None:
            maker_class = safe_import(
                locals(), 'materialpackagemakers', self.material_package_maker_class_name,
                source_parent_package_importable_name=self.scf_package_importable_name)
            return maker_class

    @property
    def material_package_maker_class_name(self):
        return self.get_tag('material_package_maker_class_name')

    @property
    def material_package_short_name(self):
        return self.material_underscored_name

    @property
    def material_spaced_name(self):
        return self.material_underscored_name.replace('_', ' ')

    @property
    def material_underscored_name(self):
        return self.package_short_name

    @property
    def materials_directory_name(self):
        return self.package_importable_name_to_directory_name(self.materials_package_importable_name)

    @property
    def materials_package_importable_name(self):
        return '.'.join(self.package_importable_name.split('.')[:-1])

    @property
    def output_material_module_body_lines(self):
        if self.should_have_material_definition_module:
            return self.output_material_module_import_statements_and_output_material_module_body_lines[1]

    @property
    def output_material_module_import_statements_and_output_material_module_body_lines(self):
        if self.should_have_material_definition_module:
            pair = self.output_material_module_import_statements_and_material_definition
            output_material_module_import_statements, output_material = pair
        elif self.has_material_package_maker:
            output_material_module_import_statements = self.output_material_module_import_statements
            output_material = self.make_output_material_from_user_input_wrapper_in_memory()
        else:
            raise ValueError
        if hasattr(self, 'make_output_material_module_body_lines'):
            output_material_module_body_lines = self.make_output_material_module_body_lines(output_material)
        else:
            line = '{} = {!r}'.format(self.material_underscored_name, output_material)
            output_material_module_body_lines = [line]
        return output_material_module_import_statements, output_material_module_body_lines

    @property
    def output_material_module_file_name(self): 
        if self.should_have_output_material_module:
            return os.path.join(self.directory_name, 'output_material.py')

    @property
    def output_material_module_importable_name(self):
        if self.should_have_output_material_module:
            return '{}.output_material'.format(self.package_importable_name)

    @property
    def output_material_module_proxy(self):
        if self.should_have_output_material_module:
            if self.has_output_material_module:
                return OutputMaterialModuleProxy(
                    self.output_material_module_importable_name, session=self.session)

    @property
    def parent_initializer_has_output_material_safe_import_statement(self):
        if self.has_parent_initializer:
            return self.parent_initializer_file_proxy.has_safe_import_statement(
            self.material_underscored_name, self.material_underscored_name)

    @property
    def should_have_illustration(self):
        return self.get_tag('should_have_illustration')

    @property
    def should_have_illustration_builder_module(self):
        if self.should_have_illustration:
            if self.material_package_maker_class_name is None:
                return True
        return False

    @property
    def should_have_illustration_ly(self):
        return self.should_have_illustration

    @property
    def should_have_illustration_pdf(self):
        return self.should_have_illustration

    @property
    def should_have_initializer(self):
        return True

    @property
    def should_have_material_definition_module(self):
        return self.material_package_maker_class_name is None

    @property
    def should_have_output_material_module(self):
        return True

    @property
    def should_have_stylesheet(self):
        return self.should_have_illustration

    @property
    def should_have_user_input_module(self):
        return self.material_package_maker_class_name is not None

    # TODO: implement
    @property
    def stylesheet_file_name(self):
        if self.should_have_stylesheet:
            self.print_not_implemented()

    @property
    def stylesheet_file_proxy(self):
        if self.should_have_stylesheet:
            return StylesheetFileProxy(self.stylesheet_file_name, session=self.session)

    @property
    def user_input_module_file_name(self): 
        if self.should_have_user_input_module:
            return os.path.join(self.directory_name, 'user_input.py')
    
    @property
    def user_input_module_importable_name(self):
        if self.should_have_user_input_module:
            return '.'.join([self.package_importable_name, 'user_input'])

    @property
    def user_input_module_proxy(self):
        if self.should_have_user_input_module:
            if not self.has_user_input_module:
                file(self.user_input_module_file_name, 'w').write('')
            return UserInputModuleProxy(self.user_input_module_importable_name, session=self.session)
    
    ### PUBLIC METHODS ###

    def add_material_to_material_initializer(self):
        self.initializer_file_proxy.add_safe_import_statement(
            'output_material', self.material_underscored_name)
        
    def add_material_to_materials_initializer(self):
        parent_package = PackageProxy(self.parent_package_importable_name, session=self.session)
        parent_package.initializer_file_proxy.add_safe_import_statement(
            self.material_underscored_name, self.material_underscored_name)

    def delete_illustration_builder_module(self, prompt=True):
        self.delete_illustration_pdf(prompt=False)
        if self.has_illustration_builder_module:
            self.illustration_builder_module_proxy.remove(prompt=prompt)

    def delete_illustration_ly(self, prompt=True):
        if self.has_illustration_ly:
            self.illustration_ly_file_proxy.remove(prompt=prompt)

    def delete_illustration_pdf(self, prompt=True):
        self.delete_illustration_ly(prompt=False)
        if self.has_illustration_pdf:
            self.illustration_pdf_file_proxy.remove(prompt=prompt)

    def delete_material_definition_module(self, prompt=True):
        self.delete_output_material_module(prompt=False)
        self.delete_illustration_builder_module(prompt=False)
        if self.has_material_definition_module:
            self.material_definition_module_proxy.remove(prompt=prompt)

    def delete_material_package(self):
        self.remove()
        self.session.is_backtracking_locally = True

    def delete_output_material_module(self, prompt=True):
        self.delete_illustration_builder_module(prompt=False)
        if self.has_output_material_module:
            self.output_material_module_proxy.remove(prompt=prompt)

    # NOTE: not currently used
    def delete_parent_initializer_pyc_file(self):
        if self.has_parent_initializer:
            parent_initializer_pyc_file_name = self.parent_initializer_file_name + 'c'
            if os.path.exists(parent_initializer_pyc_file_name):
                os.remove(parent_initializer_pyc_file_name)
        
    def delete_user_input_module(self, prompt=True):
        if self.has_user_input_module:
            self.user_input_module_proxy.remove(prompt=prompt)

    def edit_output_material_interactively(self):
        if not self.has_output_material_editor:
            return
        if self.has_output_material_module:
            self.print_not_implemented()
        else:
            output_material_editor = self.output_material_editor(session=self.session)
            output_material_editor.run()

    # TODO: audit
    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'uic':
            self.clear_user_input_wrapper(prompt=False)    
        elif result == 'uid':
            self.delete_user_input_module(prompt=True)
        elif result == 'uil':
            self.load_user_input_wrapper_demo_values(prompt=False)
        elif result == 'uip':
            self.populate_user_input_wrapper(prompt=False)
        elif result == 'uis':
            self.show_user_input_demo_values(prompt=True)
        elif result == 'uit':
            self.session.swap_user_input_values_default_status()
        elif result == 'uimv':
            self.user_input_module_proxy.view()
        elif result == 'mdcanned':
            self.material_definition_module_proxy.write_canned_file_to_disk(prompt=True)
        elif result == 'mddelete':
            self.delete_material_definition_module(prompt=True)
        elif result == 'mde':
            self.material_definition_module_proxy.edit()
        elif result == 'mdstub':
            self.write_stub_material_definition_module_to_disk(prompt=True)
        elif result == 'mdx':
            self.material_definition_module_proxy.run_python(prompt=True)
        elif result == 'mdxe':
            self.material_definition_module_proxy.run_abjad(prompt=True)
        elif result == 'ibd':
            self.delete_illustration_builder_module(prompt=True)
        elif result == 'ibe':
            self.illustration_builder_module_proxy.edit()
        elif result == 'ibt':
            self.illustration_builder_module_proxy.write_stub_to_disk(prompt=True)
        elif result == 'ibx':
            self.illustration_builder_module_proxy.run_python(prompt=True)
        elif result == 'ibxi':
            self.illustration_builder_module_proxy.run_abjad(prompt=True)
        elif result == 'ssm':
            self.stylesheet_file_proxy.edit()
        elif result == 'sss':
            self.select_stylesheet_interactively()
        elif result == 'stl':
            self.manage_stylesheets()
        elif result == 'omm':
            self.write_output_material_to_disk()
        elif result == 'omi':
            self.edit_output_material_interactively()
        elif result == 'omcanned':
            self.output_material_module_proxy.write_canned_file_to_disk(prompt=True)
        elif result == 'omdelete':
            self.delete_output_material_module(prompt=True)
        elif result == 'omv':
            self.output_material_module_proxy.view()
        elif result == 'omfetch':
            self.output_material_module_proxy.display_output_material()
        elif result == 'lym':
            self.write_illustration_ly_to_disk(is_forced=True)
        elif result == 'lyd':
            self.delete_illustration_ly(prompt=True)
        elif result == 'lyv':
            self.illustration_ly_file_proxy.view()
        elif result == 'pdfm':
            self.write_illustration_ly_and_pdf_to_disk(is_forced=True)
        elif result == 'pdfd':
            self.delete_illustration_pdf(prompt=True)
        elif result == 'pdfv':
            self.illustration_pdf_file_proxy.view()
        elif result == 'del':
            self.delete_material_package()
        elif result == 'inr':
            self.initializer_file_proxy.restore_interactively(prompt=True)
        elif result == 'inv':
            self.initializer_file_proxy.view()
        elif result == 'incanned':
            self.initializer_file_proxy.write_canned_file_to_disk(prompt=True)
        elif result == 'instub':
            self.initializer_file_proxy.write_stub_file_to_disk(prompt=True)
        elif result == 'ren':
            self.rename_material_interactively()
        elif result == 'reg':
            self.regenerate_everything(prompt=True)
        # TODO: add to package-level hidden menu
        elif result == 'tags':
            self.manage_tags()
        # TODO: add to directory-level hidden menu
        elif result == 'ls':
            self.print_directory_contents()
        elif mathtools.is_integer_equivalent_expr(result):
            self.edit_user_input_at_number(int(result))
        else:
            raise ValueError

    def make_main_menu(self):
        menu, hidden_section = self.make_new_menu(where=self.where(), is_hidden=True)
        self.make_main_menu_section_for_initializer(menu, hidden_section)
        self.make_main_menu_sections(menu, hidden_section)
        self.make_main_menu_section_for_illustration_ly(menu, hidden_section)
        self.make_main_menu_section_for_illustration_pdf(menu, hidden_section)
        self.make_main_menu_section_for_hidden_entries(menu)
        return menu
    
    def make_main_menu_section_for_hidden_entries(self, main_menu):
        hidden_section = main_menu.make_new_section(is_hidden=True)
        hidden_section.append(('del', 'delete package'))
        hidden_section.append(('ls', 'list package'))
        hidden_section.append(('reg', 'regenerate package'))
        hidden_section.append(('ren', 'rename package'))
        hidden_section.append(('stl', 'manage stylesheets'))
        hidden_section.append(('tags', 'manage tags'))

    def make_main_menu_section_for_illustration_builder(self, main_menu, hidden_section):
        section = main_menu.make_new_section()
        if self.has_output_material:
            if self.should_have_illustration:
                if not self.has_illustration_builder_module:
                    self.illustration_builder_module_proxy.write_stub_to_disk(prompt=False)
                section.append(('ibe', 'illustration builder - edit'))
                if self.has_output_material:
                    section.append(('ibx', 'illustration builder - execute'))
                hidden_section.append(('ibd', 'illustration builder - delete'))
                hidden_section.append(('ibt', 'illustration builder - stub'))
                hidden_section.append(('ibex', 'illustration builder - edit & execute'))
                section.append(('sss', 'score stylesheet - select'))
                hidden_section.append(('ssm', 'source stylesheet - edit'))

    def make_main_menu_section_for_illustration_ly(self, main_menu, hidden_section):
        if self.has_output_material:
            if self.has_illustration_builder_module or self.has_material_package_maker:
                hidden_section.append(('lym', 'output ly - make'))
        if self.has_illustration_ly:
            hidden_section.append(('lyd', 'output ly - delete'))
            hidden_section.append(('lyv', 'output ly - view'))

    def make_main_menu_section_for_illustration_pdf(self, main_menu, hidden_section):
        has_illustration_pdf_section = False
        if self.has_output_material:
            if self.has_illustration_builder_module or self.has_material_package_maker:
                section = main_menu.make_new_section()
                has_illustration_pdf_section = True
                section.append(('pdfm', 'output pdf - make'))
        if self.has_illustration_pdf:
            if not has_illustration_pdf_section:
                section = main_menu.make_new_section()
            hidden_section.append(('pdfd', 'output pdf - delete'))
            section.append(('pdfv', 'output pdf - view'))

    def make_main_menu_section_for_initializer(self, main_menu, hidden_section):
        if not self.has_initializer:
            section = main_menu.make_new_section()
            section.section_title = '(Note: package has no initializer.)' 
            section.append(('inr', 'initializer - restore'))
        elif not self.has_readable_initializer:
            section = main_menu.make_new_section()
            section.section_title = '(Note: package has invalid initializer.)' 
            section.append(('inr', 'initializer - restore'))
        hidden_section.append(('inv', 'view package initializer'))
        hidden_section.append(('incanned', 'copy canned package initializer'))
        hidden_section.append(('instub', 'write stub package initializer'))

    def make_main_menu_section_for_material_definition(self, main_menu, hidden_section):
        if not self.has_readable_initializer:
            return
        section = main_menu.make_new_section()
        if self.has_material_definition_module:
            has_invalid_material_definition_module = not self.has_readable_material_definition_module
            if has_invalid_material_definition_module:
                section.section_title = '(Note: has invalid material definition module.)'
            section.append(('mde', 'material definition - edit'))
            if not has_invalid_material_definition_module:
                section.append(('mdx', 'material definition - execute'))
            hidden_section.append(('mdcanned', 'material definition - copy canned module'))
            hidden_section.append(('mddelete', 'material definition - delete'))
            hidden_section.append(('mdstub', 'material definition - stub'))
            if not has_invalid_material_definition_module:
                hidden_section.append(('mdxe', 'material definition - execute & edit'))
        elif self.material_package_maker_class_name is None:
            section.append(('mdstub', 'material definition - stub'))

    def make_main_menu_section_for_output_material(self, main_menu, hidden_section):
        if not self.has_readable_initializer:
            return
        has_output_material_section = False
        if self.has_readable_material_definition_module or \
            self.has_complete_user_input_wrapper_in_memory or \
            self.has_output_material_editor:
            if self.has_material_definition or \
                self.has_complete_user_input_wrapper_in_memory:
                section = main_menu.make_new_section()
                if self.has_output_material_module and not self.has_readable_output_material_module:
                    section.section_title = '(Note: has invalid output material module.)'
                section.append(('omm', 'output material - make'))
                has_output_material_section = True
            if self.has_output_material_editor:
                section = main_menu.make_new_section()
                section.append(('omi', 'output material - interact'))
                has_output_material_section = True
            if self.has_output_material_module:
                if not has_output_material_section:
                    section = main_menu.make_new_section()
                section.append(('omv', 'output material - view'))
                hidden_section.append(('omdelete', 'output material - delete'))
                hidden_section.append(('omfetch', 'output material - fetch'))
        hidden_section.append(('omcanned', 'output material - copy canned module'))

    def make_main_menu_sections(self, menu, hidden_section):
        self.make_main_menu_section_for_material_definition(menu, hidden_section)
        self.make_main_menu_section_for_output_material(menu, hidden_section)
        self.make_main_menu_section_for_illustration_builder(menu, hidden_section)

    def manage_stylesheets(self):
        stylesheet_wrangler = StylesheetWrangler(session=self.session)
        stylesheet_wrangler.run()

    def overwrite_output_material_module(self):
        file(self.output_material_module_file_name, 'w').write('')

    # TODO: port
    def regenerate_everything(self, prompt=True):
        self.print_not_implemented()

    def remove(self):
        self.remove_material_from_materials_initializer()
        PackageProxy.remove(self)

    def remove_material_from_materials_initializer(self):
        import_statement = 'safe_import(globals(), {!r}, {!r})\n'
        import_statement = import_statement.format(
            self.material_underscored_name, self.material_underscored_name)
        parent_package = PackageProxy(self.parent_package_importable_name, session=self.session)
        parent_package_initializer_file_proxy = parent_package.initializer_file_proxy
        filtered_import_statements = []
        for safe_import_statement in parent_package_initializer_file_proxy.safe_import_statements:
            if not safe_import_statement == import_statement:
                filtered_import_statements.append(safe_import_statement)
        parent_package_initializer_file_proxy.safe_import_statements[:] = filtered_import_statements
        parent_package_initializer_file_proxy.write_to_disk()

    # TODO: port
    def rename_material_interactively(self):
        line = 'current material name: {}'.format(self.material_underscored_name)
        self.display(line)
        getter = self.make_new_getter(where=self.where())
        getter.append_string('new material name')
        new_material_spaced_name = getter.run()
        if self.backtrack():
            return
        new_material_underscored_name = new_material_spaced_name.replace(' ', '_')
        lines = []
        lines.append('current material name: {}'.format(self.material_underscored_name))
        lines.append('new material name:     {}'.format(new_material_underscored_name))
        lines.append('')
        self.display(lines)
        if not self.confirm():
            return
        if self.is_in_repository:
            # update parent initializer
            self.helpers.globally_replace_in_file(self.parent_initializer_file_name, 
                self.material_underscored_name, new_material_underscored_name)
            # rename package directory
            new_directory_name = self.directory.replace(
                self.material_underscored_name, new_material_underscored_name)
            command = 'svn mv {} {}'.format(self.directory_name, new_directory_name)
            os.system(command)
            # update package initializer
            parent_directory_name = os.path.directory(self.directory_name)
            new_package_directory = os.path.join(parent_directory_name, new_material_underscored_name)
            new_initializer = os.path.join(new_package_directory, '__init__.py')
            self.helpers.globally_replace_in_file(
                new_initializer, self.material_underscored_name, new_material_underscored_name)
            # rename files in package
            for old_file_name in os.listdir(new_package_directory):
                if not old_file_name.startswith(('.', '_')):
                    old_directory_name = os.path.join(new_package_directory, old_file_name)
                    new_directory_name = old_directory_name.replace(
                        self.material_underscored_name, new_material_underscored_name)
                    command = 'svn mv {} {}'.format(old_directory_name, new_directory_name)
                    os.system(command)
            # rename output material
            new_output_material = os.path.join(new_package_directory, 'output_material.py')
            self.helpers.globally_replace_in_file(
                new_output_material, self.material_underscored_name, new_material_underscored_name)
            # commit
            commit_message = 'renamed {} to {}.'.format(
                self.material_underscored_name, new_material_underscored_name)
            commit_message = commit_message.replace('_', ' ')
            command = 'svn commit -m "{}" {}'.format(commit_message, self.parent_directory_name)
            os.system(command)
        else:
            raise NotImplementedError('commit to repository and then rename.')

    def run(self, user_input=None, clear=True, cache=False):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu()
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

    def select_material_package_maker_interactively(self, prompt=True):
        material_proxy_wrangler = MaterialPackageMakerWrangler(session=self.session)
        self.push_backtrack()
        material_package_maker = material_proxy_wrangler.select_material_proxy_class_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        self.add_tag('material_package_maker', material_package_maker.class_name)
        line = 'user input handler selected.'
        self.proceed(line, prompt=prompt)

    def select_stylesheet_interactively(self, prompt=True):
        stylesheet_wrangler = StylesheetWrangler(session=self.session)
        self.push_backtrack()
        stylesheet_file_name = stylesheet_wrangler.select_stylesheet_file_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        # TODO: replace with something nonlocal
        #self.link_local_stylesheet(stylesheet_file_name, prompt=prompt)

    # NOTE: not currently used
    def touch_parent_initializer(self):
        if self.has_parent_initializer:
            self.parent_initializer_file_proxy.touch()

    def write_illustration_ly_and_pdf_to_disk(self, is_forced=False, prompt=True):
        illustration = self.illustration
        iotools.write_expr_to_pdf(illustration, self.illustration_pdf_file_name, print_status=False)
        iotools.write_expr_to_ly(illustration, self.illustration_ly_file_name, print_status=False)
        self.proceed(['PDF and LilyPond file written to disk.'], prompt=prompt)

    def write_illustration_ly_to_disk(self, is_forced=False, prompt=True):
        illustration = self.illustration
        iotools.write_expr_to_ly(illustration, self.illustration_ly_file_name, print_status=False)
        self.proceed(['LilyPond file written to disk.'], prompt=prompt)

    def write_illustration_pdf_to_disk(self, is_forced=False, prompt=True):
        illustration = self.illustration
        iotools.write_expr_to_pdf(illustration, self.illustration_pdf_file_name, print_status=False)
        self.proceed(['PDF written to disk.'], prompt=prompt)

    def write_output_material_to_disk(self, prompt=True):
        self.remove_material_from_materials_initializer()
        self.overwrite_output_material_module()
        output_material_module_proxy = self.output_material_module_proxy
        pair = self.output_material_module_import_statements_and_output_material_module_body_lines
        output_material_module_import_statements, output_material_module_body_lines = pair
        output_material_module_import_statements = [x + '\n' for x in output_material_module_import_statements]
        output_material_module_proxy.setup_statements = output_material_module_import_statements
        output_material_module_proxy.body_lines[:] = output_material_module_body_lines
        output_material_module_proxy.write_to_disk()
        self.add_material_to_materials_initializer()
        self.add_material_to_material_initializer()
        line = 'output material written to disk.'
        self.proceed(line, prompt=prompt)

    def write_stub_material_definition_module_to_disk(self, prompt=True):
        if self.should_have_material_definition_module:
            file(self.material_definition_module_file_name, 'w').write('')
            self.material_definition_module_proxy.write_stub_to_disk(self.is_data_only, prompt=True)
