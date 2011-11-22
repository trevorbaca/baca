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

    def load_prompt(self, prompt_index):
        prompt = self.prompts[prompt_index]
        prompt = iotools.capitalize_string_start(prompt)
        prompt = prompt + '> '
        self.menu_lines.append(prompt)

    def run(self):
        self.menu_lines = []
        try:
            self.conditionally_clear_terminal()
            values = []
            prompt_index = 0
            while prompt_index < len(self.prompts):
                self.load_prompt(prompt_index)
                while True:
                    user_response = self.pop_next_user_response_from_user_input()
                    if not user_response and not self.session.test:
                        user_response = raw_input(prompt)
                        print ''
                    if self.handle_hidden_key(user_response):
                        continue
                    elif user_response == 'b':
                        #return
                        break
                    elif user_response == 'help':
                        if prompt_index < len(self.helps):
                            print iotools.capitalize_string_start(self.helps[prompt_index] + '\n')
                        else:
                            print 'Help string not available.\n'
                    elif user_response == 'prev':
                        values.pop()
                        prompt_index = prompt_index - 1
                        break
                    elif user_response == 'skip':
                        #return
                        break
                    else:
                        try:
                            value = eval(user_response)
                        except (NameError, SyntaxError):
                            value = user_response
                        if prompt_index < len(self.tests):
                            input_test = self.tests[prompt_index]
                            if input_test(value):
                                values.append(value)
                                prompt_index = prompt_index + 1
                                break
                            else:
                                if prompt_index < len(self.helps):
                                    print self.helps[prompt_index] + '\n'
                        else:
                            values.append(value)
                            prompt_index = prompt_index + 1
                            break
        except KeyboardInterrupt:
            return
        except SystemExit:
            raise SystemExit
        if len(values) == 1:
            return values[0]
        else:
            return values
