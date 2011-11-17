from abjad.tools import iotools
from abjad.tools import markuptools
from baca.scf.PackageProxy import PackageProxy
import os
import subprocess
import sys


class MaterialProxy(PackageProxy):

    def __init__(self, package_importable_name=None, session=None):
        PackageProxy.__init__(self, package_importable_name, session=session)

    ### PUBLIC ATTRIBUTES ###

    @property
    def has_input_data(self):
        if not self.has_input_file:
            return False
        else:
            return bool(self.import_material_from_input_file())

    @property
    def has_input_file(self):
        if self.input_file_name is None:
            return False
        else:
            return os.path.exists(self.input_file_name)

    @property
    def has_material_underscored_name(self):
        return bool(self.material_underscored_name is not None)

    @property
    def has_output_data(self):
        if not self.has_output_file:
            return False
        else:
            return bool(self.import_material_from_output_file())

    @property
    def has_output_file(self):
        if self.output_file_name is None:
            return False
        else:
            return os.path.exists(self.output_file_name)

    @property
    def has_score_definition(self):
        if not self.has_visualizer:
            return False
        else:
            return bool(self.import_score_definition_from_visualizer())

    @property
    def has_stylesheet(self):
        if self.stylesheet_file_name is None:
            return False
        else:
            return os.path.exists(self.stylesheet_file_name)
    
    @property
    def has_visualization_ly(self):
        if self.visualization_ly_file_name is None:
            return False
        else:
            return os.path.exists(self.visualization_ly_file_name)

    @property
    def has_visualization_pdf(self):
        if self.visualization_pdf_file_name is None:
            return False
        else:
            return os.path.exists(self.visualization_pdf_file_name)

    @property
    def has_visualizer(self):
        if self.visualizer_file_name is None:
            return False
        else:
            return os.path.exists(self.visualizer_file_name)

    @property
    def input_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'input.py')

    @property
    def input_package_importable_name(self):
        if self.package_importable_name is not None:
            return '%s.input' % self.package_importable_name

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
            subtitle = '(%s)' % score_title
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
        title = material_spaced_name.capitalize()
        title = markuptools.Markup(title)
        return title

    @property
    def material_package_directory(self):
        if self.materials_directory_name:
            if self.material_package_short_name:
                return os.path.join(self.materials_directory_name, self.material_package_short_name)

    @property
    def material_package_short_name(self):
        if self.score is None:  
            return self.material_underscored_name
        # TODO: remove score namespacing of score materials
        else:
            return '%s_%s' % (self.score.package_short_name, self.material_underscored_name)

    @property
    def material_spaced_name(self):
        if self.has_material_underscored_name:
            return self.material_underscored_name.replace('_', ' ')

    @apply
    def material_underscored_name():
        def fget(self):
            #return self._material_underscored_name
            return self.package_short_name
        def fset(self, material_underscored_name):
            assert isinstance(material_underscored_name, (str, type(None)))
            if isinstance(material_underscored_name, str):
                assert iotools.is_underscore_delimited_lowercase_string(material_underscored_name)
            #self._material_underscored_name = material_underscored_name
            self.package_short_name = material_underscored_name
        return property(**locals())

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
    def output_file_name(self): 
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'output.py')

    @property
    def output_package_importable_name(self):
        if self.package_importable_name is not None:
            return '%s.output' % self.package_importable_name

    @property
    def score_package_short_name(self):
        if self.package_importable_name is not None:
            if self.package_importable_name.startswith('baca'):
                return self.package_importable_name.split('.')[0]

    @property
    def stylesheet_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'stylesheet.ly')

    @property
    def user_input_wrapper(self):
        if self.is_interactive:
            if self.input_package_importable_name is not None:
                exec('from %s import user_input' % self.input_package_importable_name)
                return user_input

    @property
    def visualizer_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'visualization.py')

    @property
    def visualization_ly_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'visualization.ly')

    @property
    def visualization_package_importable_name(self):
        if self.package_importable_name is not None:
            return '%s.visualization' % self.package_importable_name

    @property
    def visualization_pdf_file_name(self):
        if self.directory_name is not None:
            return os.path.join(self.directory_name, 'visualization.pdf')

    ### PUBLIC METHODS ###

    # TODO: MaterialProxy
    def make_material_package_directory(self):
        try:
            os.mkdir(self.material_package_directory)
        except OSError:
            pass

    # TODO: MaterialProxy ... and extend PackageProxy
    def make_tags_dictionary(self):
        tags = {}
        tags['creation_date'] = self.helpers.get_current_date()
        tags['maker'] = self.class_name
        return tags

    def add_material_to_materials_initializer(self):
        import_statement = 'from %s import %s\n' % (self.material_underscored_name, self.material_underscored_name)
        parent_package = PackageProxy(self.parent_package_importable_name)
        parent_package.add_line_to_initializer(import_statement)

    def create_ly_and_pdf_from_visualizer(self, is_forced=False):
        lilypond_file = self.import_score_definition_from_visualizer()
        if is_forced or not self.lilypond_file_format_is_equal_to_visualizer_ly(lilypond_file):
            iotools.write_expr_to_visualization_ly(lilypond_file, self.visualization_ly_file_name)
            iotools.write_expr_to_visualization_pdf(lilypond_file, self.visualization_pdf_file_name)
        else:
            print 'LilyPond file is the same. (LilyPond file and PDF preserved.)'
        print ''
        
    def create_ly_from_visualizer(self, is_forced=False):
        lilypond_file = self.import_score_definition_from_visualizer()
        if is_forced or not self.lilypond_file_format_is_equal_to_visualizer_ly(lilypond_file):
            iotools.write_expr_to_ly(lilypond_file, self.visualization_ly_file_name)
        else:
            print 'LilyPond file is the same. (LilyPond file preserved.)'
        print ''

    def create_pdf_from_visualizer(self, is_forced=False):
        lilypond_file = self.import_score_definition_from_visualizer()
        if is_forced or not self.lilypond_file_format_is_equal_to_visualizer_ly(lilypond_file):
            iotools.write_expr_to_visualzation_pdf(lilypond_file, self.visualization_pdf_file_name)
        else:
            print 'LilyPond file is the same. (PDF preserved.)'
        print ''

    def create_visualizer(self):
        file_pointer = file(self.visualizer_file_name, 'w')
        file_pointer.write('from abjad import *\n')
        file_pointer.write('from abjad.tools import layouttools\n')
        line = 'from output import %s\n' % self.material_underscored_name
        file_pointer.write(line)
        file_pointer.write('\n\n\n')
        file_pointer.close()
        self.edit_visualizer()

    def delete_material(self):
        self.remove_material_from_materials_initializer()
        PackageProxy.delete_package(self)

    def edit_input_file(self):
        os.system('vi + %s' % self.input_file_name)

    def edit_visualization_ly(self):
        os.system('vi %s' % self.visualization_ly_file_name)

    def edit_output_file(self):
        os.system('vi + %s' % self.output_file_name)

    def edit_stylesheet(self):
        os.system('vi %s' % self.stylesheet_file_name)

    def edit_visualizer(self):
        os.system('vi + %s' % self.visualizer_file_name)

    def get_materials_package_importable_name(self):
        if self.purview.is_score_local_purview:
            return self.purview.materials_package_importable_name
        elif self.purview.is_studio_global_purview:
            return self.purview.get_materials_package_importable_name_interactively()
        else:
            raise ValueError

    def get_package_short_name_of_new_material_interactively(self):
        response = raw_input('Material name: ')
        print ''
        response = response.lower()
        response = response.replace(' ', '_')
        if self.has_score_local_purview:
            package_short_name = '%s_%s' % (self.purview.package_short_name, response)
        else:
            package_short_name = response
        print 'Short package name will be %s.\n' % package_short_name
        return package_short_name

    def get_visualizer_status_of_new_material_package_interactively(self):
        response = raw_input('Include visualizer? ')
        print ''
        if response == 'y':
            return True
        else:
            return False

    def import_attribute_from_input_file(self, attribute_name):
        try:
            exec('from %s import %s' % (self.input_package_importable_name, attribute_name))
            exec('result = %s' % attribute_name)
            return result
        except ImportError:
            return None

    def import_material_from_input_file(self):
        self.unimport_input_module()
        try:
            exec('from %s import %s' % (self.input_package_importable_name, self.material_underscored_name))
            exec('result = %s' % self.material_underscored_name)
            return result
        except ImportError as e:
            raise Exception('eponymous data must be kept in all I/O modules at all times.')
    
    def import_material_from_output_file(self):
        self.unimport_output_module_hierarchy()
        try:
            exec('from %s import %s' % (self.output_package_importable_name, self.material_underscored_name))
            exec('result = %s' % self.material_underscored_name)
            return result
        except ImportError as e:
            raise Exception('eponymous data must be kept in all I/O modules at all times.')

    def import_score_definition_from_visualizer(self):
        if not self.has_visualizer:
            return None
        self.unimport_visualization_module()
        self.unimport_output_module()
        command = 'from %s import lilypond_file' % self.visualization_package_importable_name 
        exec(command)
        return lilypond_file
        
    def get_output_preamble_lines(self):
        self.unimport_input_module()
        command = 'from %s import output_preamble_lines' % self.input_package_importable_name
        try:
            exec(command)
            # keep list from persisting between multiple calls to this method
            output_preamble_lines = list(output_preamble_lines)
            output_preamble_lines.append('\n')
        except ImportError:
            output_preamble_lines = []
        return output_preamble_lines

    def lilypond_file_format_is_equal_to_visualizer_ly(self, lilypond_file):
        temp_ly_file = os.path.join(os.environ.get('HOME'), 'tmp.ly')
        iotools.write_expr_to_ly(lilypond_file, temp_ly_file, print_status=False)
        trimmed_temp_ly_file_lines = self.trim_ly_lines(temp_ly_file)
        os.remove(temp_ly_file)
        trimmed_visualizer_ly_lines = self.trim_ly_lines(self.visualization_ly_file_name)
        return trimmed_temp_ly_file_lines == trimmed_visualizer_ly_lines

    def manage_input(self, command_string):
        if command_string == 'i':
            self.edit_input_file()
        elif command_string == 'id':
            print repr(self.import_material_from_input_file())
            print ''
        elif command_string == 'ih':
            print '%s: edit input file' % 'i'.rjust(self.help_item_width)
            print '%s: display input data' % 'id'.rjust(self.help_item_width)
            print '%s: edit input file and run abjad on input file' % 'ij'.rjust(self.help_item_width)
            print '%s: write input data to output file.' % 'iw'.rjust(self.help_item_width)
            print ''
        elif command_string == 'ij':
            self.edit_input_file()
            self.run_abjad_on_input_file()
        elif command_string == 'iw':
            self.write_input_data_to_output_file(is_forced=True)
            print ''

    def manage_ly(self, command_string):
        if command_string == 'l':
            if self.has_visualization_ly:
                self.edit_visualization_ly()
            elif self.has_visualizer:
                if self.query('Create LilyPond file from visualizer? '):
                    self.create_ly_from_visualizer()    
                print ''
            elif self.has_output_data:
                print "Data exists but visualizer doesn't.\n"
                if self.query('Create visualizer? '):
                    self.create_visualizer()
                print ''
            elif self.has_input_file:
                if self.query('Write material to disk? '):
                    self.write_input_data_to_output_file(is_forced=True)
                print ''
            else:
                if self.query('Create input file? '):
                    self.edit_input_file()
                print ''
        elif command_string == 'lw':
            self.create_ly_from_visualizer(is_forced=True)
        elif command_string == 'lwo':
            self.create_ly_from_visualizer(is_forced=True)
            self.edit_visualzation_ly()
        elif command_string == 'lh':
            print '%s: open ly' % 'l'.rjust(self.help_item_width)
            print '%s: write ly' % 'lw'.rjust(self.help_item_width)
            print '%s: write ly and open' % 'lwo'.rjust(self.help_item_width)
            print ''

    def manage_material(self):
        while True:
            menu = self.Menu(where=self.where(), session=self.session)
            menu.menu_body = self.material_spaced_name
            menu_section = self.MenuSection()
            if self.is_interactive:
                menu_section.sentence_length_items.append(('k', 'reload user input'))
            menu_section.named_pairs.append(('i', 'input'))
            menu_section.named_pairs.append(('o', 'output'))
            if self.has_visualizer:
                menu_section.named_pairs.append(('v', 'visualizer'))
            if self.has_visualization_ly:
                menu_section.named_pairs.append(('l', 'ly'))
            if self.has_stylesheet:
                menu_section.named_pairs.append(('y', 'stylesheet'))
            if self.has_visualization_pdf:
                menu_section.named_pairs.append(('p', 'pdf'))
            menu_section.named_pairs.append(('n', 'initializer'))
            menu.menu_sections.append(menu_section)
            menu_section = self.MenuSection()
            menu_section.named_pairs.append(('d', 'delete'))
            menu_section.named_pairs.append(('r', 'rename'))
            menu_section.named_pairs.append(('s', 'summarize'))
            menu_section.named_pairs.append(('t', 'tags'))
            menu_section.named_pairs.append(('z', 'regenerate'))
            menu.menu_sections.append(menu_section)
            key, value = menu.run()
            if key == 'b':
                return key, None
            elif key == 'd':
                self.delete_material()
                break
            elif key == 'i':
                self.manage_input(key)
            elif key == 'k':
                self.reload_user_input()
            elif key == 'l':
                self.manage_ly(key)
            elif key == 'n':
                self.edit_initializer()
            elif key == 'o':
                self.manage_output(key)
            elif key == 'p':
                self.manage_pdf(key)
            elif key == 'r':
                self.rename_material()
            elif key == 's':
                self.summarize_material_package()
            elif key == 't':
                self.manage_tags(menu_header=menu.menu_title)
            elif key == 'v':
                self.manage_visualizer(key)
            elif key == 'y':
                self.edit_stylesheet()
            elif key == 'z':
                self.manage_regeneration(key)

    def manage_output(self, command_string):
        if command_string == 'o':
            self.edit_output_file()
        elif command_string == 'od':
            print repr(self.import_material_from_output_file())
            print ''
        elif command_string == 'oh':
            print '%s: open output file' % 'o'.rjust(self.help_item_width)
            print '%s: display output data' % 'od'.rjust(self.help_item_width)
            print ''

    def manage_pdf(self, command_string):
        if command_string == 'p':
            if self.has_visualization_pdf:
                self.open_visualization_pdf()
            elif self.has_visualizer:
                if self.query('Create PDF from visualizer? '):
                    self.create_pdf_from_visualizer()
                print ''
            elif self.has_output_data:
                print "Data exists but visualizer doesn't.\n"
                if self.query('Create visualizer? '):
                    self.create_visualizer()
                print ''
            elif self.has_input_file:
                if self.query('Write material to disk? '):
                    self.write_input_data_to_output_file(is_forced=True)
                print ''
            else:
                if self.query('Create input file? '):
                    self.edit_input_file()
                print '' 
        elif command_string == 'pw':
            self.create_pdf_from_visualizer(is_forced=True)
        elif command_string == 'pwo':
            self.create_pdf_from_visualizer(is_forced=True)
            self.open_visualization_pdf()
        elif command_string == 'ph':
            print '%s: open pdf' % 'p'.rjust(self.help_item_width)
            print '%s: write pdf ' % 'pw'.rjust(self.help_item_width)
            print '%s: write pdf and open' % 'pwo'.rjust(self.help_item_width)
            print ''

    def manage_regeneration(self, command_string):
        if command_string == 'z':
            self.regenerate_everything(is_forced=True)
        elif command_string == 'zh':
            print '%s: regenerate everything' % 'z'.rjust(self.help_item_width)
            print '%s: regenerate everything and open pdf' % 'zo'.rjust(self.help_item_width)
            print ''
        elif command_string == 'zo':
            self.regenerate_everything(is_forced=True)
            self.open_visualzation_pdf()

    def manage_visualizer(self, command_string):
        if self.has_visualizer:
            if command_string == 'v':
                self.edit_visualizer()
            elif command_string == 'vh':
                print '%s: edit visualizer' % 'v'.rjust(self.help_item_width)
                print '%s: edit visualizer and run abjad on visualizer' % 'vj'.rjust(self.help_item_width)
                print '%s: run abjad on visualizer' % 'vjj'.rjust(self.help_item_width)
                print ''
            elif command_string == 'vj':
                self.edit_visualizer()
                self.run_abjad_on_visualizer()
            elif command_string == 'vjj':
                self.run_abjad_on_visualizer()
        elif self.has_output_data:
            print "Data exists but visualizer doesn't.\n"
            if self.query('Create visualizer? '):
                self.create_visualizer()
        elif self.has_input_file:
            if self.query('Write material to disk? '):
                self.write_input_data_to_output_file(is_forced=True)
        else:
            if self.query('Create input file? '):
                self.edit_input_file()

    def open_visualization_pdf(self):
        command = 'open %s' % self.visualization_pdf_file_name
        os.system(command)

    def overwrite_output_file(self):
        output_file = file(self.output_file_name, 'w')
        output_line = '%s = None\n' % self.material_underscored_name
        output_file.write(output_line)
        output_file.close()

    def prepend_score_package_short_name(self, material_underscored_name):
        if not material_underscored_name.startswith(self.score_package_short_name + '_'):
            material_underscored_name = '%s_%s' % (self.score_package_short_name, material_underscored_name)
        return material_underscored_name

    def regenerate_everything(self, is_forced=False):
        is_changed = self.write_input_data_to_output_file(is_forced=is_forced)
        is_changed = self.create_ly_and_pdf_from_visualizer(is_forced=(is_changed or is_forced))
        return is_changed

    def reload_user_input(self):
        maker = self.import_attribute_from_input_file('maker')
        maker.materials_directory_name = self.directory_name
        user_input_wrapper = self.import_attribute_from_input_file('user_input')
        maker.edit_interactively(user_input_wrapper, score_title=self.title)

    def rename_material(self):
        print 'Current material name: %s' % self.material_underscored_name
        new_material_spaced_name = raw_input('New material name:     ')
        print ''
        new_material_underscored_name = new_material_spaced_name.replace(' ', '_')
        new_material_underscored_name = self.prepend_score_package_short_name(new_material_underscored_name)
        print 'Current material name: %s' % self.material_underscored_name
        print 'New material name:     %s' % new_material_underscored_name
        print ''
        if not self.confirm():
            return
        print ''
        if self.is_in_repository:
            # update parent initializer
            self.helpers.globally_replace_in_file(
                self.parent_initializer_file_name, self.material_underscored_name, new_material_underscored_name)
            # rename package directory
            new_directory_name = self.directory.replace(self.material_underscored_name, new_material_underscored_name)
            command = 'svn mv %s %s' % (self.directory_name, new_directory_name)
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
                    new_directory_name = old_directory_name.replace(self.material_underscored_name, new_material_underscored_name)
                    command = 'svn mv %s %s' % (old_directory_name, new_directory_name)
                    os.system(command)
            # rename output data
            new_output_data = os.path.join(new_package_directory, 'output.py')
            self.helpers.globally_replace_in_file(
                new_output_data, self.material_underscored_name, new_material_underscored_name)
            print ''
            # commit
            commit_message = 'Renamed %s to %s.' % (self.material_underscored_name, new_material_underscored_name)
            commit_message = commit_message.replace('_', ' ')
            command = 'svn commit -m "%s" %s' % (commit_message, self.parent_directory_name)
            os.system(command)
            print ''
        else:
            raise NotImplementedError('commit to repository and then rename.')

    def remove_line_from_initializer(self, initializer, line):
        file_pointer = file(initializer, 'r')
        initializer_lines = set(file_pointer.readlines())
        file_pointer.close()
        initializer_lines = list(initializer_lines)
        initializer_lines = [x for x in initializer_lines if not x == line]
        initializer_lines.sort()
        file_pointer = file(initializer, 'w')
        file_pointer.write(''.join(initializer_lines))
        file_pointer.close()

    def remove_material_from_materials_initializer(self):
        import_statement = 'from %s import %s\n' % (self.material_underscored_name, self.material_underscored_name)
        self.remove_line_from_initializer(self.parent_initializer_file_name, import_statement)

    def reveal_modules(self):
        exec('module_names = sys.modules.keys()')
        module_names = [x for x in module_names if x.startswith(self.score_package_short_name)]
        module_names.sort()
        return module_names

    def run_abjad_on_input_file(self):
        os.system('abjad %s' % self.input_file_name)
        print ''

    def run_abjad_on_visualizer(self):
        os.system('abjad %s' % self.visualizer_file_name)
        print ''

    def summarize_material_package(self):
        found = []
        missing = []
        artifact_name = 'input file'
        if self.has_input_file:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
#        artifact_name = 'input data'
#        if self.has_input_data:
#            found.append(artifact_name)
#        else:
#            missing.append(artifact_name)
#        artifact_name = 'ouput file'
#        if self.has_output_file:
#            found.append(artifact_name)
#        else:
#            missing.append(artifact_name)
#        artifact_name = 'output data'
#        if self.has_output_data:
#            found.append(artifact_name)
#        else:
#            missing.append(artifact_name)
#        artifact_name = 'visualizer'
#        if self.has_visualizer:
#            found.append(artifact_name)
#        else:
#            missing.append(artifact_name)
#        artifact_name = 'score definition'
#        if self.has_score_definition:
#            found.append(artifact_name)
#        else:
#            missing.append(artifact_name)
        artifact_name = 'ly'
        if self.has_visualization_ly:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        artifact_name = 'pdf'
        if self.has_visualization_pdf:
            found.append(artifact_name)
        else:
            missing.append(artifact_name)
        if found:
            print 'Found %s.' % ', '.join(found)
        if missing:
            print 'Missing %s.' % ', '.join(missing)
        print ''
        self.proceed()
        
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

    def unimport_input_module(self):
        self.remove_package_importable_name_from_sys_modules(self.input_package_importable_name)

    def unimport_material_module(self):
        self.remove_package_importable_name_from_sys_modules(self.package_importable_name)

    def unimport_materials_module(self):
        self.remove_package_importable_name_from_sys_modules(self.materials_package_importable_name)

    def unimport_output_module(self):
        self.remove_package_importable_name_from_sys_modules(self.output_package_importable_name)

    def unimport_output_module_hierarchy(self):
        self.unimport_materials_module()
        self.unimport_material_module()
        self.unimport_output_module()

    def unimport_score_package(self):
        self.remove_package_importable_name_from_sys_modules(self.score_package_short_name)

    def unimport_visualization_module(self):
        self.remove_package_importable_name_from_sys_modules(self.visualization_package_importable_name)

    def _write_input_data_to_output_file(self):
        self.remove_material_from_materials_initializer()
        self.overwrite_output_file()
        output_file = file(self.output_file_name, 'w')
        output_preamble_lines = self.get_output_preamble_lines()
        if output_preamble_lines:
            output_file.write('\n'.join(output_preamble_lines))
        input_data = self.import_material_from_input_file()
        output_line = '%s = %r' % (self.material_underscored_name, input_data)
        output_file.write(output_line)
        output_file.close()
        self.add_material_to_materials_initializer()
        print "Material in 'input.py' written to 'output.py'."

    def write_input_data_to_output_file(self, is_forced=False):
        is_changed = self.import_material_from_input_file() != self.import_material_from_output_file()
        if is_changed or is_forced:
            self._write_input_data_to_output_file()
        else:
            print 'Input data equals output data. (Output data preserved.)'
        return is_changed

    def write_output_file_to_disk(self, material):
        output_file = file(os.path.join(self.material_package_directory, 'output.py'), 'w')
        output_file_import_statements = self.output_file_import_statements[:]
        for line in output_file_import_statements:
            output_file.write(line + '\n')
        if output_file_import_statements:
            output_file.write('\n\n')
        material_underscored_name = os.path.basename(self.material_package_directory)
        output_file_lines = self.get_output_file_lines(material, material_underscored_name)
        for line in output_file_lines:
            output_file.write(line + '\n')
        output_file.close()

    def write_stylesheet_to_disk(self):
        stylesheet = os.path.join(self.material_package_directory, 'stylesheet.ly')
        shutil.copy(self.stylesheet, stylesheet)
        header_block = lilypondfiletools.HeaderBlock()
        header_block.title = self.lilypond_score_title
        header_block.subtitle = self.lilypond_score_subtitle
        header_block.tagline = markuptools.Markup('""')
        fp = file(stylesheet, 'a')
        fp.write('\n')
        fp.write(header_block.format)
        fp.close()
