from baca.scf.menuing.Wizard import Wizard


class ScoreTemplateWizard(Wizard):

    ### PUBLIC METHODS ###

    def run(self):
        self.clear_terminal()
        print 'Score template wizard.\n'
        print 'This wizard works in four largescale steps.\n'
        print 'Part 1: number of players.\n'
        response = raw_input("Enter the number of players. Or type 'skip'> ")
        number_players = eval(response)
        print number_players
