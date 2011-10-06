from abjad.tools import iotools
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from baca.scf._MaterialPackageMaker import _MaterialPackageMaker
from baca.scf.CatalogProxy import CatalogProxy
from baca.scf.MenuSpecifier import MenuSpecifier
from baca.scf.SCFObject import SCFObject
from baca.scf.UserInputWrapper import UserInputWrapper
import copy
import os
import shutil


class InteractiveMaterialMaker(SCFObject, _MaterialPackageMaker):

    def __init__(self, directory=None, materials_directory=None, material_name=None, score=None):
        SCFObject.__init__(self)
        self.directory = directory
        self.materials_directory = materials_directory
        self.material_name = material_name
        self.score = score

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
            print 'Package name will be %s.\n' % material_package_name
            if not self.confirm():
                continue
            target = os.path.join(base_directory, material_package_name)
            if os.path.exists(target):
                print 'Directory %r already exists.' % target
                print ''
                response = raw_input('Press return to try again.')
                print ''
                self.clear_terminal()
            else:
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
        user_input_lines = user_input_wrapper.formatted_lines
        input_file = file(os.path.join(self.material_package_directory, 'input.py'), 'w')
        for line in user_input_import_statements:
            input_file.write(line + '\n')
        if user_input_import_statements:
            input_file.write('\n\n')
        for line in user_input_lines:
            input_file.write(line + '\n')
        input_file.write('\n')
        material_name = os.path.basename(self.material_package_directory)
        input_file.write('maker = %s()\n' % type(self).__name__)
        input_file.write('%s = maker.make(**user_input)\n' % material_name)
        input_file.close()

    def _write_output_file_to_disk(self, material):
        output_file = file(os.path.join(self.material_package_directory, 'output.py'), 'w')
        output_file_import_statements = self.output_file_import_statements[:]
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

    ### PUBLIC ATTRIBUTES ###

    @property
    def class_spaced_name(self):
        from abjad.tools import iotools
        class_spaced_name = iotools.uppercamelcase_to_underscore_delimited_lowercase(type(self).__name__)
        class_spaced_name = class_spaced_name.replace('_', ' ')
        return class_spaced_name

    @property
    def has_material_name(self):
        return bool(self.material_name is not None)

    @property
    def location_name(self):
        if self.score is not None:
            return self.score.score_title
        else:
            return 'Studio'

    @apply
    def material_name():
        def fget(self):
            return self._material_name
        def fset(self, material_name):
            assert isinstance(material_name, (str, type(None)))
            self._material_name = material_name
        return property(**locals())

    @property
    def material_spaced_name(self):
        from abjad.tools import iotools
        if self.has_material_name:
            return self.material_name.replace('_', ' ')
        else:
            return '(unnamed material)'

    @apply
    def score():
        def fget(self):
            return self._score
        def fset(self, score):
            from baca.scf.ScorePackageProxy import ScorePackageProxy
            assert isinstance(score, (ScorePackageProxy, type(None)))
            self._score = score
        return property(**locals())

    ### PUBLIC METHODS ###

    def clear_values(self, user_input_wrapper):
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        
    def edit_interactively(self, menu_header=None, user_input_wrapper=None):
        if user_input_wrapper is None:
            user_input_wrapper = self._initialize_user_input_wrapper()
        while True:
            #menu_specifier = MenuSpecifier(menu_header=menu_header)
            menu_specifier = MenuSpecifier()
            menu_body = '%s - %s - %s - edit interactively'
            menu_body %= (self.location_name, self.class_spaced_name, self.material_spaced_name)
            menu_specifier.menu_body = menu_body
            pairs = list(user_input_wrapper.iteritems())
            lines = []
            for pair in pairs:
                key, value = pair
                key = key.replace('_', ' ')
                if value is None:
                    line = '%s: ' % key
                else:
                    line = '%s: %r' % (key, value)
                lines.append(line)
            menu_specifier.items_to_number = lines
            if user_input_wrapper.is_complete:
                menu_specifier.sentence_length_items.append(('p', 'show pdf of given input'))
                menu_specifier.sentence_length_items.append(('m', 'write material to disk'))
            if self.has_material_name:
                menu_specifier.sentence_length_items.append(('r', 'rename material'))
            else:
                menu_specifier.sentence_length_items.append(('n', 'name material'))
            menu_specifier.sentence_length_items.append(('d', 'show demo input values'))
            menu_specifier.sentence_length_items.append(('o', 'overwrite with demo input values'))
            menu_specifier.sentence_length_items.append(('c', 'clear values'))
            menu_specifier.sentence_length_items.append(('ed', 'edit source'))
            menu_specifier.sentence_length_items.append(('l', 'set location'))
            key, value = menu_specifier.display_menu()
            if key == 'b':
                self.interactively_check_and_save_material(user_input_wrapper)
                return key, None
            elif key == 'c':
                self.clear_values(user_input_wrapper)
            elif key == 'd':
                self.show_demo_input_values()
            elif key == 'ed':
                self.edit_source_file()
            elif key == 'l':
                self.set_location()
            elif key == 'm':
                self.save_material(user_input_wrapper)
                return key, None
            elif key == 'n':
                self.name_material()
            elif key == 'o':
                self.overwrite_with_demo_input_values(user_input_wrapper)
            elif key == 'p':
                lilypond_file = self.make_lilypond_file_from_user_input_wrapper(user_input_wrapper)
                lilypond_file.file_initial_user_includes.append(self.stylesheet)
                lilypond_file.header_block.title = markuptools.Markup(self.generic_output_name.capitalize())
                lilypond_file.header_block.subtitle = markuptools.Markup('(unsaved)')
                iotools.show(lilypond_file)
            elif key == 'r':
                self.rename_material()
            else:
                try:
                    number = int(key)
                except:
                    continue
                index = number - 1
                key, value = user_input_wrapper.items[index]
                new_value = self.edit_item(key, value)
                user_input_wrapper[key] = new_value

    def edit_item(self, key, value):
        prompt = key.replace('_', ' ')
        default = repr(value)
        response = self.raw_input_with_default('%s> ' % prompt, default=default)
        exec('from abjad import *')
        new_value = eval(response)
        return new_value
    
    def interactively_check_and_save_material(self, user_input_wrapper):
        if user_input_wrapper.is_complete:
            if self.query('Save material? '):
                self.save_material(user_input_wrapper)

    def make_lilypond_file_from_user_input_wrapper(self, user_input_wrapper):
        material = self.make(*user_input_wrapper.values)
        lilypond_file = self.make_lilypond_file_from_output_material(material)
        return lilypond_file

    def name_material(self):
        self.material_name = raw_input('Material name> ')

    def overwrite_with_demo_input_values(self, user_input_wrapper):
        for key in self.user_input_template:
            user_input_wrapper[key] = self.user_input_template[key]    

    def rename_material(self):
        self.name_material()

    def save_material(self, user_input_wrapper):
        material = self.make(*user_input_wrapper.values)
        lilypond_file = self.make_lilypond_file_from_output_material(material)
        material_directory = self.write_material_to_disk(user_input_wrapper, material, lilypond_file)
        print ''
        print 'Material saved to %s.\n' % material_directory
        self.proceed()
        return True

    # TODO
    def set_location(self):
        menu_specifier = MenuSpecifier()        

    def show_demo_input_values(self, menu_header=None):
        menu_specifier = MenuSpecifier(menu_header=menu_header)
        menu_specifier.menu_body = 'demo values'
        items = []
        for i, (key, value) in enumerate(self.user_input_template.iteritems()):
            item = '%s: %r' % (key.replace('_', ' '), value)
            items.append(item)
        menu_specifier.items_to_number = items
        menu_specifier.display_menu(score_title=self.score_title)

    def write_material_to_disk(self, user_input_wrapper, material, lilypond_file):
        self._get_new_material_package_directory_from_user(base_directory=self.materials_directory)
        os.mkdir(self.material_package_directory)
        self._write_initializer_to_disk()
        self._write_input_file_to_disk(self.user_input_import_statements, user_input_wrapper)
        self._write_output_file_to_disk(material)
        self._write_stylesheet_to_disk()
        stylesheet = os.path.join(self.material_package_directory, 'stylesheet.ly')
        lilypond_file.file_initial_user_includes.append(stylesheet)
        ly_file = os.path.join(self.material_package_directory, 'visualization.ly')
        iotools.write_expr_to_ly(lilypond_file, ly_file, print_status=False, tagline=True)
        pdf = os.path.join(self.material_package_directory, 'visualization.pdf')
        iotools.write_expr_to_pdf(lilypond_file, pdf, print_status=False, tagline=True)
        self._add_line_to_materials_initializer()
        return self.material_package_directory
