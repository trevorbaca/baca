from baca.scf.MaterialPackageProxy import MaterialPackageProxy
from baca.scf.UserInputWrapper import UserInputWrapper
import copy


class MaterialPackageMaker(MaterialPackageProxy):

    def __init__(self, package_importable_name=None, session=None):
        MaterialPackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        self._user_input_wrapper_in_memory = self._init_user_input_wrapper_in_memory()

    ### PRIVATE METHODS ###

    def _init_user_input_wrapper_in_memory(self):
        user_input_wrapper_in_memory = self.user_input_module_proxy.read_user_input_wrapper_from_disk()
        if user_input_wrapper_in_memory:
            user_input_wrapper_in_memory._user_input_module_import_statements = \
                self.user_input_module_import_statements[:]
        else:
            user_input_wrapper_in_memory = self.make_empty_user_input_wrapper()
        return user_input_wrapper_in_memory

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def illustration(self):
        output_material = self.output_material_module_proxy.import_output_material_safely()
        illustration = self.illustration_maker(output_material)
        return illustration

    @property
    def output_material(self):
        output_material = self.output_material_maker(*self.user_input_wrapper_in_memory.values)
        assert type(self).output_material_checker(output_material)
        return output_material

    @property
    def user_input_wrapper_in_memory(self):
        return self._user_input_wrapper_in_memory

    ### PUBLIC METHODS ###

    def clear_user_input_wrapper(self, prompt=True):
        if self.user_input_wrapper_in_memory.is_empty:
            self.proceed('user input already empty.')
        else:
            self.user_input_wrapper_in_memory.clear()
            self.user_input_module_proxy.write_to_disk(self.user_input_wrapper_in_memory)
            self.proceed('user input wrapper cleared and written to disk.', prompt=prompt)

    def edit_user_input_at_number(self, number):
        #user_input_wrapper = self.user_input_wrapper
        if self.user_input_wrapper_in_memory is None:
            return
        if len(self.user_input_wrapper_in_memory) < number:
            return
        index = number - 1
        key, current_value = self.user_input_wrapper_in_memory.list_items[index]
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
        self.user_input_wrapper_in_memory[key] = new_value 
        self.user_input_module_proxy.write_to_disk(self.user_input_wrapper_in_memory)

    def load_user_input_wrapper_demo_values(self, prompt=True):
        #user_input_wrapper = self.user_input_wrapper
        user_input_demo_values = copy.deepcopy(type(self).user_input_demo_values)
        for key, value in user_input_demo_values:
            self.user_input_wrapper_in_memory[key] = value
        self.user_input_module_proxy.write_to_disk(self.user_input_wrapper_in_memory)
        self.proceed('demo values loaded and written to disk.', prompt=prompt)

    def make_empty_user_input_wrapper(self):
        user_input_wrapper = UserInputWrapper()
        user_input_wrapper._user_input_module_import_statements = \
            self.user_input_module_import_statements[:]
        return user_input_wrapper

    def make_main_menu_section_for_user_input_module(self, main_menu, hidden_section):
        section = main_menu.make_new_section(is_numbered=True)
        section.tokens = self.user_input_wrapper_in_memory.editable_lines
        section.return_value_attribute = 'number'
        section = main_menu.make_new_section()
        section.append(('uic', 'user input - clear'))
        section.append(('uid', 'user input - delete module'))
        section.append(('uil', 'user input - load demo values'))
        section.append(('uip', 'user input - populate'))
        section.append(('uis', 'user input - show demo values'))
        section.append(('uimv', 'user input module - view'))
        hidden_section.append(('uit','user input - toggle default mode'))

    def make_main_menu_sections(self, menu, hidden_section):
        self.make_main_menu_section_for_user_input_module(menu, hidden_section)
        self.make_main_menu_section_for_output_material(menu, hidden_section)

    def populate_user_input_wrapper(self, prompt=True):
        total_elements = len(self.self.user_input_wrapper_in_memory)
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
