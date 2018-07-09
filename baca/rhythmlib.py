"""
Rhythm library.
"""
import abjad
import collections
import inspect
import math
import typing
from . import evallib
from . import typings
from . import divisionlib
from .LMRSpecifier import LMRSpecifier
from .Selection import Selection
from .Sequence import Sequence
from abjadext import rmakers
mask_typing = typing.Union[rmakers.SilenceMask, rmakers.SustainMask]


### CLASSES ###

class AcciaccaturaSpecifier(abjad.AbjadObject):
    r"""
    Acciaccatura specifier.

    >>> from abjadext import rmakers

    ..  container:: example

        Default acciaccatura specifier:

        >>> rhythm_maker = baca.PitchFirstRhythmMaker(
        ...     acciaccatura_specifiers=[
        ...         baca.AcciaccaturaSpecifier()
        ...         ],
        ...     talea=rmakers.Talea(
        ...         counts=[1],
        ...         denominator=8,
        ...         ),
        ...     )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ...     ]
        >>> selections, state_manifest = rhythm_maker(collections)
        >>> lilypond_file = rhythm_maker.show(selections)
        >>> score = lilypond_file[abjad.Score]
        >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
        >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            {
                {   % measure
                    \time 3/4
                    \scaleDurations #'(1 . 1) {
                        c'8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            fs''16 [                                                                 %! ACC1
                            e''16 ]                                                                  %! ACC1
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            af''16 [                                                                 %! ACC1
                            g''16
                            a'16 ]                                                                   %! ACC1
                        }
                        c'8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            d'16 [                                                                   %! ACC1
                            bf'16
                            fs''16
                            e''16 ]                                                                  %! ACC1
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            af''16 [                                                                 %! ACC1
                            g''16
                            a'16
                            c'16
                            d'16 ]                                                                   %! ACC1
                        }
                        bf'8
                    }
                }   % measure
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_durations',
        '_lmr_specifier',
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        durations=None,
        lmr_specifier=None,
        pattern=None,
        ):
        if durations is not None:
            assert isinstance(durations, list), repr(durations)
            durations = [abjad.Duration(_) for _ in durations]
        self._durations = durations
        if lmr_specifier is not None:
            prototype = LMRSpecifier
            assert isinstance(lmr_specifier, prototype)
        self._lmr_specifier = lmr_specifier
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern

    ### SPECIAL METHODS ###

    def __call__(self, collection=None):
        """
        Calls acciaccatura specifier on ``collection``.

        Returns acciaccatura container together with new collection.
        """
        prototype = (list, abjad.Segment)
        assert isinstance(collection, prototype), repr(collection)
        lmr_specifier = self._get_lmr_specifier()
        segment_parts = lmr_specifier(collection)
        segment_parts = [_ for _ in segment_parts if _]
        collection = [_[-1] for _ in segment_parts]
        durations = self._get_durations()
        acciaccatura_containers = []
        maker = abjad.LeafMaker()
        for segment_part in segment_parts:
            if len(segment_part) <= 1:
                acciaccatura_containers.append(None)
                continue
            grace_token = list(segment_part[:-1])
            grace_leaves = maker(grace_token, durations)
            acciaccatura_container = abjad.AcciaccaturaContainer(grace_leaves)
            if 1 < len(acciaccatura_container):
                abjad.attach(
                    abjad.Beam(),
                    acciaccatura_container[:],
                    tag='ACC1',
                    )
            acciaccatura_containers.append(acciaccatura_container)
        assert len(acciaccatura_containers) == len(collection)
        return acciaccatura_containers, collection

    ### PRIVATE METHODS ###

    def _get_durations(self):
        return self.durations or [abjad.Duration(1, 16)]

    def _get_lmr_specifier(self):
        if self.lmr_specifier is not None:
            return self.lmr_specifier
        return LMRSpecifier()

    def _get_pattern(self):
        return self.pattern or abjad.index_all()

    ### PUBLIC PROPERTIES ###

    @property
    def durations(self):
        r"""
        Gets durations.

        ..  container:: example

            Sixteenth-note acciaccaturas by default:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier()
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16 [                                                                 %! ACC1
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16 ]                                                                   %! ACC1
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16 [                                                                   %! ACC1
                                bf'16
                                fs''16
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16
                                c'16
                                d'16 ]                                                                   %! ACC1
                            }
                            bf'8
                        }
                    }   % measure
                }

        ..  container:: example

            Eighth-note acciaccaturas:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             durations=[(1, 8)],
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'8
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''8 [                                                                  %! ACC1
                                e''8 ]                                                                   %! ACC1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''8 [                                                                  %! ACC1
                                g''8
                                a'8 ]                                                                    %! ACC1
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'8 [                                                                    %! ACC1
                                bf'8
                                fs''8
                                e''8 ]                                                                   %! ACC1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''8 [                                                                  %! ACC1
                                g''8
                                a'8
                                c'8
                                d'8 ]                                                                    %! ACC1
                            }
                            bf'8
                        }
                    }   % measure
                }

        Defaults to none.

        Set to durations or none.

        Returns durations or none.
        """
        return self._durations

    @property
    def lmr_specifier(self):
        r"""
        Gets LMR specifier.

        ..  container:: example

            As many acciaccaturas as possible per collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier()
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16 [                                                                 %! ACC1
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16 ]                                                                   %! ACC1
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16 [                                                                   %! ACC1
                                bf'16
                                fs''16
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16
                                c'16
                                d'16 ]                                                                   %! ACC1
                            }
                            bf'8
                        }
                    }   % measure
                }


        ..  container:: example

            At most two acciaccaturas at the beginning of every collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier(
            ...                 left_length=3,
            ...                 right_counts=[1],
            ...                 right_cyclic=True,
            ...                 ),
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/2
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16 [                                                                 %! ACC1
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16 ]                                                                  %! ACC1
                            }
                            a'8
                            [
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16 [                                                                   %! ACC1
                                bf'16 ]                                                                  %! ACC1
                            }
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16 ]                                                                  %! ACC1
                            }
                            a'8
                            [
                            c'8
                            d'8
                            bf'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            At most two acciaccaturas at the end of every collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier(
            ...                 right_length=3,
            ...                 left_counts=[1],
            ...                 left_cyclic=True,
            ...                 ),
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/2
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16 [                                                                 %! ACC1
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            \acciaccatura {
                                g''16 [                                                                  %! ACC1
                                a'16 ]                                                                   %! ACC1
                            }
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            \acciaccatura {
                                fs''16 [                                                                 %! ACC1
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            g''8
                            a'8
                            \acciaccatura {
                                c'16 [                                                                   %! ACC1
                                d'16 ]                                                                   %! ACC1
                            }
                            bf'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            At most two acciaccaturas at the beginning of every collection and
            then at most two acciaccaturas at the end of every collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier(
            ...                 left_length=3,
            ...                 middle_counts=[1],
            ...                 middle_cyclic=True,
            ...                 right_length=3,
            ...                 ),
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 9/8
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16 [                                                                 %! ACC1
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16 ]                                                                  %! ACC1
                            }
                            a'8
                            [
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16 [                                                                   %! ACC1
                                bf'16 ]                                                                  %! ACC1
                            }
                            fs''8
                            [
                            \acciaccatura {
                                e''16
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16 ]                                                                  %! ACC1
                            }
                            a'8
                            [
                            \acciaccatura {
                                c'16 [                                                                   %! ACC1
                                d'16 ]                                                                   %! ACC1
                            }
                            bf'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            As many acciaccaturas as possible in the middle of every collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier(
            ...                 left_length=1,
            ...                 ),
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 11/8
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            \acciaccatura {
                                e''16
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            \acciaccatura {
                                g''16 [                                                                  %! ACC1
                                a'16 ]                                                                   %! ACC1
                            }
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            \acciaccatura {
                                bf'16 [                                                                  %! ACC1
                                fs''16
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            \acciaccatura {
                                g''16 [                                                                  %! ACC1
                                a'16
                                c'16
                                d'16 ]                                                                   %! ACC1
                            }
                            bf'8
                            ]
                        }
                    }   % measure
                }

        Defaults to none.

        Set to LMR specifier or none.

        Returns LMR specifier or none.
        """
        return self._lmr_specifier

    @property
    def pattern(self):
        r"""
        Gets pattern.

        ..  container:: example

            Applies to all collections by default:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier()
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16 [                                                                 %! ACC1
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16 ]                                                                   %! ACC1
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16 [                                                                   %! ACC1
                                bf'16
                                fs''16
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16
                                c'16
                                d'16 ]                                                                   %! ACC1
                            }
                            bf'8
                        }
                    }   % measure
                }

        ..  container:: example

            Applies to last collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             pattern=abjad.index_last(1),
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 2/1
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            g''8
                            a'8
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            fs''8
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16
                                c'16
                                d'16 ]                                                                   %! ACC1
                            }
                            bf'8
                        }
                    }   % measure
                }

        ..  container:: example

            Applies to every other collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             pattern=abjad.index([1], 2),
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/2
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16 ]                                                                   %! ACC1
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            fs''8
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16
                                c'16
                                d'16 ]                                                                   %! ACC1
                            }
                            bf'8
                        }
                    }   % measure
                }

        Defaults to none.

        Set to pattern or none.

        Returns pattern or none.
        """
        return self._pattern

class PitchFirstRhythmCommand(evallib.Command):
    """
    Pitch-first rhythm command.

    ..  container:: example

        >>> baca.PitchFirstRhythmCommand()
        PitchFirstRhythmCommand()

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_pattern',
        '_rhythm_maker',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        pattern=None,
        rhythm_maker=None,
        ):
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern
        self._rhythm_maker = rhythm_maker

    ### SPECIAL METHODS ###

    def __call__(
        self,
        collections,
        selections,
        division_masks=None,
        logical_tie_masks=None,
        rest_affix_specifier=None,
        talea_counts=None,
        talea_denominator=None,
        thread=None,
        time_treatments=None,
        tuplet_denominator=None,
        tuplet_force_fraction=None,
        ):
        assert len(selections) == len(collections)
        rhythm_maker = self._get_rhythm_maker(
            division_masks=division_masks,
            logical_tie_masks=logical_tie_masks,
            talea_counts=talea_counts,
            talea_denominator=talea_denominator,
            time_treatments=time_treatments,
            tuplet_denominator=tuplet_denominator,
            tuplet_force_fraction=tuplet_force_fraction,
            )
        length = len(selections)
        pattern = self.pattern or abjad.index_all()
        prototype = (abjad.Segment, abjad.Set, list)
        collections_, indices = [], []
        for index, collection in enumerate(collections):
            assert isinstance(collection, prototype), repr(collection)
            if isinstance(collection, (abjad.Set, set)):
                collection_ = list(sorted(collection))[:1]
            else:
                collection_ = collection
            if not pattern.matches_index(index, length):
                continue
            collections_.append(collection_)
            indices.append(index)
        if thread:
            stage_selections, state_manifest = rhythm_maker(
                collections_,
                rest_affix_specifier=rest_affix_specifier,
                )
        else:
            stage_selections = []
            total_collections = len(collections_)
            for collection_index, collection_ in enumerate(collections_):
                stage_selections_, stage_manifest = rhythm_maker(
                    [collection_],
                    rest_affix_specifier=rest_affix_specifier,
                    collection_index=collection_index,
                    total_collections=total_collections,
                    )
                stage_selections.extend(stage_selections_)
        triples = zip(indices, stage_selections, collections)
        for index, stage_selection, collection in triples:
            assert len(stage_selection) == 1, repr(stage_selection)
            if not isinstance(collection, (abjad.Set, set)):
                selections[index] = stage_selection
                continue
            assert len(stage_selection) == 1, repr(stage_selection)
            tuplet = stage_selection[0]
            assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
            agent = abjad.iterate(stage_selection)
            logical_ties = agent.logical_ties(pitched=True)
            logical_ties = list(logical_ties)
            assert len(logical_ties) == 1, repr(stage_selection)
            logical_tie = logical_ties[0]
            for note in logical_tie.leaves:
                assert isinstance(note, abjad.Note), repr(note)
                duration = note.written_duration
                pitches = collection
                chord = abjad.Chord(pitches, duration)
                abjad.mutate(note).replace([chord])
            selections[index] = stage_selection
        return selections

    def _get_rhythm_maker(
        self,
        division_masks=None,
        logical_tie_masks=None,
        talea_counts=None,
        talea_denominator=None,
        time_treatments=None,
        tuplet_denominator=None,
        tuplet_force_fraction=None,
        ):
        rhythm_maker = self.rhythm_maker
        if rhythm_maker is None:
            mask = rmakers.silence([0], 1, use_multimeasure_rests=True)
            rhythm_maker = rmakers.NoteRhythmMaker(division_masks=[mask])
        keywords = {}
        if division_masks is not None:
            keywords['division_masks'] = division_masks
        if logical_tie_masks is not None:
            keywords['logical_tie_masks'] = logical_tie_masks
        if talea_counts is not None:
            keywords['talea__counts'] = talea_counts
        if talea_denominator is not None:
            keywords['talea__denominator'] = talea_denominator
        if time_treatments is not None:
            keywords['time_treatments'] = time_treatments
        if keywords:
            rhythm_maker = abjad.new(rhythm_maker, **keywords)
        if (tuplet_denominator is not None or
            tuplet_force_fraction is not None):
            specifier = rhythm_maker.tuplet_specifier
            if specifier is None:
                specifier = rmakers.TupletSpecifier()
            specifier = abjad.new(
                specifier,
                denominator=tuplet_denominator,
                force_fraction=tuplet_force_fraction,
                )
            rhythm_maker = abjad.new(
                rhythm_maker,
                tuplet_specifier=specifier,
                )
        return rhythm_maker

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        """
        Gets pattern.

        Set to pattern or none.

        Defaults to none.

        Returns pattern or none.
        """
        return self._pattern

    @property
    def rhythm_maker(self):
        """
        Gets rhythm-maker.

        Set to rhythm-maker or none.

        Defaults to none.

        Returns rhythm-maker or music.
        """
        return self._rhythm_maker

class PitchFirstRhythmMaker(rmakers.RhythmMaker):
    r"""
    Collection rhythm-maker.

    >>> from abjadext import rmakers

    ..  container:: example

        Sixteenths and eighths:

        >>> rhythm_maker = baca.PitchFirstRhythmMaker(
        ...     talea=rmakers.Talea(
        ...         counts=[1, 1, 2],
        ...         denominator=16,
        ...         ),
        ...     )

        >>> collections = [[0, 2, 10, 8]]
        >>> selections, state = rhythm_maker(collections)
        >>> lilypond_file = rhythm_maker.show(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            {
                {   % measure
                    \time 5/16
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d'16
                        bf'8
                        af'16
                        ]
                    }
                }   % measure
            }

        >>> collections = [[18, 16, 15, 20, 19]]
        >>> selections, state = rhythm_maker(collections)
        >>> lilypond_file = rhythm_maker.show(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            {
                {   % measure
                    \time 3/8
                    \scaleDurations #'(1 . 1) {
                        fs''16
                        [
                        e''16
                        ef''8
                        af''16
                        g''16
                        ]
                    }
                }   % measure
            }

        >>> collections = [[9]]
        >>> selections, state = rhythm_maker(collections)
        >>> lilypond_file = rhythm_maker.show(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            {
                {   % measure
                    \time 1/16
                    \scaleDurations #'(1 . 1) {
                        a'16
                    }
                }   % measure
            }

        >>> collections = [[0, 2, 10, 8], [18, 16, 15, 20, 19], [9]]
        >>> selections, state = rhythm_maker(collections)
        >>> lilypond_file = rhythm_maker.show(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            {
                {   % measure
                    \time 13/16
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d'16
                        bf'8
                        af'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        fs''16
                        [
                        e''8
                        ef''16
                        af''16
                        g''8
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        a'16
                    }
                }   % measure
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_acciaccatura_specifiers',
        '_next_attack',
        '_next_segment',
        '_talea',
        '_time_treatments',
        )

    _state_variables = (
        '_next_attack',
        '_next_segment',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        acciaccatura_specifiers=None,
        beam_specifier=None,
        division_masks=None,
        duration_specifier=None,
        logical_tie_masks=None,
        talea=None,
        tie_specifier=None,
        time_treatments=None,
        tuplet_specifier=None,
        ):
        rmakers.RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_specifier=duration_specifier,
            division_masks=division_masks,
            logical_tie_masks=logical_tie_masks,
            tie_specifier=tie_specifier,
            tuplet_specifier=tuplet_specifier,
            )
        if acciaccatura_specifiers is not None:
            prototype = AcciaccaturaSpecifier
            for acciaccatura_specifier in acciaccatura_specifiers:
                assert isinstance(acciaccatura_specifier, prototype)
        self._acciaccatura_specifiers = acciaccatura_specifiers
        self._next_attack = 0
        self._next_segment = 0
        self._state = abjad.OrderedDict()
        talea = talea or rmakers.Talea()
        if not isinstance(talea, rmakers.Talea):
            raise TypeError(f'must be talea: {talea!r}.')
        self._talea = talea
        if time_treatments is not None:
            for time_treatment in time_treatments:
                if not self._is_time_treatment(time_treatment):
                    raise Exception(f'bad time treatment: {time_treatment!r}.')
        self._time_treatments = time_treatments

    ### SPECIAL METHODS ###

    def __call__(
        self,
        collections,
        collection_index=None,
        rest_affix_specifier=None,
        state=None,
        total_collections=None,
        ):
        r"""
        Calls rhythm-maker on ``collections``.

        ..  container:: example

            Without state manifest:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

            >>> abjad.f(rhythm_maker._make_state())
            abjad.OrderedDict(
                [
                    ('_next_attack', 9),
                    ('_next_segment', 3),
                    ]
                )

        ..  container:: example

            With state manifest:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> state = {'_next_attack': 2}
            >>> selections, state = rhythm_maker(
            ...     collections,
            ...     state=state,
            ...     )
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'8
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            e''16
                            ef''16
                            af''8
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                        }
                    }   % measure
                }

            >>> abjad.f(rhythm_maker._make_state())
            abjad.OrderedDict(
                [
                    ('_next_attack', 11),
                    ('_next_segment', 3),
                    ]
                )

        Returns selections together with state manifest.
        """
        self._state = state or abjad.OrderedDict()
        self._apply_state(state=state)
        selections = self._make_music(
            collections,
            rest_affix_specifier=rest_affix_specifier,
            collection_index=collection_index,
            total_collections=total_collections,
            )
        selections = self._apply_specifiers(selections)
        #self._check_wellformedness(selections)
        state = self._make_state()
        return selections, state

    ### PRIVATE METHODS ###

    @staticmethod
    def _add_rest_affixes(
        leaves,
        talea,
        rest_prefix,
        rest_suffix,
        affix_skips_instead_of_rests,
        decrease_durations,
        ):
        if rest_prefix:
            durations = [(_, talea.denominator) for _ in rest_prefix]
            maker = abjad.LeafMaker(
                decrease_monotonic=decrease_durations,
                skips_instead_of_rests=affix_skips_instead_of_rests,
                )
            leaves_ = maker([None], durations)
            leaves[0:0] = leaves_
        if rest_suffix:
            durations = [(_, talea.denominator) for _ in rest_suffix]
            maker = abjad.LeafMaker(
                decrease_monotonic=decrease_durations,
                skips_instead_of_rests=affix_skips_instead_of_rests,
                )
            leaves_ = maker([None], durations)
            leaves.extend(leaves_)
        return leaves

    def _apply_state(self, state=None):
        for name in self._state_variables:
            value = setattr(self, name, 0)
        state = state or {}
        assert isinstance(state, dict), repr(state)
        for key in state:
            value = state[key]
            setattr(self, key, value)

    @staticmethod
    def _fix_rounding_error(durations, total_duration):
        current_duration = sum(durations)
        if current_duration < total_duration:
            missing_duration = total_duration - current_duration
            if durations[0] < durations[-1]:
                durations[-1] += missing_duration
            else:
                durations[0] += missing_duration
        elif sum(durations) == total_duration:
            return durations
        elif total_duration < current_duration:
            extra_duration = current_duration - total_duration
            if durations[0] < durations[-1]:
                durations[-1] -= extra_duration
            else:
                durations[0] -= extra_duration
        assert sum(durations) == total_duration
        return durations

    def _get_acciaccatura_specifier(self, collection_index, total_collections):
        if not self.acciaccatura_specifiers:
            return
        for acciaccatura_specifier in self.acciaccatura_specifiers:
            pattern = acciaccatura_specifier._get_pattern()
            if pattern.matches_index(collection_index, total_collections):
                return acciaccatura_specifier

    def _get_talea(self):
        if self.talea is not None:
            return self.talea
        return rmakers.Talea()

    def _get_time_treatments(self):
        if not self.time_treatments:
            return abjad.CyclicTuple([0])
        return abjad.CyclicTuple(self.time_treatments)

    @staticmethod
    def _is_time_treatment(argument):
        if argument is None:
            return True
        elif isinstance(argument, int):
            return True
        elif isinstance(argument, str):
            return True
        elif isinstance(argument, abjad.Ratio):
            return True
        elif isinstance(argument, abjad.Multiplier):
            return True
        elif argument.__class__ is abjad.Duration:
            return True
        elif argument in ('accel', 'rit'):
            return True
        return False

    @classmethod
    def _make_accelerando(class_, leaf_selection, accelerando_indicator):
        assert accelerando_indicator in ('accel', 'rit')
        tuplet = abjad.Tuplet((1, 1), leaf_selection)
        if len(tuplet) == 1:
            return tuplet
        durations = [abjad.inspect(_).get_duration() for _ in leaf_selection]
        if accelerando_indicator == 'accel':
            exponent = 0.625
        elif accelerando_indicator == 'rit':
            exponent = 1.625
        multipliers = class_._make_accelerando_multipliers(durations, exponent)
        assert len(leaf_selection) == len(multipliers)
        for multiplier, leaf in zip(multipliers, leaf_selection):
            abjad.attach(multiplier, leaf)
        rhythm_maker_class = rmakers.AccelerandoRhythmMaker
        if rhythm_maker_class._is_accelerando(leaf_selection):
            abjad.override(leaf_selection[0]).beam.grow_direction = abjad.Right
        elif rhythm_maker_class._is_ritardando(leaf_selection):
            abjad.override(leaf_selection[0]).beam.grow_direction = abjad.Left
        duration = abjad.inspect(tuplet).get_duration()
        duration = abjad.Duration(duration)
        markup = duration.to_score_markup()
        markup = markup.scale((0.75, 0.75))
        abjad.override(tuplet).tuplet_number.text = markup
        return tuplet

    @classmethod
    def _make_accelerando_multipliers(class_, durations, exponent):
        r"""
        Makes accelerando multipliers.

        ..  container:: example

            Set exponent less than 1 for decreasing durations:

            >>> class_ = baca.PitchFirstRhythmMaker
            >>> durations = 4 * [abjad.Duration(1)]
            >>> result = class_._make_accelerando_multipliers(
            ...     durations,
            ...     0.5,
            ...     )
            >>> for multiplier in result: multiplier
            ...
            NonreducedFraction(2048, 1024)
            NonreducedFraction(848, 1024)
            NonreducedFraction(651, 1024)
            NonreducedFraction(549, 1024)

        ..  container:: example

            Set exponent to 1 for trivial multipliers:

            >>> class_ = baca.PitchFirstRhythmMaker
            >>> durations = 4 * [abjad.Duration(1)]
            >>> result = class_._make_accelerando_multipliers(durations, 1)
            >>> for multiplier in result: multiplier
            ...
            NonreducedFraction(1024, 1024)
            NonreducedFraction(1024, 1024)
            NonreducedFraction(1024, 1024)
            NonreducedFraction(1024, 1024)

        ..  container:: example

            Set exponent greater than 1 for increasing durations:

            >>> class_ = baca.PitchFirstRhythmMaker
            >>> durations = 4 * [abjad.Duration(1)]
            >>> result = class_._make_accelerando_multipliers(
            ...     durations,
            ...     0.5,
            ...     )
            >>> for multiplier in result: multiplier
            ...
            NonreducedFraction(2048, 1024)
            NonreducedFraction(848, 1024)
            NonreducedFraction(651, 1024)
            NonreducedFraction(549, 1024)

        Set exponent greater than 1 for ritardando.

        Set exponent less than 1 for accelerando.
        """
        pairs = abjad.mathtools.cumulative_sums_pairwise(durations)
        total_duration = pairs[-1][-1]
        start_offsets = [_[0] for _ in pairs]
        #print(total_duration, start_offsets)
        start_offsets = [_ / total_duration for _ in start_offsets]
        #print(total_duration, start_offsets)
        start_offsets_ = []
        rhythm_maker_class = rmakers.AccelerandoRhythmMaker
        for start_offset in start_offsets:
            start_offset_ = rhythm_maker_class._interpolate_exponential(
                0,
                total_duration,
                start_offset,
                exponent,
                )
            start_offsets_.append(start_offset_)
        #print(start_offsets_)
        #start_offsets_ = [float(total_duration * _) for _ in start_offsets_]
        start_offsets_.append(float(total_duration))
        durations_ = abjad.mathtools.difference_series(start_offsets_)
        durations_ = rhythm_maker_class._round_durations(durations_, 2**10)
        durations_ = class_._fix_rounding_error(durations_, total_duration)
        multipliers = []
        assert len(durations) == len(durations_)
        for duration_, duration in zip(durations_, durations):
            multiplier = duration_ / duration
            multiplier = abjad.Multiplier(multiplier)
            multiplier = multiplier.with_denominator(2**10)
            multipliers.append(multiplier)
        return multipliers

    def _make_music(
        self,
        collections,
        rest_affix_specifier=None,
        collection_index=None,
        total_collections=None,
        ):
        segment_count = len(collections)
        selections = []
        if collection_index is None:
            for i, segment in enumerate(collections):
                if rest_affix_specifier is not None:
                    result = rest_affix_specifier(i, segment_count)
                    rest_prefix, rest_suffix = result
                    affix_skips_instead_of_rests = \
                        rest_affix_specifier.skips_instead_of_rests
                else:
                    rest_prefix, rest_suffix = None, None
                    affix_skips_instead_of_rests = None
                selection = self._make_selection(
                    segment,
                    segment_count,
                    rest_prefix=rest_prefix,
                    rest_suffix=rest_suffix,
                    affix_skips_instead_of_rests=affix_skips_instead_of_rests,
                    )
                selections.append(selection)
        else:
            assert len(collections) == 1, repr(collections)
            segment = collections[0]
            if rest_affix_specifier is not None:
                result = rest_affix_specifier(collection_index, total_collections)
                rest_prefix, rest_suffix = result
                affix_skips_instead_of_rests = \
                    rest_affix_specifier.skips_instead_of_rests
            else:
                rest_prefix, rest_suffix = None, None
                affix_skips_instead_of_rests = None
            selection = self._make_selection(
                segment,
                segment_count,
                rest_prefix=rest_prefix,
                rest_suffix=rest_suffix,
                affix_skips_instead_of_rests=affix_skips_instead_of_rests,
                )
            selections.append(selection)
        beam_specifier = self._get_beam_specifier()
        beam_specifier(selections)
        selections = self._apply_division_masks(selections)
        specifier = self._get_duration_specifier()
        if specifier.rewrite_meter:
            #selections = specifier._rewrite_meter_(
            #    selections,
            #    input_divisions,
            #    )
            raise NotImplementedError()
        return selections

    def _make_selection(
        self,
        segment,
        segment_count,
        rest_prefix=None,
        rest_suffix=None,
        affix_skips_instead_of_rests=None,
        ):
        collection_index = self._next_segment
        acciaccatura_specifier = self._get_acciaccatura_specifier(
            collection_index,
            segment_count,
            )
        self._next_segment += 1
        if not segment:
            return abjad.Selection()
        talea = self._get_talea()
        leaves = []
        specifier = self._get_duration_specifier()
        decrease_durations = specifier.decrease_monotonic
        current_selection = self._next_segment - 1
        time_treatment = self._get_time_treatments()[current_selection]
        if time_treatment is None:
            time_treatment = 0
        grace_containers = None
        if acciaccatura_specifier is not None:
            grace_containers, segment = acciaccatura_specifier(segment)
            assert len(grace_containers) == len(segment)
        for pitch_expression in segment:
            prototype = abjad.NumberedPitchClass
            if isinstance(pitch_expression, prototype):
                pitch_expression = pitch_expression.number
            count = self._next_attack
            while talea[count] < 0:
                self._next_attack += 1
                duration = -talea[count]
                maker = abjad.LeafMaker(
                    decrease_monotonic=decrease_durations,
                    )
                leaves_ = maker([None], [duration])
                leaves.extend(leaves_)
                count = self._next_attack
            self._next_attack += 1
            duration = talea[count]
            assert 0 < duration, repr(duration)
            skips_instead_of_rests = False
            if (isinstance(pitch_expression, tuple) and
                len(pitch_expression) == 2 and
                pitch_expression[-1] in (None, 'skip')):
                multiplier = pitch_expression[0]
                duration = abjad.Duration(1, talea.denominator)
                duration *= multiplier
                if pitch_expression[-1] == 'skip':
                    skips_instead_of_rests = True
                pitch_expression = None
            maker = abjad.LeafMaker(
                decrease_monotonic=decrease_durations,
                skips_instead_of_rests=skips_instead_of_rests,
                )
            leaves_ = maker([pitch_expression], [duration])
            leaves.extend(leaves_)
            count = self._next_attack
            while talea[count] < 0 and not count % len(talea) == 0:
                self._next_attack += 1
                duration = -talea[count]
                maker = abjad.LeafMaker(
                    decrease_monotonic=decrease_durations,
                    )
                leaves_ = maker([None], [duration])
                leaves.extend(leaves_)
                count = self._next_attack
        leaves = self._add_rest_affixes(
            leaves,
            talea,
            rest_prefix,
            rest_suffix,
            affix_skips_instead_of_rests,
            decrease_durations,
            )
        leaf_selection = abjad.select(leaves)
        if isinstance(time_treatment, int):
            tuplet = self._make_tuplet_with_extra_count(
                leaf_selection,
                time_treatment,
                talea.denominator,
                )
        elif time_treatment in ('accel', 'rit'):
            tuplet = self._make_accelerando(leaf_selection, time_treatment)
        elif isinstance(time_treatment, abjad.Ratio):
            numerator, denominator = time_treatment.numbers
            multiplier = abjad.NonreducedFraction((denominator, numerator))
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
        elif isinstance(time_treatment, abjad.Multiplier):
            tuplet = abjad.Tuplet(time_treatment, leaf_selection)
        elif time_treatment.__class__ is abjad.Duration:
            tuplet_duration = time_treatment
            contents_duration = abjad.inspect(leaf_selection).get_duration()
            multiplier = tuplet_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
            if not tuplet.multiplier.normalized():
                tuplet.normalize_multiplier()
        else:
            raise Exception(f'bad time treatment: {time_treatment!r}.')
        assert isinstance(tuplet, abjad.Tuplet)
        if grace_containers is not None:
            logical_ties = abjad.iterate(tuplet).logical_ties()
            pairs = zip(grace_containers, logical_ties)
            for grace_container, logical_tie in pairs:
                if grace_container is None:
                    continue
                abjad.attach(
                    grace_container,
                    logical_tie.head,
                    tag='PFRM1',
                    )
        if tuplet.trivial():
            tuplet.hide = True
        selection = abjad.select([tuplet])
        return selection

    def _make_state(self):
        state = abjad.OrderedDict()
        for name in sorted(self._state_variables):
            value = getattr(self, name)
            state[name] = value
        return state

    @staticmethod
    def _make_tuplet_with_extra_count(
        leaf_selection,
        extra_count,
        denominator,
        ):
        contents_duration = abjad.inspect(leaf_selection).get_duration()
        contents_duration = contents_duration.with_denominator(denominator)
        contents_count = contents_duration.numerator
        if 0 < extra_count:
            extra_count %= contents_count
        elif extra_count < 0:
            extra_count = abs(extra_count)
            extra_count %= math.ceil(contents_count / 2.0)
            extra_count *= -1
        new_contents_count = contents_count + extra_count
        tuplet_multiplier = abjad.Multiplier(
            new_contents_count,
            contents_count,
            )
        if not tuplet_multiplier.normalized():
            message = f'{leaf_selection!r} gives {tuplet_multiplier}'
            message += ' with {contents_count} and {new_contents_count}.'
            raise Exception(message)
        tuplet = abjad.Tuplet(tuplet_multiplier, leaf_selection)
        return tuplet

    @staticmethod
    def _normalize_multiplier(multiplier):
        assert 0 < multiplier, repr(multiplier)
        while multiplier <= abjad.Multiplier(1, 2):
            multiplier *= 2
        while abjad.Multiplier(2) <= multiplier:
            multiplier /= 2
        return multiplier

    ### PUBLIC PROPERTIES ###

    @property
    def acciaccatura_specifiers(self):
        r"""
        Gets acciaccatura specifiers.

        ..  container:: example

            Graced quarters:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier()
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=4,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/2
                        \scaleDurations #'(1 . 1) {
                            c'4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16 [                                                                 %! ACC1
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16 ]                                                                   %! ACC1
                            }
                            c'4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16 [                                                                   %! ACC1
                                bf'16
                                fs''16
                                e''16 ]                                                                  %! ACC1
                            }
                            ef''4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16
                                c'16
                                d'16 ]                                                                   %! ACC1
                            }
                            bf'4
                        }
                    }   % measure
                }

        ..  container:: example

            Graced rests:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier()
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=4,
            ...         ),
            ...     )

            >>> collections = [
            ...     [None],
            ...     [0, None],
            ...     [2, 10, None],
            ...     [18, 16, 15, None],
            ...     [20, 19, 9, 0, None],
            ...     [2, 10, 18, 16, 15, None],
            ...     [20, 19, 9, 0, 2, 10, None],
            ...     ]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 7/4
                        \scaleDurations #'(1 . 1) {
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                c'16
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16 [                                                                   %! ACC1
                                bf'16 ]                                                                  %! ACC1
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16 [                                                                 %! ACC1
                                e''16
                                ef''16 ]                                                                 %! ACC1
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16
                                c'16 ]                                                                   %! ACC1
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16 [                                                                   %! ACC1
                                bf'16
                                fs''16
                                e''16
                                ef''16 ]                                                                 %! ACC1
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16 [                                                                 %! ACC1
                                g''16
                                a'16
                                c'16
                                d'16
                                bf'16 ]                                                                  %! ACC1
                            }
                            r4
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.acciaccatura_specifiers is None
            True

        Set to acciaccatura specifiers or none.

        Returns acciaccatura specifiers or none.
        """
        return self._acciaccatura_specifiers

    @property
    def beam_specifier(self):
        r"""
        Gets beam specifier.

        ..  container:: example

            Beams each division by default:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[1],
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Beams divisions together:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     beam_specifier=rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[1],
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).beam.positions = (-5.5, -5.5)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Beam.positions = #'(-5.5 . -5.5)
                }
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            c'16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            d'16
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            bf'8
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            fs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            e''16
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            ef''8
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            af''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            g''16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 0
                            a'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Beams nothing:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     beam_specifier=rmakers.BeamSpecifier(
            ...         beam_each_division=False,
            ...         ),
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[1],
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'16
                            d'16
                            bf'8
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16
                            e''16
                            ef''8
                            af''16
                            g''16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Does not beam rests:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[1],
            ...     )

            >>> collections = [[None, 2, 10], [18, 16, 15, 20, None], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            r16
                            d'16
                            [
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            ]
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Does beam rests:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     beam_specifier=rmakers.BeamSpecifier(
            ...         beam_rests=True,
            ...     ),
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[1],
            ...     )

            >>> collections = [[None, 2, 10], [18, 16, 15, 20, None], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            r16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            r16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Beams rests with stemlets:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     beam_specifier=rmakers.BeamSpecifier(
            ...         beam_rests=True,
            ...         stemlet_length=0.75,
            ...     ),
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[1],
            ...     )

            >>> collections = [[None, 2, 10], [18, 16, 15, 20, None], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            \override Staff.Stem.stemlet-length = 0.75
                            r16
                            [
                            d'16
                            \revert Staff.Stem.stemlet-length
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            \override Staff.Stem.stemlet-length = 0.75
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            \revert Staff.Stem.stemlet-length
                            r16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            \override Staff.Stem.stemlet-length = 0.75
                            \revert Staff.Stem.stemlet-length
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.beam_specifier is None
            True

        Set to beam specifier or none.

        Returns beam specifier or none.
        """
        return rmakers.RhythmMaker.beam_specifier.fget(self)

    @property
    def division_masks(self):
        r"""
        Gets division masks.

        ..  container:: example

            No division masks:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Silences every other division:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     division_masks=[
            ...         rmakers.silence([1], 2),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        r4.
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Sustains every other division:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     division_masks=[
            ...         rmakers.sustain([1], 2),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        c'4.
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.division_masks is None
            True

        Set to division masks or none.

        Returns tuple of division masks or none.
        """
        return rmakers.RhythmMaker.division_masks.fget(self)

    @property
    def duration_specifier(self):
        r"""
        Gets duration specifier.

        ..  container:: example

            Spells nonassignable durations with monontonically decreasing
            durations by default:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[4, 4, 5],
            ...         denominator=32,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 39/32
                        \scaleDurations #'(1 . 1) {
                            c'8
                            [
                            d'8
                            bf'8
                            ~
                            bf'32
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            e''8
                            ef''8
                            ~
                            ef''32
                            af''8
                            g''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                            ~
                            [
                            a'32
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Spells nonassignable durations with monontonically increasing
            durations:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     duration_specifier=rmakers.DurationSpecifier(
            ...         decrease_monotonic=False,
            ...         ),
            ...     talea=rmakers.Talea(
            ...         counts=[4, 4, 5],
            ...         denominator=32,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 39/32
                        \scaleDurations #'(1 . 1) {
                            c'8
                            [
                            d'8
                            bf'32
                            ~
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            e''8
                            ef''32
                            ~
                            ef''8
                            af''8
                            g''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'32
                            ~
                            [
                            a'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.duration_specifier is None
            True

        Set to duration specifier or none.

        Returns duration specifier or none.
        """
        return rmakers.RhythmMaker.duration_specifier.fget(self)

    @property
    def logical_tie_masks(self):
        r"""
        Gets logical tie masks.

        ..  container:: example

            Silences every third logical tie:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     logical_tie_masks=[
            ...         rmakers.silence([2], 3),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            ]
                            r8
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ]
                            r8
                            af''16
                            [
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            r8
                        }
                    }   % measure
                }

        ..  container:: example

            Silences first and last logical ties:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     logical_tie_masks=[
            ...         rmakers.silence([0]),
            ...         rmakers.silence([-1]),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            r16
                            d'16
                            [
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            r8
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.logical_tie_masks is None
            True

        Set to patterns or none.

        Returns tuple patterns or none.
        """
        return rmakers.RhythmMaker.logical_tie_masks.fget(self)

    @property
    def talea(self):
        r"""
        Gets talea.

        ..  container:: example

            With rests:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     beam_specifier=rmakers.BeamSpecifier(
            ...         beam_rests=True,
            ...         stemlet_length=1.5,
            ...         ),
            ...     talea=rmakers.Talea(
            ...         counts=[3, -1, 2, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/2
                        \scaleDurations #'(1 . 1) {
                            \override Staff.Stem.stemlet-length = 1.5
                            c'8.
                            [
                            r16
                            d'8
                            \revert Staff.Stem.stemlet-length
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \override Staff.Stem.stemlet-length = 1.5
                            fs''8.
                            [
                            r16
                            e''8
                            ef''8
                            af''8.
                            r16
                            \revert Staff.Stem.stemlet-length
                            g''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \override Staff.Stem.stemlet-length = 1.5
                            \revert Staff.Stem.stemlet-length
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            With very large nonassignable counts:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[29],
            ...         denominator=64,
            ...         ),
            ...     tie_specifier=rmakers.TieSpecifier(
            ...         repeat_ties=True,
            ...         ),
            ...     )

            >>> collections = [[0, 2]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 29/32
                        \scaleDurations #'(1 . 1) {
                            c'4..
                            c'64
                            \repeatTie
                            d'4..
                            d'64
                            \repeatTie
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to even sixteenths:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.talea
            Talea(counts=[1], denominator=16)

        Set to talea or none.

        Returns talea.
        """
        return self._talea

    @property
    def tie_specifier(self):
        r"""
        Gets tie specifier.

        ..  container:: example

            Ties across divisions with matching pitches:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     tie_specifier=rmakers.TieSpecifier(
            ...         tie_across_divisions=True,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [10, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ~
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            bf'16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Ties consecutive notes with matching pitches:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     tie_specifier=rmakers.TieSpecifier(
            ...         tie_consecutive_notes=True,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [10, 16, 16, 19, 19], [19]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ~
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            bf'16
                            [
                            e''16
                            ~
                            e''8
                            g''16
                            ~
                            g''16
                            ~
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            g''8
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.tie_specifier is None
            True

        Set to tie specifier or none.

        Returns tie specifier or none.
        """
        return rmakers.RhythmMaker.tie_specifier.fget(self)

    @property
    def time_treatments(self):
        r"""
        Gets time treatments.

        ..  container:: example

            One extra count per division:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=[1],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            One missing count per division:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=[-1],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 5/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Accelerandi:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=['accel'],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 5/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Ritardandi:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=['rit'],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 5/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Accelerandi followed by ritardandi:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=['accel', 'rit'],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0, 2],
            ...     [10, 18, 16, 15, 20],
            ...     [19, 9, 0, 2, 10, 18],
            ...     ]
            >>> selections, state = rhythm_maker(collections)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 5/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Mixed accelerandi, ritardandi and prolation:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=['accel', -2, 'rit'],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2],
            ...     [10, 18, 16, 15, 20],
            ...     [19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 5/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Specified by tuplet multiplier:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=[abjad.Ratio((3, 2))],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.override(staff).stem.direction = Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            c'8
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            d'8
                            [
                            bf'8
                            ]
                        }
                        \times 2/3 {
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            af''8
                            [
                            g''8
                            a'8
                            c'8
                            ]
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            d'8
                            [
                            bf'8
                            fs''8
                            e''8
                            ef''8
                            ]
                        }
                        \times 2/3 {
                            af''8
                            [
                            g''8
                            a'8
                            c'8
                            d'8
                            bf'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Segment durations equal to a quarter:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=[abjad.Duration(1, 4)],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     tuplet_specifier=rmakers.TupletSpecifier(
            ...         denominator=abjad.Duration(1, 16),
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.override(staff).stem.direction = Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                {
                    {   % measure
                        \time 3/2
                        \scaleDurations #'(1 . 1) {
                            c'4
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            ]
                        }
                        \times 4/6 {
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''16
                            [
                            g''16
                            a'16
                            c'16
                            ]
                        }
                        \times 4/5 {
                            d'16
                            [
                            bf'16
                            fs''16
                            e''16
                            ef''16
                            ]
                        }
                        \times 4/6 {
                            af''16
                            [
                            g''16
                            a'16
                            c'16
                            d'16
                            bf'16
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Segment durations alternating between a quarter and a dotted
            quarter:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=[abjad.Duration(1, 4), abjad.Duration(3, 8)],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=8,
            ...         ),
            ...     tuplet_specifier=rmakers.TupletSpecifier(
            ...         denominator=abjad.Duration(1, 16),
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2],
            ...     [10, 18, 16, 15, 20],
            ...     [19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.override(staff).stem.direction = Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                {
                    {   % measure
                        \time 15/8
                        \times 4/6 {
                            c'16
                            [
                            d'16
                            bf'8
                            fs''16
                            e''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            ef''8
                            [
                            af''16
                            g''16
                            a'8
                            c'16
                            ]
                        }
                        \times 4/7 {
                            d'16
                            [
                            bf'8
                            fs''16
                            e''16
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''16
                            [
                            g''16
                            a'8
                            c'16
                            d'16
                            ]
                        }
                        \times 4/7 {
                            bf'8
                            [
                            fs''16
                            e''16
                            ef''8
                            af''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            g''16
                            [
                            a'8
                            c'16
                            d'16
                            bf'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.time_treatments is None
            True

        Set to time treatments or none.

        Time treatments defined equal to integers; positive multipliers;
        positive durations; and the strings ``'accel'`` and ``'rit'``.

        Returns tuple of time treatments or none.
        """
        return self._time_treatments

    @property
    def tuplet_specifier(self):
        r"""
        Gets tuplet specifier.

        ..  container:: example

            Does not simplify redudant tuplets by default:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[3],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[-2],
            ...     )

            >>> collections = [[0, 2], [10, 18, 16], [15, 20], [19, 9, None]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                {
                    {   % measure
                        \time 11/8
                        \times 2/3 {
                            c'8.
                            [
                            d'8.
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/9 {
                            bf'8.
                            [
                            fs''8.
                            e''8.
                            ]
                        }
                        \times 2/3 {
                            ef''8.
                            [
                            af''8.
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/9 {
                            g''8.
                            [
                            a'8.
                            ]
                            r8.
                        }
                    }   % measure
                }

        ..  container:: example

            Trivializes tuplets:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[3],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[-2],
            ...     tuplet_specifier=rmakers.TupletSpecifier(
            ...         trivialize=True,
            ...         ),
            ...     )

            >>> collections = [[0, 2], [10, 18, 16], [15, 20], [19, 9, None]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                {
                    {   % measure
                        \time 11/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8
                            [
                            d'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/9 {
                            bf'8.
                            [
                            fs''8.
                            e''8.
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            ef''8
                            [
                            af''8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/9 {
                            g''8.
                            [
                            a'8.
                            ]
                            r8.
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.tuplet_specifier is None
            True

        Set to tuplet specifier or none.

        Returns tuplet specifier or none.
        """
        return rmakers.RhythmMaker.tuplet_specifier.fget(self)

    ### PUBLIC METHODS ###

    @staticmethod
    def show(selections, time_signatures=None):
        """
        Makes rhythm-maker-style LilyPond file for documentation examples.

        Returns LilyPond file.
        """
        return abjad.LilyPondFile.rhythm(
            selections,
            time_signatures=time_signatures,
            )

class RhythmCommand(evallib.Command):
    r"""
    Rhythm command.

    >>> from abjadext import rmakers

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (4, 8), (3,8), (4, 8)],
        ...     )

        >>> command = baca.RhythmCommand(
        ...     rhythm_maker=rmakers.EvenDivisionRhythmMaker(
        ...         tuplet_specifier=rmakers.TupletSpecifier(
        ...             extract_trivial=True,
        ...             ),
        ...         ),
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     command,
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
                            [
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
                            [
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
                            [
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
                            [
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
            <BLANKLINE>
                            \baca_unpitched_music_warning                                            %! SM24
                            c'8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_division_maker',
        '_division_expression',
        '_left_broken',
        '_multimeasure_rests',
        '_payload',
        '_persist',
        '_reference_meters',
        '_rewrite_meter',
        '_rewrite_rest_filled',
        '_rhythm_maker',
        '_right_broken',
        '_split_at_measure_boundaries',
        '_stages',
        '_state',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        division_maker: divisionlib.DivisionMaker = None,
        division_expression: abjad.Expression = None,
        left_broken: bool = None,
        multimeasure_rests: bool = None,
        persist: str = None,
        reference_meters: typing.Iterable[abjad.Meter] = None,
        rewrite_meter: bool = None,
        rewrite_rest_filled: bool = None,
        rhythm_maker: typings.RhythmMakerTyping = None,
        right_broken: bool = None,
        split_at_measure_boundaries: bool = None,
        stages: typing.Tuple[int, int] = None,
        ) -> None:
        evallib.Command.__init__(self)
        if division_expression is not None and division_maker is not None:
            message = 'can not set both division expression and division-maker'
            message += f':\n{division_expression} {division_maker}.'
            raise Exception(message)
        if division_maker is not None:
            assert isinstance(division_maker, divisionlib.division_maker_type), repr(division_maker)
        self._division_maker = division_maker
        if division_expression is not None:
            assert isinstance(division_expression, abjad.Expression)
        self._division_expression = division_expression
        if left_broken is not None:
            left_broken = bool(left_broken)
        self._left_broken = left_broken
        if multimeasure_rests is not None:
            multimeasure_rests = bool(multimeasure_rests)
        self._multimeasure_rests = multimeasure_rests
        if persist is not None:
            assert isinstance(persist, str), repr(persist)
        self._persist = persist
        if reference_meters is not None:
            assert isinstance(reference_meters, collections.Iterable)
            assert all(isinstance(_, abjad.Meter) for _ in reference_meters)
        self._reference_meters = reference_meters
        if rewrite_meter is not None:
            rewrite_meter = bool(rewrite_meter)
        self._rewrite_meter = rewrite_meter
        if rewrite_rest_filled is not None:
            rewrite_rest_filled = bool(rewrite_rest_filled)
        self._rewrite_rest_filled = rewrite_rest_filled
        self._check_rhythm_maker_input(rhythm_maker)
        self._rhythm_maker = rhythm_maker
        if right_broken is not None:
            right_broken = bool(right_broken)
        self._right_broken = right_broken
        if split_at_measure_boundaries is not None:
            split_at_measure_boundaries = bool(split_at_measure_boundaries)
        self._split_at_measure_boundaries = split_at_measure_boundaries
        if stages is not None:
            assert isinstance(stages, tuple), repr(stages)
            assert len(stages) == 2, repr(stages)
        self._stages = stages
        self._state: typing.Optional[abjad.OrderedDict] = None

    ### SPECIAL METHODS ###

    def __call__(
        self,
        start_offset: abjad.Offset = None,
        time_signatures: typing.Iterable[abjad.TimeSignature] = None,
        ) -> None:
        """
        Calls command on ``start_offset`` and ``time_signatures``.
        """
        music, start_offset = self._make_rhythm(start_offset, time_signatures)
        assert isinstance(music, (tuple, list, abjad.Voice))
        first_leaf = abjad.inspect(music).get_leaf(0)
        last_leaf = abjad.inspect(music).get_leaf(-1)
        pitched_prototype = (abjad.Note, abjad.Chord)
        payload = abjad.AnnotatedTimespan(
            start_offset=start_offset,
            stop_offset=None,
            annotation=music,
            )
        self._payload = payload

    ### PRIVATE METHODS ###

    @staticmethod
    def _annotate_unpitched_notes(argument):
        rest_prototype = (
            abjad.MultimeasureRest,
            abjad.Rest,
            abjad.Skip,
            )
        for leaf in abjad.iterate(argument).leaves():
            if isinstance(leaf, abjad.Chord):
                message = f'rhythm-makers make only notes and rests: {leaf!r}.'
                raise Exception(message)
            elif isinstance(leaf, abjad.Note):
                abjad.attach(abjad.tags.NOT_YET_PITCHED, leaf, tag=None)
            elif isinstance(leaf, rest_prototype):
                pass
            else:
                raise TypeError(leaf)

    def _apply_division_expression(
        self,
        divisions,
        ) -> typing.Optional[abjad.Sequence]:
        if self.division_expression is not None:
            divisions_ = self.division_expression(divisions)
            if not isinstance(divisions_, abjad.Sequence):
                message = 'division expression must return sequence:\n'
                message += f'  Input divisions:\n'
                message += f'    {divisions}\n'
                message += f'  Division expression:\n'
                message += f'    {self.division_expression}\n'
                message += f'  Output divisions:\n'
                message += f'    {divisions_}'
                raise Exception(message)
            divisions = divisions_
        return divisions

    def _check_rhythm_maker_input(self, rhythm_maker):
        if rhythm_maker is None:
            return
        prototype = (abjad.Selection, rmakers.RhythmMaker)
        if isinstance(rhythm_maker, prototype):
            return
        if not self._check_rhythm_maker_pattern_pairs(rhythm_maker):
            message = "\n  Input parameter 'rhythm_maker' accepts:"
            message += '\n    rhythm-maker'
            message += '\n    selection'
            message += '\n    sequence of (rhythm-maker-or-selection, pattern) pairs'
            message += '\n    none'
            message += "\n  Input parameter 'rhythm_maker' received:"
            message += f'\n    {format(rhythm_maker)}'
            raise Exception(message)

    def _check_rhythm_maker_pattern_pairs(self, pairs):
        if not isinstance(pairs, collections.Sequence): 
            return False
        prototype = (abjad.Selection, rmakers.RhythmMaker, type(self))
        for pair in pairs:
            if not isinstance(pair, tuple) or len(pair) != 2:
                return False
            if not isinstance(pair[0], prototype):
                return False
            if pair[1] is True:
                return True
            if not isinstance(pair[1], (list, tuple, abjad.Pattern)):
                return False
        return True

    @staticmethod
    def _durations_to_divisions(durations, start_offset):
        divisions = [divisionlib.Division(_) for _ in durations]
        durations = [_.duration for _ in divisions]
        start_offset = abjad.Offset(start_offset)
        durations.insert(0, start_offset)
        start_offsets = abjad.mathtools.cumulative_sums(durations)[1:-1]
        assert len(divisions) == len(start_offsets)
        divisions_ = []
        for division, start_offset in zip(divisions, start_offsets):
            division_ = divisionlib.Division(
                division,
                start_offset=start_offset,
                )
            divisions_.append(division_)
        assert not any(_.start_offset is None for _ in divisions_)
        return divisions_

    def _make_rhythm(self, start_offset, time_signatures):
        rhythm_maker = self.rhythm_maker
        literal_selections = False
        if rhythm_maker is None:
            mask = rmakers.silence([0], 1, use_multimeasure_rests=True)
            rhythm_maker = rmakers.NoteRhythmMaker(division_masks=[mask])
        if isinstance(rhythm_maker, abjad.Selection):
            selections = [rhythm_maker]
            literal_selections = True
        else:
            if isinstance(rhythm_maker, rmakers.RhythmMaker):
                pairs = [(rhythm_maker, abjad.index([0], 1))]
            else:
                pairs = list(rhythm_maker)
            assert self._check_rhythm_maker_pattern_pairs(pairs)
            division_maker = self.division_maker
            if division_maker is None:
                division_maker = divisionlib.DivisionMaker()
            divisions = self._durations_to_divisions(
                time_signatures,
                start_offset,
                )
            divisions = division_maker(divisions)
            divisions = Sequence(divisions).flatten(depth=-1)
            divisions = self._apply_division_expression(divisions)
            division_count = len(divisions)
            start_offset = divisions[0].start_offset
            labelled_divisions = []
            for i, division in enumerate(divisions):
                for pair in pairs:
                    rhythm_maker, pattern = pair
                    if pattern is True:
                        pattern = abjad.index([0], 1)
                    if isinstance(pattern, list):
                        indices = pattern
                        pattern = abjad.index(indices)
                    elif isinstance(pattern, tuple):
                        triple = slice(*pattern).indices(division_count)
                        indices = list(range(*triple))
                        pattern = abjad.index(indices)
                    if pattern.matches_index(i, division_count):
                        labelled_divisions.append((division, rhythm_maker))
                        break
                else:
                    raise Exception(f'no rhythm-maker for division {i}.')
            assert len(labelled_divisions) == len(divisions)
            labelled_divisions = Sequence(labelled_divisions)
            labelled_divisions = labelled_divisions.group_by(
                lambda pair: pair[1],
                )
            selections = []
            previous_segment_stop_state = self._previous_segment_stop_state()
            maker_to_state = abjad.OrderedDict()
            for subsequence in labelled_divisions:
                divisions_ = [pair[0] for pair in subsequence]
                rhythm_maker = subsequence[0][1]
                if isinstance(rhythm_maker, type(self)):
                    rhythm_maker = rhythm_maker.rhythm_maker
                    assert isinstance(rhythm_maker, rmakers.RhythmMaker)
                # TODO: eventually allow previous segment stop state
                #       and local stop state to work together
                if previous_segment_stop_state is None:
                    previous_state = maker_to_state.get(rhythm_maker, None)
                else:
                    previous_state = previous_segment_stop_state
                selections_ = rhythm_maker(
                    divisions_,
                    previous_state=previous_state,
                    )
                maker_to_state[rhythm_maker] = rhythm_maker.state
                selections.extend(selections_)
            self._state = rhythm_maker.state
        assert all(isinstance(_, abjad.Selection) for _ in selections)
        if self.split_at_measure_boundaries:
            specifier = rmakers.DurationSpecifier
            selections = specifier._split_at_measure_boundaries(
                selections,
                time_signatures,
                repeat_ties=self.repeat_ties,
                )
        assert all(isinstance(_, abjad.Selection) for _ in selections)
        if self.rewrite_meter:
            selections = rmakers.DurationSpecifier._rewrite_meter_(
                selections,
                time_signatures,
                reference_meters=self.reference_meters,
                rewrite_tuplets=False,
                repeat_ties=self.repeat_ties,
                )
        if self.rewrite_rest_filled:
            selections = rmakers.DurationSpecifier._rewrite_rest_filled_(
                selections,
                multimeasure_rests=self.multimeasure_rests,
                )
        self._tag_broken_ties(selections)
        if not literal_selections:
            self._annotate_unpitched_notes(selections)
        return selections, start_offset

    def _previous_segment_stop_state(self):
        previous_segment_stop_state = None
        dictionary = self.runtime.get('previous_segment_voice_metadata')
        if dictionary:
            previous_segment_stop_state = dictionary.get(abjad.tags.RHYTHM)
            if previous_segment_stop_state.get('name') != self.persist:
                previous_segment_stop_state = None
        return previous_segment_stop_state

    def _tag_broken_ties(self, selections):
        if not isinstance(self.rhythm_maker, rmakers.RhythmMaker):
            return
        if (self.left_broken and
            self.rhythm_maker.previous_state.get('incomplete_last_note')):
            if not self.repeat_ties:
                raise Exception('left-broken ties must be repeat ties.')
            first_leaf = abjad.select(selections).leaf(0)
            if isinstance(first_leaf, abjad.Note):
                abjad.attach(abjad.tags.LEFT_BROKEN_REPEAT_TIE_TO, first_leaf)
        if (self.right_broken and
            self.rhythm_maker.state.get('incomplete_last_note')):
            if self.repeat_ties:
                raise Exception('right-broken ties must be conventional.')
            last_leaf = abjad.select(selections).leaf(-1)
            if isinstance(last_leaf, abjad.Note):
                abjad.attach(abjad.tags.RIGHT_BROKEN_TIE_FROM, last_leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def division_expression(self) -> typing.Optional[abjad.Expression]:
        r"""
        Gets division expression.

        ..  container:: example

            Sums divisions:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(3, 8), (4, 8), (3, 8), (4, 8)],
            ...     )

            >>> command = baca.RhythmCommand(
            ...     division_expression=abjad.sequence().sum().sequence(),
            ...     rhythm_maker=rmakers.EvenDivisionRhythmMaker(
            ...         tuplet_specifier=rmakers.TupletSpecifier(
            ...             extract_trivial=True,
            ...             ),
            ...         ),
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     command,
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return self._division_expression

    @property
    def division_maker(self) -> typing.Optional[divisionlib.DivisionMakerTyping]:
        """
        Gets division-maker.
        """
        return self._division_maker

    @property
    def left_broken(self) -> typing.Optional[bool]:
        """
        Is true when rhythm is left-broken.

        Talea rhythm-maker knows how to tag incomplete last notes.
        """
        return self._left_broken

    @property
    def multimeasure_rests(self) -> typing.Optional[bool]:
        """
        Is true when command spells each rest-filled division as a
        single multimeasure rest.
        """
        return self._multimeasure_rests

    @property
    def parameter(self) -> str:
        """
        Gets persistence parameter.

        ..  container:: example

            >>> baca.RhythmCommand().parameter
            'RHYTHM'

        """
        return abjad.tags.RHYTHM

    @property
    def payload(self) -> abjad.AnnotatedTimespan:
        """
        Gets payload.
        """
        return self._payload

    @property
    def persist(self) -> typing.Optional[str]:
        """
        Gets persist name.
        """
        return self._persist

    @property
    def reference_meters(self) -> typing.Optional[
        typing.Iterable[abjad.Meter]
        ]:
        """
        Gets reference meters.

        Only used to rewrite meters.
        """
        return self._reference_meters

    @property
    def repeat_ties(self) -> typing.Optional[bool]:
        tie_specifier = getattr(self.rhythm_maker, 'tie_specifier', None)
        if tie_specifier is None:
            return False
        return tie_specifier.repeat_ties

    @property
    def rewrite_meter(self) -> typing.Optional[bool]:
        r"""
        Is true when command rewrites meter.

        ..  container:: example

            REGRESSION. All notes below are tagged unpitched (and colored
            gold), even tied notes resulting from meter rewriting:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(10, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_repeat_tied_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            \time 10/8                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 5/4
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4.
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4
                                \repeatTie
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4.
                                \repeatTie
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4
                                \repeatTie
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return self._rewrite_meter

    @property
    def rewrite_rest_filled(self) -> typing.Optional[bool]:
        """
        Is true when command rewrites rest-filled divisions.
        """
        return self._rewrite_rest_filled

    @property
    def rhythm_maker(self) -> typing.Optional[typings.RhythmMakerTyping]:
        r"""
        Gets rhythm-maker-or-selection or (rhythm-maker-or-selection, pattern)
        pairs.

        ..  container:: example

            Talea rhythm-maker remembers previous state across divisions:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=5 * [(4, 8)],
            ...     )

            >>> rhythm_maker_1 = rmakers.NoteRhythmMaker(
            ...     division_masks=[rmakers.silence([0], 1)],
            ...     )
            >>> rhythm_maker_2 = rmakers.TaleaRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[3, 4],
            ...         denominator=16,
            ...         ),
            ...     )
            >>> command = baca.RhythmCommand(
            ...     rhythm_maker=[
            ...         (rhythm_maker_1, [2]),
            ...         (rhythm_maker_2, True),
            ...         ],
            ...     )

            >>> label = abjad.label().with_durations(
            ...     direction=abjad.Down,
            ...     denominator=16,
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.label(label),
            ...     baca.text_script_font_size(-2),
            ...     baca.text_script_staff_padding(5),
            ...     command,
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 5]                                                    %! SM4
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            s1 * 1/2
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \override TextScript.font-size = #-2                                     %! OC1
                                \override TextScript.staff-padding = #5                                  %! OC1
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'16
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                                ~
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                _ \markup {
                                    \fraction
                                        2
                                        16
                                    }
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                r2
                                _ \markup {
                                    \fraction
                                        8
                                        16
                                    }
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'16
                                _ \markup {
                                    \fraction
                                        1
                                        16
                                    }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                <BLANKLINE>
                                % [MusicVoice measure 5]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'16
                                _ \markup {
                                    \fraction
                                        1
                                        16
                                    }
                                ]
                                \revert TextScript.font-size                                             %! OC2
                                \revert TextScript.staff-padding                                         %! OC2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Raises exception on invalid input:

            >>> command = baca.RhythmCommand(
            ...     rhythm_maker='text',
            ...     )
            Traceback (most recent call last):
                ...
            Exception:
              Input parameter 'rhythm_maker' accepts:
                rhythm-maker
                selection
                sequence of (rhythm-maker-or-selection, pattern) pairs
                none
              Input parameter 'rhythm_maker' received:
                text

        """
        return self._rhythm_maker

    @property
    def right_broken(self) -> typing.Optional[bool]:
        """
        Is true when rhythm is right-broken.

        Talea rhythm-maker knows how to tag incomplete last notes.
        """
        return self._right_broken

    @property
    def split_at_measure_boundaries(self) -> typing.Optional[bool]:
        """
        Is true when command splits at measure boundaries.
        """
        return self._split_at_measure_boundaries

    @property
    def stages(self) -> typing.Optional[typing.Tuple[int, int]]:
        """
        Gets stages.
        """
        return self._stages

    @property
    def state(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets postcall state of rhythm command.

        Populated by segment-maker.
        """
        return self._state

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

class TieCorrectionCommand(evallib.Command):
    """
    Tie correction command.

    ..  container:: example

        >>> baca.TieCorrectionCommand()
        TieCorrectionCommand(selector=baca.pleaf(-1))

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_repeat',
        '_untie',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: abjad.HorizontalAlignment = None,
        repeat: bool = None,
        selector: typings.Selector = 'baca.pleaf(-1)',
        untie: bool = None,
        ) -> None:
        evallib.Command.__init__(self, selector=selector)
        if direction is not None:
            assert direction in (abjad.Right, abjad.Left, None)
        self._direction = direction
        if repeat is not None:
            repeat = bool(repeat)
        self._repeat = repeat
        if untie is not None:
            untie = bool(untie)
        self._untie = untie

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Applies command to result of selector called on ``argument``.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = Selection(argument).leaves()
        for leaf in leaves:
            if self.untie is True:
                self._sever_tie(leaf, self.direction, self.repeat)
            else:
                self._add_tie(leaf, self.direction, self.repeat)

    ### PRIVATE METHODS ###

    @staticmethod
    def _add_tie(current_leaf, direction, repeat):
        assert direction in (abjad.Left, abjad.Right, None), repr(direction)
        left_broken, right_broken = None, None
        if direction is None:
            direction = abjad.Right
        current_tie = abjad.inspect(current_leaf).get_spanner(abjad.Tie)
        if direction == abjad.Right:
            next_leaf = abjad.inspect(current_leaf).get_leaf(1)
            if next_leaf is None:
                right_broken = True
                if current_tie is not None:
                    new_leaves = list(current_tie.leaves)
                    new_tie = abjad.new(current_tie)
                else:
                    new_leaves = [current_leaf]
                    new_tie = abjad.Tie(repeat=repeat)
            else:
                next_tie = abjad.inspect(next_leaf).get_spanner(abjad.Tie)
                if current_tie is not None and next_tie is not None:
                    if current_tie is next_tie:
                        return
                    else:
                        new_leaves = list(current_tie) + list(next_tie)
                        new_tie = abjad.new(current_tie)
                elif current_tie is not None and next_tie is None:
                    new_leaves = list(current_tie) + [next_leaf]
                    new_tie = abjad.new(current_tie)
                elif current_tie is None and next_tie is not None:
                    new_leaves = [current_leaf] + list(next_tie)
                    new_tie = abjad.Tie(repeat=repeat)
                else:
                    assert current_tie is None and next_tie is None
                    new_leaves = [current_leaf, next_leaf]
                    new_tie = abjad.Tie(repeat=repeat)
        else:
            assert direction == abjad.Left
            previous_leaf = abjad.inspect(current_leaf).get_leaf(-1)
            if previous_leaf is None:
                left_broken = True
                if current_tie is not None:
                    new_leaves = list(current_tie.leaves)
                    new_tie = abjad.new(current_tie, repeat=repeat)
                else:
                    new_leaves = [current_leaf]
                    new_tie = abjad.Tie(repeat=repeat)
            else:
                previous_tie = abjad.inspect(previous_leaf).get_spanner(
                    abjad.Tie)
                if previous_tie is not None and current_tie is not None:
                    if previous_tie is current_tie:
                        return
                    else:
                        new_leaves = list(previous_tie) + list(current_tie)
                        new_tie = abjad.new(previous_tie)
                elif previous_tie is not None and current_tie is None:
                    new_leaves = list(previous_tie) + [current_leaf]
                    new_tie = abjad.new(previous_tie)
                elif previous_tie is None and current_tie is not None:
                    new_leaves = [previous_leaf] + list(current_tie)
                    new_tie = abjad.Tie(repeat=repeat)
                else:
                    assert previous_tie is None and current_tie is None
                    new_leaves = [previous_leaf, current_leaf]
                    new_tie = abjad.Tie(repeat=repeat)
        new_leaves = abjad.select(new_leaves)
        for leaf in new_leaves:
            abjad.detach(abjad.Tie, leaf)
        new_tie = abjad.new(
            new_tie,
            left_broken=left_broken,
            right_broken=right_broken,
            )
        abjad.attach(new_tie, new_leaves, tag='TCC')

    @staticmethod
    def _sever_tie(current_leaf, direction, repeat):
        current_tie = abjad.inspect(current_leaf).get_spanner(abjad.Tie)
        if current_tie is None:
            return
        if direction is None:
            direction = abjad.Right
        leaf_index = current_tie.leaves.index(current_leaf)
        current_tie._fracture(leaf_index, direction=direction)
            
    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> typing.Optional[abjad.HorizontalAlignment]:
        """
        Gets direction.

        Interprets none equal to right.
        """
        return self._direction

    @property
    def repeat(self) -> typing.Optional[bool]:
        """
        Is true when newly created ties should be repeat ties.
        """
        return self._repeat

    @property
    def untie(self) -> typing.Optional[bool]:
        """
        Is true when command severs tie instead of creating tie.
        """
        return self._untie

### FACTORY FUNCTIONS ###

def make_even_divisions() -> RhythmCommand:
    """
    Makes even divisions.
    """
    return RhythmCommand(
        rhythm_maker=rmakers.EvenDivisionRhythmMaker(
            tuplet_specifier=rmakers.TupletSpecifier(
                extract_trivial=True,
                ),
            ),
        )

def make_fused_tuplet_monads(
    tuplet_ratio: typing.Tuple[int] = None,
    ) -> RhythmCommand:
    """
    Makes fused tuplet monads.
    """
    tuplet_ratios = []
    if tuplet_ratio is None:
        tuplet_ratios.append((1,))
    else:
        tuplet_ratios.append(tuplet_ratio)
    return RhythmCommand(
        division_expression=abjad.sequence()
            .sum()
            .sequence(),
        rhythm_maker=rmakers.TupletRhythmMaker(
            tie_specifier=rmakers.TieSpecifier(
                repeat_ties=True,
                ),
            tuplet_ratios=tuplet_ratios,
            tuplet_specifier=rmakers.TupletSpecifier(
                extract_trivial=True,
                rewrite_rest_filled=True,
                trivialize=True,
                ),
            ),
        )

def make_multimeasure_rests() -> RhythmCommand:
    """
    Makes multimeasure rests.
    """
    mask = rmakers.SilenceMask(
        pattern=abjad.index_all(),
        use_multimeasure_rests=True,
        )
    return RhythmCommand(
        rhythm_maker=rmakers.NoteRhythmMaker(
            division_masks=[mask],
            ),
        )

def make_notes(
    division_mask: mask_typing = None,
    repeat_ties: bool = False,
    ) -> RhythmCommand:
    """
    Makes notes; rewrites meter.
    """
    if division_mask is None:
        division_masks = None
    else:
        division_masks = [division_mask]
    tie_specifier = None
    if repeat_ties:
        tie_specifier = rmakers.TieSpecifier(repeat_ties=True)
    return RhythmCommand(
        rewrite_meter=True,
        rhythm_maker=rmakers.NoteRhythmMaker(
            division_masks=division_masks,
            tie_specifier=tie_specifier,
            )
        )

def make_repeat_tied_notes(
    division_mask: mask_typing = None,
    do_not_rewrite_meter: bool = None,
    ) -> RhythmCommand:
    """
    Makes repeat-tied notes; rewrites meter.
    """
    if division_mask is None:
        division_masks = None
    elif isinstance(division_mask, list):
        division_masks = division_mask[:]
    else:
        division_masks = [division_mask]
    return RhythmCommand(
        rewrite_meter=not(do_not_rewrite_meter),
        rhythm_maker=rmakers.NoteRhythmMaker(
            division_masks=division_masks,
            tie_specifier=rmakers.TieSpecifier(
                tie_across_divisions=True,
                repeat_ties=True,
                ),
            ),
        )

def make_repeated_duration_notes(
    durations: typing.Iterable,
    *,
    beam_specifier: rmakers.BeamSpecifier = None,
    division_mask: rmakers.Mask = None,
    do_not_rewrite_meter: bool = None,
    ) -> RhythmCommand:
    """
    Makes repeated-duration notes; rewrites meter.
    """
    if division_mask is None:
        division_masks = None
    else:
        division_masks = [division_mask]
    if isinstance(durations, abjad.Duration):
        durations = [durations]
    elif isinstance(durations, tuple):
        assert len(durations) == 2
        durations = [abjad.Duration(durations)]
    tie_specifier = rmakers.TieSpecifier(
        repeat_ties=True,
        )
    division_expression = divisionlib.split_by_durations(durations=durations)
    return RhythmCommand(
        division_expression=division_expression,
        rewrite_meter=not(do_not_rewrite_meter),
        rhythm_maker=rmakers.NoteRhythmMaker(
            beam_specifier=beam_specifier,
            division_masks=division_masks,
            tie_specifier=tie_specifier,
            ),
        )

def make_rests() -> RhythmCommand:
    """
    Makes rests.
    """
    return RhythmCommand(
        rhythm_maker=rmakers.NoteRhythmMaker(
            division_masks=[rmakers.silence([0], 1)],
            ),
        )

def make_rhythm(selection: abjad.Selection) -> RhythmCommand:
    """
    Sets rhythm to ``selection``.
    """
    assert isinstance(selection, abjad.Selection), repr(selection)
    assert all(isinstance(_,  abjad.Component) for _ in selection)
    return RhythmCommand(
        rhythm_maker=selection,
        )

def make_single_attack(duration) -> RhythmCommand:
    """
    Makes single attacks with ``duration``.
    """
    duration = abjad.Duration(duration)
    numerator, denominator = duration.pair
    rhythm_maker = rmakers.IncisedRhythmMaker(
        incise_specifier=rmakers.InciseSpecifier(
            fill_with_notes=False,
            outer_divisions_only=True,
            prefix_talea=[numerator],
            prefix_counts=[1],
            talea_denominator=denominator,
            ),
        )
    return RhythmCommand(
        rhythm_maker=rhythm_maker,
        )

def make_skips() -> RhythmCommand:
    """
    Makes skips.
    """
    return RhythmCommand(
        rhythm_maker=SkipRhythmMaker()
        )

def make_tied_notes() -> RhythmCommand:
    """
    Makes tied notes; rewrites meter.
    """
    return RhythmCommand(
        rewrite_meter=True,
        rhythm_maker=rmakers.NoteRhythmMaker(
            tie_specifier=rmakers.TieSpecifier(
                tie_across_divisions=True,
                ),
            ),
        )

def make_tied_repeated_durations(
    durations: typing.Iterable,
    ) -> RhythmCommand:
    """
    Makes tied repeated durations; does not rewrite meter.
    """
    command = make_repeated_duration_notes(durations)
    return abjad.new(
        command,
        rewrite_meter=False,
        rhythm_maker__tie_specifier__tie_across_divisions=True,
        )

def repeat_tie_from(
    *,
    selector: typings.Selector = 'baca.pleaf(-1)',
    ) -> TieCorrectionCommand:
    r"""
    Repeat-ties from leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     ignore_unpitched_notes=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_notes(),
        ...     baca.repeat_tie_from(selector=baca.leaf(1)),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            c'2
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            c'2
                            \repeatTie                                                               %! TCC
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return TieCorrectionCommand(
        repeat=True,
        selector=selector,
        )

def repeat_tie_to(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> TieCorrectionCommand:
    r"""
    Repeat-ties to leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     ignore_unpitched_notes=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_notes(),
        ...     baca.repeat_tie_to(selector=baca.leaf(2)),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            c'2
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            c'2
                            \repeatTie                                                               %! TCC
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return TieCorrectionCommand(
        direction=abjad.Left,
        repeat=True,
        selector=selector,
        )

def rhythm(
    rhythm_maker: typings.RhythmMakerTyping,
    *,
    division_maker: divisionlib.DivisionMaker = None,
    division_expression: abjad.Expression = None,
    left_broken: bool = None,
    multimeasure_rests: bool = None,
    persist: str = None,
    reference_meters: typing.Iterable[abjad.Meter] = None,
    rewrite_meter: bool = None,
    rewrite_rest_filled: bool = None,
    right_broken: bool = None,
    split_at_measure_boundaries: bool = None,
    stages: typing.Tuple[int, int] = None,
    ) -> RhythmCommand:
    """
    Makes rhythm command.
    """
    return RhythmCommand(
        division_maker=division_maker,
        division_expression=division_expression,
        left_broken=left_broken,
        multimeasure_rests=multimeasure_rests,
        persist=persist,
        reference_meters=reference_meters,
        rewrite_meter=rewrite_meter,
        rewrite_rest_filled=rewrite_rest_filled,
        rhythm_maker=rhythm_maker,
        right_broken=right_broken,
        split_at_measure_boundaries=split_at_measure_boundaries,
        stages=stages,
        )

def tie_from(
    *,
    selector: typings.Selector = 'baca.pleaf(-1)',
    ) -> TieCorrectionCommand:
    r"""
    Ties from leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     ignore_unpitched_notes=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_notes(),
        ...     baca.tie_from(selector=baca.leaf(1)),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            c'2
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            c'4.
                            ~                                                                        %! TCC
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            c'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return TieCorrectionCommand(
        repeat=False,
        selector=selector,
        )

def tie_to(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> TieCorrectionCommand:
    r"""
    Ties to leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     ignore_unpitched_notes=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_notes(),
        ...     baca.tie_to(selector=baca.leaf(1)),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            c'2
                            ~                                                                        %! TCC
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            c'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return TieCorrectionCommand(
        direction=abjad.Left,
        repeat=False,
        selector=selector,
        )

def untie_to(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> TieCorrectionCommand:
    r"""
    Unties to leaf.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     ignore_unpitched_notes=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_tied_notes(),
        ...     baca.untie_to(selector=baca.leaf(2)),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            c'2
                            ~
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            c'2
                            ~
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            c'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return TieCorrectionCommand(
        direction=abjad.Left,
        selector=selector,
        untie=True,
        )
