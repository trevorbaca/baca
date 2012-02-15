class MusicSpecifier(object):

    def __init__(self, 
        music_specifier_name=None, 
        performer_contribution_specifiers=None,
        tempo=None,
        ):
        self._perfomer_contribution_specifiers = performer_contribution_specifiers or None
        self.music_specifier_name = music_specifier_name
        self.tempo = tempo

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(type(self).__name__)

    ### READ-ONLY ATTRIBUTES ###

    @property
    def performer_contribution_specifiers(self):
        return self._performer_contribution_specifiers
