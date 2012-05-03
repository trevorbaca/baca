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

    def get_values(self, attribute_name=None, context_name=None, scope=None):
        if context_name is None:
            context_proxies = list(self.itervalues())
        else:
            context_proxies = [self[context_name]]
        values = []
        for context_proxy in context_proxies:
            values.extend(context_proxy.get_values(attribute_name=attribute_name, scope=scope))
        return values 

    def initialize_context_proxies(self):
        context_names = []
        if self.score is not None:
            for context in contexttools.iterate_contexts_forward_in_expr(self.score):
                assert context.context_name is not None
                context_names.append(context.name)
        for context_name in sorted(context_names):
            self[context_name] = ContextProxy()

    def show(self):
        for context_name in self:
            print context_name
            for setting_name in self[context_name]:
                print '\t{}'.format(self[context_name][setting_name]._one_line_format)
