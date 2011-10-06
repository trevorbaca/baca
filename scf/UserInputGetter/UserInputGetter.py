from baca.scf.MenuObject import MenuObject


class UserInputGetter(MenuObject):

    def __init__(self, prompts=None, menu_header=None, menu_body=None):
        MenuObject.__init__(self, menu_header=menu_header, menu_body=menu_body)
        self.prompts = prompts

    ### PUBLIC ATTRIBUTES ###

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
                    print self.menu_title.capitalize() + '\n'
                responses = []
                for prompt in self.prompts:
                    response = raw_input(prompt)
                    responses.append(response)
                print ''
                if self.confirm():
                    print ''
                    break
        except KeyboardInterrupt:
            return []
        return responses
