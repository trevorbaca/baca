from abjad.tools import iotools
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from baca.scf._SCFObject import _SCFObject
from baca.scf.MaterialWrangler import MaterialWrangler
from baca.scf.menuing import Menu
from baca.scf.menuing import MenuSection
from baca.scf.ScoreWrangler import ScoreWrangler
from baca.scf.UserInputWrapper import UserInputWrapper
import copy
import os
import shutil


class _Maker(_SCFObject):

    def __init__(self, underscore_material_name=None, score=None):
        _SCFObject.__init__(self)
        self.underscore_material_name = underscore_material_name
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
        if self.is_shared:
            material_parts = material_name.split('_')
        else:
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
            score_package_short_name = os.path.basename(score_package_directory)
            score_wrangler = ScoreWrangler()
            score_title = score_wrangler.score_package_short_name_to_score_title(score_package_short_name)
            subtitle = '(%s)' % score_title
        else:
            subtitle = '(shared material)'
        subtitle = markuptools.Markup(subtitle)
        return subtitle

    def set_material_package_directory(self):
        while True:
            if self.underscored_material_name is None:
                self.name_material()
                print ''
            print 'Package short name will be %s.\n' % self.material_package_short_name
            if self.confirm():
                break

    def _initialize_user_input_wrapper(self):
        user_input_wrapper = copy.deepcopy(self.user_input_template)
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        return user_input_wrapper
        
    def _write_initializer_to_disk(self):
        initializer = file(os.path.join(self.material_package_directory, '__init__.py'), 'w')
        initializer.write('from output import *\n')
        initializer.write('import datetime\n')
        initializer.write('\n\n')
        tags_dictionary = self.make_tags_dictionary()
        initializer.write('tags = %r\n' % tags_dictionary)
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
    def directory(self):
        raise Exception('needs to be derived from material name')

    @property
    def generic_output_name(self):
        return self._generic_output_name

    @property
    def has_changes(self):
        if not self.score == self._original_score:
            return True
        elif not self.underscored_material_name == self._original_underscored_material_name:
            return True
        elif not self.user_input_wrapper == self._original_user_input_wrapper:
            return True
        else:
            return False

    @property
    def has_location(self):
        return bool(self.score is not None)

    @property
    def has_material_name(self):
        return bool(self.underscored_material_name is not None)

    @property
    def is_shared(self):
        return bool(self.score is None)

    @property
    def location_name(self):
        if self.score is not None:
            return self.score.score_title
        else:
            return 'Studio'

    @property
    def material_menu_name(self):
        if self.has_material_name:
            return self.underscored_material_name
        else:
            return '(unnamed material)'

    @property
    def material_package_directory(self):
        if self.materials_directory_name:
            if self.material_package_short_name:
                return os.path.join(self.materials_directory_name, self.material_package_short_name)

    @property
    def material_package_short_name(self):
        if self.score is None:  
            return self.underscored_material_name
        else:
            return '%s_%s' % (self.score.package_short_name, self.underscored_material_name)

    @property
    def materials_directory_name(self):
        if self.score is None:
            return self.baca_materials_directory
        else:
            return self.score.materials_directory_name

    @apply
    def score():
        def fget(self):
            return self._score
        def fset(self, score):
            from baca.scf.ScoreProxy import ScoreProxy
            assert isinstance(score, (ScoreProxy, type(None)))
            self._score = score
        return property(**locals())

    @property
    def score_package_short_name(self):
        if self.score is not None:
            return self.score.package_short_name

    @apply
    def underscored_material_name():
        def fget(self):
            return self._underscored_material_name
        def fset(self, underscored_material_name):
            assert isinstance(underscored_material_name, (str, type(None)))
            self._underscored_material_name = underscored_material_name
        return property(**locals())

    ### PUBLIC METHODS ###

    def append_status_indicator(self, menu_body):
        if self.has_changes:
            menu_body = '%s (*)' % menu_body
        return menu_body

    def clear_values(self, user_input_wrapper):
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        
    def edit_interactively(self, menu_header=None, user_input_wrapper=None):
        if user_input_wrapper is None:
            user_input_wrapper = self._initialize_user_input_wrapper()
        self.user_input_wrapper = user_input_wrapper
        self._original_score = self.score
        self._original_underscored_material_name = self.underscored_material_name
        self._original_user_input_wrapper = copy.deepcopy(user_input_wrapper)
        while True:
            menu_specifier = Menu(client=self)
            menu_body = '%s - %s - %s - edit interactively'
            menu_body %= (self.location_name, self.spaced_class_name, self.material_menu_name)
            menu_body = self.append_status_indicator(menu_body)
            menu_specifier.menu_body = menu_body
            menu_specifier.items_to_number = self.user_input_wrapper.editable_lines
            if self.user_input_wrapper.is_complete:
                menu_specifier.sentence_length_items.append(('p', 'show pdf of given input'))
                menu_specifier.sentence_length_items.append(('m', 'write material to disk'))
            if self.has_material_name:
                menu_specifier.sentence_length_items.append(('n', 'rename material'))
            else:
                menu_specifier.sentence_length_items.append(('n', 'name material'))
            menu_specifier.sentence_length_items.append(('nc', 'clear name'))
            menu_specifier.sentence_length_items.append(('d', 'show demo input values'))
            menu_specifier.sentence_length_items.append(('o', 'overwrite with demo input values'))
            menu_specifier.sentence_length_items.append(('i', 'import values'))
            menu_specifier.sentence_length_items.append(('c', 'clear values'))
            #menu_specifier.sentence_length_items.append(('ed', 'edit source'))
            if self.has_location:
                menu_specifier.sentence_length_items.append(('l', 'change location'))
            else:
                menu_specifier.sentence_length_items.append(('l', 'set location'))
            key, value = menu_specifier.display_menu()
            if key == 'b':
                self.interactively_check_and_save_material(self.user_input_wrapper)
                return key, None
            elif key == 'c':
                self.clear_values(self.user_input_wrapper)
            elif key == 'd':
                self.show_demo_input_values()
            elif key == 'ed':
                self.edit_source_file()
            elif key == 'i':
                self.import_values()
            elif key == 'l':
                menu_header = ' - '.join(menu_specifier.menu_title_parts[:-1])
                self.set_location(menu_header=menu_header)
            elif key == 'm':
                self.save_material(self.user_input_wrapper)
                return key, None
            elif key == 'n':
                self.name_material()
            elif key == 'nc':
                self.unname_material()
            elif key == 'o':
                self.overwrite_with_demo_input_values(self.user_input_wrapper)
            elif key == 'p':
                lilypond_file = self.make_lilypond_file_from_user_input_wrapper(self.user_input_wrapper)
                lilypond_file.file_initial_user_includes.append(self.stylesheet)
                lilypond_file.header_block.title = markuptools.Markup(self.generic_output_name.capitalize())
                lilypond_file.header_block.subtitle = markuptools.Markup('(unsaved)')
                iotools.show(lilypond_file)
            else:
                try:
                    number = int(key)
                except:
                    continue
                index = number - 1
                key, value = self.user_input_wrapper.list_items[index]
                new_value = self.edit_item(key, value)
                self.user_input_wrapper[key] = new_value

    def edit_item(self, key, value):
        prompt = key.replace('_', ' ')
        default = repr(value)
        response = self.raw_input_with_default('%s> ' % prompt, default=default)
        exec('from abjad import *')
        new_value = eval(response)
        return new_value

    def import_values(self):
        from baca.scf.ScoreWrangler import ScoreWrangler
        score_wrangler = ScoreWrangler()
        menu_header = 'import %s' % self.spaced_class_name
        material_package_proxy = score_wrangler.select_interactive_material_package_proxy(
            menu_header=menu_header, klasses=(type(self),))
        self.user_input_wrapper = copy.deepcopy(material_package_proxy.user_input_wrapper)
    
    def interactively_check_and_save_material(self, user_input_wrapper):
        if user_input_wrapper.is_complete:
            if self.query('Save material? '):
                self.save_material(user_input_wrapper)

    def iterate_materials_based_on_maker(self):
        from baca.scf.ScoreWrangler import ScoreWrangler
        score_wrangler = ScoreWrangler()
        for material_proxy in score_wrangler.iterate_material_package_proxies(class_names=(self.class_name,)):
            yield material_proxy

    def make_lilypond_file_from_user_input_wrapper(self, user_input_wrapper):
        material = self.make(*user_input_wrapper.values)
        lilypond_file = self.make_lilypond_file_from_output_material(material)
        return lilypond_file

    def make_material_package_directory(self):
        print self.material_package_directory, 'foo'
        try:
            os.mkdir(self.material_package_directory)
        except OSError:
            pass

    def make_tags_dictionary(self):
        tags = {}
        tags['creation_date'] = self.get_date()
        tags['maker'] = self.class_name
        return tags

    def manage_maker(self, menu_header=None):
        while True:
            menu = Menu(client=self)
            menu.menu_header = menu_header
            menu.menu_body = self.spaced_class_name
            menu_section = MenuSection()
            menu_section.menu_section_title = 'existing %s' % self.generic_output_name
            menu_section.items_to_number = list(self.iterate_materials_based_on_maker())
            menu.menu_sections.append(menu_section)
            menu.sentence_length_items.append(('new', 'create %s' % self.generic_output_name))
            key, value = menu.display_menu()
            if key == 'b':
                return key, None
            elif key == 'n':
                self.edit_interactively(menu_header=menu.menu_title)
            else:
                material_package_proxy = value
                material_package_proxy.manage_material(menu_header=menu.menu_title)

    def name_material(self):
        self.underscored_material_name = raw_input('Material name> ')

    def overwrite_with_demo_input_values(self, user_input_wrapper):
        for key in self.user_input_template:
            user_input_wrapper[key] = self.user_input_template[key]    

    def save_material(self, user_input_wrapper):
        material = self.make(*user_input_wrapper.values)
        lilypond_file = self.make_lilypond_file_from_output_material(material)
        material_directory = self.write_material_to_disk(user_input_wrapper, material, lilypond_file)
        print ''
        print 'Material saved to %s.\n' % material_directory
        self.proceed()
        return True

    def set_location(self, menu_header=None):
        from baca.scf.ScoreWrangler import ScoreWrangler
        catalog = ScoreWrangler()
        result = catalog.select_score_interactively(menu_header=menu_header)
        self.score = result

    def show_demo_input_values(self, menu_header=None):
        menu_specifier = Menu(client=self, menu_header=menu_header)
        menu_specifier.menu_body = 'demo values'
        items = []
        for i, (key, value) in enumerate(self.user_input_template.iteritems()):
            item = '%s: %r' % (key.replace('_', ' '), value)
            items.append(item)
        menu_specifier.items_to_number = items
        menu_specifier.display_menu(score_title=self.score_title)

    def unname_material(self):
        self.underscored_material_name = None

    def write_material_to_disk(self, user_input_wrapper, material, lilypond_file):
        self.set_material_package_directory()
        self.make_material_package_directory()
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
