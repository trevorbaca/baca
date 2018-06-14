import abjad


class MeasureWrapper(abjad.AbjadObject):
    """
    Measure wrapper.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_command',
        '_measures',
        )

    ### INITIALIZER ###

    def __init__(self, *, command=None, measures=None):
        self._command = command
        self._measures = measures

    ### PUBLIC PROPERTIES ###

    @property
    def command(self):
        """
        Gets command.
        """
        return self._command

    @property
    def measures(self):
        """
        Gets measures.
        """
        return self._measures
