from baca.scf.menuing._MenuObject import _MenuObject


class UserInputGetter(_MenuObject):

    def __init__(self, client=None, prompts=None, tests=None, helps=None,
        menu_header=None, menu_body=None):
        _MenuObject.__init__(self, client=client, menu_header=menu_header, menu_body=menu_body)
        self.prompts = prompts
        self.tests = tests
        self.helps = helps

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, len(self.prompts))

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
        try:
            if clear_terminal:
                self.clear_terminal()
                if self.menu_title is not None:
                    print self.menu_title.capitalize() + '\n'
            values = []
            i = 0
            while i < len(self.prompts):
                prompt = self.prompts[i]
                prompt = prompt.capitalize()
                prompt = prompt + '> '
                while True:
                    response = raw_input(prompt)
                    print ''
                    if self.handle_hidden_key(response):
                        continue
                    elif response == 'b':
                         return
                    elif response == 'help':
                        if i < len(self.helps):
                            print self.helps[i].capitalize() + '\n'
                        else:
                            print 'Help string not available.\n'
                    elif response == 'prev':
                        values.pop()
                        i = i - 1
                        break
                    elif response == 'skip':
                        return
                    else:
                        try:
                            value = eval(response)
                        except (NameError, SyntaxError):
                            value = response
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
