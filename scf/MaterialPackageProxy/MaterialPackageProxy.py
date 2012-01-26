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
import baca
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
    def has_complete_user_input_wrapper(self):
        if self.has_user_input_wrapper:
            user_input_wrapper = self.user_input_wrapper
            return user_input_wrapper.is_complete
        return False

    @property
    def has_illustration(self):
        if not self.has_illustration_builder:
            return False
        else:
            return bool(self.illustration_builder_module_proxy.import_illustration())

    @property
    def has_illustration_builder(self):
        if self.illustration_builder_module_file_name is None:
            return False
        else:
            return os.path.exists(self.illustration_builder_module_file_name)

    @property
    def has_illustration_ly(self):
        if self.illustration_ly_file_name is None:
            return False
        else:
            return os.path.exists(self.illustration_ly_file_name)

    @property
    def has_illustration_pdf(self):
        if self.illustration_pdf_file_name is None:
            return False
        else:
            return os.path.exists(self.illustration_pdf_file_name)

    @property
    def has_material_definition(self):
        if not self.has_material_definition_module:
            return False
        else:
            return bool(self.material_definition_module_proxy.import_material_definition())

    @property
    def has_material_definition_module(self):
        if self.material_definition_module_file_name is None:
            return False
        else:
            return os.path.exists(self.material_definition_module_file_name)

    @property
    def has_material_package_maker(self):
        return bool(self.material_package_maker_class_name)

    @property
    def has_output_material(self):
        if not self.has_output_material_module:
            return False
        else:
            return bool(self.output_material_module_proxy.import_output_material())

    @property
    def has_output_material_module(self):
        if self.output_material_module_file_name is None:
            return False
        else:
            return os.path.exists(self.output_material_module_file_name)

    @property
    def has_user_input_module(self):
        if self.user_input_module_file_name is None:
            return False
        else:
            return os.path.exists(self.user_input_module_file_name)

    @property
    def has_user_input_wrapper(self):
        if not self.has_user_input_module:
            return False
        else:
            return bool(self.user_input_module_proxy.import_user_input_wrapper())

    @property
    def illustration(self):
        return self.illustration_builder_module_proxy.import_illustration()

    @property
    def illustration_builder_module_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'illustration_builder.py')

    @property
    def illustration_builder_module_proxy(self):
        if not self.has_illustration_builder:
            file(self.illustration_builder_module_file_name, 'w').write('')
        return IllustrationBuilderModuleProxy(
            self.illustration_builder_module_importable_name, session=self.session)

    @property
    def illustration_builder_module_importable_name(self):
        if self.illustration_builder_module_file_name is not None:
            return '{}.illustration_builder'.format(self.package_importable_name)

    @property
    def illustration_ly_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'illustration.ly')

    @property
    def illustration_ly_file_proxy(self):
        return IllustrationLyFileProxy(self.illustration_ly_file_name, session=self.session)

    @property
    def illustration_pdf_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'illustration.pdf')

    @property
    def illustration_pdf_file_proxy(self):
        return IllustrationPdfFileProxy(self.illustration_pdf_file_name, session=self.session)

    # TODO: make work
    @property
    def is_changed(self):
        material_definition = self.material_definition_module_proxy.import_material_definition()
        output_material = self.output_material_module_proxy.import_output_material()
        return material_definition != output_material

    @property
    def is_data_only(self):
        return not self.should_have_illustration

    @property
    def is_handmade(self):
        return not(self.has_material_package_maker)

    @property
    def material_definition_module_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'material_definition.py')

    # TODO: write test
    @property
    def material_definition_module_proxy(self):
        if not self.has_material_definition_module:
            file(self.material_definition_module_file_name, 'w').write('')    
        return MaterialDefinitionModuleProxy(
            self.material_definition_module_importable_name, session=self.session)

    @property
    def material_definition_module_importable_name(self):
        if self.material_definition_module_file_name is not None:
            return '{}.material_definition'.format(self.package_importable_name)

    @property
    def material_package_directory(self):
        if self.materials_directory_name:
            if self.material_package_short_name:
                return os.path.join(self.materials_directory_name, self.material_package_short_name)

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
        if self.score is None:
            return self.baca_materials_directory
        else:
            return self.score.materials_directory_name

    # TODO: remove
#    @property
#    def materials_package_importable_name(self):
#        result = self.package_importable_name
#        result = result.split('.')
#        result = result[:-1]
#        result = '.'.join(result)
#        return result

    # TODO: reimplement with helpers.safe_import()
    @property
    def material_package_maker(self):
        material_package_maker_class_name = self.material_package_maker_class_name
        try:
            command = 'from baca.scf.materialpackagemakers import {}'.format(material_package_maker_class_name)
            exec(command)
            command = 'result = {}(client_material_package_importable_name={!r}, session=self.session)'
            command = command.format(material_package_maker_class_name, self.package_importable_name)
            exec(command)
            return result
        except:
            pass

    @property
    def material_package_maker_class_name(self):
        return self.get_tag('material_package_maker_class_name')

    # TODO: ambigous; change name to show explicitly material comes from
    @property
    def output_material(self):
        return self.material_definition_module_proxy.import_material_definition()

    @property
    def output_material_module_body_lines(self):
        lines = []
        output_material = self.output_material
        lines.append('{} = {!r}'.format(self.material_underscored_name, output_material))
        return lines

    @property
    def output_material_module_file_name(self): 
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'output_material.py')

    # TODO: write test
    @property
    def output_material_module_proxy(self):
        if not self.has_output_material_module:
            file(self.output_material_module_file_name, 'w').write('')    
        return OutputMaterialModuleProxy(self.output_material_module_importable_name, session=self.session)

    @property
    def output_material_module_importable_name(self):
        if self.output_material_module_file_name is not None:
            return '{}.output_material'.format(self.package_importable_name)

    @property
    def score_package_short_name(self):
        if self.package_importable_name is not None:
            if self.package_importable_name.startswith(self.studio_package_importable_name):
                return self.package_importable_name.split('.')[0]

    @property
    def should_have_illustration(self):
        return self.get_tag('should_have_illustration')

    # TODO: reimplement and write test
    @property
    def source_stylesheet_file_name(self):
        self.print_not_implemented()

    @property
    def source_stylesheet_file_proxy(self):
        return StylesheetFileProxy(self.source_stylesheet_file_name, session=self.session)

    # TODO: write test
    @property
    def user_input_module_file_name(self): 
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'user_input.py')
    
    # TODO: write test
    @property
    def user_input_module_proxy(self):
        return UserInputModuleProxy(self.user_input_module_importable_name, session=self.session)

    # TODO: write test
    @property
    def user_input_module_importable_name(self):
        if self.user_input_module_file_name is not None:
            return '{}.user_input'.format(self.package_importable_name)
    
    # TODO: write test
    # TODO: reimplement with helpers.safe_import()
    @property
    def user_input_wrapper(self):
        if self.has_user_input_module:
            if True:
                command = 'from {} import user_input'.format(self.user_input_module_importable_name)
                exec(command)
                return user_input

    ### PUBLIC METHODS ###

    def add_material_to_material_initializer(self):
        self.initializer_file_proxy.add_protected_import_statement(
            'output_material', self.material_underscored_name)
        
    def add_material_to_materials_initializer(self):
        parent_package = PackageProxy(self.parent_package_importable_name, session=self.session)
        parent_package.initializer_file_proxy.add_protected_import_statement(
            self.material_underscored_name, self.material_underscored_name)

    # TODO: audit
    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'uic':
            self.clear_user_input_wrapper(prompt=False)    
        elif result == 'uid':
            self.user_input_module_proxy.remove(prompt=True)
        elif result == 'uil':
            self.load_user_input_wrapper_demo_values(prompt=False)
        elif result == 'uip':
            self.populate_user_input_wrapper(prompt=False)
        elif result == 'uis':
            self.show_user_input_demo_values(prompt=True)
        elif result == 'uit':
            self.session.use_current_user_input_values_as_default = \
                not self.session.use_current_user_input_values_as_default
        elif result == 'mdd':
            self.material_definition_module_proxy.remove(prompt=True)
        elif result == 'mde':
            self.material_definition_module_proxy.edit()
        elif result == 'mdt':
            #self.write_stub_material_definition_to_disk()
            self.material_definition_module_proxy.write_stub_to_disk(self.is_data_only, prompt=True)
        elif result == 'mdx':
            self.run_python_on_material_definition()
        elif result == 'mdxi':
            self.run_abjad_on_material_definition()
        elif result == 'ibd':
            self.illustration_builder_module_proxy.remove(prompt=True)
        elif result == 'ibe':
            self.illustration_builder_module_proxy.edit()
        elif result == 'ibt':
            self.illustration_builder_module_proxy.write_stub_to_disk(prompt=True)
        elif result == 'ibx':
            self.run_python_on_illustration_builder()
        elif result == 'ibxi':
            self.run_abjad_on_illustration_builder()
        elif result == 'ssm':
            self.source_stylesheet_file_proxy.edit()
        elif result == 'sss':
            self.select_stylesheet_interactively()
        elif result == 'stl':
            self.manage_stylesheets()
        elif result == 'dc':
            self.write_output_material_to_disk()
        elif result == 'di':
            self.output_material_module_proxy.view()
        elif result == 'dd':
            self.output_material_module_proxy.remove(prompt=True)
        elif result == 'lyc':
            self.write_illustration_ly_to_disk(is_forced=True)
        elif result == 'lyd':
            self.illustration_ly_file_proxy.remove(prompt=True)
        elif result == 'lyi':
            self.illustration_ly_file_proxy.view()
        elif result == 'pdfc':
            self.write_illustration_ly_and_pdf_to_disk(is_forced=True)
            self.illustration_pdf_file_proxy.view()
        elif result == 'pdfd':
            self.illustration_pdf_file_proxy.remove(prompt=True)
        elif result == 'pdfi':
            self.illustration_pdf_file_proxy.view()
        elif result == 'del':
            self.remove()
            self.session.is_backtracking_locally = True
        elif result == 'init':
            self.initializer_file_proxy.view()
        elif result == 'ren':
            self.rename_material()
        elif result == 'reg':
            self.regenerate_everything(is_forced=True)
        # TODO: add to packge-level hidden menu
        elif result == 'tags':
            self.manage_tags()
        # TODO: add to directory-level hidden menu
        elif result == 'ls':
            self.list_directory()
        elif mathtools.is_integer_equivalent_expr(result):
            self.edit_user_input_at_number(int(result))
        else:
            raise ValueError

    def make_main_menu(self):
        if self.is_handmade:
            menu, hidden_section = self.make_main_menu_for_material_made_by_hand()
        else:
            menu, hidden_section = self.make_main_menu_for_material_made_with_material_package_maker()
        self.make_main_menu_section_for_illustration_ly(menu, hidden_section)
        self.make_main_menu_section_for_illustration_pdf(menu, hidden_section)
        self.make_main_menu_section_for_hidden_entries(menu)
        return menu
    
    def make_main_menu_for_material_made_by_hand(self):
        menu, hidden_section = self.make_new_menu(where=self.where(), is_hidden=True)
        self.make_main_menu_section_for_material_definition(menu, hidden_section)
        self.make_main_menu_section_for_output_material(menu, hidden_section)
        self.make_main_menu_section_for_illustration_builder(menu, hidden_section)
        self.make_main_menu_section_for_stylesheet_management(menu, hidden_section)
        return menu, hidden_section

    def make_main_menu_section_for_hidden_entries(self, main_menu):
        hidden_section = main_menu.make_new_section(is_hidden=True)
        hidden_section.append(('del', 'delete material'))
        hidden_section.append(('init', 'edit initializer'))
        hidden_section.append(('ls', 'list directory'))
        hidden_section.append(('reg', 'regenerate material'))
        hidden_section.append(('ren', 'rename material'))
        hidden_section.append(('stl', 'manage stylesheets'))
        hidden_section.append(('tags', 'manage tags'))

    def make_main_menu_section_for_material_definition(self, main_menu, hidden_section):
        section = main_menu.make_new_section()
        if self.has_material_definition_module:
            section.append(('mde', 'material definition - edit'))
            section.append(('mdx', 'material definition - execute'))
            hidden_section.append(('mdd', 'material definition - delete'))
            hidden_section.append(('mdt', 'material definition - stub'))
            hidden_section.append(('mdxi', 'material definition - execute & inspect'))
        elif self.material_package_maker_class_name is None:
            section.append(('mdt', 'material definition - stub'))

    def make_main_menu_section_for_output_material(self, main_menu, hidden_section):
        has_output_material_section = False
        if self.has_material_definition or self.has_complete_user_input_wrapper:
            section = main_menu.make_new_section()
            section.append(('dc', 'output data - create'))
            has_output_material_section = True
        if self.has_output_material_module:
            if not has_output_material_section:
                section = main_menu.make_new_section()
            section.append(('di', 'output data - inspect'))
            hidden_section.append(('dd', 'output data - delete'))

    def make_main_menu_section_for_illustration_ly(self, main_menu, hidden_section):
        if self.has_output_material:
            if self.has_illustration_builder or self.has_material_package_maker:
                hidden_section.append(('lyc', 'output ly - create'))
        if self.has_illustration_ly:
            hidden_section.append(('lyd', 'output ly - delete'))
            hidden_section.append(('lyi', 'output ly - inspect'))

    def make_main_menu_section_for_illustration_pdf(self, main_menu, hidden_section):
        has_illustration_pdf_section = False
        if self.has_output_material:
            if self.has_illustration_builder or self.has_material_package_maker:
                section = main_menu.make_new_section()
                has_illustration_pdf_section = True
                section.append(('pdfc', 'output pdf - create'))
        if self.has_illustration_pdf:
            if not has_illustration_pdf_section:
                section = main_menu.make_new_section()
            hidden_section.append(('pdfd', 'output pdf - delete'))
            section.append(('pdfi', 'output pdf - inspect'))

    def make_main_menu_section_for_illustration_builder(self, main_menu, hidden_section):
        section = main_menu.make_new_section()
        if self.has_output_material:
            if self.has_illustration_builder:
                section.append(('ibe', 'illustration builder - edit'))
                if self.has_output_material:
                    section.append(('ibx', 'illustration builder - execute'))
                hidden_section.append(('ibd', 'illustration builder - delete'))
                hidden_section.append(('ibt', 'illustration builder - stub'))
                hidden_section.append(('ibxi', 'illustration builder - execute & inspect'))
            elif self.should_have_illustration:
                section.append(('ibt', 'illustration builder - stub'))

    def make_main_menu_section_for_stylesheet_management(self, main_menu, hidden_section):
        if self.has_output_material:
            if self.has_illustration_builder or self.should_have_illustration:
                section = main_menu.make_new_section()
                section.append(('sss', 'score stylesheet - select'))
                # TODO: fix this
                if True:
                    hidden_section.append(('ssm', 'source stylesheet - edit'))

    def manage_stylesheets(self):
        stylesheet_wrangler = StylesheetWrangler(session=self.session)
        stylesheet_wrangler.run()

    def regenerate_everything(self, is_forced=False):
        self.print_not_implemented()

    def rename_material(self):
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
            # rename output data
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

    def remove(self):
        self.remove_material_from_materials_initializer()
        PackageProxy.remove(self)

    def remove_material_from_materials_initializer(self):
        import_statement = 'safe_import({!r}, {!r})\n'.format(
            self.material_underscored_name, self.material_underscored_name)
        parent_package = PackageProxy(self.parent_package_importable_name, session=self.session)
        if import_statement in parent_package.initializer_file_proxy.protected_import_statements:
            parent_package.initializer_file_proxy.protected_import_statements.remove(import_statement)

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

    # TODO: migrate to material definition module proxy
    def run_abjad_on_material_definition(self):
        os.system('abjad {}'.format(self.material_definition_module_file_name))
        self.display('')

    # TODO: migrate to illustration builder module proxy
    def run_abjad_on_illustration_builder(self):
        os.system('abjad {}'.format(self.illustration_builder_module_file_name))
        self.display('')

    # TODO: migrate to material definition module proxy
    def run_python_on_material_definition(self, prompt=True):
        os.system('python {}'.format(self.material_definition_module_file_name))
        line = 'material definition executed.'
        self.proceed(line, prompt=prompt)

    # TODO: migrate to illustration builder module proxy
    def run_python_on_illustration_builder(self, prompt=True):
        os.system('python {}'.format(self.illustration_builder_module_file_name))
        line = 'illustration builder executed.'
        self.proceed(line, prompt=prompt)

    # TODO: write test
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

    # TODO: write test
    def select_stylesheet_interactively(self, prompt=True):
        stylesheet_wrangler = StylesheetWrangler(session=self.session)
        self.push_backtrack()
        source_stylesheet_file_name = stylesheet_wrangler.select_stylesheet_file_name_interactively()
        self.pop_backtrack()
        if self.backtrack():
            return
        # TODO: replace with something nonlocal
        #self.link_local_stylesheet(source_stylesheet_file_name, prompt=prompt)

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
        output_material_module_proxy = self.output_material_module_proxy
        lines = self.output_material_module_body_lines
        output_material_module_proxy.body_lines[:] = lines
        output_material_module_proxy.write_to_disk()
        self.add_material_to_materials_initializer()
        self.add_material_to_material_initializer()
        line = 'output data written to disk.'
        self.proceed(line, prompt=prompt)
