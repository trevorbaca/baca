from baca.scf.MaterialProxy import MaterialProxy


class UserInputHandlingMaterialProxy(MaterialProxy):

    ### PUBLIC METHODS ###

    def clear_user_input(self):
        self.print_not_implemented()

    def edit_user_input_at_number(self, number):
        user_input_wrapper = self.user_input_wrapper
        if user_input_wrapper is None:
            return
        if len(user_input_wrapper) < number:
            return
        index = number - 1
        key, current_value = user_input_wrapper.list_items[index]
        test = type(self).user_input_tests[index][1]
        default = type(self).user_input_demo_values[index][1]
        getter = self.make_new_getter()
        spaced_attribute_name = key.replace('_', ' ')
        message = "value for '{}' must satisfy " + 'foo' + '.'
        getter.append_something(spaced_attribute_name, message, default=default)
        getter.tests.append(test)
        new_value = getter.run()
        if self.backtrack():
            return
        user_input_wrapper[key] = new_value 
        self.write_user_input_wrapper_to_disk(user_input_wrapper, prompt_proceed=False)

    def format_user_input_wrapper_for_writing_to_disk(self, user_input_wrapper):
        result = []
        result.extend(type(self).user_input_module_import_statements)
        if result:
            result.append('')
            result.append('')
        result.extend(user_input_wrapper.formatted_lines)
        return result

    def make_main_menu_for_material_made_with_editor(self):
        menu, hidden_section = self.make_new_menu(where=self.where(), is_hidden=True)
        section = menu.make_new_section(is_numbered=True)
        section.tokens = self.formatted_user_input_lines
        section.return_value_attribute = 'number'
        section = menu.make_new_section()
        section.append(('uic', 'user input - clear'))
        return menu, hidden_section

    def write_stub_user_input_module_to_disk(self, prompt_proceed=True):
        user_input_module = file(self.user_input_module_file_name, 'w')
        lines = []
        lines.append('from baca.scf import UserInputWrapper')
        lines.append('')
        lines.append('')
        lines.append('user_input = UserInputWrapper([])')
        user_input_module.write('\n'.join(lines))
        user_input_module.close()
        if prompt_proceed:
            line = 'stub user input module written to disk.'
            self.proceed(lines=[line])

    def write_user_input_wrapper_to_disk(self, user_input_wrapper, prompt_proceed=True):
        formatted_user_input_lines = self.format_user_input_wrapper_for_writing_to_disk(user_input_wrapper)
        user_input_module = file(self.user_input_module_file_name, 'w')
        user_input_module.write('\n'.join(formatted_user_input_lines))
        user_input_module.close()
        if prompt_proceed:
            line = 'user input written to disk.'
            self.proceed(lines=[line])

    ### OLD INTERACTIVE MATERIAL PROXY PUBLIC METHODS ###

    def clear_user_input_wrapper(self, user_input_wrapper):
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        
    def edit_item(self, key, value):
        prompt = key.replace('_', ' ')
        default = repr(value)
        response = self.handle_raw_input_with_default('{}> '.format(prompt), default=default)
        command = 'from abjad import *'
        exec(command)
        new_value = eval(response)
        return new_value

    def initialize_user_input_wrapper(self):
        user_input_wrapper = copy.deepcopy(self.user_input_demo_values)
        for key in user_input_wrapper:
            user_input_wrapper[key] = None
        return user_input_wrapper

    def make_lilypond_file_from_user_input_wrapper(self, user_input_wrapper):
        material = self.make(*user_input_wrapper.values)
        lilypond_file = self.make_lilypond_file_from_output_material(material)
        return lilypond_file

    def overwrite_user_input_wrapper_with_demo_user_input_values(self, user_input_wrapper):
        for key in self.user_input_demo_values:
            user_input_wrapper[key] = self.user_input_demo_values[key]    

    def read_user_input_values_from_disk(self):
        import baca
        score_wrangler = baca.scf.ScoreWrangler()
        material_proxy = score_wrangler.select_interactive_material_proxy(klasses=(type(self),))
        self.user_input_wrapper = copy.deepcopy(material_proxy.user_input_wrapper)
    
    def old_run_interactive(self):
        self._original_score = self.score
        self._original_material_underscored_name = self.material_underscored_name
        self._original_user_input_wrapper = copy.deepcopy(self.user_input_wrapper)
        while True:
            menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
            section.tokens = self.user_input_wrapper.editable_lines
            if self.user_input_wrapper.is_complete:
                section.append(('p', 'show pdf of given input'))
                section.append(('m', 'write material to disk'))
            if self.has_material_underscored_name:
                section.append(('n', 'rename material'))
            else:
                section.append(('n', 'name material'))
            section.append(('nc', 'clear name'))
            section.append(('d', 'show demo input values'))
            section.append(('o', 'overwrite with demo input values'))
            section.append(('i', 'read values from disk'))
            section.append(('c', 'clear values'))
            section.append(('l', 'change location'))
            result = menu.run()
            if result == 'c':
                self.clear_user_input_wrapper(self.user_input_wrapper)
            elif result == 'd':
                self.show_demo_user_input_values()
            elif result == 'i':
                self.read_user_input_values_from_disk()
            elif result == 'l':
                self.move_material_to_location()
            elif result == 'n':
                self.name_material()
            elif result == 'nc':
                self.unname_material()
            elif result == 'o':
                self.overwrite_user_input_wrapper_with_demo_user_input_values(self.user_input_wrapper)
            elif result == 'p':
                lilypond_file = self.make_lilypond_file_from_user_input_wrapper(self.user_input_wrapper)
                lilypond_file.file_initial_user_includes.append(self.stylesheet)
                lilypond_file.header_block.title = markuptools.Markup(self.generic_output_name.capitalize())
                lilypond_file.header_block.subtitle = markuptools.Markup('(unsaved)')
                iotools.show(lilypond_file)
            elif result == 'src':
                self.edit_source_file()
            elif mathtools.is_integer_equivalent_expr(result):
                number = int(result)    
                index = number - 1
                result, value = self.user_input_wrapper.list_items[index]
                new_value = self.edit_item(result)
                self.user_input_wrapper[result] = new_value

    def show_demo_user_input_values(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        items = []
        for i, (key, value) in enumerate(self.user_input_demo_values.iteritems()):
            item = '{}: {!r}'.format(key.replace('_', ' '), value)
            items.append(item)
        section.tokens = items
        menu.run()
