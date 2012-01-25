from baca.scf.MaterialPackageProxy import MaterialPackageProxy
import copy


class MaterialPackageMaker(MaterialPackageProxy):

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def illustration(self):
        output_material = self.import_output_material_from_output_material_module()
        illustration = self.illustration_maker(output_material)
        return illustration

    ### PUBLIC METHODS ###

    def clear_user_input_wrapper(self, prompt=True):
        user_input_wrapper = self.user_input_wrapper
        if user_input_wrapper.is_empty:
            lines=['user input already empty.', '']
            self.display(lines)
            self.proceed()
        else:
            user_input_wrapper.clear()
            self.write_user_input_wrapper_to_disk(user_input_wrapper)
            lines=['user input wrapper cleared.']
            self.proceed(lines, prompt=prompt)

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

    def load_user_input_wrapper_demo_values(self, prompt=True):
        user_input_wrapper = self.user_input_wrapper
        user_input_demo_values = copy.deepcopy(type(self).user_input_demo_values)
        for key, value in user_input_demo_values:
            user_input_wrapper[key] = value
        self.write_user_input_wrapper_to_disk(user_input_wrapper) 
        line = 'demo values loaded.'
        self.proceed(line, prompt=prompt)

    def make_main_menu_for_material_made_with_material_package_maker(self):
        menu, hidden_section = self.make_new_menu(where=self.where(), is_hidden=True)
        self.make_main_menu_section_for_user_input_module(menu, hidden_section)
        self.make_main_menu_section_for_output_material(menu, hidden_section)
        return menu, hidden_section

    def make_main_menu_section_for_user_input_module(self, main_menu, hidden_section):
        section = main_menu.make_new_section(is_numbered=True)
        section.tokens = self.user_input_wrapper.editable_lines
        section.return_value_attribute = 'number'
        section = main_menu.make_new_section()
        section.append(('uic', 'user input - clear'))
        section.append(('uil', 'user input - load demo values'))
        section.append(('uip', 'user input - populate'))
        section.append(('uis', 'user input - show demo values'))
        hidden_section.append(('uit','user input - toggle default mode'))

    # TODO: consider making read-only attribute
    def make_output_material(self):
        output_material = self.output_material_maker(*self.user_input_wrapper.values)
        assert type(self).output_material_checker(output_material)
        return output_material

    def populate_user_input_wrapper(self, prompt=True):
        total_elements = len(self.user_input_wrapper)
        getter = self.make_new_getter(where=self.where())
        getter.append_integer_in_closed_range('start at element number', 1, total_elements, default=1)
        self.push_backtrack()
        current_element_number = getter.run()
        self.pop_backtrack()
        if self.backtrack():
            return
        current_element_index = current_element_number - 1
        while True:
            self.push_backtrack()
            self.edit_user_input_at_number(current_element_number)
            self.pop_backtrack()
            if self.backtrack():
                return
            current_element_index += 1
            current_element_index %= total_elements
            current_element_number = current_element_index + 1

    def show_user_input_demo_values(self, prompt=True):
        lines = []
        for i, (key, value) in enumerate(self.user_input_demo_values):
            line = '    {}: {!r}'.format(key.replace('_', ' '), value)
            lines.append(line)
        lines.append('')
        self.display(lines)
        self.proceed(prompt=prompt)

    def write_stub_user_input_module_to_disk(self, prompt=True):
        user_input_module = file(self.user_input_module_file_name, 'w')
        lines = []
        lines.append('from baca.scf import UserInputWrapper')
        lines.append('')
        lines.append('')
        lines.append('user_input = UserInputWrapper([])')
        user_input_module.write('\n'.join(lines))
        user_input_module.close()
        line = 'stub user input module written to disk.'
        self.proceed(line, prompt=prompt)

    def write_user_input_wrapper_to_disk(self, user_input_wrapper):
        formatted_user_input_wrapper_lines = self.format_user_input_wrapper_for_writing_to_disk(user_input_wrapper)
        user_input_module = file(self.user_input_module_file_name, 'w')
        user_input_module.write('\n'.join(formatted_user_input_wrapper_lines))
        user_input_module.close()

    ### OLD INTERACTIVE MATERIAL PROXY PUBLIC METHODS ###

    def old_run_interactive(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        while True:
            menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
            section.tokens = self.user_input_wrapper.editable_lines
            if self.user_input_wrapper.is_complete:
                section.append(('p', 'show pdf of given input'))
            section.append(('d', 'show demo input values'))
            section.append(('l', 'change location'))
            result = menu.run(clear=clear)
            if result == 'd':
                self.show_demo_user_input_values()
            elif result == 'l':
                self.move_material_to_location()
            elif result == 'p':
                illustration = self.illustration
                illustration.file_initial_user_includes.append(self.stylesheet)
                illustration.header_block.title = markuptools.Markup(self.generic_output_name.capitalize())
                illustration.header_block.subtitle = markuptools.Markup('(unsaved)')
                iotools.show(illustration)
        self.restore_breadcrumbs(cache=cache)
