import abjad
import collections


class Loop(abjad.CyclicTuple):
    r"""Loop.

    ..  container::

        >>> loop = baca.Loop([0, 2, 4], [1])
        >>> abjad.f(loop, strict=89)
        baca.Loop(
            [
                abjad.NamedPitch("c'"),
                abjad.NamedPitch("d'"),
                abjad.NamedPitch("e'"),
                ],
            intervals=abjad.CyclicTuple(
                [1]
                ),
            )

        >>> for i in range(12):
        ...     loop[i]
        NamedPitch("c'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("cs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("fs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("g'")

        >>> isinstance(loop, abjad.CyclicTuple)
        True

    ..  container:: example

        >>> command = baca.loop([0, 2, 4], [1])
        >>> abjad.f(command, strict=89)
        baca.PitchCommand(
            cyclic=True,
            pitches=baca.Loop(
                [
                    abjad.NamedPitch("c'"),
                    abjad.NamedPitch("d'"),
                    abjad.NamedPitch("e'"),
                    ],
                intervals=abjad.CyclicTuple(
                    [1]
                    ),
                ),
            selector=baca.pleaves(),
            )

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_intervals',
        '_items',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, items=None, intervals=None):
        if items is not None:
            assert isinstance(items, collections.Iterable), repr(items)
            items = [abjad.NamedPitch(_) for _ in items]
            items = abjad.CyclicTuple(items)
        abjad.CyclicTuple.__init__(self, items=items)
        if intervals is not None:
            assert isinstance(items, collections.Iterable), repr(items)
            intervals = abjad.CyclicTuple(intervals)
        self._intervals = intervals

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        r"""Gets pitch `i` cyclically with intervals.

        Returns pitch.
        """
        if isinstance(i, slice):
            raise NotImplementedError
        iteration = i // len(self)
        if self.intervals is None:
            transposition = 0
        else:
            transposition = sum(self.intervals[:iteration])
        pitch = abjad.CyclicTuple(self)[i]
        pitch = type(pitch)(pitch.number + transposition)
        return pitch

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[list(self.items)],
            storage_format_kwargs_names=['intervals'],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def intervals(self):
        r"""Gets intervals.
        """
        return self._intervals

    @property
    def items(self):
        r"""Gets items.
        """
        return self._items
