import abjad
import typing
from abjadext import rmakers


class SkipRhythmMaker(rmakers.RhythmMaker):
    r"""
    Skip rhythm-maker.

    >>> import abjadext

    ..  container:: example

        Makes skips equal to the duration of input divisions.

        >>> rhythm_maker = baca.SkipRhythmMaker()

        >>> divisions = [(1, 4), (3, 16), (5, 8)]
        >>> selections = rhythm_maker(divisions)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     selections,
        ...     divisions,
        ...     )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
            \new RhythmicStaff
            {
                {   % measure
                    \time 1/4
                    s1 * 1/4
                }   % measure
                {   % measure
                    \time 3/16
                    s1 * 3/16
                }   % measure
                {   % measure
                    \time 5/8
                    s1 * 5/8
                }   % measure
            }

    Usage follows the two-step configure-once / call-repeatedly pattern shown
    here.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Rhythm-makers'

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(
        self,
        divisions: typing.List[typing.Tuple[int, int]],
        previous_state: abjad.OrderedDict = None,
        ) -> typing.List[abjad.Selection]:
        """
        Calls skip rhythm-maker on ``divisions``.
        """
        return rmakers.RhythmMaker.__call__(
            self,
            divisions,
            previous_state=previous_state,
            )

    def __format__(self, format_specification='') -> str:
        """
        Formats skip rhythm-maker.

        Set ``format_specification`` to ``''`` or ``'storage'``.

        ..  container:: example

            >>> rhythm_maker = baca.SkipRhythmMaker()
            >>> abjad.f(rhythm_maker)
            baca.SkipRhythmMaker()

        """
        return super(SkipRhythmMaker, self).__format__(
            format_specification=format_specification,
            )

    ### PRIVATE METHODS ###

    def _make_music(self, divisions):
        result = []
        for division in divisions:
            prototype = abjad.NonreducedFraction
            assert isinstance(division, prototype), repr(division)
            written_duration = abjad.Duration(1)
            multiplied_duration = division
            skip = self._make_skips(written_duration, [multiplied_duration])
            result.append(skip)
        return result

    @staticmethod
    def _make_skips(written_duration, multiplied_durations):
        skips = []
        written_duration = abjad.Duration(written_duration)
        for multiplied_duration in multiplied_durations:
            multiplied_duration = abjad.Duration(multiplied_duration)
            skip = abjad.Skip(written_duration)
            multiplier = multiplied_duration / written_duration
            abjad.attach(multiplier, skip)
            skips.append(skip)
        return abjad.select(skips)

    ### PUBLIC PROPERTIES ###

    @property
    def tuplet_specifier(self) -> typing.Optional[rmakers.TupletSpecifier]:
        r"""
        Gets tuplet specifier.

        ..  container:: example

            No effect because ``SkipRhythmMaker`` makes skips instead of
            tuplets:

            >>> rhythm_maker = baca.SkipRhythmMaker(
            ...     tuplet_specifier=abjadext.rmakers.TupletSpecifier(
            ...         force_fraction=True,
            ...         ),
            ...     )

            >>> divisions = [(1, 4), (3, 16), (5, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 1/4
                        s1 * 1/4
                    }   % measure
                    {   % measure
                        \time 3/16
                        s1 * 3/16
                    }   % measure
                    {   % measure
                        \time 5/8
                        s1 * 5/8
                    }   % measure
                }

        Returns tuplet specifier or none.
        """
        return super(SkipRhythmMaker, self).tuplet_specifier
