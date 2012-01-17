from baca.scf.MaterialProxy import MaterialProxy
import copy


class UserInputHandlingMaterialProxy(MaterialProxy):

    ### PUBLIC METHODS ###

    def clear_user_input_wrapper(self, prompt_proceed=True):
        user_input_wrapper = self.user_input_wrapper
        if user_input_wrapper.is_empty:
            self.conditionally_display_lines(lines=['user input already empty.', ''])
            self.proceed()
        else:
            user_input_wrapper.clear()
            self.write_user_input_wrapper_to_disk(user_input_wrapper)
            if prompt_proceed:
                self.proceed(lines=['user input wrapper cleared.'])

    def edit_user_input_at_number(self, number):
        user_input_wrapper = self.user_input_wrapper
        if user_input_wrapper is None:
            return
        if len(user_input_wrapper) < number:
            return
        index = number - 1
        key, current_value = user_input_wrapper.list_items[index]
        test_tuple = type(self).user_input_tests[index]
        test = test_tuple[1]
        if len(test_tuple) == 3:
            exec_string = test_tuple[2]
        else:   
            exec_string = 'value = {}'
        if self.session.use_current_user_input_values_as_default:
            default = current_value
        else:
            default = None
        getter = self.make_new_getter()
        spaced_attribute_name = key.replace('_', ' ')
        message = "value for '{}' must satisfy " + test.__name__ + '().'
        getter.append_something(spaced_attribute_name, message, default=default)
        getter.tests.append(test)
        getter.execs[-1].append('from abjad import *')
        getter.execs[-1].append(exec_string)
        new_value = getter.run()
        if self.backtrack():
            return
        user_input_wrapper[key] = new_value 
        self.write_user_input_wrapper_to_disk(user_input_wrapper)

    def format_user_input_wrapper_for_writing_to_disk(self, user_input_wrapper):
        result = []
        result.extend(type(self).user_input_module_import_statements)
        if result:
            result.append('')
            result.append('')
        result.extend(user_input_wrapper.formatted_lines)
        return result

    def load_user_input_wrapper_demo_values(self, prompt_proceed=True):
        user_input_wrapper = self.user_input_wrapper
        user_input_demo_values = copy.deepcopy(type(self).user_input_demo_values)
        for key, value in user_input_demo_values:
            user_input_wrapper[key] = value
        self.write_user_input_wrapper_to_disk(user_input_wrapper) 
        if prompt_proceed:
            self.proceed(lines=['demo values loaded.'])

    def make_main_menu_for_material_made_with_editor(self):
        menu, hidden_section = self.make_new_menu(where=self.where(), is_hidden=True)
        section = menu.make_new_section(is_numbered=True)
        section.tokens = self.formatted_user_input_lines
        section.return_value_attribute = 'number'
        section = menu.make_new_section()
        section.append(('uic', 'user input - clear'))
        section.append(('uil', 'user input - load demo values'))
        section.append(('uip', 'user input - populate'))
        hidden_section.append(('uit','user input - toggle default mode'))
        return menu, hidden_section

    def populate_user_input_wrapper(self, prompt_proceed=True):
        self.print_not_implemented()

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

    def write_user_input_wrapper_to_disk(self, user_input_wrapper):
        formatted_user_input_lines = self.format_user_input_wrapper_for_writing_to_disk(user_input_wrapper)
        user_input_module = file(self.user_input_module_file_name, 'w')
        user_input_module.write('\n'.join(formatted_user_input_lines))
        user_input_module.close()

    ### OLD INTERACTIVE MATERIAL PROXY PUBLIC METHODS ###

    def make_lilypond_file_from_user_input_wrapper(self, user_input_wrapper):
        material = self.make(*user_input_wrapper.values)
        lilypond_file = self.make_lilypond_file_from_output_material(material)
        return lilypond_file

    def old_run_interactive(self):
        while True:
            menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
            section.tokens = self.user_input_wrapper.editable_lines
            if self.user_input_wrapper.is_complete:
                section.append(('p', 'show pdf of given input'))
            section.append(('d', 'show demo input values'))
            section.append(('l', 'change location'))
            result = menu.run()
            if result == 'd':
                self.show_demo_user_input_values()
            elif result == 'l':
                self.move_material_to_location()
            elif result == 'p':
                lilypond_file = self.make_lilypond_file_from_user_input_wrapper(self.user_input_wrapper)
                lilypond_file.file_initial_user_includes.append(self.stylesheet)
                lilypond_file.header_block.title = markuptools.Markup(self.generic_output_name.capitalize())
                lilypond_file.header_block.subtitle = markuptools.Markup('(unsaved)')
                iotools.show(lilypond_file)

    # TODO: promote to current code
    def show_demo_user_input_values(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        items = []
        for i, (key, value) in enumerate(self.user_input_demo_values.iteritems()):
            item = '{}: {!r}'.format(key.replace('_', ' '), value)
            items.append(item)
        section.tokens = items
        menu.run()
