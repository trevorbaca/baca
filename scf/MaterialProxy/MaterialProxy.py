from abjad.tools import iotools
from abjad.tools import markuptools
from abjad.tools import mathtools
from baca.scf.MaterialProxyWrangler import MaterialProxyWrangler
from baca.scf.PackageProxy import PackageProxy
from baca.scf.StylesheetProxy import StylesheetProxy
from baca.scf.StylesheetWrangler import StylesheetWrangler
import os


class MaterialProxy(PackageProxy):

    def __init__(self, package_importable_name=None, session=None):
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        self._generic_output_name = None

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.package_spaced_name

    @property
    def formatted_user_input_lines(self):
        lines = []
        if self.has_user_input_module:
            user_input_wrapper = self.user_input_wrapper 
            # TODO: implement on user input wrapper
            for parameter_name, parameter_value in user_input_wrapper.iteritems():
                line = '{}: {!r}'.format(parameter_name, parameter_value)
                lines.append(line)
        return lines

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
            return bool(self.import_illustration_from_illustration_builder())

    @property
    def has_illustration_builder(self):
        if self.illustration_builder_file_name is None:
            return False
        else:
            return os.path.exists(self.illustration_builder_file_name)

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

    # TODO: remove
    @property
    def has_local_stylesheet(self):
        if self.local_stylesheet_file_name is None:
            return False
        else:
            return os.path.exists(self.local_stylesheet_file_name)
    
    @property
    def has_material_definition(self):
        if not self.has_material_definition_module:
            return False
        else:
            return bool(self.import_material_definition_from_material_definition_module())

    @property
    def has_material_definition_module(self):
        if self.material_definition_file_name is None:
            return False
        else:
            return os.path.exists(self.material_definition_file_name)

    @property
    def has_output_material(self):
        if not self.has_output_material_module:
            return False
        else:
            return bool(self.import_output_material_from_output_material_module())

    @property
    def has_output_material_module(self):
        if self.output_material_module_file_name is None:
            return False
        else:
            return os.path.exists(self.output_material_module_file_name)

    @property
    def has_user_input_handler(self):
        return bool(self.user_input_handler_class_name)

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
            return self.import_user_input_from_user_input_module() is not None

    @property
    def illustration_builder_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'illustration_builder.py')

    @property
    def illustration_builder_module_importable_name(self):
        if self.illustration_builder_file_name is not None:
            return '{}.illustration_builder'.format(self.package_importable_name)

    @property
    def illustration_ly_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'illustration.ly')

    @property
    def illustration_pdf_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'illustration.pdf')

    # TODO: make work
    @property
    def is_changed(self):
        material_definition = self.import_material_definition_from_material_definition_module()
        output_material = self.import_output_material_from_output_material_module()
        return material_definition != output_material

    @property
    def is_data_only(self):
        return not self.should_have_illustration

    @property
    def is_handmade(self):
        return not(self.has_user_input_handler)

    # TODO: remove
    @property
    def local_stylesheet_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'stylesheet.ly')

    @property
    def material_definition_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'material_definition.py')

    @property
    def material_definition_module_importable_name(self):
        if self.material_definition_file_name is not None:
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

    @property
    def materials_package_importable_name(self):
        result = self.package_importable_name
        result = result.split('.')
        result = result[:-1]
        result = '.'.join(result)
        return result

    @property
    def output_material_module_file_name(self): 
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'output_material.py')

    @property
    def output_material_module_importable_name(self):
        if self.output_material_module_file_name is not None:
            return '{}.output_material'.format(self.package_importable_name)

    @property
    def output_material_module_import_statements(self):
        self.unimport_material_definition_module()
        try:
            command = 'from {} import output_material_module_import_statements'.format(
                self.material_definition_module_importable_name)
            exec(command)
            # keep list from persisting between multiple calls to this method
            output_material_module_import_statements = list(output_material_module_import_statements)
        except ImportError:
            output_material_module_import_statements = []
        return output_material_module_import_statements

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
        if self.has_local_stylesheet:
            local_stylesheet = file(self.local_stylesheet_file_name, 'r')
            first_line = local_stylesheet.readlines()[0].strip()
            assert first_line.endswith('.ly')
            result = first_line.split()[-1]
            return result

    # TODO: write test
    @property
    def stub_material_definition_file_name(self):
        return os.path.join(self.assets_directory, 'stub_material_definition.py')

    # TODO: write test
    @property
    def stub_illustration_builder_file_name(self):
        return os.path.join(self.assets_directory, 'stub_illustration_builder.py')

    @property
    def user_input_handler(self):
        user_input_handler_class_name = self.user_input_handler_class_name
        try:
            command = 'from baca.scf.materialproxies import {}'.format(user_input_handler_class_name)
            exec(command)
            command = 'result = {}(client_material_package_importable_name={!r}, session=self.session)'
            command = command.format(user_input_handler_class_name, self.package_importable_name)
            exec(command)
            return result
        except:
            pass

    @property
    def user_input_handler_class_name(self):
        return self.get_tag('user_input_handler_class_name')

    # TODO: write test
    @property
    def user_input_module_file_name(self): 
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'user_input.py')

    # TODO: write test
    @property
    def user_input_module_importable_name(self):
        if self.user_input_module_file_name is not None:
            return '{}.user_input'.format(self.package_importable_name)
    
    # TODO: write test
    @property
    def user_input_wrapper(self):
        if self.has_user_input_module:
            if True:
                command = 'from {} import user_input'.format(self.user_input_module_importable_name)
                exec(command)
                return user_input

    ### PUBLIC METHODS ###

    def add_material_to_material_initializer(self):
        import_statement = 'from output_material import {}\n'.format(self.material_underscored_name)
        self.add_import_statement_to_initializer(import_statement) 
        
    def add_material_to_materials_initializer(self):
        import_statement = 'from {} import {}\n'.format(
            self.material_underscored_name, self.material_underscored_name)
        parent_package = PackageProxy(self.parent_package_importable_name, session=self.session)
        parent_package.add_import_statement_to_initializer(import_statement)

    # TODO: remove
    def delete_local_stylesheet(self, prompt=True):
        if self.has_local_stylesheet:
            os.remove(self.local_stylesheet_file_name)
            line = 'stylesheet deleted.'
            self.proceed(line, prompt=prompt)
           
    def delete_material_definition_module(self, prompt=True):
        if self.has_material_definition_module:
            os.remove(self.material_definition_file_name)
            line = 'material definition deleted.'
            self.proceed(line, prompt=prompt)
        
    def delete_material_package(self):
        self.remove_material_from_materials_initializer()
        PackageProxy.delete_package(self)

    def delete_output_material_module(self, prompt=True):
        if self.has_output_material_module:
            self.remove_material_from_materials_initializer()
            os.remove(self.output_material_module_file_name)
            line = 'output data module deleted.'
            self.proceed(line, prompt=prompt)

    def delete_illustration_ly(self, prompt=True):
        if self.has_illustration_ly:
            os.remove(self.illustration_ly_file_name)
            line = 'output LilyPond file deleted.'
            self.proceed(line, prompt=prompt)

    def delete_illustration_pdf(self, prompt=True):
        if self.has_illustration_pdf:
            os.remove(self.illustration_pdf_file_name)
            line = 'output PDF deleted.'
            self.proceed(line, prompt=prompt)

    # TODO: make read only
    def edit_illustration_ly(self):
        os.system('vi {}'.format(self.illustration_ly_file_name))

    def edit_illustration_builder(self):
        os.system('vi + {}'.format(self.illustration_builder_file_name))

    # TODO: remove
    def edit_local_stylesheet(self):
        os.system('vi {}'.format(self.local_stylesheet_file_name))

    def edit_material_definition_module(self):
        os.system('vi + {}'.format(self.material_definition_file_name))

    # TODO: make read only
    def edit_output_material_module(self):
        os.system('vi + {}'.format(self.output_material_module_file_name))

    # TODO: reimplement and keep
    def edit_source_stylesheet(self):
        stylesheet_proxy = StylesheetProxy(self.source_stylesheet_file_name, session=self.session)
        stylesheet_proxy.vi_stylesheet()

    def import_material_definition_from_material_definition_module(self):
        self.unimport_material_definition_module()
        try:
            command = 'from {} import {}'.format(
                self.material_definition_module_importable_name, self.material_underscored_name)
            exec(command)
            command = 'result = {}'.format(self.material_underscored_name)
            exec(command)
            return result
        except ImportError as e:
            pass
    
    def import_output_material_from_output_material_module(self):
        self.unimport_module_hierarchy()
        try:
            command = 'from {} import {}'.format(
                self.output_material_module_importable_name, self.material_underscored_name)
            exec(command)
            command = 'result = {}'.format(self.material_underscored_name)
            exec(command)
            return result
        except ImportError as e:
            pass

    # TODO: change name to self.import_illustration_from_illustration_builder_module
    def import_illustration_from_illustration_builder(self):
        if not self.has_illustration_builder:
            return None
        self.unimport_illustration_builder_module()
        self.unimport_output_material_module()
        command = 'from {} import illustration'.format(self.illustration_builder_module_importable_name) 
        exec(command)
        if self.has_local_stylesheet:
            illustration.file_initial_user_includes.append(self.local_stylesheet_file_name)
        illustration.header_block.title = markuptools.Markup(self.material_spaced_name)
        return illustration
        
    # TODO: change name to self.import_user_input_wrapper_from_user_input_module()
    def import_user_input_from_user_input_module(self):
        self.unimport_user_input_module()
        try:
            command = 'from {} import user_input'.format(self.user_input_module_importable_name)
            exec(command)
            return user_input
        except ImportError as e:
            pass

    # TODO: audit
    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'uic':
            self.clear_user_input_wrapper(prompt=False)    
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
            self.delete_material_definition_module()
        elif result == 'mde':
            self.edit_material_definition_module()
        elif result == 'mdt':
            self.write_stub_material_definition_to_disk()
        elif result == 'mdx':
            self.run_python_on_material_definition()
        elif result == 'mdxi':
            self.run_abjad_on_material_definition()
        elif result == 'ibd':
            self.delete_illustration_builder()
        elif result == 'ibe':
            self.edit_illustration_builder()
        elif result == 'ibt':
            self.write_stub_illustration_builder_to_disk()
        elif result == 'ibx':
            self.run_python_on_illustration_builder()
        elif result == 'ibxi':
            self.run_abjad_on_illustration_builder()
        elif result == 'ssd':
            self.delete_local_stylesheet()
        elif result == 'sse':
            self.edit_local_stylesheet()
        elif result == 'ssm':
            self.edit_source_stylesheet()
        elif result == 'ssl':
            self.link_local_stylesheet()
        elif result == 'sss':
            self.select_stylesheet_interactively()
        elif result == 'stl':
            self.manage_stylesheets()
        elif result == 'dc':
            self.write_output_material_to_disk()
        elif result == 'di':
            self.edit_output_material_module()
        elif result == 'dd':
            self.delete_output_material_module()
        elif result == 'lyc':
            self.write_illustration_ly_to_disk(is_forced=True)
        elif result == 'lyd':
            self.delete_illustration_ly()
        elif result == 'lyi':
            self.edit_illustration_ly()
        elif result == 'pdfc':
            self.write_illustration_ly_and_pdf_to_disk(is_forced=True)
            self.open_illustration_pdf()
        elif result == 'pdfd':
            self.delete_illustration_pdf()
        elif result == 'pdfi':
            self.open_illustration_pdf()
        elif result == 'del':
            self.delete_material_package()
            self.session.is_backtracking_locally = True
        elif result == 'init':
            self.edit_initializer()
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

    # TODO: remove
    def link_local_stylesheet(self, source_stylesheet_file_name=None, prompt=True):
        if source_stylesheet_file_name is None:
            source_stylesheet_file_name = self.source_stylesheet_file_name
        source = file(source_stylesheet_file_name, 'r')
        target = file(self.local_stylesheet_file_name, 'w')
        target.write('% source: {}\n\n'.format(source_stylesheet_file_name))
        for line in source.readlines():
            target.write(line)
        source.close()
        target.close()
        line = 'stylesheet linked.'
        self.proceed(line, prompt=prompt)

    def make_main_menu(self):
        if self.is_handmade:
            menu, hidden_section = self.make_main_menu_for_material_made_by_hand()
        else:
            menu, hidden_section = self.make_main_menu_for_material_made_with_user_input_handler()
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
        elif self.user_input_handler_class_name is None:
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
            if self.has_illustration_builder or self.has_user_input_handler:
                hidden_section.append(('lyc', 'output ly - create'))
        if self.has_illustration_ly:
            hidden_section.append(('lyd', 'output ly - delete'))
            hidden_section.append(('lyi', 'output ly - inspect'))

    def make_main_menu_section_for_illustration_pdf(self, main_menu, hidden_section):
        has_illustration_pdf_section = False
        if self.has_output_material:
            if self.has_illustration_builder or self.has_user_input_handler:
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
                if self.has_local_stylesheet:
                    hidden_section.append(('ssd', 'score stylesheet - delete'))
                    section.append(('sse', 'score stylesheet - edit'))
                    hidden_section.append(('ssm', 'source stylesheet - edit'))
                    hidden_section.append(('ssl', 'score stylesheet - relink'))

    def make_illustration(self):
        return self.import_illustration_from_illustration_builder()

    def make_output_material(self):
        return self.import_material_definition_from_material_definition_module()

    def make_output_material_module_body_lines(self):
        lines = []
        output_material = self.make_output_material()
        lines.append('{} = {!r}'.format(self.material_underscored_name, output_material))
        return lines

    def manage_stylesheets(self):
        stylesheet_wrangler = StylesheetWrangler(session=self.session)
        stylesheet_wrangler.run()

    def open_illustration_pdf(self):
        command = 'open {}'.format(self.illustration_pdf_file_name)
        os.system(command)

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

    def remove_material_from_materials_initializer(self):
        import_statement = 'from {} import {}\n'.format(
            self.material_underscored_name, self.material_underscored_name)
        self.remove_import_statement_from_initializer(import_statement, self.parent_initializer_file_name)

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

    def run_abjad_on_material_definition(self):
        os.system('abjad {}'.format(self.material_definition_file_name))
        self.display('')

    def run_abjad_on_illustration_builder(self):
        os.system('abjad {}'.format(self.illustration_builder_file_name))
        self.display('')

    def run_python_on_material_definition(self, prompt=True):
        os.system('python {}'.format(self.material_definition_file_name))
        line = 'material definition executed.'
        self.proceed(line, prompt=prompt)

    def run_python_on_illustration_builder(self, prompt=True):
        os.system('python {}'.format(self.illustration_builder_file_name))
        line = 'illustration builder executed.'
        self.proceed(line, prompt=prompt)

    # TODO: write test
    def select_user_input_handler_interactively(self, prompt=True):
        material_proxy_wrangler = MaterialProxyWrangler(session=self.session)
        self.push_backtracking()
        user_input_handler = material_proxy_wrangler.select_material_proxy_class_name_interactively()
        self.pop_backtracking()
        if self.backtrack():
            return
        self.add_tag('user_input_handler', user_input_handler.class_name)
        line = 'user input handler selected.'
        self.proceed(line, prompt=prompt)

    # TODO: write test
    def select_stylesheet_interactively(self, prompt=True):
        stylesheet_wrangler = StylesheetWrangler(session=self.session)
        self.push_backtracking()
        source_stylesheet_file_name = stylesheet_wrangler.select_stylesheet_file_name_interactively()
        self.pop_backtracking()
        if self.backtrack():
            return
        self.link_local_stylesheet(source_stylesheet_file_name, prompt=prompt)

    def unimport_material_definition_module(self):
        self.remove_package_importable_name_from_sys_modules(self.material_definition_module_importable_name)

    def unimport_material_module(self):
        self.unimport_package()

    def unimport_materials_module(self):
        self.remove_package_importable_name_from_sys_modules(self.materials_package_importable_name)

    def unimport_output_material_module(self):
        self.remove_package_importable_name_from_sys_modules(self.output_material_module_importable_name)

    def unimport_module_hierarchy(self):
        self.unimport_materials_module()
        self.unimport_material_module()
        self.unimport_output_material_module()

    def unimport_illustration_builder_module(self):
        self.remove_package_importable_name_from_sys_modules(self.illustration_builder_module_importable_name)

    def unimport_score_package(self):
        self.remove_package_importable_name_from_sys_modules(self.score_package_short_name)

    def unimport_user_input_module(self):
        self.remove_package_importable_name_from_sys_modules(self.user_input_module_importable_name)

    def write_illustration_ly_and_pdf_to_disk(self, is_forced=False, prompt=True):
        lines = []
        illustration = self.make_illustration()
        iotools.write_expr_to_pdf(illustration, self.illustration_pdf_file_name, print_status=False)
        iotools.write_expr_to_ly(illustration, self.illustration_ly_file_name, print_status=False)
        lines.append('PDF and LilyPond file written to disk.')
        self.proceed(lines, prompt=prompt)
        
    def write_illustration_ly_to_disk(self, is_forced=False, prompt=True):
        lines = []
        illustration = self.import_illustration_from_illustration_builder()
        iotools.write_expr_to_ly(illustration, self.illustration_ly_file_name, print_status=False)
        lines.append('LilyPond file written to disk.')
        lines.append('')
        self.proceed(lines, prompt=prompt)

    def write_illustration_pdf_to_disk(self, is_forced=False, prompt=True):
        lines = []
        illustration = self.import_illustration_illustration_builder()
        iotools.write_expr_to_pdf(illustration, self.illustration_pdf_file_name, print_status=False)
        lines.append('PDF written to disk.')
        lines.append('')
        self.proceed(lines, prompt=prompt)

    def write_output_material_to_disk(self, prompt=True):
        self.remove_material_from_materials_initializer()
        output_material_module_body_lines = self.make_output_material_module_body_lines()
        output_material_module = file(self.output_material_module_file_name, 'w')
        output_material_module.write('\n'.join(self.output_material_module_import_statements))
        output_material_module.write('\n'.join(['\n', '\n']))
        output_material_module.write('\n'.join(output_material_module_body_lines))
        output_material_module.close()
        self.add_material_to_materials_initializer()
        self.add_material_to_material_initializer()
        line = 'output data written to disk.'
        self.proceed(line, prompt=prompt)

    def write_stub_data_material_definition_to_disk(self):
        material_definition = file(self.material_definition_file_name, 'w')
        material_definition.write('from abjad.tools import sequencetools\n')
        material_definition.write('output_material_module_import_statements = []\n')
        material_definition.write('\n')
        material_definition.write('\n')
        material_definition.write('{} = None'.format(self.material_underscored_name))
        
    def write_stub_material_definition_to_disk(self, prompt=True):
        if self.is_data_only:
            self.write_stub_data_material_definition_to_disk()
        else:
            self.write_stub_music_material_definition_to_disk()
        line = 'stub material definition written to disk.'
        self.proceed(line, prompt=prompt)

    def write_stub_music_material_definition_to_disk(self):
        material_definition = file(self.material_definition_file_name, 'w')
        material_definition.write('from abjad import *\n')
        material_definition.write("output_material_module_import_statements = ['from abjad import *']\n")
        material_definition.write('\n')
        material_definition.write('\n')
        material_definition.write('{} = None'.format(self.material_underscored_name))

    def write_stub_illustration_builder_to_disk(self, prompt=True):
        illustration_builder = file(self.illustration_builder_file_name, 'w')
        lines = []
        lines.append('from abjad import *')
        lines.append('from output_material import {}'.format(self.material_underscored_name))
        lines.append('')
        lines.append('')
        line = 'score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves({})'.format(
            self.material_underscored_name)
        lines.append(line)
        lines.append('illustration = lilypondfiletools.make_basic_lilypond_file(score)')
        illustration_builder.write('\n'.join(lines))
        illustration_builder.close()
        line = 'stub illustration builder written to disk.'
        self.proceed(line, prompt=prompt)
