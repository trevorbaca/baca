import abjad
import baca


class FlattenDivisionCallback(abjad.AbjadValueObject):
    """
    Flatten division callback.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(6) Divisions'

    __slots__ = (
        '_depth',
        )

    ### INITIALIZER ###

    def __init__(self, depth=-1):
        self._depth = depth

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        """
        Calls flatten division callback on `argument`.

        Returns list of divisions or list of division lists.
        """
        return baca.Sequence(argument).flatten(depth=self.depth)

    ### PUBLIC PROPERTIES ###

    @property
    def depth(self):
        """
        Gets depth of callback.

        Returns integer.
        """
        return self._depth
