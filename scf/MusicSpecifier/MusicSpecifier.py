from baca.scf.Specifier import Specifier


class MusicSpecifier(Specifier):

    def __init__(self, 
        music_specifier_name=None, 
        performer_contribution_specifiers=None,
        tempo=None,
        ):
        self.music_specifier_name = music_specifier_name
        self.performer_contribution_specifiers = performer_contribution_specifiers or []
        self.tempo = tempo

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(type(self).__name__)

    ### READ-ONLY ATTRIBUTES ###
