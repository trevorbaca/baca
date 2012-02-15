class PerformerContributionSpecifier(object):

    def __init__(self,
        articulation_indicator=None,
        clef_indicator=None,
        directive_indicator=None,
        dynamic_indicator=None,
        instrument_indicator=None,
        note_head_indicator=None,
        override_spanner_indicator=None,
        pitch_class_indicator=None,
        registration_indicator=None,
        rhythm_indicator=None,
        staff_indicator=None,
        trill_indicator=None,
        troping_indicator=None,
        ):
        self.articulation_indicator = articulation_indicator
        self.clef_indicator = clef_indicator
        self.directive_indicator = directive_indicator
        self.dynamic_indicator = dynamic_indicator
        self.instrument_indicator = instrument_indicator
        self.note_head_indicator = note_head_indicator
        self.override_spanner_indicator = override_spanner_indicator
        self.pitch_class_indicator = pitch_class_indicator
        self.registration_indicator = registration_indicator
        self.rhythm_indicator = rhythm_indicator
        self.staff_indicator = staff_indicator
        self.trill_indicator = trill_indicator
        self.troping_indicator=troping_indicator
        
    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(type(self).__name__)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def attribute_format_pieces(self):
        result = []
        for co_name in self.__init__.im_func.func_code.co_names:
            value = getattr(self, co_name)
            if value is not None:
                format_pieces = self.get_format_pieces_of_expr(value)
                format_pieces = self.indent_format_pieces(co_name, format_pieces)
                result.extend(format_pieces)
        return result

    @property
    def format(self):
        return '\n'.join(self.format_pieces)

    @property
    def format_pieces(self):
        result = []
        result.append('{}('.format(type(self).__name__))
        for attribute_format_piece in self.attribute_format_pieces:
            result.append('\t' + attribute_format_piece + ',')
        result.append('\t' + ')')
        return result

    ### PUBLIC METHODS ###

    def get_format_pieces_of_expr(self, expr):
        if hasattr(expr, 'format_pieces'):
            return expr.format_pieces
        else:
            return [repr(expr)]

    def indent_format_pieces(self, name, format_pieces):
        result = []
        if len(format_pieces) == 1:
            result.append('{}={}'.format(name, format_pieces[0]))
        elif 1 < len(format_pieces):
            result.append('{}={}'.format(name, format_pieces[0]))
            for format_piece in format_pieces[1:]:
                result.append('\t' + format_piece)
        return result
