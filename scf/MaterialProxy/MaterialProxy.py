from abjad.tools import iotools
from abjad.tools import markuptools
from baca.scf.MakerWrangler import MakerWrangler
from baca.scf.PackageProxy import PackageProxy
from baca.scf.StylesheetProxy import StylesheetProxy
from baca.scf.StylesheetWrangler import StylesheetWrangler
import shutil
import os
import subprocess
import sys


# TODO: add 'list package directory' user command & inherit from PackageProxy, somehow
# TODO: remove interactive and static material proxies
class MaterialProxy(PackageProxy):

    def __init__(self, package_importable_name=None, session=None):
        PackageProxy.__init__(self, package_importable_name, session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.package_spaced_name

    @property
    def editor(self):
        editor_class_name = self.editor_class_name
        try:
            command = 'from baca.scf.makers import {}'.format(editor_class_name)
            exec(command)
            command = 'result = {}()'.format(editor_class_name)
            exec(command)
            return result
        except:
            pass

    @property
    def editor_class_name(self):
        return self.get_tag('editor_class_name')

    @property
    def has_editor(self):
        return bool(self.editor_class_name)

    @property
    def has_illustration(self):
        return self.get_tag('has_illustration')

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
    def has_material_underscored_name(self):
        return bool(self.material_underscored_name is not None)

    @property
    def has_output_data(self):
        if not self.has_output_data_module:
            return False
        else:
            return bool(self.import_output_data_from_output_data_module())

    @property
    def has_output_data_module(self):
        if self.output_data_file_name is None:
            return False
        else:
            return os.path.exists(self.output_data_file_name)

    @property
    def has_output_ly(self):
        if self.output_ly_file_name is None:
            return False
        else:
            return os.path.exists(self.output_ly_file_name)

    @property
    def has_output_pdf(self):
        if self.output_pdf_file_name is None:
            return False
        else:
            return os.path.exists(self.output_pdf_file_name)

    @property
    def has_score_builder(self):
        if self.score_builder_file_name is None:
            return False
        else:
            return os.path.exists(self.score_builder_file_name)

    @property
    def has_score_definition(self):
        if not self.has_score_builder:
            return False
        else:
            return bool(self.import_score_definition_from_score_builder())

    @property
    def has_local_stylesheet(self):
        if self.local_stylesheet_file_name is None:
            return False
        else:
            return os.path.exists(self.local_stylesheet_file_name)
    
    @property
    def is_changed(self):
        material_definition = self.import_material_definition_from_material_definition_module()
        output_data = self.import_output_data_from_output_data_module()
        return material_definition != output_data

    @property
    def is_data_only(self):
        return not self.has_illustration

    @property
    def is_in_score(self):
        if self.purview is None:
            return False
        else:
            return not self.is_shared        

    @property
    def is_interactive(self):
        return bool(self.has_tag('maker'))

    @property
    def is_shared(self):
        if self.purview is None:
            return False
        else:
            return self.purview.is_studio_global_purview

    @property
    def is_static(self):
        return not self.is_interactive

    @property
    def lilypond_score_subtitle(self):
        import baca
        if 'scores' in self.material_package_directory:
            materials_directory = os.path.dirname(self.material_package_directory)
            mus_directory = os.path.dirname(materials_directory)
            score_package_directory = os.path.dirname(mus_directory)
            score_package_short_name = os.path.basename(score_package_directory)
            score_wrangler = baca.scf.ScoreWrangler()
            score_title = score_wrangler.score_package_short_name_to_score_title(score_package_short_name)
            subtitle = '({})'.format(score_title)
        else:
            subtitle = '(shared material)'
        subtitle = markuptools.Markup(subtitle)
        return subtitle

    @property
    def lilypond_score_title(self):
        material_underscored_name = os.path.basename(self.material_package_directory)
        if self.is_shared:
            material_parts = material_underscored_name.split('_')
        else:
            material_parts = material_underscored_name.split('_')[1:]
        material_spaced_name = ' '.join(material_parts)
        title = iotools.capitalize_string_start(material_spaced_name)
        title = markuptools.Markup(title)
        return title

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
        if self.has_material_underscored_name:
            return self.material_underscored_name.replace('_', ' ')

    @property
    def materials_directory_name(self):
        if self.score is None:
            return self.baca_materials_directory
        else:
            return self.score.materials_directory_name

    @property
    def materials_package_importable_name(self):
        if self.purview is not None:
            return self.purview.materials_package_importable_name

    @property
    def output_data_file_name(self): 
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'output.py')

    @property
    def output_data_module_importable_name(self):
        if self.output_data_file_name is not None:
            return '{}.output'.format(self.package_importable_name)

    @property
    def output_data_preamble_lines(self):
        self.unimport_material_definition_module()
        command = 'from {} import output_data_preamble_lines'.format(
            self.material_definition_module_importable_name)
        try:
            exec(command)
            # keep list from persisting between multiple calls to this method
            output_data_preamble_lines = list(output_data_preamble_lines)
            # TODO: think the following line should be removed
            #output_data_preamble_lines.append('\n')
        except ImportError:
            output_data_preamble_lines = []
        return output_data_preamble_lines

    @property
    def output_ly_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'output.ly')

    @property
    def output_pdf_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'output.pdf')

    @property
    def score_builder_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'score_builder.py')

    @property
    def score_builder_module_importable_name(self):
        if self.score_builder_file_name is not None:
            return '{}.score_builder'.format(self.package_importable_name)

    @property
    def score_package_short_name(self):
        if self.package_importable_name is not None:
            if self.package_importable_name.startswith('baca'):
                return self.package_importable_name.split('.')[0]

    # TODO: write test
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
    def stub_score_builder_file_name(self):
        return os.path.join(self.assets_directory, 'stub_score_builder.py')

    @property
    def user_input_wrapper(self):
        if self.is_interactive:
            if self.material_definition_module_importable_name is not None:
                command = 'from {} import user_input'.format(self.material_definition_module_importable_name)
                exec(command)
                return user_input

    @property
    def was_created_by_hand(self):
        return not(self.has_editor)

    ### READ / WRITE PUBLIC ATTRIBUTES ##

    @apply
    def material_underscored_name():
        def fget(self):
            return self.package_short_name
        def fset(self, material_underscored_name):
            assert isinstance(material_underscored_name, (str, type(None)))
            if isinstance(material_underscored_name, str):
                assert iotools.is_underscore_delimited_lowercase_string(material_underscored_name)
            self.package_short_name = material_underscored_name
        return property(**locals())

    ### PUBLIC METHODS ###

    def add_material_to_material_initializer(self):
        import_statement = 'from output import {}\n'.format(self.material_underscored_name)
        self.add_import_statement_to_initializer(import_statement) 
        
    def add_material_to_materials_initializer(self):
        import_statement = 'from {} import {}\n'.format(
            self.material_underscored_name, self.material_underscored_name)
        parent_package = PackageProxy(self.parent_package_importable_name, session=self.session)
        parent_package.add_import_statement_to_initializer(import_statement)

    # TODO: remove this overly complicated method
    def conditionally_edit_score_builder(self):
        if self.has_score_builder:
            self.edit_score_builder()
        elif self.has_output_data:
            line = "data exists but score builder doesn't.\n"
            self.conditionally_display_lines([line])
            if self.query('create score builder? '):
                self.write_stub_score_builder_to_disk()
        elif self.has_material_definition_module:
            if self.query('write material to disk? '):
                self.write_material_definition_to_output_data_module(is_forced=True)
        else:
            if self.query('create material definition? '):
                self.edit_material_definition_module()

    def create_output_ly_and_output_pdf_from_score_builder(self, is_forced=False, prompt_proceed=True):
        lines = []
        lilypond_file = self.import_score_definition_from_score_builder()
        if is_forced or not self.lilypond_file_format_is_equal_to_score_builder_ly(lilypond_file):
            iotools.write_expr_to_pdf(lilypond_file, self.output_pdf_file_name, print_status=False)
            iotools.write_expr_to_ly(lilypond_file, self.output_ly_file_name, print_status=False)
            lines.append('PDF and LilyPond file written to disk.')
        else:
            lines.append('LilyPond file is the same. (PDF and LilyPond file preserved.)')
        if prompt_proceed:
            self.proceed(lines=lines)
        
    def create_output_ly_from_score_builder(self, is_forced=False, prompt_proceed=True):
        lines = []
        lilypond_file = self.import_score_definition_from_score_builder()
        if is_forced or not self.lilypond_file_format_is_equal_to_score_builder_ly(lilypond_file):
            iotools.write_expr_to_ly(lilypond_file, self.output_ly_file_name, print_status=False)
            lines.append('LilyPond file written to disk.')
        else:
            lines.append('LilyPond file is the same. (LilyPond file preserved.)')
        lines.append('')
        if prompt_proceed:
            self.proceed(lines=lines)

    def create_output_pdf_from_score_builder(self, is_forced=False, prompt_proceed=True):
        lines = []
        lilypond_file = self.import_score_definition_from_score_builder()
        if is_forced or not self.lilypond_file_format_is_equal_to_score_builder_ly(lilypond_file):
            iotools.write_expr_to_pdf(lilypond_file, self.output_pdf_file_name, print_status=False)
            lines.append('PDF written to disk.')
        else:
            lines.append('LilyPond file is the same. (PDF preserved.)')
        lines.append('')
        if prompt_proceed:
            self.proceed(lines=lines)

    def delete_local_stylesheet(self, prompt_proceed=True):
        if self.has_local_stylesheet:
            os.remove(self.local_stylesheet_file_name)
            if prompt_proceed:
                line = 'stylesheet deleted.'
                self.proceed(lines=[line])
           
    def delete_material_definition_module(self, prompt_proceed=True):
        if self.has_material_definition_module:
            os.remove(self.material_definition_file_name)
            if prompt_proceed:
                line = 'material definition deleted.'
                self.proceed(lines=[line])
        
    def delete_material_package(self):
        self.remove_material_from_materials_initializer()
        PackageProxy.delete_package(self)

    def delete_output_data_module(self, prompt_proceed=True):
        if self.has_output_data_module:
            self.remove_material_from_materials_initializer()
            os.remove(self.output_data_file_name)
            if prompt_proceed:
                line = 'output data module deleted.'
                self.proceed(lines=[line])

    def delete_output_ly(self, prompt_proceed=True):
        if self.has_output_ly:
            os.remove(self.output_ly_file_name)
            if prompt_proceed:
                line = 'output LilyPond file deleted.'
                self.procced(lines=[line])

    def delete_output_pdf(self, prompt_proceed=True):
        if self.has_output_pdf:
            os.remove(self.output_pdf_file_name)
            if prompt_proceed:
                line = 'output PDF deleted.'
                self.proceed(lines=[line])

    # TODO: remove this overly complicated method
    def edit_ly(self):
        if self.has_output_ly:
            self.edit_output_ly()
        elif self.has_score_builder:
            if self.query('create LilyPond file from score builder? '):
                self.create_output_ly_from_score_builder()    
        elif self.has_output_data:
            line = "output data exists but score builder doesn't.\n"
            self.conditionally_display_lines([line])
            if self.query('create score builder? '):
                self.write_stub_score_builder_to_disk()
        elif self.has_material_definition_module:
            if self.query('write material to disk? '):
                self.write_material_definition_to_output_data_module(is_forced=True)
        else:
            if self.query('create material definition? '):
                self.edit_material_definition_module()

    def edit_material_definition_module(self):
        os.system('vi + {}'.format(self.material_definition_file_name))

    def edit_output_data_module(self):
        os.system('vi + {}'.format(self.output_data_file_name))

    def edit_output_ly(self):
        os.system('vi {}'.format(self.output_ly_file_name))

    def edit_score_builder(self):
        os.system('vi + {}'.format(self.score_builder_file_name))

    def edit_source_stylesheet(self):
        stylesheet_proxy = StylesheetProxy(self.source_stylesheet_file_name, session=self.session)
        stylesheet_proxy.vi_stylesheet()

    def edit_local_stylesheet(self):
        os.system('vi {}'.format(self.local_stylesheet_file_name))

    # TODO: reimplement with getter and backtracking
    def get_package_short_name_of_new_material_interactively(self):
        response = self.handle_raw_input('material name')
        response = response.lower()
        response = response.replace(' ', '_')
        if self.has_score_local_purview:
            package_short_name = '{}_{}'.format(self.purview.package_short_name, response)
        else:
            package_short_name = response
        line = 'short package name will be {}.\n'.format(package_short_name)
        self.conditionally_display_lines([line])
        return package_short_name

    # TODO: reimplement with getter and backtracking
    def get_score_builder_status_of_new_material_package_interactively(self):
        response = self.handle_raw_input('include score builder?')
        if response == 'y':
            return True
        else:
            return False

    def import_attribute_from_material_definition(self, attribute_name):
        try:
            command = 'from {} import {}'.format(self.material_definition_module_importable_name, attribute_name)
            exec(command)
            command = 'result = {}'.format(attribute_name)
            exec(command)
            return result
        except ImportError:
            return None

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
    
    def import_output_data_from_output_data_module(self):
        self.unimport_module_hierarchy()
        try:
            command = 'from {} import {}'.format(
                self.output_data_module_importable_name, self.material_underscored_name)
            exec(command)
            command = 'result = {}'.format(self.material_underscored_name)
            exec(command)
            return result
        except ImportError as e:
            pass

    def import_score_definition_from_score_builder(self):
        if not self.has_score_builder:
            return None
        self.unimport_score_builder_module()
        self.unimport_output_data_module()
        command = 'from {} import lilypond_file'.format(self.score_builder_module_importable_name) 
        exec(command)
        if self.has_local_stylesheet:
            lilypond_file.file_initial_user_includes.append(self.local_stylesheet_file_name)
        lilypond_file.header_block.title = markuptools.Markup(self.material_spaced_name)
        return lilypond_file
        
    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'k':
            self.reload_user_input()
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
        elif result == 'sbd':
            self.delete_score_builder()
        elif result == 'sbe':
            self.conditionally_edit_score_builder()
        elif result == 'sbt':
            self.write_stub_score_builder_to_disk()
        elif result == 'sbx':
            self.run_python_on_score_builder()
        elif result == 'sbxi':
            self.run_abjad_on_score_builder()
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
            self.write_material_definition_to_output_data_module(is_forced=True)
        elif result == 'di':
            self.edit_output_data_module()
        elif result == 'dd':
            self.delete_output_data_module()
        elif result == 'lyc':
            self.create_output_ly_from_score_builder(is_forced=True)
        elif result == 'lyd':
            self.delete_output_ly()
        elif result == 'lyi':
            self.edit_ly()
        elif result == 'pdfc':
            self.create_output_ly_and_output_pdf_from_score_builder(is_forced=True)
            self.open_output_pdf()
        elif result == 'pdfd':
            self.delete_output_pdf()
        elif result == 'pdfi':
            self.open_output_pdf()
        elif result == 'er':
            self.run_editor()
        # TODO: write tests
        elif result == 'del':
            self.delete_material_package()
            self.session.is_backtracking_locally = True
        elif result == 'editors':
            self.manage_editors()
        elif result == 'init':
            self.edit_initializer()
        elif result == 'ren':
            self.rename_material()
        elif result == 'reg':
            self.regenerate_everything(is_forced=True)
        elif result == 'sum':
            self.summarize_material_package()
        # TODO: add to packge-level hidden menu
        elif result == 'tags':
            self.manage_tags()
        # TODO: add to global hidden menu
        elif result == 'ls':
            self.list_directory()
        else:
            raise ValueError

    def lilypond_file_format_is_equal_to_score_builder_ly(self, lilypond_file):
        temp_ly_file = os.path.join(os.environ.get('HOME'), 'tmp.ly')
        iotools.write_expr_to_ly(lilypond_file, temp_ly_file, print_status=False)
        trimmed_temp_ly_file_lines = self.trim_ly_lines(temp_ly_file)
        os.remove(temp_ly_file)
        trimmed_score_builder_ly_lines = self.trim_ly_lines(self.output_ly_file_name)
        return trimmed_temp_ly_file_lines == trimmed_score_builder_ly_lines

    def link_local_stylesheet(self, source_stylesheet_file_name=None, prompt_proceed=True):
        if source_stylesheet_file_name is None:
            source_stylesheet_file_name = self.source_stylesheet_file_name
        source = file(source_stylesheet_file_name, 'r')
        target = file(self.local_stylesheet_file_name, 'w')
        target.write('% source: {}\n\n'.format(source_stylesheet_file_name))
        for line in source.readlines():
            target.write(line)
        source.close()
        target.close()
        if prompt_proceed:
            line = 'stylesheet linked.'
            self.proceed(lines=[line])

    def make_main_menu(self):
        if self.was_created_by_hand:
            menu, hidden_section = self.make_main_menu_for_material_made_by_hand()
        else:
            menu, hidden_section = self.make_main_menu_for_material_made_with_editor()
        #self.make_main_menu_section_for_output_data(menu, hidden_section)
        self.make_main_menu_section_for_output_ly(menu, hidden_section)
        self.make_main_menu_section_for_output_pdf(menu, hidden_section)
        self.make_main_menu_section_for_hidden_entries(menu)
        return menu
    
    def make_main_menu_for_material_made_with_editor(self):
        menu, hidden_section = self.make_new_menu(where=self.where(), is_hidden=True)
        section = menu.make_new_section()
        if self.has_editor:
            section.append(('er', 'editor - run'))
        return menu, hidden_section

    def make_main_menu_for_material_made_by_hand(self):
        menu, hidden_section = self.make_new_menu(where=self.where(), is_hidden=True)
        self.make_main_menu_section_for_material_definition(menu, hidden_section)
        self.make_main_menu_section_for_output_data(menu, hidden_section)
        self.make_main_menu_section_for_score_builder(menu, hidden_section)
        self.make_main_menu_section_for_stylesheet_management(menu, hidden_section)
        return menu, hidden_section

    def make_main_menu_section_for_hidden_entries(self, main_menu):
        hidden_section = main_menu.make_new_section(is_hidden=True)
        hidden_section.append(('del', 'delete material'))
        hidden_section.append(('editors', 'manage editors'))
        hidden_section.append(('init', 'edit initializer'))
        hidden_section.append(('ls', 'list directory'))
        hidden_section.append(('reg', 'regenerate material'))
        hidden_section.append(('ren', 'rename material'))
        hidden_section.append(('stl', 'manage stylesheets'))
        hidden_section.append(('sum', 'summarize material'))
        hidden_section.append(('tags', 'manage tags'))

    def make_main_menu_section_for_material_definition(self, main_menu, hidden_section):
        section = main_menu.make_new_section()
        if self.has_material_definition_module:
            section.append(('mde', 'material definition - edit'))
            section.append(('mdx', 'material definition - execute'))
            hidden_section.append(('mdd', 'material definition - delete'))
            hidden_section.append(('mdt', 'material definition - stub'))
            hidden_section.append(('mdxi', 'material definition - execute & inspect'))
        else:
            section.append(('mdt', 'material definition - stub'))

    def make_main_menu_section_for_output_data(self, main_menu, hidden_section):
        if self.has_output_data_module:
            section = main_menu.make_new_section()
            section.append(('dc', 'output data - recreate'))
            section.append(('di', 'output data - inspect'))
            hidden_section.append(('dd', 'output data - delete'))
        elif self.has_material_definition:
            section = main_menu.make_new_section()
            section.append(('dc', 'output data - create'))

    def make_main_menu_section_for_output_ly(self, main_menu, hidden_section):
        if self.has_output_ly:
            hidden_section.append(('lyc', 'output ly - recreate'))
            hidden_section.append(('lyd', 'output ly - delete'))
            hidden_section.append(('lyi', 'output ly - inspect'))
        elif self.has_score_builder:
            hidden_section.append(('lyc', 'output ly - create'))

    def make_main_menu_section_for_output_pdf(self, main_menu, hidden_section):
        if self.has_output_pdf:
            section = main_menu.make_new_section()
            section.append(('pdfc', 'output pdf - recreate'))
            hidden_section.append(('pdfd', 'output pdf - delete'))
            section.append(('pdfi', 'output pdf - inspect'))
        elif self.has_output_data and self.has_score_builder:
            section = main_menu.make_new_section()
            section.append(('pdfc', 'output pdf - create'))

    def make_main_menu_section_for_score_builder(self, main_menu, hidden_section):
        section = main_menu.make_new_section()
        if self.has_output_data:
            if self.has_score_builder:
                section.append(('sbe', 'score builder - edit'))
                if self.has_output_data:
                    section.append(('sbx', 'score builder - execute'))
                hidden_section.append(('sbd', 'score builder - delete'))
                hidden_section.append(('sbt', 'score builder - stub'))
                hidden_section.append(('sbxi', 'score builder - execute & inspect'))
            elif self.has_illustration:
                section.append(('sbt', 'score builder - stub'))

    def make_main_menu_section_for_stylesheet_management(self, main_menu, hidden_section):
        if self.has_output_data:
            if self.has_score_builder or self.has_illustration:
                section = main_menu.make_new_section()
                section.append(('sss', 'score stylesheet - select'))
                if self.has_local_stylesheet:
                    hidden_section.append(('ssd', 'score stylesheet - delete'))
                    section.append(('sse', 'score stylesheet - edit'))
                    hidden_section.append(('ssm', 'source stylesheet - edit'))
                    hidden_section.append(('ssl', 'score stylesheet - relink'))

    def manage_stylesheets(self):
        stylesheet_wrangler = StylesheetWrangler(session=self.session)
        stylesheet_wrangler.run()

    def open_output_pdf(self):
        command = 'open {}'.format(self.output_pdf_file_name)
        os.system(command)

    def overwrite_output_data(self):
        output_data_module = file(self.output_data_file_name, 'w')
        line = '{} = None\n'.format(self.material_underscored_name)
        output_data_module.write(line)
        output_data_module.close()

    def regenerate_everything(self, is_forced=False):
        is_changed = self.write_material_definition_to_output_data_module(is_forced=is_forced)
        is_changed = self.create_output_ly_and_output_pdf_from_score_builder(is_forced=(is_changed or is_forced))
        return is_changed

    def reload_user_input(self):
        maker = self.import_attribute_from_material_definition('maker')
        maker.materials_directory_name = self.directory_name
        user_input_wrapper = self.import_attribute_from_material_definition('user_input')
        maker.run(user_input_wrapper, score_title=self.title)

    def rename_material(self):
        line = 'current material name: {}'.format(self.material_underscored_name)
        self.conditionally_display_lines([line])
        new_material_spaced_name = self.handle_raw_input('new material name:     ')
        new_material_underscored_name = new_material_spaced_name.replace(' ', '_')
        lines = []
        lines.append('current material name: {}'.format(self.material_underscored_name))
        lines.append('new material name:     {}'.format(new_material_underscored_name))
        lines.append('')
        self.conditionally_display_lines(lines)
        if not self.confirm():
            return
        if self.is_in_repository:
            # update parent initializer
            self.helpers.globally_replace_in_file(
                self.parent_initializer_file_name, self.material_underscored_name, new_material_underscored_name)
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
            new_output_data = os.path.join(new_package_directory, 'output.py')
            self.helpers.globally_replace_in_file(
                new_output_data, self.material_underscored_name, new_material_underscored_name)
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

    def run_abjad_on_material_definition(self):
        os.system('abjad {}'.format(self.material_definition_file_name))
        self.conditionally_display_lines([''])

    def run_abjad_on_score_builder(self):
        os.system('abjad {}'.format(self.score_builder_file_name))
        self.conditionally_display_lines([''])

    def run_editor(self):
        if self.has_editor:
            self.editor.run()

    def run_python_on_material_definition(self, prompt_proceed=True):
        os.system('python {}'.format(self.material_definition_file_name))
        if prompt_proceed:
            line = 'material definition executed.'
            self.proceed(lines=[line])

    def run_python_on_score_builder(self, prompt_proceed=True):
        os.system('python {}'.format(self.score_builder_file_name))
        if prompt_proceed:
            line = 'score builder executed.'
            self.proceed(lines=[line])

    # TODO: write test
    def select_editor_interactively(self, prompt_proceed=True):
        maker_wrangler = MakerWrangler(session=self.session)
        self.preserve_backtracking = True
        editor = maker_wrangler.select_maker_interactively()
        self.preserve_backtracking = False
        if self.backtrack():
            return
        self.add_tag('editor', editor.class_name)
        if prompt_proceed:
            line = 'editor selected.'
            self.proceed(lines=[line])

    # TODO: write test
    def select_stylesheet_interactively(self, prompt_proceed=True):
        stylesheet_wrangler = StylesheetWrangler(session=self.session)
        self.preserve_backtracking = True
        source_stylesheet_file_name = stylesheet_wrangler.select_stylesheet_file_name_interactively()
        self.preserve_backtracking = False
        if self.backtrack():
            return
        self.link_local_stylesheet(source_stylesheet_file_name, prompt_proceed=prompt_proceed)

    def summarize_material_package(self):
        lines = []
        found = []
        missing = []
        artifact_name = 'material definition'
        if self.has_material_definition_module:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        artifact_name = 'LilyPond file'
        if self.has_output_ly:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        artifact_name = 'PDF'
        if self.has_output_pdf:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        if found:
            lines.append('found {}.'.format(', '.join(found)))
        if missing:
            lines.append('missing {}.'.format(', '.join(missing)))
        lines.append('')
        self.proceed(lines=lines)
        
    def trim_ly_lines(self, ly_file_name):
        '''Remove "Abjad revision 4776" and "2011-09-13 18:33" lines.
        '''
        trimmed_ly_lines = []
        file_pointer = file(ly_file_name, 'r')
        found_version_command = False
        for line in file_pointer.readlines():
            if found_version_command:
                trimmed_ly_lines.append(line)
            if line.startswith(r'\version'):
                found_version_command = True
        trimmed_ly_content = ''.join(trimmed_ly_lines)
        return trimmed_ly_content

    def unimport_material_definition_module(self):
        self.remove_package_importable_name_from_sys_modules(self.material_definition_module_importable_name)

    def unimport_material_module(self):
        self.unimport_package()

    def unimport_materials_module(self):
        self.remove_package_importable_name_from_sys_modules(self.materials_package_importable_name)

    def unimport_output_data_module(self):
        self.remove_package_importable_name_from_sys_modules(self.output_data_module_importable_name)

    def unimport_module_hierarchy(self):
        self.unimport_materials_module()
        self.unimport_material_module()
        self.unimport_output_data_module()

    def unimport_score_builder_module(self):
        self.remove_package_importable_name_from_sys_modules(self.score_builder_module_importable_name)

    def unimport_score_package(self):
        self.remove_package_importable_name_from_sys_modules(self.score_package_short_name)

    def write_material_definition_to_output_data_module(self, is_forced=False, prompt_proceed=True):
        if not self.is_changed and not is_forced:
            line = 'material definition equals output data. (Output data preserved.)'
            self.conditionally_display_lines([line, ''])
            return self.is_changed
        if not self.has_material_definition:
            if prompt_proceed:
                line = 'material not yet defined.'
                self.proceed(lines=[line])
            return self.is_changed
        self.remove_material_from_materials_initializer()
        self.overwrite_output_data()
        output_data_module = file(self.output_data_file_name, 'w')
        output_data_preamble_lines = self.output_data_preamble_lines
        if output_data_preamble_lines:
            for line in output_data_preamble_lines:
                output_data_module.write(line + '\n')
            output_data_module.write('\n')
            output_data_module.write('\n')
        material_definition = self.import_material_definition_from_material_definition_module()
        line = '{} = {!r}'.format(self.material_underscored_name, material_definition)
        output_data_module.write(line)
        output_data_module.close()
        self.add_material_to_materials_initializer()
        self.add_material_to_material_initializer()
        if prompt_proceed:
            line = 'data written to disk.'
            self.proceed(lines=[line])
        return self.is_changed

    def write_stub_data_material_definition_to_disk(self):
        material_definition = file(self.material_definition_file_name, 'w')
        material_definition.write('from abjad.tools import sequencetools\n')
        material_definition.write('output_data_preamble_lines = []\n')
        material_definition.write('\n')
        material_definition.write('\n')
        material_definition.write('{} = None'.format(self.material_underscored_name))
        
    def write_stub_material_definition_to_disk(self, prompt_proceed=True):
        if self.is_data_only:
            self.write_stub_data_material_definition_to_disk()
        else:
            self.write_stub_music_material_definition_to_disk()
        if prompt_proceed:
            line = 'stub material definition written to disk.'
            self.proceed(lines=[line])

    def write_stub_music_material_definition_to_disk(self):
        material_definition = file(self.material_definition_file_name, 'w')
        material_definition.write('from abjad import *\n')
        material_definition.write("output_data_preamble_lines = ['from abjad import *']\n")
        material_definition.write('\n')
        material_definition.write('\n')
        material_definition.write('{} = None'.format(self.material_underscored_name))

    def write_stub_score_builder_to_disk(self, prompt_proceed=True):
        score_builder = file(self.score_builder_file_name, 'w')
        lines = []
        lines.append('from abjad import *')
        lines.append('from output import {}'.format(self.material_underscored_name))
        lines.append('')
        lines.append('')
        line = 'score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves({})'.format(
            self.material_underscored_name)
        lines.append(line)
        lines.append('lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)')
        score_builder.write('\n'.join(lines))
        score_builder.close()
        line = 'stub score builder written to disk.'
        if prompt_proceed:
            self.proceed(lines=[line])
