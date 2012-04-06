from abjad.tools.abctools.AbjadObject import AbjadObject


class TemporalScope(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, criterion=None, start=None, stop=None):
        self.criterion = criterion
        self.start = start
        self.stop = stop
