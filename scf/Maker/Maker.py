from abjad.tools import iotools
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from baca.scf.PackageProxy import PackageProxy
import copy
import os
import shutil


# TODO: maybe Maker class doesn't exist at all? Maybe replaced by (Interactive)MaterialProxy?
class Maker(PackageProxy):

    def __init__(self, material_underscored_name=None, score=None):
        package_importable_name = 'baca.makers.%s' % self.class_name
        PackageProxy.__init__(self, package_importable_name=package_importable_name)
        self.material_underscored_name = material_underscored_name
        self.score = score

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PRIVATE METHODS ###

    # TODO: MaterialProxy ... and reimplement as read-only property
    def _get_lilypond_score_title(self):
        material_underscored_name = os.path.basename(self.material_package_directory)
        if self.is_shared:
            material_parts = material_underscored_name.split('_')
        else:
            material_parts = material_underscored_name.split('_')[1:]
        material_spaced_name = ' '.join(material_parts)
        title = material_spaced_name.capitalize()
        title = markuptools.Markup(title)
        return title

    # TODO: MaterialProxy and reimplement as read-only property
    def _get_lilypond_score_subtitle(self):
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

    # TODO: InteractiveMaterialProxy ... and rename to show interactivity
    def set_material_package_directory(self):
        while True:
            if self.material_underscored_name is None:
                self.name_material()
                print ''
            print 'Package short name will be %s.\n' % self.material_package_short_name
            if self.confirm():
                break

    # TODO: InteractiveMaterialProxy
    def _initialize_user_input_wrapper(self):
        user_input_wrapper = copy.deepcopy(self.user_input_template)
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        return user_input_wrapper
        
    # TODO: InteractiveMaterialMaker
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
        material_underscored_name = os.path.basename(self.material_package_directory)
        input_file.write('maker = %s()\n' % type(self).__name__)
        input_file.write('%s = maker.make(**user_input)\n' % material_underscored_name)
        input_file.close()

    # TODO: MaterialProxy
    def _write_output_file_to_disk(self, material):
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

    # TODO: MaterialProxy
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

    # TODO: MaterialProxy
    @property
    def has_changes(self):
        if not self.score == self._original_score:
            return True
        elif not self.material_underscored_name == self._original_material_underscored_name:
            return True
        elif not self.user_input_wrapper == self._original_user_input_wrapper:
            return True
        else:
            return False

    # TODO: remove and use purview instead
    @property
    def has_location(self):
        return bool(self.score is not None)

    # TODO: MaterialProxy
    @property
    def has_material_underscored_name(self):
        return bool(self.material_underscored_name is not None)

    # TODO: MaterialProxy
    @property
    def is_shared(self):
        return bool(self.score is None)

    # TODO: remove and use purview instead
    @property
    def location_name(self):
        if self.score is not None:
            return self.score.title
        else:
            return 'Studio'

    # TODO: MaterialProxy
    @property
    def material_menu_name(self):
        if self.has_material_underscored_name:
            return self.material_spaced_name
        else:
            return '(unnamed material)'

    # TODO: MaterialProxy
    @property
    def material_package_directory(self):
        if self.materials_directory_name:
            if self.material_package_short_name:
                return os.path.join(self.materials_directory_name, self.material_package_short_name)

    # TODO: MaterialProxy
    @property
    def material_package_short_name(self):
        if self.score is None:  
            return self.material_underscored_name
        else:
            return '%s_%s' % (self.score.package_short_name, self.material_underscored_name)

    # TODO: MaterialProxy
    @property
    def material_spaced_name(self):
        if self.has_material_underscored_name:
            return self.material_underscored_name.replace('_', ' ')

    # TODO: MaterialProxy
    @apply
    def material_underscored_name():
        def fget(self):
            return self._material_underscored_name
        def fset(self, material_underscored_name):
            assert isinstance(material_underscored_name, (str, type(None)))
            if isinstance(material_underscored_name, str):
                assert iotools.is_underscore_delimited_lowercase_string(material_underscored_name)
            self._material_underscored_name = material_underscored_name
        return property(**locals())

    # TODO: MaterialProxy
    @property
    def materials_directory_name(self):
        if self.score is None:
            return self.baca_materials_directory
        else:
            return self.score.materials_directory_name

    # TODO: remove
    @apply
    def score():
        def fget(self):
            return self._score
        def fset(self, score):
            from baca.scf.ScoreProxy import ScoreProxy
            assert isinstance(score, (ScoreProxy, type(None)))
            self._score = score
        return property(**locals())

    # TODO: remove
    @property
    def score_package_short_name(self):
        if self.score is not None:
            return self.score.package_short_name

    ### PUBLIC METHODS ###

    # TODO: InteractiveMaterialProxy
    def append_status_indicator(self, menu_body):
        if self.has_changes:
            menu_body = '%s (*)' % menu_body
        return menu_body

    # TODO: InteractiveMaterialProxy
    def clear_values(self, user_input_wrapper):
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        
    # TODO: InteractiveMaterialProxy
    def edit_interactively(self, menu_header=None, user_input_wrapper=None):
        if user_input_wrapper is None:
            user_input_wrapper = self._initialize_user_input_wrapper()
        self.user_input_wrapper = user_input_wrapper
        self._original_score = self.score
        self._original_material_underscored_name = self.material_underscored_name
        self._original_user_input_wrapper = copy.deepcopy(user_input_wrapper)
        while True:
            menu = self.Menu(client=self.where())
            menu_body = '%s - %s - %s - edit interactively'
            menu_body %= (self.location_name, self.spaced_class_name, self.material_menu_name)
            menu_body = self.append_status_indicator(menu_body)
            menu.menu_body = menu_body
            menu_section = self.MenuSection()
            menu_section.items_to_number = self.user_input_wrapper.editable_lines
            if self.user_input_wrapper.is_complete:
                menu_section.sentence_length_items.append(('p', 'show pdf of given input'))
                menu_section.sentence_length_items.append(('m', 'write material to disk'))
            if self.has_material_underscored_name:
                menu_section.sentence_length_items.append(('n', 'rename material'))
            else:
                menu_section.sentence_length_items.append(('n', 'name material'))
            menu_section.sentence_length_items.append(('nc', 'clear name'))
            menu_section.sentence_length_items.append(('d', 'show demo input values'))
            menu_section.sentence_length_items.append(('o', 'overwrite with demo input values'))
            menu_section.sentence_length_items.append(('i', 'import values'))
            menu_section.sentence_length_items.append(('c', 'clear values'))
            #menu_section.sentence_length_items.append(('src', 'edit source'))
            if self.has_location:
                menu_section.sentence_length_items.append(('l', 'change location'))
            else:
                menu_section.sentence_length_items.append(('l', 'set location'))
            menu.menu_sections.append(menu_section)
            key, value = menu.display_menu()
            if key == 'b':
                self.interactively_check_and_save_material(self.user_input_wrapper)
                return key, None
            elif key == 'c':
                self.clear_values(self.user_input_wrapper)
            elif key == 'd':
                self.show_demo_input_values()
            elif key == 'i':
                self.import_values()
            elif key == 'l':
                menu_header = ' - '.join(menu.menu_title_parts[:-1])
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
            elif key == 'src':
                self.edit_source_file()
            else:
                try:
                    number = int(key)
                except:
                    continue
                index = number - 1
                key, value = self.user_input_wrapper.list_items[index]
                new_value = self.edit_item(key, value)
                self.user_input_wrapper[key] = new_value

    # TODO: InteractiveMaterialProxy
    def edit_item(self, key, value):
        prompt = key.replace('_', ' ')
        default = repr(value)
        response = self.raw_input_with_default('%s> ' % prompt, default=default)
        exec('from abjad import *')
        new_value = eval(response)
        return new_value

    # TODO: InteractiveMaterialProxy ... and rename this method to show interactivity
    def import_values(self):
        import baca
        score_wrangler = baca.scf.ScoreWrangler()
        menu_header = 'import %s' % self.spaced_class_name
        material_proxy = score_wrangler.select_interactive_material_proxy(
            menu_header=menu_header, klasses=(type(self),))
        self.user_input_wrapper = copy.deepcopy(material_proxy.user_input_wrapper)
    
    # TODO: InteractiveMaterialProxy
    def interactively_check_and_save_material(self, user_input_wrapper):
        if user_input_wrapper.is_complete:
            if self.query('Save material? '):
                self.save_material(user_input_wrapper)

    # TODO: ScoreWrangler
    def iterate_materials_based_on_maker(self):
        import baca
        score_wrangler = baca.scf.ScoreWrangler()
        for material_proxy in score_wrangler.iterate_material_proxies(class_names=(self.class_name,)):
            yield material_proxy

    # TODO: InteractiveMaterialProxy
    def make_lilypond_file_from_user_input_wrapper(self, user_input_wrapper):
        material = self.make(*user_input_wrapper.values)
        lilypond_file = self.make_lilypond_file_from_output_material(material)
        return lilypond_file

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

    # TODO: InteractiveMaterialProxy
    def name_material(self):
        material_spaced_name = raw_input('Material name> ')
        self.material_underscored_name = material_spaced_name.replace(' ', '_')

    # TODO: InteractiveMaterialProxy
    def overwrite_with_demo_input_values(self, user_input_wrapper):
        for key in self.user_input_template:
            user_input_wrapper[key] = self.user_input_template[key]    

    # TODO: MaterialProxy
    def save_material(self, user_input_wrapper):
        material = self.make(*user_input_wrapper.values)
        lilypond_file = self.make_lilypond_file_from_output_material(material)
        material_directory = self.write_material_to_disk(user_input_wrapper, material, lilypond_file)
        print ''
        print 'Material saved to %s.\n' % material_directory
        self.proceed()
        return True

    # TODO: InteractiveMaterialProxy ... then replace with PackageProxy method
    def set_location(self, menu_header=None):
        import baca
        score_wrangler = baca.scf.ScoreWrangler()
        score_proxy = score_wrangler.select_score_proxy(menu_header=menu_header)
        self.score = score_proxy

    # TODO: InteractiveMaterialProxy
    def show_demo_input_values(self, menu_header=None):
        menu = self.Menu(client=self.where(), menu_header=menu_header)
        menu.menu_body = 'demo values'
        items = []
        for i, (key, value) in enumerate(self.user_input_template.iteritems()):
            item = '%s: %r' % (key.replace('_', ' '), value)
            items.append(item)
        menu.items_to_number = items
        menu.display_menu(score_title=self.title)

    # TODO: MaterialProxy
    def unname_material(self):
        self.material_underscored_name = None

    # TODO: InteractiveMaterialProxy
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
