from baca.scf.Specifier import Specifier


class PerformerContributionSpecifierList(Specifier, list):
    
    ### OVERLOADS ###
    
    def __repr__(self):
        return '{}({})'.format(type(self).__name__, len(self))

    ### READ-ONLY ATTRIBUTES ###

    @property
    def format_pieces(self):
        result = []
        result.append('{}('.format(type(self).__name__))
        for performer_contribution_specifier in self[:]:
            format_pieces = performer_contribution_specifier.format_pieces
            for format_piece in format_pieces[:-1]:
                result.append('\t' + format_piece)
            result.append('\t' + format_pieces[-1] + ',')
        result.append('\t)')
        return result
