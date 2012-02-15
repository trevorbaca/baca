class MusicSpecifier(object):

    def __init__(self):
        self._perfomer_contribution_specifiers = []

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(type(self).__name__)

    ### READ-ONLY ATTRIBUTES ###

    @property
    def performer_contribution_specifiers(self):
        return self._performer_contribution_specifiers
