from baca.scf.menuing.Wizard import Wizard


class ScoreTemplateWizard(Wizard):

    ### PUBLIC METHODS ###

    def run(self):
        self.clear_terminal()
        print 'Score template wizard.\n'
        print 'This wizard works in four largescale steps.\n'
        print 'Part 1: number of players.\n'
        getter = self.UserInputGetter()
        getter.prompts.append("Enter the number of players or type 'skip'")
        getter.input_tests.append(lambda x: isinstance(x, int) or x == 'skip')
        player_count = getter.run()
        print player_count
