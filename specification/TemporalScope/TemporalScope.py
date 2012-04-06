from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools import componenttools


class TemporalScope(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, criterion=None, start=None, stop=None):
        assert self.is_valid_criterion(criterion)
        assert isinstance(start, (int, type(None)))
        assert isinstance(stop, (int, type(None)))
        self.criterion = criterion
        self.start = start
        self.stop = stop

    ### PUBLIC METHODS ###

    def all_are_component_subclasses(self, expr):
        try:
            return all([issubclass(x, componenttools.Component) for x in expr])
        except:
            return False

    def is_valid_criterion(self, criterion):
        if criterion is None:
            return True
        elif self.all_are_component_subclasses(criterion):
            return True
        else:
            raise ValueError('invalid temporal scope criterion: {!r}'.format(criterion))
