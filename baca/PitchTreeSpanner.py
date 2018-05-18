import abjad


class PitchTreeSpanner(abjad.Spanner):
    """
    Pitch tree spanner.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_level',
        )

    ### INITIALIZER ###

    def __init__(self, level=0):
        abjad.Spanner.__init__(self)
        assert isinstance(level, int), repr(level)
        self._level = level

    ### PUBLIC PROPERTIES ###

    @property
    def level(self):
        """
        Gets level of pitch tree spanner.

        Returns integer.
        """
        return self._level

    @property
    def foo(self):
        """
        Gets foo.
        """
        return 'foo'
