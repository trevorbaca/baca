from abjad.tools import instrumenttools
from baca.scf.menuing.Wizard import Wizard


# TODO: change name to NewScoreWizard
class ScoreTemplateWizard(Wizard):

    ### PUBLIC METHODS ###

    def assign_instruments_to_player(self, player):
        #for 
        pass
        
    def get_players(self):
        lines = []
        lines.append('Part 1: the players.')
        lines.append('')
        self.display_lines(lines)
        getter = self.make_new_getter(where=self.where())
        getter.prompts.append("enter the number of players or type 'skip'")
        getter.tests.append(lambda x: isinstance(x, int))
        player_count = getter.run()
        players = []
        if player_count is not None:
            for i in xrange(player_count):
                getter = self.make_new_getter(where=self.where())
                getter.prompts.append("name of player {}".format(i + 1))
                getter.tests.append(lambda x: isinstance(x, str))
                getter.should_clear_terminal = False
                player_name = getter.run()
                player = instrumenttools.HumanMusician(player_name)
                players.append(player)
                self.assign_instruments_to_player(player)
        return players

    def run(self):
        self.conditionally_clear_terminal()
        lines = []
        lines.append('Score template wizard.')
        lines.append('This wizard works in four largescale steps.')
        self.display_lines(lines)
        players = self.get_players()
