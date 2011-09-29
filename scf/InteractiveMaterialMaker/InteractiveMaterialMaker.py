from abjad.tools import iotools
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from baca.scf._MaterialPackageMaker import _MaterialPackageMaker
from baca.scf.CatalogProxy import CatalogProxy
from baca.scf.MenuSpecifier import MenuSpecifier
from baca.scf.UserInputWrapper import UserInputWrapper
import copy
import os
import shutil


class InteractiveMaterialMaker(_MaterialPackageMaker):
    '''Interactive material-maker base class.
    '''

    def __init__(self, directory=None, score_title=None):
        self.directory = directory
        self.score_title = score_title

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PRIVATE METHODS ###

    def _add_line_to_initializer(self, initializer, line):
        file_pointer = file(initializer, 'r')
        initializer_lines = set(file_pointer.readlines())
        file_pointer.close()
        initializer_lines.add(line)
        initializer_lines = list(initializer_lines)
        initializer_lines = [x for x in initializer_lines if not x == '\n']
        initializer_lines.sort()
        file_pointer = file(initializer, 'w')
        file_pointer.write(''.join(initializer_lines))
        file_pointer.close()

    def _add_line_to_materials_initializer(self):
        material_name = os.path.basename(self.material_package_directory)
        import_statement = 'from %s import %s\n' % (material_name, material_name)
        initializer = self._get_initializer()
        self._add_line_to_initializer(initializer, import_statement)

    def _get_initializer(self):
        if 'scores' in self.material_package_directory:
            materials_directory = os.path.dirname(self.material_package_directory)
            initializer = os.path.join(materials_directory, '__init__.py')
        else:
            initializer = os.path.join(os.environ.get('BACA'), 'materials', '__init__.py')        
        return initializer

    def _get_lilypond_score_title(self):
        material_name = os.path.basename(self.material_package_directory)
        material_parts = material_name.split('_')[1:]
        material_name = ' '.join(material_parts)
        title = material_name.capitalize()
        title = markuptools.Markup(title)
        return title

    def _get_lilypond_score_subtitle(self):
        if 'scores' in self.material_package_directory:
            materials_directory = os.path.dirname(self.material_package_directory)
            mus_directory = os.path.dirname(materials_directory)
            score_package_directory = os.path.dirname(mus_directory)
            score_package_name = os.path.basename(score_package_directory)
            catalog_proxy = CatalogProxy()
            score_title = catalog_proxy.score_package_name_to_score_title(score_package_name)
            subtitle = '(%s)' % score_title
        else:
            subtitle = '(shared material)'
        subtitle = markuptools.Markup(subtitle)
        return subtitle

    def _get_new_material_package_directory_from_user(self, base_directory=None):
        from baca.scf.CatalogProxy import CatalogProxy
        from baca.scf.SharedMaterialsProxy import SharedMaterialsProxy
        if base_directory is None:
            while True:
                response = raw_input('Save to shared materials (m)? Or to existing score (s)? ')
                print ''
                if response == 'm':
                    score_package_name = None
                    base_directory = self.shared_materials_directory
                    break
                elif response == 's':
                    catalog_proxy = CatalogProxy()
                    score_package_name = catalog_proxy.get_score_package_name_from_user()
                    base_directory = os.path.join(
                        self.scores_directory, score_package_name, 'mus', 'materials')
                    break
        else:
            if 'scores' in base_directory:
                parts = base_directory.split(os.path.sep)
                for i, part in enumerate(parts):
                    if part == 'scores':
                        score_package_name = parts[i+1]
                        break
                else:
                    raise Exception('Can not determine score package name.')
            else:
                score_package_name = None
        while True:
            response = raw_input('Material name: ')
            print ''
            response = response.lower()
            response = response.replace(' ', '_')
            if score_package_name is not None:
                material_package_name = '%s_%s' % (score_package_name, response)
            else:
                material_package_name = response
            print 'Package name will be %s\n' % material_package_name
            response = raw_input('ok? ')
            print ''
            if not response == 'y':
                continue
            target = os.path.join(base_directory, material_package_name)
            if os.path.exists(target):
                print 'Directory %r already exists.' % target
                print ''
                response = raw_input('Press return to try again.')
                print ''
                os.system('clear')
            else:
                #return target
                self.material_package_directory = target
                return

    def _initialize_user_input_wrapper(self):
        user_input_wrapper = copy.deepcopy(self.user_input_template)
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        return user_input_wrapper
        
    def _write_initializer_to_disk(self):
        initializer = file(os.path.join(self.material_package_directory, '__init__.py'), 'w')
        initializer.write('from output import *\n')
        initializer.close()

    def _write_input_file_to_disk(self, user_input_import_statements, user_input_wrapper):
        user_input_lines = user_input_wrapper.formatted_lines()
        input_file = file(os.path.join(self.material_package_directory, 'input.py'), 'w')
        for line in user_input_import_statements:
            input_file.write(line + '\n')
        if user_input_import_statements:
            input_file.write('\n\n')
        for line in user_input_lines:
            input_file.write(line + '\n')
        input_file.write('\n')
        material_name = os.path.basename(self.material_package_directory)
        for line in self.get_primary_input_lines(user_input_wrapper, material_name):
            input_file.write(line + '\n')
        input_file.close()

    def _write_output_file_to_disk(self, material):
        output_file = file(os.path.join(self.material_package_directory, 'output.py'), 'w')
        output_file_import_statements = self.get_output_file_import_statements()
        for line in output_file_import_statements:
            output_file.write(line + '\n')
        if output_file_import_statements:
            output_file.write('\n\n')
        material_name = os.path.basename(self.material_package_directory)
        output_file_lines = self.get_output_file_lines(material, material_name)
        for line in output_file_lines:
            output_file.write(line + '\n')
        output_file.close()

    def _write_stylesheet_to_disk(self):
        stylesheet = os.path.join(self.material_package_directory, 'stylesheet.ly')
        shutil.copy(self.stylesheet, stylesheet)
        header_block = lilypondfiletools.HeaderBlock()
        header_block.title = self._get_lilypond_score_title()
        header_block.subtitle = self._get_lilypond_score_subtitle()
        header_block.tagline = markuptools.Markup('""')
        fp = file(stylesheet, 'a')
        fp.write('\n')
        fp.write(header_block.format)
        fp.close()

    ### PUBLIC METHODS ###

    def edit_interactively(self, user_input_wrapper=None):
        if user_input_wrapper is None:
            user_input_wrapper = self._initialize_user_input_wrapper()
        while True:
            menu_specifier = MenuSpecifier()
            menu_title = '%s - edit interactively' % type(self).__name__
            if self.score_title is not None:
                menu_title = '%s - %s' % (self.score_title, menu_title)
            menu_specifier.menu_title = menu_title
            pairs = list(user_input_wrapper.iteritems())
            pairs = ['%s: %s' % (pair[0].replace('_', ' '), pair[1]) for pair in pairs]
            menu_specifier.items_to_number = pairs
            if user_input_wrapper.is_complete:
                menu_specifier.sentence_length_items.append(('p', 'render pdf of given input'))
            menu_specifier.sentence_length_items.append(('d', 'show demo input values'))
            key, value = menu_specifier.display_menu()
            if key == 'b':
                return None
            elif key == 'd':
                self.show_demo_input_values()
            elif key == 'p':
                self.render_pdf_from_input(user_input_wrapper)
            elif key == 'q':
                raise SystemExit
            elif key == 'x':
                self.exec_statement()

    def read_user_input_from_disk(self):
        raise Exception('Call on derived concrete classes.')

    def show_demo_input_values(self):
        clear_terminal = True
        while True:
            menu_specifier = MenuSpecifier()
            menu_title = '%s - demo values' % type(self).__name__
            if self.score_title is not None:
                menu_title = '%s - %s' % (self.score_title, menu_title)
            menu_specifier.menu_title = menu_title
            items = []
            for i, (key, value) in enumerate(self.user_input_template.iteritems()):
                item = '%s: %r' % (key.replace('_', ' '), value)
                items.append(item)
            menu_specifier.items_to_number = items
            key, value = menu_specifier.display_menu(clear_terminal=clear_terminal)
            clear_terminal = False
            if key == 'b':
                return
            elif key == 'q':
                raise SystemExit
            elif key == 'w':
                clear_terminal = True
            elif key == 'x':
                self.exec_statement()

    def write_material_to_disk(self, 
        user_input_import_statements, user_input_wrapper, material, lilypond_file):
        self._get_new_material_package_directory_from_user(base_directory=self.materials_directory)
        os.mkdir(self.material_package_directory)
        self._write_initializer_to_disk()
        self._write_input_file_to_disk(user_input_import_statements, user_input_wrapper)
        self._write_output_file_to_disk(material)
        self._write_stylesheet_to_disk()
        stylesheet = os.path.join(self.material_package_directory, 'stylesheet.ly')
        lilypond_file.file_initial_user_includes.append(stylesheet)
        ly_file = os.path.join(self.material_package_directory, 'visualization.ly')
        iotools.write_expr_to_ly(lilypond_file, ly_file, print_status=False, tagline=True)
        pdf = os.path.join(self.material_package_directory, 'visualization.pdf')
        iotools.write_expr_to_pdf(lilypond_file, pdf, print_status=False, tagline=True)
        self._add_line_to_materials_initializer()
