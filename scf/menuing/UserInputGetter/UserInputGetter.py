from abjad.tools import iotools
from baca.scf.menuing.MenuObject import MenuObject


class UserInputGetter(MenuObject):

    def __init__(self, execs=None, helps=None, prompts=None, session=None, 
        should_clear_terminal=False, tests=None, where=None):
        MenuObject.__init__(self, session=session, should_clear_terminal=should_clear_terminal, where=where)
        self.execs = execs
        self.helps = helps
        self.prompts = prompts
        self.tests = tests

    ### OVERLOADS ###

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, len(self.prompts))

    ### PUBLIC ATTRIBUTES ###

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

    def append_boolean(self, spaced_attribute_name):
        assert isinstance(spaced_attribute_name, str)
        self.prompts.append(spaced_attribute_name)
        self.execs.append([])
        self.tests.append(self.is_boolean)
        message = "value for '{}' must be boolean.".format(spaced_attribute_name)
        self.helps.append(message)

    def append_integer(self, spaced_attribute_name):
        assert isinstance(spaced_attribute_name, str)
        self.prompts.append(spaced_attribute_name)
        self.execs.append([])
        self.tests.append(self.is_integer)
        message = "value for '{}' must be integer.".format(spaced_attribute_name)
        self.helps.append(message)

    def append_integer_in_closed_range(self, spaced_attribute_name, start, stop):
        assert isinstance(spaced_attribute_name, str)
        self.prompts.append(spaced_attribute_name)
        self.execs.append([])
        self.tests.append(self.make_is_integer_in_closed_range(start, stop))
        message = "value for '{}' must be integer between {} and {}, inclusive."
        message = message.format(spaced_attribute_name, start, stop)
        self.helps.append(message)

    def append_integer_range_in_closed_range(self, spaced_attribute_name, start, stop):
        assert isinstance(spaced_attribute_name, str)
        self.prompts.append(spaced_attribute_name)
        self.execs.append([])
        self.tests.append(self.is_integer_range_string)
        message = "value for '{}' must be integer range within {} and {}, inclusive."
        message = message.format(spaced_attribute_name, start, stop)
        self.helps.append(message)

    def append_markup(self, spaced_attribute_name):
        assert isinstance(spaced_attribute_name, str)
        self.prompts.append(spaced_attribute_name)
        execs = []
        execs.append('from abjad import *')
        execs.append('value = markuptools.Markup(user_response)')
        self.execs.append(execs)
        self.tests.append(self.is_markup)
        message = "value for '{}' must be markup.".format(spaced_attribute_name)
        self.helps.append(message)

    def append_named_chromatic_pitch(self, spaced_attribute_name):
        assert isinstance(spaced_attribute_name, str)
        self.prompts.append(spaced_attribute_name)
        execs = []
        execs.append('from abjad import *')
        execs.append('value = pitchtools.NamedChromaticPitch(user_response)')
        self.execs.append(execs)
        self.tests.append(self.is_named_chromatic_pitch)
        message = "value for '{}' must be named chromaic pitch.".format(spaced_attribute_name)
        self.helps.append(message)

    def append_string(self, spaced_attribute_name):
        assert isinstance(spaced_attribute_name, str)
        self.prompts.append(spaced_attribute_name)
        self.execs.append([])
        self.tests.append(self.is_string)
        self.helps.append('must be string.')

    def append_string_or_none(self, spaced_attribute_name):
        assert isinstance(spaced_attribute_name, str)
        self.prompts.append(spaced_attribute_name)
        self.execs.append([])
        self.tests.append(self.is_string_or_none)
        self.helps.append('must be string or None.')

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
            user_response = self.handle_raw_input(prompt)
            if user_response is None:
                self.prompt_index = self.prompt_index + 1
                break
            user_response = self.handle_hidden_key(user_response)
            if user_response is None:
                return False
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
        if user_input is not None:
            self.session.user_input = user_input
        self.present_prompts_and_store_values()
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
        self.display_cap_lines(lines)

    def store_value(self, user_response):
        assert isinstance(user_response, str)
        input_test = self.tests[self.prompt_index]
        if input_test == self.is_integer_range_string:
            value = user_response
        else:
            execs = self.execs[self.prompt_index]
            assert isinstance(execs, list)
            if execs:
                for exec_string in execs:
                    try:
                        exec(exec_string)
                    except:
                        if self.prompt_index < len(self.helps):
                            lines = []
                            lines.append(self.helps[self.prompt_index])
                            lines.append('')
                            self.display_cap_lines(lines)
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
                    self.display_cap_lines(lines)
        else:
            self.values.append(value)
            self.prompt_index = self.prompt_index + 1
            return True
