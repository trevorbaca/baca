from abjad.tools.abctools.AbjadObject import AbjadObject


class Selection(AbjadObject):

    ### INITIALIZER ###

    #def __init__(self, context_name=None, criterion=None, score_segment_name=None, start=None, stop=None):
    def __init__(self, score_segment_name, context_name, scope=None):
        self.score_segment_name = score_segment_name
        self.context_name = context_name
        self.scope = scope

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if not self._mandatory_argument_values == expr._mandatory_argument_values:
            return False
        for keyword_argument_name in self._keyword_argument_names:
            if not getattr(self, keyword_argument_name) == getattr(expr, keyword_argument_name):
                return False
        return True

    def __ne__(self, expr):
        return not self == expr
