from abjad.tools import iotools
from baca.scf.menuing.MenuObject import MenuObject


class UserInputGetter(MenuObject):

    def __init__(self, where=None, session=None, prompts=None, tests=None, helps=None):
        MenuObject.__init__(self, where=where, session=session)
        self.prompts = prompts
        self.tests = tests
        self.helps = helps

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
    def tests():
        def fget(self):
            return self._tests
        def fset(self, tests):
            if tests is None:
                self._tests = []
            else:
                self._tests = tests
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

    ### PUBLIC METHODS ###

    def run(self, clear_terminal=True):
        menu_lines = []
        try:
            if clear_terminal:
                if not user_response and not self.session.test:
                    self.clear_terminal()
            values = []
            i = 0
            while i < len(self.prompts):
                prompt = self.prompts[i]
                prompt = iotools.capitalize_string(prompt)
                prompt = prompt + '> '
                menu_lines.append(prompt)
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
                        if i < len(self.helps):
                            print iotools.capitalize_string(self.helps[i] + '\n')
                        else:
                            print 'Help string not available.\n'
                    elif user_response == 'prev':
                        values.pop()
                        i = i - 1
                        break
                    elif user_response == 'skip':
                        #return
                        break
                    else:
                        try:
                            value = eval(user_response)
                        except (NameError, SyntaxError):
                            value = user_response
                        if i < len(self.tests):
                            input_test = self.tests[i]
                            if input_test(value):
                                values.append(value)
                                i = i + 1
                                break
                            else:
                                if i < len(self.helps):
                                    print self.helps[i] + '\n'
                        else:
                            values.append(value)
                            i = i + 1
                            break
        except KeyboardInterrupt:
            return
        except SystemExit:
            raise SystemExit
        if len(values) == 1:
            return values[0]
        else:
            return values
