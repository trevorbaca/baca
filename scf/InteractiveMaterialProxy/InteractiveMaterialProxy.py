from baca.scf.MaterialProxy import MaterialProxy


class InteractiveMaterialProxy(MaterialProxy):

    ### PUBLIC ATTRIBUTES ###

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

    @property
    def material_menu_name(self):
        if self.has_material_underscored_name:
            return self.material_spaced_name
        else:
            return '(unnamed material)'

    @property
    def status_indicator_string(self):
        if self.has_changes:
            return ' (*)'
        else:
            return ''

    ### PUBLIC METHODS ###

    def clear_values(self, user_input_wrapper):
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        
    def create(self, package_importable_name):
        self.print_not_implemented()
        line = 'Interactive material package {} created.\n'.format(package_importable_name)
        self.display_lines([line])

    def create_interactively(self):
        while True:
            key, value = self.maker_wrangler.select_maker()
            if value is None:
                break
            else:
                maker = value
            maker.score = self
            result = maker.run()
            if result:
                break
        self.proceed()
        return True, None

    def run(self, user_input_wrapper=None):
        if user_input_wrapper is None:
            user_input_wrapper = self.initialize_user_input_wrapper()
        self.user_input_wrapper = user_input_wrapper
        self._original_score = self.score
        self._original_material_underscored_name = self.material_underscored_name
        self._original_user_input_wrapper = copy.deepcopy(user_input_wrapper)
        while True:
            menu, section = self.make_new_menu(where=self.where())
            section.items_to_number = self.user_input_wrapper.editable_lines
            if self.user_input_wrapper.is_complete:
                section.keyed_menu_entry_tuples.append(('p', 'show pdf of given input'))
                section.keyed_menu_entry_tuples.append(('m', 'write material to disk'))
            if self.has_material_underscored_name:
                section.keyed_menu_entry_tuples.append(('n', 'rename material'))
            else:
                section.keyed_menu_entry_tuples.append(('n', 'name material'))
            section.keyed_menu_entry_tuples.append(('nc', 'clear name'))
            section.keyed_menu_entry_tuples.append(('d', 'show demo input values'))
            section.keyed_menu_entry_tuples.append(('o', 'overwrite with demo input values'))
            section.keyed_menu_entry_tuples.append(('i', 'read values from disk'))
            section.keyed_menu_entry_tuples.append(('c', 'clear values'))
            #section.keyed_menu_entry_tuples.append(('src', 'edit source'))
            if self.purview is not None:
                section.keyed_menu_entry_tuples.append(('l', 'change location'))
            else:
                section.keyed_menu_entry_tuples.append(('l', 'set location'))
            key, value = menu.run()
            if key == 'b':
                self.interactively_check_and_save_material(self.user_input_wrapper)
                return key, None
            elif key == 'c':
                self.clear_values(self.user_input_wrapper)
            elif key == 'd':
                self.show_demo_input_values()
            elif key == 'i':
                self.read_user_input_values_from_disk()
            elif key == 'l':
                self.set_purview_interactively()
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

    def edit_item(self, key, value):
        prompt = key.replace('_', ' ')
        default = repr(value)
        response = self.handle_raw_input_with_default('{}> '.format(prompt), default=default)
        exec('from abjad import *')
        new_value = eval(response)
        return new_value

    def initialize_user_input_wrapper(self):
        user_input_wrapper = copy.deepcopy(self.user_input_template)
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        return user_input_wrapper

    def interactively_check_and_save_material(self, user_input_wrapper):
        if user_input_wrapper.is_complete:
            if self.query('Save material? '):
                self.save_material(user_input_wrapper)

    def make_lilypond_file_from_user_input_wrapper(self, user_input_wrapper):
        material = self.make(*user_input_wrapper.values)
        lilypond_file = self.make_lilypond_file_from_output_material(material)
        return lilypond_file

    def name_material_interactively(self):
        material_spaced_name = self.handle_raw_input('material name')
        self.material_underscored_name = material_spaced_name.replace(' ', '_')

    def overwrite_with_demo_input_values(self, user_input_wrapper):
        for key in self.user_input_template:
            user_input_wrapper[key] = self.user_input_template[key]    

    def read_user_input_values_from_disk(self):
        import baca
        score_wrangler = baca.scf.ScoreWrangler()
        material_proxy = score_wrangler.select_interactive_material_proxy(klasses=(type(self),))
        self.user_input_wrapper = copy.deepcopy(material_proxy.user_input_wrapper)
    
    def save_material(self, user_input_wrapper):
        lines = []
        material = self.make(*user_input_wrapper.values)
        lilypond_file = self.make_lilypond_file_from_output_material(material)
        material_directory = self.write_material_to_disk(user_input_wrapper, material, lilypond_file)
        lines.append('')
        lines.append('material saved to {}.\n'.format(material_directory))
        self.display_lines(lines)
        self.proceed()
        return True

    def show_demo_input_values(self):
        menu, section = self.make_new_menu(where=self.where())
        items = []
        for i, (key, value) in enumerate(self.user_input_template.iteritems()):
            item = '{}: {!r}'.format(key.replace('_', ' '), value)
            items.append(item)
        menu.items_to_number = items
        menu.run()

    def unname_material(self):
        self.material_underscored_name = None

    def set_material_package_spaced_name_interactively(self):
        '''This should also cause material package underscored name and directory name to be set.
        '''
        while True:
            lines = []
            if self.material_underscored_name is None:
                self.name_material()
                lines.append('')
            lines.append('Package short name will be {}.\n'.format(self.material_package_short_name))
            self.display_lines(lines)
            if self.confirm():
                break

    def write_input_file_to_disk(self, user_input_import_statements, user_input_wrapper):
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
        input_file.write('maker = {}()\n'.format(type(self).__name__))
        input_file.write('{} = maker.make(**user_input)\n'.format(material_underscored_name))
        input_file.close()

    def write_material_to_disk(self, user_input_wrapper, material, lilypond_file):
        self.set_material_package_spaced_name_interactively()
        self.make_material_package_directory()
        self._write_initializer_to_disk()
        self._write_input_file_to_disk(self.user_input_import_statements, user_input_wrapper)
        self.write_output_file_to_disk(material)
        self.write_stylesheet_to_disk()
        stylesheet = os.path.join(self.material_package_directory, 'stylesheet.ly')
        lilypond_file.file_initial_user_includes.append(stylesheet)
        ly_file = os.path.join(self.material_package_directory, 'visualization.ly')
        iotools.write_expr_to_ly(lilypond_file, ly_file, print_status=False, tagline=True)
        pdf = os.path.join(self.material_package_directory, 'visualization.pdf')
        iotools.write_expr_to_pdf(lilypond_file, pdf, print_status=False, tagline=True)
        self._add_line_to_materials_initializer()
        return self.material_package_directory
