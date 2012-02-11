from abjad.tools import iotools
from abjad.tools import pitchtools
from baca.scf.menuing.MenuSectionAggregator import MenuSectionAggregator
from baca.scf import predicates
import types


class UserInputGetter(MenuSectionAggregator):

    def __init__(self, session=None, where=None):
        MenuSectionAggregator.__init__(self, session=session, where=where)
        self._argument_lists = []
        self._chevrons = []
        self._defaults = []
        self._execs = []
        self._helps = []
        self._prompts = []
        self._tests = []
        self.capitalize_prompts = True
        self.include_newlines = True
        self.indent_level = 0
        self.number_prompts = False
        self.prompt_character = '>'
        self.title = None

    ### OVERLOADS ###

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, len(self.prompts))

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def argument_lists(self):
        return self._argument_lists

    @property
    def chevrons(self):
        return self._chevrons

    @property
    def defaults(self):
        return self._defaults

    @property
    def execs(self):
        return self._execs

    @property
    def helps(self):
        return self._helps

    @property
    def prompts(self):
        return self._prompts

    @property
    def tests(self):
        return self._tests

    ### PUBLIC METHODS ###

    def append_argument_range(self, spaced_attribute_name, argument_list, default=None):
        message = "value for '{}' must be argument range."
        self.append_something(spaced_attribute_name, message, default=default)
        self.argument_lists[-1] = argument_list
        test = lambda expr: predicates.is_readable_argument_range_string_for_argument_list(expr, argument_list)
        self.tests.append(test)

    def append_available_underscore_delimited_lowercase_package_name(self, spaced_attribute_name, default=None):
        message = \
            "value for {!r} must be available underscore-delimited lowercase package name of length at least 3."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_available_underscore_delimited_lowercase_package_name)

    def append_boolean(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be boolean."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_boolean)

    def append_existing_package_name(self, spaced_attribute_name, default=None):
        message = "value for {!r} must be existing package name."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_existing_package_name)

    def append_integer(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be integer."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_integer)

    def append_integer_in_range(self, spaced_attribute_name, 
        start=None, stop=None, allow_none=False, default=None):
        message = "value for '{}' must be integer between {} and {}, inclusive."
        self.append_something(spaced_attribute_name, message, (start, stop), default=default)
        self.tests.append(self.make_is_integer_in_range(start, stop, allow_none=allow_none))

    def append_markup(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be markup."
        self.append_something(spaced_attribute_name, message, default=default)
        execs = []
        execs.append('from abjad import *')
        execs.append('value = markuptools.Markup({})')
        self.execs[-1] = execs
        self.tests.append(predicates.is_markup)

    def append_named_chromatic_pitch(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be named chromatic pitch."
        self.append_something(spaced_attribute_name, message, default=default)
        execs = []
        execs.append('from abjad import *')
        execs.append('value = pitchtools.NamedChromaticPitch({})')
        self.execs[-1] = execs
        self.tests.append(predicates.is_named_chromatic_pitch)

    def append_pitch_range(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be pitch range."
        self.append_something(spaced_attribute_name, message, default=default)
        execs = []
        execs.append('from abjad import *')
        execs.append('value = pitchtools.PitchRange({})')
        self.execs[-1] = execs
        self.tests.append(predicates.is_pitch_range_or_none)

    def append_something(self, spaced_attribute_name, message, 
        additional_message_arguments=None, default=None, include_chevron=True):
        assert isinstance(spaced_attribute_name, str)
        self.prompts.append(spaced_attribute_name)
        self.argument_lists.append([])
        self.execs.append([])
        if additional_message_arguments is None:
            additional_message_arguments = []
        self.helps.append(message.format(spaced_attribute_name, *additional_message_arguments))
        self.defaults.append(default)
        self.chevrons.append(include_chevron)

    def append_string(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be string."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_string)

    def append_string_or_none(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be string or none."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_string_or_none)

    def append_symbolic_pitch_range_string(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be symbolic pitch range string. Ex: [A0, C8]."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(pitchtools.is_symbolic_pitch_range_string)

    def append_underscore_delimited_lowercase_package_name(self, spaced_attribute_name, default=None):
        message = "value for {!r} must be underscore-delimited lowercase package name of length at least 3."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(predicates.is_underscore_delimited_lowercase_package_name)

    def append_yes_no_string(self, spaced_attribute_name, default=None, include_chevron=False):
        message = "value for '{}' must be 'y' or 'n'."
        self.append_something(spaced_attribute_name, message, default=default, include_chevron=include_chevron)
        self.tests.append(predicates.is_yes_no_string)

    def apply_tests_to_value(self, value):
        if self.prompt_index < len(self.tests):
            input_test = self.tests[self.prompt_index]
            return self.evaluate_test(input_test, value)
        return True

    def change_user_response_to_value(self, user_response):
        execs = self.execs[self.prompt_index]
        assert isinstance(execs, list)
        if execs:
            value = self.get_value_from_execs(user_response, execs)
            if not value:
                return '!!!'
        else:
            value = self.get_value_from_direct_evaluation(user_response)
        return value

    def conditionally_display_help(self):
        if self.prompt_index < len(self.helps):
            lines = []
            lines.append(self.helps[self.prompt_index])
            lines.append('')
            self.display(lines)

    def evaluate_test(self, test, argument):
        if isinstance(test, types.TypeType):
            return isinstance(argument, test)
        else:
            return test(argument)

    def display_title(self):
        title_lines = self.make_title_lines()
        if title_lines:
            self.display(title_lines)
        pass

    def get_value_from_direct_evaluation(self, user_response):
        try:
            value = eval(user_response)
        except (NameError, SyntaxError):
            value = user_response
        return value

    def get_value_from_execs(self, user_response, execs):
        for exec_string in execs:
            try:
                command = exec_string.format(user_response)
                exec(command)
            except:
                try:
                    command = exec_string.format(repr(user_response))
                    exec(command)
                except:
                    self.conditionally_display_help()
                    return False
        return value

    def indent_and_number_prompt(self, prompt):
        if self.number_prompts:
            prompt_number = self.prompt_index + 1
            total_prompts = len(self.prompts)
            prompt = '({}/{}) {}'.format(prompt_number, total_prompts, prompt)
        if self.indent_level:
            return '{} {}'.format(self.make_tab(self.indent_level), prompt)
        else:
            return prompt

    def load_prompt(self):
        prompt = self.prompts[self.prompt_index]
        if self.capitalize_prompts:
            prompt = iotools.capitalize_string_start(prompt)
        self.menu_lines.append(prompt)

    def move_to_prev_prompt(self):
        self.values.pop()
        self.prompt_index = self.prompt_index - 1

    def present_prompt_and_store_value(self):
        '''True when user response obtained. Or when user skips prompt.
        False when user quits system or aborts getter.
        '''
        self.load_prompt()
        while True:
            prompt = self.menu_lines[-1]
            default = str(self.defaults[self.prompt_index])
            include_chevron = self.chevrons[self.prompt_index]
            prompt = self.indent_and_number_prompt(prompt)
            user_response = self.handle_raw_input_with_default(prompt, default=default, 
                include_chevron=include_chevron, include_newline=self.include_newlines,
                prompt_character=self.prompt_character, capitalize_prompt=self.capitalize_prompts)
            if user_response is None:
                self.prompt_index = self.prompt_index + 1
                break
            user_response = self.handle_hidden_key(user_response)
            if self.backtrack():
                return False
            elif user_response is None:
                continue
            elif user_response == 'help':
                self.show_help()
            elif user_response == 'prev':
                self.move_to_prev_prompt()
                break
            elif user_response == 'skip':
                break
            elif isinstance(user_response, str):
                if self.store_value(user_response):
                    break
            else:
                self.print_not_implemented()
        return True

    def present_prompts_and_store_values(self):
        self.conditionally_clear_terminal()
        self.menu_lines, self.values, self.prompt_index = [], [], 0
        self.display_title()
        while self.prompt_index < len(self.prompts):
            if not self.present_prompt_and_store_value():
                break

    def run(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.push_backtrack()
        self.present_prompts_and_store_values()
        self.pop_backtrack()
        if len(self.values) == 1:
            return self.values[0]
        else:
            return self.values

    def show_help(self):
        lines = []
        if self.prompt_index < len(self.helps):
            lines.append(self.helps[self.prompt_index])
        else:
            lines.append('help string not available.')
        lines.append('')
        self.display(lines)

    def store_value(self, user_response):
        assert isinstance(user_response, str)
        if self.try_to_store_value_from_argument_list(user_response):
            return True
        value = self.change_user_response_to_value(user_response)
        if value == '!!!':
            return False
        if not self.apply_tests_to_value(value):
            self.conditionally_display_help()
            return False
        self.values.append(value)
        self.prompt_index = self.prompt_index + 1
        return True

    def store_value_from_argument_list(self, user_response, argument_list):
        from baca.scf.menuing.MenuSection import MenuSection
        dummy_section = MenuSection()
        dummy_section.tokens = argument_list[:]
        value = dummy_section.argument_range_string_to_numbers(user_response)
        self.values.append(value)
        self.prompt_index = self.prompt_index + 1

    def try_to_store_value_from_argument_list(self, user_response):
        input_test = self.tests[self.prompt_index]
        argument_list = self.argument_lists[self.prompt_index]
        if argument_list and self.evaluate_test(input_test, user_response):
            self.store_value_from_argument_list(user_response, argument_list)
            return True
        else:
            return False
