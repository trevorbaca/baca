from abjad.tools import iotools
from baca.scf.menuing.MenuObject import MenuObject


class UserInputGetter(MenuObject):

    def __init__(self, helps=None, prompts=None, tests=None, session=None, 
        should_clear_terminal=True, where=None):
        MenuObject.__init__(self, session=session, should_clear_terminal=should_clear_terminal, where=where)
        self.helps = helps
        self.prompts = prompts
        self.tests = tests

    ### OVERLOADS ###

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, len(self.prompts))

    ### PUBLIC ATTRIBUTES ###

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

    def conditionally_display_prompt_and_get_user_response(self):
        if self.session.is_displayable:
            prompt = self.menu_lines[-1]
            user_response = raw_input(prompt)
            print ''
            return user_response
        else:
            user_response = self.pop_next_user_response_from_user_input()
            # TODO: encapsulate remaining lines of this function in pop_...
            if user_response == '':
                user_response = None
            if user_response is None:
                if self.session.test == 'menu_lines':
                    self.session.test_result = self.menu_lines
            return user_response

    def load_prompt(self):
        prompt = self.prompts[self.prompt_index]
        prompt = iotools.capitalize_string_start(prompt)
        prompt = prompt + '> '
        self.menu_lines.append(prompt)

    def move_to_prev_prompt(self):
        self.values.pop()
        self.prompt_index = self.prompt_index - 1

    def present_prompt_and_store_value(self):
        self.load_prompt()
        while True:
            user_response = self.conditionally_display_prompt_and_get_user_response()
            if user_response is None:
                self.prompt_index = self.prompt_index + 1
                break
            elif self.handle_hidden_key(user_response):
                continue
            elif user_response == 'b':
                break
            elif user_response == 'help':
                self.show_help()
            elif user_response == 'prev':
                self.move_to_prev_prompt()
                break
            elif user_response == 'skip':
                break
            else:
                if self.store_value(user_response):
                    break

    def present_prompts_and_store_values(self):
        self.conditionally_clear_terminal()
        self.menu_lines = []
        self.values = []
        self.prompt_index = 0
        while self.prompt_index < len(self.prompts):
            self.present_prompt_and_store_value()

    def run(self):
        try:
            self.present_prompts_and_store_values()
        except KeyboardInterrupt:
            return
        if len(self.values) == 1:
            return self.values[0]
        else:
            return self.values

    def show_help(self):
        if self.prompt_index < len(self.helps):
            print iotools.capitalize_string_start(self.helps[self.prompt_index] + '\n')
        else:
            print 'Help string not available.\n'

    def store_value(self, user_response):
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
                    print self.helps[self.prompt_index] + '\n'
        else:
            self.values.append(value)
            self.prompt_index = self.prompt_index + 1
            return True
