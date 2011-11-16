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

    def run(self, session=None, clear_terminal=True):
        session = session or self.Session()
        menu_lines = []
        try:
            if clear_terminal:
                if not response and not session.test:
                    self.clear_terminal()
                    #if self.menu_title is not None:
                    #    print self.menu_title.capitalize() + '\n'
            values = []
            i = 0
            while i < len(self.prompts):
                prompt = self.prompts[i]
                prompt = prompt.capitalize()
                prompt = prompt + '> '
                menu_lines.append(prompt)
                while True:
                    response = self.pop_next_response_from_user_input(session=session)
                    if not response and not session.test:
                        response = raw_input(prompt)
                        print ''
                    if self.handle_hidden_key(response):
                        continue
                    elif response == 'b':
                        #return
                        break
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
                        #return
                        break
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
