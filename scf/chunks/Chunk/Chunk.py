from abjad.tools.abctools.AbjadObject import AbjadObject


class Chunk(AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        self._tempo = TempoSpecifier()
