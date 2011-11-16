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

    ### PUBLIC METHODS ###

    def append_status_indicator(self, menu_body):
        if self.has_changes:
            menu_body = '%s (*)' % menu_body
        return menu_body

    def clear_values(self, user_input_wrapper):
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        
    def create(self, package_importable_name):
        self.print_not_implemented()
        print 'Interactive material package %s created.\n' % package_importable_name

    def create_interactively(self, menu_header=None):
        while True:
            key, value = self.maker_wrangler.select_maker(menu_header=menu_header)
            if value is None:
                break
            else:
                maker = value
            maker.score = self
            result = maker.edit_interactively(menu_header=menu_header)
            if result:
                break
        self.proceed()
        return True, None

    def edit_interactively(self, menu_header=None, user_input_wrapper=None):
        if user_input_wrapper is None:
            user_input_wrapper = self.initialize_user_input_wrapper()
        self.user_input_wrapper = user_input_wrapper
        self._original_score = self.score
        self._original_material_underscored_name = self.material_underscored_name
        self._original_user_input_wrapper = copy.deepcopy(user_input_wrapper)
        while True:
            menu = self.Menu(where=self.where())
            menu_body = '%s - %s - %s - edit interactively'
            menu_body %= (self.purview_name, self.spaced_class_name, self.material_menu_name)
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
            menu_section.sentence_length_items.append(('i', 'read values from disk'))
            menu_section.sentence_length_items.append(('c', 'clear values'))
            #menu_section.sentence_length_items.append(('src', 'edit source'))
            if self.purview is not None:
                menu_section.sentence_length_items.append(('l', 'change location'))
            else:
                menu_section.sentence_length_items.append(('l', 'set location'))
            menu.menu_sections.append(menu_section)
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
                menu_header = ' - '.join(menu.menu_title_parts[:-1])
                self.set_purview_interactively(menu_header=menu_header)
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
        response = self.raw_input_with_default('%s> ' % prompt, default=default)
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
        material_spaced_name = raw_input('Material name> ')
        self.material_underscored_name = material_spaced_name.replace(' ', '_')

    def overwrite_with_demo_input_values(self, user_input_wrapper):
        for key in self.user_input_template:
            user_input_wrapper[key] = self.user_input_template[key]    

    def read_user_input_values_from_disk(self):
        import baca
        score_wrangler = baca.scf.ScoreWrangler()
        menu_header = 'import %s' % self.spaced_class_name
        material_proxy = score_wrangler.select_interactive_material_proxy(
            menu_header=menu_header, klasses=(type(self),))
        self.user_input_wrapper = copy.deepcopy(material_proxy.user_input_wrapper)
    
    def save_material(self, user_input_wrapper):
        material = self.make(*user_input_wrapper.values)
        lilypond_file = self.make_lilypond_file_from_output_material(material)
        material_directory = self.write_material_to_disk(user_input_wrapper, material, lilypond_file)
        print ''
        print 'Material saved to %s.\n' % material_directory
        self.proceed()
        return True

    def show_demo_input_values(self, menu_header=None):
        menu = self.Menu(where=self.where(), menu_header=menu_header)
        menu.menu_body = 'demo values'
        items = []
        for i, (key, value) in enumerate(self.user_input_template.iteritems()):
            item = '%s: %r' % (key.replace('_', ' '), value)
            items.append(item)
        menu.items_to_number = items
        menu.run(score_title=self.title)

    def unname_material(self):
        self.material_underscored_name = None

    def set_material_package_spaced_name_interactively(self):
        '''This should also cause material package underscored name and directory name to be set.
        '''
        while True:
            if self.material_underscored_name is None:
                self.name_material()
                print ''
            print 'Package short name will be %s.\n' % self.material_package_short_name
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
        input_file.write('maker = %s()\n' % type(self).__name__)
        input_file.write('%s = maker.make(**user_input)\n' % material_underscored_name)
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
