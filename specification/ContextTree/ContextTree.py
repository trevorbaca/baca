from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools import contexttools
from abjad.tools import scoretools
from baca.specification.ContextProxy import ContextProxy
from collections import OrderedDict


class ContextTree(AbjadObject, OrderedDict):

    ### INITIALIZER ###

    def __init__(self, score):
        assert isinstance(score, scoretools.Score)
        OrderedDict.__init__(self)
        self.score = score
        self.initialize_context_proxies()

    ### SPECIAL METHODS ###

    def __repr__(self):
        contents = ', '.join([repr(x) for x in self])
        return '{}([{}])'.format(self._class_name, contents)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score_name(self):
        for context in contexttools.iterate_contexts_forward_in_expr(self.score):
            if isinstance(context, scoretools.Score):
                return context.name

    ### PUBLIC METHODS ###

    def all_are_context_names(self, expr):
        try:
            return all([x in self for x in expr])
        except:
            return False

    def initialize_context_proxies(self):
        context_names = []
        if self.score is not None:
            for context in contexttools.iterate_contexts_forward_in_expr(self.score):
                assert context.context_name is not None
                context_names.append(context.name)
        for context_name in sorted(context_names):
            self[context_name] = ContextProxy()
