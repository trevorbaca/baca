from abjad.tools import iotools
from abjad.tools import pitchtools
from baca.scf.menuing.MenuObject import MenuObject


# TODO: create MenuSectionAggregator for Menu and UserInputGetter to both inherit from
class UserInputGetter(MenuObject):

    def __init__(self, session=None, where=None):
        MenuObject.__init__(self, session=session, where=where)
        self._sections = []
        self.argument_lists = None
        self.defaults = None
        self.execs = None
        self.helps = None
        self.prompts = None
        self.tests = None

    ### OVERLOADS ###

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, len(self.prompts))

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def sections(self):
        return self._sections

    ### READ / WRITE PUBLIC ATTRIBUTES ###

    @apply
    def argument_lists():
        def fget(self):
            return self._argument_lists
        def fset(self, argument_lists):
            if argument_lists is None:
                self._argument_lists = []
            else:
                assert all([isinstance(x, list) for x in argument_lists])
                self._argument_lists = argument_lists
        return property(**locals())

    @apply
    def defaults():
        def fget(self):
            return self._defaults
        def fset(self, defaults):
            if defaults is None:
                self._defaults = []
            else:
                assert all([isinstance(x, list) for x in defaults])
                self._defaults = defaults
        return property(**locals())

    @apply
    def execs():
        def fget(self):
            return self._execs
        def fset(self, execs):
            if execs is None:
                self._execs = []
            else:
                assert all([isinstance(x, list) for x in execs])
                self._execs = execs
        return property(**locals())

    @apply
    def helps():
        def fget(self):
            return self._helps
        def fset(self, helps):
            if helps is None:
                self._helps = []
            else:
                assert all([isinstance(x, str) for x in helps])
                self._helps = helps
        return property(**locals())

    @apply
    def prompts():
        def fget(self):
            return self._prompts
        def fset(self, prompts):
            if prompts is None:
                self._prompts = []
            else:
                self._prompts = prompts
        return property(**locals())

    @apply
    def tests():
        def fget(self):
            return self._tests
        def fset(self, tests):
            if tests is None:
                self._tests = []
            else:
                self._tests = tests
        return property(**locals())

    ### PUBLIC METHODS ###

    def append_something(self, spaced_attribute_name, message, 
        additional_message_arguments=None, default=None):
        assert isinstance(spaced_attribute_name, str)
        self.prompts.append(spaced_attribute_name)
        self.argument_lists.append([])
        self.execs.append([])
        if additional_message_arguments is None:
            additional_message_arguments = []
        self.helps.append(message.format(spaced_attribute_name, *additional_message_arguments))
        self.defaults.append(default)

    def append_argument_range(self, spaced_attribute_name, argument_list, default=None):
        message = "value for '{}' must be argument range."
        self.append_something(spaced_attribute_name, message, default=default)
        self.argument_lists[-1] = argument_list
        test = lambda expr: self.is_valid_argument_range_string_for_argument_list(expr, argument_list)
        self.tests.append(test)

    def append_boolean(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be boolean."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(self.is_boolean)

    def append_integer(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be integer."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(self.is_integer)

    def append_integer_in_closed_range(self, spaced_attribute_name, start, stop, default=None):
        message = "value for '{}' must be integer between {} and {}, inclusive."
        self.append_something(spaced_attribute_name, message, (start, stop), default=default)
        self.tests.append(self.make_is_integer_in_closed_range(start, stop))

    def append_integer_or_none(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be integer or none."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(self.is_integer_or_none)

    def append_markup(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be markup."
        self.append_something(spaced_attribute_name, message, default=default)
        execs = []
        execs.append('from abjad import *')
        execs.append('value = markuptools.Markup({})')
        self.execs[-1] = execs
        self.tests.append(self.is_markup)

    def append_named_chromatic_pitch(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be named chromatic pitch."
        self.append_something(spaced_attribute_name, message, default=default)
        execs = []
        execs.append('from abjad import *')
        execs.append('value = pitchtools.NamedChromaticPitch({})')
        self.execs[-1] = execs
        self.tests.append(self.is_named_chromatic_pitch)

    def append_pitch_range(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be pitch range."
        self.append_something(spaced_attribute_name, message, default=default)
        execs = []
        execs.append('from abjad import *')
        execs.append('value = pitchtools.PitchRange({})')
        self.execs[-1] = execs
        self.tests.append(self.is_pitch_range_or_none)

    def append_string(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be string."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(self.is_string)

    def append_string_or_none(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be string or none."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(self.is_string_or_none)

    def append_symbolic_pitch_range_string(self, spaced_attribute_name, default=None):
        message = "value for '{}' must be symbolic pitch range string. Ex: [A0, C8]."
        self.append_something(spaced_attribute_name, message, default=default)
        self.tests.append(pitchtools.is_symbolic_pitch_range_string)

    def load_prompt(self):
        prompt = self.prompts[self.prompt_index]
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
            default = self.defaults[self.prompt_index]
            default = str(default)
            user_response = self.handle_raw_input_with_default(prompt, default=default)
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
        self.menu_lines = []
        self.values = []
        self.prompt_index = 0
        while self.prompt_index < len(self.prompts):
            if not self.present_prompt_and_store_value():
                break

    def run(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.session.backtrack_preservation_is_active = True
        self.present_prompts_and_store_values()
        self.session.backtrack_preservation_is_active = False
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
        self.conditionally_display_lines(lines)

    def store_value(self, user_response):
        from baca.scf.menuing.MenuSection import MenuSection
        assert isinstance(user_response, str)
        input_test = self.tests[self.prompt_index]
        argument_list = self.argument_lists[self.prompt_index]
        if argument_list and input_test(user_response):
            dummy_section = MenuSection()
            dummy_section.menu_entry_tokens = argument_list[:]
            value = dummy_section.argument_range_string_to_numbers(user_response)
            self.values.append(value)
            self.prompt_index = self.prompt_index + 1
            return True
        else:
            execs = self.execs[self.prompt_index]
            assert isinstance(execs, list)
            if execs:
                for exec_string in execs:
                    try:
                        formatted_exec_string = exec_string.format(user_response)
                        exec(formatted_exec_string)
                    except:
                        try:
                            formatted_exec_string = exec_string.format(repr(user_response))
                            exec(formatted_exec_string)
                        except:
                            if self.prompt_index < len(self.helps):
                                lines = []
                                lines.append(self.helps[self.prompt_index])
                                lines.append('')
                                self.conditionally_display_lines(lines)
                            return
            else:
                try:
                    value = eval(user_response)
                except (NameError, SyntaxError):
                    value = user_response
        if self.prompt_index < len(self.tests):
            input_test = self.tests[self.prompt_index]
            if input_test(value):
                self.values.append(value)
                self.prompt_index = self.prompt_index + 1
                return True
            else:
                if self.prompt_index < len(self.helps):
                    lines = []
                    lines.append(self.helps[self.prompt_index])
                    lines.append('')
                    self.conditionally_display_lines(lines)
        else:
            self.values.append(value)
            self.prompt_index = self.prompt_index + 1
            return True
