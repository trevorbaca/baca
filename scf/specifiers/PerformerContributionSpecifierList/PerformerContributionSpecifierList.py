from scf.specifiers.Specifier import Specifier


class PerformerContributionSpecifierList(Specifier, list):
    
    def __init__(self, *args):
        Specifier.__init__(self)
        list.__init__(self, *args)

    ### SPECIAL METHODS ###
    
    def __eq__(self, other):
        return list.__eq__(self, other)

    def __repr__(self):
        return '{}({})'.format(self.class_name, len(self))

    ### READ-ONLY ATTRIBUTES ###

    @property
    def format_pieces(self):
        result = []
        result.append('{}(['.format(self.importable_class_name))
        for performer_contribution_specifier in self[:]:
            format_pieces = performer_contribution_specifier.format_pieces
            for format_piece in format_pieces[:-1]:
                result.append('\t' + format_piece)
            result.append('\t' + format_pieces[-1] + ',')
        result.append('\t])')
        return result

    @property
    def one_line_menuing_summary(self):
        pieces = [performer.performer_label for performer in self]
        if pieces:
            return ', '.join(pieces)
