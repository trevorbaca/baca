from abjad.tools import instrumenttools
from baca.scf.menuing.Wizard import Wizard


# TODO: change name to NewScoreWizard
class ScoreTemplateWizard(Wizard):

    ### PUBLIC METHODS ###

    def assign_instruments_to_player(self, player):
        pass
        
    def get_players(self):
        lines = []
        lines.append('Part 1: the players.')
        lines.append('')
        self.display_lines(lines)
        getter = self.make_new_getter(where=self.where())
        getter.append_integer("enter the number of players or type 'skip'")
        player_count = getter.run()
        players = []
        if player_count is not None:
            for i in xrange(player_count):
                getter = self.make_new_getter(where=self.where())
                getter.append_string("name of player {}".format(i + 1))
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
