from baca.scf.menuing._MenuObject import _MenuObject


class UserInputGetter(_MenuObject):

    def __init__(self, client=None, prompts=None, input_tests=None, input_help_strings=None,
        menu_header=None, menu_body=None):
        _MenuObject.__init__(self, client=client, menu_header=menu_header, menu_body=menu_body)
        self.prompts = prompts
        self.input_tests = input_tests
        self.input_help_strings = input_help_strings

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, len(self.prompts))

    ### PUBLIC ATTRIBUTES ###

    @apply
    def input_help_strings():
        def fget(self):
            return self._input_help_strings
        def fset(self, input_help_strings):
            if input_help_strings is None:
                self._input_help_strings = []
            else:
                assert all([isinstance(x, str) for x in input_help_strings])
                self._input_help_strings = input_help_strings
        return property(**locals())

    @apply
    def input_tests():
        def fget(self):
            return self._input_tests
        def fset(self, input_tests):
            if input_tests is None:
                self._input_tests = []
            else:
                self._input_tests = input_tests
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

    def get_user_input(self, clear_terminal=True):
        try:
            while True:
                if clear_terminal:
                    self.clear_terminal()
                    if self.menu_title is not None:
                        print self.menu_title.capitalize() + '\n'
                values = []
                for i, prompt in enumerate(self.prompts):
                    while True:
                        response = raw_input(prompt)
                        if response == 'b':
                            print 'back will be implemented soon!'
                        elif response == 'help':
                            if i < len(self.input_help_strings):
                                print self.input_help_strings[i] + '\n'
                            else:
                                print 'Help string not available.\n'
                        elif response == 'next':
                            print 'next will be implemented soon!'
                        elif response == 'prev':
                            print 'prev will be implemented soon!'
                        elif response == 'q':
                            print 'quit will be implemented soon!'
                        else:
                            value = eval(response)
                            if i < len(self.input_tests):
                                input_test = self.input_tests[i]
                                is_good = apply(input_test, value)
                                if is_good:
                                    values.append(value)
                                    break
                            else:
                                values.append(value)
                                break
                print ''
                if self.confirm():
                    print ''
                    break
        except KeyboardInterrupt:
            return []
        return values
