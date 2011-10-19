from abjad.tools import instrumenttools
from baca.scf.menuing.Wizard import Wizard


class ScoreTemplateWizard(Wizard):

    ### PUBLIC METHODS ###

    def assign_instruments_to_player(self, player):
        #for 
        pass
        
    def get_players(self):
        print 'Part 1: the players.\n'
        getter = self.UserInputGetter()
        getter.prompts.append("enter the number of players or type 'skip'")
        getter.input_tests.append(lambda x: isinstance(x, int))
        player_count = getter.run()
        players = []
        if player_count is not None:
            for i in xrange(player_count):
                getter = self.UserInputGetter()
                getter.prompts.append("name of player %s" % (i + 1))
                getter.input_tests.append(lambda x: isinstance(x, str))
                player_name = getter.run(clear_terminal=False)
                player = instrumenttools.HumanMusician(player_name)
                players.append(player)
                self.assign_instruments_to_player(player)
        return players

    def run(self):
        self.clear_terminal()
        print 'Score template wizard.\n'
        print 'This wizard works in four largescale steps.\n'
        players = self.get_players()
