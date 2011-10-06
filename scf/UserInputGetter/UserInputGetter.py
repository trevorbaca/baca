from baca.scf.SCFObject import SCFObject


class UserInputGetter(SCFObject):

    def __init__(self, prompts=None, title=None):
        self.prompts = prompts
        self.title = title

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

    def get_user_input(self):
        try:
            while True:
                self.clear_terminal()
                print self.title.capitalize() + '\n'
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
