import abjad
import collections
import copy
import math
import typing
from abjadext import rmakers
from . import classes
from . import commands
from . import pitchcommands
from . import pitchclasses
from . import rhythmcommands
from . import scoping
from . import spannercommands
from . import typings

_commands = commands


### CLASSES ###


class AcciaccaturaSpecifier(object):
    r"""
    Acciaccatura specifier.

    >>> from abjadext import rmakers

    ..  container:: example

        Default acciaccatura specifier:

        >>> rhythm_maker = baca.PitchFirstCommand(
        ...     baca.pitch_first(
        ...         [1],
        ...         8,
        ...         acciaccatura=baca.AcciaccaturaSpecifier(),
        ...     ),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ...     ]
        >>> selections = rhythm_maker(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
        >>> score = lilypond_file[abjad.Score]
        >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
        >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override SpacingSpanner.strict-grace-spacing = ##f
                \override SpacingSpanner.strict-note-spacing = ##f
            }
            <<
                \new GlobalContext
                {
                    \time 3/4
                    s1 * 3/4
                }
                \new Staff
                {
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
                            fs''16
                            [                                                                        %! AcciaccaturaSpecifier
                            e''16
                            ]                                                                        %! AcciaccaturaSpecifier
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            af''16
                            [                                                                        %! AcciaccaturaSpecifier
                            g''16
                            a'16
                            ]                                                                        %! AcciaccaturaSpecifier
                        }
                        c'8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            d'16
                            [                                                                        %! AcciaccaturaSpecifier
                            bf'16
                            fs''16
                            e''16
                            ]                                                                        %! AcciaccaturaSpecifier
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            af''16
                            [                                                                        %! AcciaccaturaSpecifier
                            g''16
                            a'16
                            c'16
                            d'16
                            ]                                                                        %! AcciaccaturaSpecifier
                        }
                        bf'8
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_durations", "_lmr_specifier")

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        durations: typing.Sequence[abjad.DurationTyping] = None,
        lmr_specifier: "LMRSpecifier" = None,
    ) -> None:
        if durations is not None:
            assert isinstance(durations, list), repr(durations)
            durations = [abjad.Duration(_) for _ in durations]
        self._durations = durations
        if lmr_specifier is not None:
            prototype = LMRSpecifier
            assert isinstance(lmr_specifier, prototype)
        self._lmr_specifier = lmr_specifier

    ### SPECIAL METHODS ###

    def __call__(
        self, collection: typing.Union[list, abjad.Segment] = None
    ) -> typing.Tuple[
        typing.List[typing.Optional[abjad.AcciaccaturaContainer]], list
    ]:
        """
        Calls acciaccatura specifier on ``collection``.
        """
        prototype = (list, abjad.Segment)
        assert isinstance(collection, prototype), repr(collection)
        lmr_specifier = self._get_lmr_specifier()
        segment_parts = lmr_specifier(collection)
        segment_parts = [_ for _ in segment_parts if _]
        collection = [_[-1] for _ in segment_parts]
        durations = self._get_durations()
        acciaccatura_containers: typing.List[
            typing.Union[abjad.AcciaccaturaContainer, None]
        ] = []
        maker = abjad.LeafMaker()
        for segment_part in segment_parts:
            if len(segment_part) <= 1:
                acciaccatura_containers.append(None)
                continue
            grace_token = list(segment_part[:-1])
            grace_leaves = maker(grace_token, durations)
            acciaccatura_container = abjad.AcciaccaturaContainer(grace_leaves)
            if 1 < len(acciaccatura_container):
                abjad.beam(
                    acciaccatura_container[:], tag="AcciaccaturaSpecifier"
                )
            acciaccatura_containers.append(acciaccatura_container)
        assert len(acciaccatura_containers) == len(collection)
        assert isinstance(collection, list), repr(collection)
        return acciaccatura_containers, collection

    def __eq__(self, argument) -> bool:
        """
        Is true when initialization values are equal.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes with storage format manager.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __format__(self, format_specification="") -> str:
        """
        Formats with storage format manager.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_durations(self):
        return self.durations or [abjad.Duration(1, 16)]

    def _get_lmr_specifier(self):
        if self.lmr_specifier is not None:
            return self.lmr_specifier
        return LMRSpecifier()

    ### PUBLIC PROPERTIES ###

    @property
    def durations(self):
        r"""
        Gets durations.

        ..  container:: example

            Sixteenth-note acciaccaturas by default:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1],
            ...         8,
            ...         acciaccatura=baca.AcciaccaturaSpecifier(),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
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
                                fs''16
                                [                                                                        %! AcciaccaturaSpecifier
                                e''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! AcciaccaturaSpecifier
                                g''16
                                a'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! AcciaccaturaSpecifier
                                bf'16
                                fs''16
                                e''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! AcciaccaturaSpecifier
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            bf'8
                        }
                    }
                >>

        ..  container:: example

            Eighth-note acciaccaturas:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1],
            ...         8,
            ...         acciaccatura=baca.AcciaccaturaSpecifier(durations=[(1, 8)]),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
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
                                fs''8
                                [                                                                        %! AcciaccaturaSpecifier
                                e''8
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''8
                                [                                                                        %! AcciaccaturaSpecifier
                                g''8
                                a'8
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'8
                                [                                                                        %! AcciaccaturaSpecifier
                                bf'8
                                fs''8
                                e''8
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''8
                                [                                                                        %! AcciaccaturaSpecifier
                                g''8
                                a'8
                                c'8
                                d'8
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            bf'8
                        }
                    }
                >>

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

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1],
            ...         8,
            ...         acciaccatura=baca.AcciaccaturaSpecifier(),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
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
                                fs''16
                                [                                                                        %! AcciaccaturaSpecifier
                                e''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! AcciaccaturaSpecifier
                                g''16
                                a'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! AcciaccaturaSpecifier
                                bf'16
                                fs''16
                                e''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! AcciaccaturaSpecifier
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            bf'8
                        }
                    }
                >>


        ..  container:: example

            At most two acciaccaturas at the beginning of every collection:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1],
            ...         8,
            ...         acciaccatura=baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier(
            ...                 left_length=3,
            ...                 right_counts=[1],
            ...                 right_cyclic=True,
            ...                 ),
            ...             ),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
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
                                fs''16
                                [                                                                        %! AcciaccaturaSpecifier
                                e''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! AcciaccaturaSpecifier
                                g''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            a'8
                            [
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! AcciaccaturaSpecifier
                                bf'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! AcciaccaturaSpecifier
                                g''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            a'8
                            [
                            c'8
                            d'8
                            bf'8
                            ]
                        }
                    }
                >>

        ..  container:: example

            At most two acciaccaturas at the end of every collection:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1],
            ...         8,
            ...         acciaccatura=baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier(
            ...                 right_length=3,
            ...                 left_counts=[1],
            ...                 left_cyclic=True,
            ...                 ),
            ...             ),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
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
                                fs''16
                                [                                                                        %! AcciaccaturaSpecifier
                                e''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            \acciaccatura {
                                g''16
                                [                                                                        %! AcciaccaturaSpecifier
                                a'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            \acciaccatura {
                                fs''16
                                [                                                                        %! AcciaccaturaSpecifier
                                e''16
                                ]                                                                        %! AcciaccaturaSpecifier
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
                                c'16
                                [                                                                        %! AcciaccaturaSpecifier
                                d'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            bf'8
                            ]
                        }
                    }
                >>

        ..  container:: example

            At most two acciaccaturas at the beginning of every collection and
            then at most two acciaccaturas at the end of every collection:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1],
            ...         8,
            ...         acciaccatura=baca.AcciaccaturaSpecifier(
            ...              lmr_specifier=baca.LMRSpecifier(
            ...                 left_length=3,
            ...                 middle_counts=[1],
            ...                 middle_cyclic=True,
            ...                 right_length=3,
            ...                 ),
            ...             ),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 9/8
                        s1 * 9/8
                    }
                    \new Staff
                    {
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
                                fs''16
                                [                                                                        %! AcciaccaturaSpecifier
                                e''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! AcciaccaturaSpecifier
                                g''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            a'8
                            [
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! AcciaccaturaSpecifier
                                bf'16
                                ]                                                                        %! AcciaccaturaSpecifier
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
                                af''16
                                [                                                                        %! AcciaccaturaSpecifier
                                g''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            a'8
                            [
                            \acciaccatura {
                                c'16
                                [                                                                        %! AcciaccaturaSpecifier
                                d'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            bf'8
                            ]
                        }
                    }
                >>

        ..  container:: example

            As many acciaccaturas as possible in the middle of every
            collection:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1],
            ...         8,
            ...         acciaccatura=baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier(
            ...                 left_length=1,
            ...                 ),
            ...             ),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 11/8
                        s1 * 11/8
                    }
                    \new Staff
                    {
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
                                g''16
                                [                                                                        %! AcciaccaturaSpecifier
                                a'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            \acciaccatura {
                                bf'16
                                [                                                                        %! AcciaccaturaSpecifier
                                fs''16
                                e''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            \acciaccatura {
                                g''16
                                [                                                                        %! AcciaccaturaSpecifier
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            bf'8
                            ]
                        }
                    }
                >>

        Defaults to none.

        Set to LMR specifier or none.

        Returns LMR specifier or none.
        """
        return self._lmr_specifier


class AnchorSpecifier(object):
    """
    Anchor specifier.

    ..  container:: example

        >>> baca.AnchorSpecifier()
        AnchorSpecifier()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_figure_name",
        "_local_selector",
        "_remote_selector",
        "_remote_voice_name",
        "_use_remote_stop_offset",
    )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        figure_name: str = None,
        local_selector: abjad.SelectorTyping = None,
        remote_selector: abjad.SelectorTyping = None,
        remote_voice_name: str = None,
        use_remote_stop_offset: bool = None,
    ) -> None:
        # for selector evaluation:
        import baca

        if figure_name is not None:
            assert isinstance(figure_name, str), repr(figure_name)
        self._figure_name = figure_name
        if isinstance(local_selector, str):
            local_selector = eval(local_selector)
        if local_selector is not None and not isinstance(
            local_selector, abjad.Expression
        ):
            raise TypeError(f"must be selector: {local_selector!r}.")
        self._local_selector = local_selector
        if isinstance(remote_selector, str):
            remote_selector = eval(remote_selector)
        if remote_selector is not None and not isinstance(
            remote_selector, abjad.Expression
        ):
            raise TypeError(f"must be selector: {remote_selector!r}.")
        self._remote_selector = remote_selector
        if remote_voice_name is not None and not isinstance(
            remote_voice_name, str
        ):
            raise TypeError(f"must be string: {remote_voice_name!r}.")
        self._remote_voice_name = remote_voice_name
        if use_remote_stop_offset is not None:
            use_remote_stop_offset = bool(use_remote_stop_offset)
        self._use_remote_stop_offset = use_remote_stop_offset

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Formats Abjad object.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def figure_name(self):
        """
        Gets figure name.

        Returns strings or none.
        """
        return self._figure_name

    @property
    def local_selector(self):
        """
        Gets local selector.

        Returns selector or none.
        """
        return self._local_selector

    @property
    def remote_selector(self):
        """
        Gets remote selector.

        Returns selector or none.
        """
        return self._remote_selector

    @property
    def remote_voice_name(self):
        """
        Gets remote voice name.

        Set to string or none.

        Returns strings or none.
        """
        return self._remote_voice_name

    @property
    def use_remote_stop_offset(self):
        """
        Is true when contribution anchors to remote selection stop offset.

        Otherwise anchors to remote selection start offset.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        """
        return self._use_remote_stop_offset


class Coat(object):
    """
    Coat.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_argument",)

    ### INITIALIZER ###

    def __init__(self, argument: typing.Union[int, str, abjad.Pitch]) -> None:
        self._argument = argument

    ### PUBLIC PROPERTIES ###

    @property
    def argument(self) -> typing.Union[int, str, abjad.Pitch]:
        """
        Gets argument.
        """
        return self._argument


class Imbrication(object):
    r"""
    Imbrication command.

    >>> from abjadext import rmakers

    ..  container:: example

        Defaults:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([1], 16),
        ...     rmakers.beam_groups(),
        ...     baca.imbricate(
        ...         'Voice_1',
        ...         [2, 19, 9, 18, 16],
        ...         rmakers.beam_groups(),
        ...     ),
        ... )

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     ]
        >>> contribution = music_maker(
        ...     'Voice_2',
        ...     collections,
        ... )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 15/16
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16                                                                 %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                g''16                                                                %! baca.MusicMaker.__call__
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                a'16                                                                 %! baca.MusicMaker.__call__
                                ]
                                s16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                e''16                                                                %! baca.MusicMaker.__call__
                                ]
                                s16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                    \context Voice = "Voice_2"
                    {
                        \voiceTwo
                        {                                                                            %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16                                                                 %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16                                                                %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16                                                               %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16                                                                %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                ef''16                                                               %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16                                                               %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16                                                                %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16                                                                 %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                c'16                                                                 %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                d'16                                                                 %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16                                                                %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16                                                               %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16                                                                %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                ef''16                                                               %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    ..  container:: example

        Multiple imbricated voices:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([1], 16),
        ...     rmakers.beam_groups(),
        ...     baca.imbricate(
        ...         'Voice_1',
        ...         [2, 19, 9],
        ...         rmakers.beam_groups(beam_rests=True),
        ...         baca.staccato(selector=baca.pheads()),
        ...         ),
        ...     baca.imbricate(
        ...         'Voice_3',
        ...         [16, 10, 18],
        ...         rmakers.beam_groups(beam_rests=True),
        ...         baca.accent(selector=baca.pheads()),
        ...         ),
        ... )

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     ]
        >>> contribution = music_maker(
        ...     'Voice_2',
        ...     collections,
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 15/16
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16                                                                 %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16                                                                %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16                                                                 %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                s16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                    \context Voice = "Voice_2"
                    {
                        \voiceTwo
                        {                                                                            %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16                                                                 %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16                                                                %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16                                                               %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16                                                                %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                ef''16                                                               %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16                                                               %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16                                                                %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16                                                                 %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                c'16                                                                 %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                d'16                                                                 %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16                                                                %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16                                                               %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16                                                                %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                ef''16                                                               %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                    \context Voice = "Voice_3"
                    {
                        \voiceThree
                        {                                                                            %! baca.MusicMaker.__call__
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                [
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16                                                                %! baca.MusicMaker.__call__
                                - \accent                                                            %! baca.accent:IndicatorCommand
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16                                                                %! baca.MusicMaker.__call__
                                - \accent                                                            %! baca.accent:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16                                                               %! baca.MusicMaker.__call__
                                - \accent                                                            %! baca.accent:IndicatorCommand
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    ..  container:: example

        Hides tuplet brackets above imbricated voice:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([1], 16, time_treatments=[1]),
        ...     rmakers.beam_groups(beam_rests=True),
        ...     baca.imbricate(
        ...         'Voice_1',
        ...         [2, 19, 9, 18, 16],
        ...         baca.accent(selector=baca.pheads()),
        ...         rmakers.beam_groups(beam_rests=True),
        ...         ),
        ...     baca.staccato(selector=baca.pheads()),
        ... )

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     ]
        >>> contribution = music_maker(
        ...     'Voice_2',
        ...     collections,
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 9/8
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 6/5 {                                                             %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16                                                                 %! baca.MusicMaker.__call__
                                - \accent                                                            %! baca.accent:IndicatorCommand
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 6/5 {                                                             %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16                                                                %! baca.MusicMaker.__call__
                                - \accent                                                            %! baca.accent:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16                                                                 %! baca.MusicMaker.__call__
                                - \accent                                                            %! baca.accent:IndicatorCommand
                                s16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 6/5 {                                                             %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16                                                               %! baca.MusicMaker.__call__
                                - \accent                                                            %! baca.accent:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16                                                                %! baca.MusicMaker.__call__
                                - \accent                                                            %! baca.accent:IndicatorCommand
                                s16                                                                  %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                    \context Voice = "Voice_2"
                    {
                        \voiceTwo
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 6/5 {                                                             %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                c'16                                                                 %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16                                                                 %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16                                                                %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16                                                               %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16                                                                %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 6/5 {                                                             %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                ef''16                                                               %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16                                                               %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16                                                                %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16                                                                 %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                c'16                                                                 %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 6/5 {                                                             %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                d'16                                                                 %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16                                                                %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16                                                               %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16                                                                %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                ef''16                                                               %! baca.MusicMaker.__call__
                                - \staccato                                                          %! baca.staccato:IndicatorCommand
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_allow_unused_pitches",
        "_by_pitch_class",
        "_extend_beam",
        "_hocket",
        "_segment",
        "_selector",
        "_specifiers",
        "_truncate_ties",
        "_voice_name",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        voice_name: str = None,
        segment: typing.List[int] = None,
        *specifiers,
        allow_unused_pitches: bool = None,
        by_pitch_class: bool = None,
        extend_beam: bool = None,
        hocket: bool = None,
        selector: abjad.SelectorTyping = None,
        truncate_ties: bool = None,
    ) -> None:
        if voice_name is not None:
            assert isinstance(voice_name, str), repr(voice_name)
        self._voice_name = voice_name
        if segment is not None:
            assert isinstance(segment, list), repr(segment)
        self._segment = segment
        self._specifiers = specifiers
        if allow_unused_pitches is not None:
            allow_unused_pitches = bool(allow_unused_pitches)
        self._allow_unused_pitches = allow_unused_pitches
        if by_pitch_class is not None:
            by_pitch_class = bool(by_pitch_class)
        self._by_pitch_class = by_pitch_class
        if extend_beam is not None:
            extend_beam = bool(extend_beam)
        self._extend_beam = extend_beam
        if hocket is not None:
            hocket = bool(hocket)
        self._hocket = hocket
        if selector is not None:
            if not isinstance(selector, abjad.Expression):
                raise TypeError(f"selector or none only: {selector!r}.")
        self._selector = selector
        if truncate_ties is not None:
            truncate_ties = bool(truncate_ties)
        self._truncate_ties = truncate_ties

    ### SPECIAL METHODS ###

    def __call__(
        self, container: abjad.Container = None
    ) -> typing.Dict[str, abjad.Selection]:
        r"""
        Calls imbrication on ``container``.

        ..  container:: example

            Works with pitch-classes:

            >>> segment = [
            ...     abjad.NumberedPitchClass(10),
            ...     abjad.NumberedPitchClass(6),
            ...     abjad.NumberedPitchClass(4),
            ...     abjad.NumberedPitchClass(3),
            ...     ]
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([3], 16),
            ...     rmakers.beam(),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         segment,
            ...         baca.accent(selector=baca.pheads()),
            ...         rmakers.beam_groups(beam_rests=True),
            ...     ),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 27/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s8.                                                                  %! baca.MusicMaker.__call__
                                    [
                                    s8.                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    bf'8.                                                                %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    fs''8.                                                               %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    e''8.                                                                %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    ef''8.                                                               %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    s8.                                                                  %! baca.MusicMaker.__call__
                                    s8.                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s8.                                                                  %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'8.                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'8.                                                                 %! baca.MusicMaker.__call__
                                    bf'8.                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    fs''8.                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''8.                                                                %! baca.MusicMaker.__call__
                                    ef''8.                                                               %! baca.MusicMaker.__call__
                                    af''8.                                                               %! baca.MusicMaker.__call__
                                    g''8.                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a'8.                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Skips wrapped pitches:

            >>> segment = [
            ...     0,
            ...     baca.coat(10),
            ...     baca.coat(18),
            ...     10, 18,
            ...     ]
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam(),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         segment,
            ...         baca.accent(selector=baca.pheads()),
            ...         rmakers.beam_groups(beam_rests=True),
            ...     ),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
            ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 9/8
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    [
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Segment-maker allows for beam extension.

            Extends beam across figures:

            >>> voice_1_selections = []
            >>> voice_2_selections = []
            >>> time_signatures = []

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam_groups(),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [2, 10],
            ...         baca.staccato(selector=baca.pheads()),
            ...         rmakers.beam_groups(beam_rests=True),
            ...         extend_beam=True,
            ...     ),
            ... )
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     [[0, 2, 10, 18], [16, 15, 23]],
            ...     )
            >>> dictionary = contribution.voice_to_selection
            >>> voice_1_selections.append(dictionary['Voice_1'])
            >>> voice_2_selections.append(dictionary['Voice_2'])
            >>> time_signatures.append(contribution.time_signature)

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam_groups(),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [13, 9],
            ...         baca.staccato(selector=baca.pheads()),
            ...         rmakers.beam_groups(beam_rests=True),
            ...     ),
            ... )
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     [[19, 13, 9, 8]],
            ...     )
            >>> dictionary = contribution.voice_to_selection
            >>> voice_1_selections.append(dictionary['Voice_1'])
            >>> voice_2_selections.append(dictionary['Voice_2'])
            >>> time_signatures.append(contribution.time_signature)

            >>> maker = baca.SegmentMaker(
            ...     ignore_repeat_pitch_classes=True,
            ...     score_template=baca.TwoVoiceStaffScoreTemplate(),
            ...     spacing=baca.HorizontalSpacingSpecifier(
            ...         minimum_duration=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     ('Music_Voice_Two', 1),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=voice_2_selections[0],
            ...         ),
            ...     )
            >>> maker(
            ...     ('Music_Voice_Two', 2),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=voice_2_selections[1],
            ...         ),
            ...     )
            >>> maker(
            ...     ('Music_Voice_One', 1),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=voice_1_selections[0],
            ...         ),
            ...     )
            >>> maker(
            ...     ('Music_Voice_One', 2),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=voice_1_selections[1],
            ...         ),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                        {                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 7/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 7/16                                                                    %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 1/4                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/4                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                            \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                            s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                            \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                            \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                <BLANKLINE>
                        }                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                    >>                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                        \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                        <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                            \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                            {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                                {                                                                        %! baca.MusicMaker.__call__
                                    \override TupletBracket.stencil = ##f
                                    \override TupletNumber.stencil = ##f
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        % [Music_Voice_One measure 1]                                    %! _comment_measure_numbers
                                        s16                                                              %! baca.MusicMaker.__call__
                                        [
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        d'16                                                             %! baca.MusicMaker.__call__
                                        - \staccato                                                      %! baca.staccato:IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        bf'!16                                                           %! baca.MusicMaker.__call__
                                        - \staccato                                                      %! baca.staccato:IndicatorCommand
                <BLANKLINE>
                                        s16                                                              %! baca.MusicMaker.__call__
                <BLANKLINE>
                                    }                                                                    %! baca.MusicMaker.__call__
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        s16                                                              %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        s16                                                              %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        s16                                                              %! baca.MusicMaker.__call__
                <BLANKLINE>
                                    }                                                                    %! baca.MusicMaker.__call__
                                    \revert TupletBracket.stencil
                                    \revert TupletNumber.stencil
                <BLANKLINE>
                                }                                                                        %! baca.MusicMaker.__call__
                <BLANKLINE>
                                {                                                                        %! baca.MusicMaker.__call__
                                    \override TupletBracket.stencil = ##f
                                    \override TupletNumber.stencil = ##f
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        % [Music_Voice_One measure 2]                                    %! _comment_measure_numbers
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        s16                                                              %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        cs''!16                                                          %! baca.MusicMaker.__call__
                                        - \staccato                                                      %! baca.staccato:IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        a'16                                                             %! baca.MusicMaker.__call__
                                        - \staccato                                                      %! baca.staccato:IndicatorCommand
                <BLANKLINE>
                                        s16                                                              %! baca.MusicMaker.__call__
                                        ]
                <BLANKLINE>
                                    }                                                                    %! baca.MusicMaker.__call__
                                    \revert TupletBracket.stencil
                                    \revert TupletNumber.stencil
                <BLANKLINE>
                                }                                                                        %! baca.MusicMaker.__call__
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    \context Voice = "Music_Voice_One"                                   %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        % [Music_Voice_One measure 3]                                    %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                        c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    \context Voice = "Rest_Voice_One"                                    %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        % [Rest_Voice_One measure 3]                                     %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                            }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                            \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                            {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                                {                                                                        %! baca.MusicMaker.__call__
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        % [Music_Voice_Two measure 1]                                    %! _comment_measure_numbers
                                        \set stemLeftBeamCount = 0
                                        \set stemRightBeamCount = 2
                                        c'16                                                             %! baca.MusicMaker.__call__
                                        [
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        d'16                                                             %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        bf'!16                                                           %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        fs''!16                                                          %! baca.MusicMaker.__call__
                <BLANKLINE>
                                    }                                                                    %! baca.MusicMaker.__call__
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        e''16                                                            %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        ef''!16                                                          %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 0
                                        b''16                                                            %! baca.MusicMaker.__call__
                                        ]
                <BLANKLINE>
                                    }                                                                    %! baca.MusicMaker.__call__
                <BLANKLINE>
                                }                                                                        %! baca.MusicMaker.__call__
                <BLANKLINE>
                                {                                                                        %! baca.MusicMaker.__call__
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        % [Music_Voice_Two measure 2]                                    %! _comment_measure_numbers
                                        \set stemLeftBeamCount = 0
                                        \set stemRightBeamCount = 2
                                        g''16                                                            %! baca.MusicMaker.__call__
                                        [
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        cs''!16                                                          %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        a'16                                                             %! baca.MusicMaker.__call__
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 0
                                        af'!16                                                           %! baca.MusicMaker.__call__
                                        ]
                <BLANKLINE>
                                    }                                                                    %! baca.MusicMaker.__call__
                <BLANKLINE>
                                }                                                                        %! baca.MusicMaker.__call__
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    \context Voice = "Music_Voice_Two"                                   %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        % [Music_Voice_Two measure 3]                                    %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                        c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        % [Rest_Voice_Two measure 3]                                     %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                            }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                        >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                    >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

        ..  container:: example

            Works with chords:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam_groups(),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [2, 19, 9, 18, 16],
            ...         rmakers.beam_groups(),
            ...     ),
            ... )

            >>> collections = [
            ...     {0, 2, 10, 18, 16},
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     collections,
            ... )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 11/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    ]
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    <c' d' bf' e'' fs''>16
                                    [
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Works with rests:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first(
            ...         [1],
            ...         16,
            ...         affix=baca.rests_around([2], [2]),
            ...     ),
            ...     rmakers.beam_groups(),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [2, 19, 9, 18, 16],
            ...         rmakers.beam_groups(),
            ...     ),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 19/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s8                                                                   %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    ]
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s8                                                                   %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    r8                                                                   %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16                                                                %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    ]
                                    r8                                                                   %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        """
        original_container = container
        container = copy.deepcopy(container)
        abjad.override(container).tuplet_bracket.stencil = False
        abjad.override(container).tuplet_number.stencil = False
        segment = classes.Sequence(self.segment).flatten(depth=-1)
        if self.by_pitch_class:
            segment = [abjad.NumberedPitchClass(_) for _ in segment]
        cursor = classes.Cursor(
            singletons=True, source=segment, suppress_exception=True
        )
        pitch_number = cursor.next()
        if self.selector is not None:
            selection = self.selector(original_container)
        selected_logical_ties = None
        if self.selector is not None:
            selection = self.selector(container)
            agent = abjad.iterate(selection)
            selected_logical_ties = agent.logical_ties(pitched=True)
            selected_logical_ties = list(selected_logical_ties)
        selector = abjad.select(original_container)
        original_logical_ties = selector.logical_ties()
        logical_ties = abjad.select(container).logical_ties()
        pairs = zip(logical_ties, original_logical_ties)
        for logical_tie, original_logical_tie in pairs:
            if (
                selected_logical_ties is not None
                and logical_tie not in selected_logical_ties
            ):
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(leaf).replace([skip])
            elif isinstance(logical_tie.head, abjad.Rest):
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(leaf).replace([skip])
            elif isinstance(logical_tie.head, abjad.Skip):
                pass
            elif self._matches_pitch(logical_tie.head, pitch_number):
                if isinstance(pitch_number, Coat):
                    for leaf in logical_tie:
                        duration = leaf.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(leaf).replace([skip])
                    pitch_number = cursor.next()
                    continue
                self._trim_matching_chord(logical_tie, pitch_number)
                pitch_number = cursor.next()
                if self.truncate_ties:
                    head = logical_tie.head
                    tail = logical_tie.tail
                    for leaf in logical_tie[1:]:
                        duration = leaf.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(leaf).replace([skip])
                    abjad.detach(abjad.Tie, head)
                    next_leaf = abjad.inspect(tail).leaf(1)
                    if next_leaf is not None:
                        abjad.detach(abjad.RepeatTie, next_leaf)
                if self.hocket:
                    for leaf in original_logical_tie:
                        duration = leaf.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(leaf).replace([skip])
            else:
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(leaf).replace([skip])
        if not self.allow_unused_pitches and not cursor.is_exhausted:
            current, total = cursor.position - 1, len(cursor)
            message = f"{cursor!r} used only {current} of {total} pitches."
            raise Exception(message)
        self._apply_specifiers(container)
        if self.extend_beam:
            final_leaf = abjad.select(container).leaf(-1)
            abjad.attach(abjad.tags.RIGHT_BROKEN_BEAM, final_leaf)
        selection = abjad.select(container)
        if not self.hocket:
            pleaves = classes.Selection(container).pleaves()
            assert isinstance(pleaves, abjad.Selection)
            for pleaf in pleaves:
                abjad.attach(abjad.tags.ALLOW_OCTAVE, pleaf)
        return {self.voice_name: selection}

    ### PRIVATE METHODS ###

    def _apply_specifiers(self, container):
        assert isinstance(container, abjad.Container), repr(container)
        nested_selections = None
        specifiers = self.specifiers or []
        selections = container[:]
        for specifier in specifiers:
            if isinstance(specifier, PitchFirstAssignment):
                continue
            if isinstance(specifier, rhythmcommands.RhythmCommand):
                continue
            if isinstance(specifier, Imbrication):
                continue
            prototype = (
                rmakers.BeamCommand,
                rmakers.FeatherBeamCommand,
                rmakers.BeamGroupsCommand,
                rmakers.UnbeamCommand,
            )
            if isinstance(specifier, prototype):
                rmakers.unbeam()(selections)
            if isinstance(specifier, Nesting):
                nested_selections = specifier(selections)
            else:
                specifier(selections)
        if nested_selections is not None:
            return nested_selections
        return selections

    @staticmethod
    def _matches_pitch(pitched_leaf, pitch_object):
        if isinstance(pitch_object, Coat):
            pitch_object = pitch_object.argument
        if pitch_object is None:
            return False
        if isinstance(pitched_leaf, abjad.Note):
            written_pitches = [pitched_leaf.written_pitch]
        elif isinstance(pitched_leaf, abjad.Chord):
            written_pitches = pitched_leaf.written_pitches
        else:
            raise TypeError(pitched_leaf)
        if isinstance(pitch_object, (int, float)):
            source = [_.number for _ in written_pitches]
        elif isinstance(pitch_object, abjad.NamedPitch):
            source = written_pitches
        elif isinstance(pitch_object, abjad.NumberedPitch):
            source = [abjad.NumberedPitch(_) for _ in written_pitches]
        elif isinstance(pitch_object, abjad.NamedPitchClass):
            source = [abjad.NamedPitchClass(_) for _ in written_pitches]
        elif isinstance(pitch_object, abjad.NumberedPitchClass):
            source = [abjad.NumberedPitchClass(_) for _ in written_pitches]
        else:
            raise TypeError(f"unknown pitch object: {pitch_object!r}.")
        if not type(source[0]) is type(pitch_object):
            raise TypeError(f"{source!r} type must match {pitch_object!r}.")
        return pitch_object in source

    @staticmethod
    def _trim_matching_chord(logical_tie, pitch_object):
        if isinstance(logical_tie.head, abjad.Note):
            return
        assert isinstance(logical_tie.head, abjad.Chord), repr(logical_tie)
        if isinstance(pitch_object, abjad.PitchClass):
            raise NotImplementedError(logical_tie, pitch_object)
        for chord in logical_tie:
            duration = chord.written_duration
            note = abjad.Note(pitch_object, duration)
            abjad.mutate(chord).replace([note])

    ### PUBLIC PROPERTIES ###

    @property
    def allow_unused_pitches(self):
        r"""
        Is true when specifier allows unused pitches.

        ..  container:: example

            Allows unused pitches:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam_groups(beam_rests=True),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [2, 19, 9, 18, 16],
            ...         baca.accent(selector=baca.pheads()),
            ...         rmakers.beam_groups(beam_rests=True),
            ...         allow_unused_pitches=True,
            ...     ),
            ...     baca.staccato(selector=baca.pheads()),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 5/8
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example exception

            Raises exception on unused pitches:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam_groups(beam_rests=True),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [2, 19, 9, 18, 16],
            ...         baca.accent(selector=baca.pheads()),
            ...         rmakers.beam_groups(beam_rests=True),
            ...     ),
            ...     baca.staccato(selector=baca.pheads()),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     ]
            >>> result = music_maker(
            ...     'Voice_2',
            ...     collections,
            ...     )
            Traceback (most recent call last):
                ...
            Exception: Cursor(source=Sequence(items=(2, 19, 9, 18, 16)),
            position=4, singletons=True, suppress_exception=True) used only 3
            of 5 pitches.

        ..  container:: example

            Defaults to none:

            >>> specifier = baca.Imbrication()
            >>> specifier.allow_unused_pitches is None
            True

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._allow_unused_pitches

    @property
    def by_pitch_class(self):
        """
        Is true when specifier matches on pitch-class rather than pitch.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        """
        return self._by_pitch_class

    @property
    def extend_beam(self):
        """
        Is true when specifier extends beam.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._extend_beam

    @property
    def hocket(self):
        r"""
        Is true when specifier hockets voices.

        ..  container:: example

            Hockets voices:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam_groups(beam_rests=True),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [2, 19, 9, 18, 16],
            ...         baca.accent(selector=baca.pheads()),
            ...         rmakers.beam_groups(beam_rests=True),
            ...         hocket=True,
            ...     ),
            ...     baca.staccato(selector=baca.pheads()),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 15/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    [
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Defaults to none:

            >>> specifier = baca.Imbrication()
            >>> specifier.hocket is None
            True

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._hocket

    @property
    def segment(self):
        """
        Gets to-be-imbricated segment.

        Returns pitch or pitch-class segment.
        """
        return self._segment

    @property
    def selector(self):
        r"""
        Gets selector.

        ..  container:: example

            Selects last nine notes:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam_groups(beam_rests=True),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [2, 18, 16, 15],
            ...         baca.accent(selector=baca.pheads()),
            ...         rmakers.beam_groups(beam_rests=True),
            ...         selector=baca.plts()[-9:],
            ...     ),
            ...     baca.staccato(selector=baca.pheads()),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
            ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 9/8
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    [
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    - \accent                                                            %! baca.accent:IndicatorCommand
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    - \staccato                                                          %! baca.staccato:IndicatorCommand
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Defaults to none:

            >>> specifier = baca.Imbrication()
            >>> specifier.selector is None
            True

        Set to selector or none.

        Returns selector or none.
        """
        return self._selector

    @property
    def specifiers(self):
        r"""
        Gets specifiers.

        ..  container:: example

            Beams nothing:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [2, 19, 9, 18, 16],
            ...     ),
            ...     rmakers.beam_groups(),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 15/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16                                                                %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Beams divisions together but excludes skips:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam_groups(),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [2, 19, 9, 18, 16],
            ...         rmakers.beam_groups(),
            ...     ),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     collections,
            ... )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 15/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    ]
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16                                                                %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Beams divisions together and includes skips:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam_groups(),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [2, 19, 9, 18, 16],
            ...         rmakers.beam_groups(beam_rests=True),
            ...     ),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 15/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16                                                                %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Beams each division and includes skips:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam_groups(),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [2, 19, 9, 18, 16],
            ...         rmakers.beam(beam_rests=True),
            ...     ),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     collections,
            ... )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 15/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    [
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    [
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    s16                                                                  %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16                                                                %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Beams each division by default:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1, 1, 2], 16, time_treatments=[1]),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                <<
                    \new GlobalContext
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            Beams divisions together:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1, 1, 2], 16, time_treatments=[1]),
            ...     rmakers.beam_groups(abjad.select().tuplets()),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).beam.positions = (-5.5, -5.5)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Beam.positions = #'(-5.5 . -5.5)
                }
                <<
                    \new GlobalContext
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                    \new Staff
                    {
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
                            \set stemRightBeamCount = 1
                            a'8
                            ]
                        }
                    }
                >>

        ..  container:: example

            Beams nothing:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1, 1, 2], 16, time_treatments=[1]),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            Does not beam rests:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1, 1, 2], 16, time_treatments=[1]),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[None, 2, 10], [18, 16, 15, 20, None], [9]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                <<
                    \new GlobalContext
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            Does beam rests:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1, 1, 2], 16, time_treatments=[1]),
            ...     rmakers.beam(beam_rests=True),
            ... )

            >>> collections = [[None, 2, 10], [18, 16, 15, 20, None], [9]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                <<
                    \new GlobalContext
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            Beams rests with stemlets:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1, 1, 2], 16, time_treatments=[1]),
            ...     rmakers.beam(
            ...         beam_rests=True,
            ...         stemlet_length=0.75,
            ...     ),
            ... )

            >>> collections = [[None, 2, 10], [18, 16, 15, 20, None], [9]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                <<
                    \new GlobalContext
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                    \new Staff
                    {
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
                            a'8
                        }
                    }
                >>

        Returns specifiers or none.
        """
        return list(self._specifiers)

    @property
    def truncate_ties(self):
        r"""
        Is true when specifier truncates ties.

        ..  container:: example

            Truncates ties:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([5], 32),
            ...     rmakers.beam(),
            ...     baca.imbricate(
            ...         'Voice_1',
            ...         [2, 10, 18, 19, 9],
            ...         rmakers.beam_groups(beam_rests=True),
            ...         truncate_ties=True,
            ...     ),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice_2',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 45/32
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    s8                                                                   %! baca.MusicMaker.__call__
                                    [
                                    s32                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    d'8                                                                  %! baca.MusicMaker.__call__
                                    s32                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    bf'8                                                                 %! baca.MusicMaker.__call__
                                    s32                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    fs''8                                                                %! baca.MusicMaker.__call__
                                    s32                                                                  %! baca.MusicMaker.__call__
                                    s8                                                                   %! baca.MusicMaker.__call__
                                    s32                                                                  %! baca.MusicMaker.__call__
                                    s8                                                                   %! baca.MusicMaker.__call__
                                    s32                                                                  %! baca.MusicMaker.__call__
                                    s8                                                                   %! baca.MusicMaker.__call__
                                    s32                                                                  %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    g''8                                                                 %! baca.MusicMaker.__call__
                                    s32                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    a'8                                                                  %! baca.MusicMaker.__call__
                                    s32                                                                  %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                        \context Voice = "Voice_2"
                        {
                            \voiceTwo
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'8                                                                  %! baca.MusicMaker.__call__
                                    ~
                                    [
                                    c'32                                                                 %! baca.MusicMaker.__call__
                                    d'8                                                                  %! baca.MusicMaker.__call__
                                    ~
                                    d'32                                                                 %! baca.MusicMaker.__call__
                                    bf'8                                                                 %! baca.MusicMaker.__call__
                                    ~
                                    bf'32                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    fs''8                                                                %! baca.MusicMaker.__call__
                                    ~
                                    [
                                    fs''32                                                               %! baca.MusicMaker.__call__
                                    e''8                                                                 %! baca.MusicMaker.__call__
                                    ~
                                    e''32                                                                %! baca.MusicMaker.__call__
                                    ef''8                                                                %! baca.MusicMaker.__call__
                                    ~
                                    ef''32                                                               %! baca.MusicMaker.__call__
                                    af''8                                                                %! baca.MusicMaker.__call__
                                    ~
                                    af''32                                                               %! baca.MusicMaker.__call__
                                    g''8                                                                 %! baca.MusicMaker.__call__
                                    ~
                                    g''32                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a'8                                                                  %! baca.MusicMaker.__call__
                                    ~
                                    [
                                    a'32                                                                 %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Defaults to none:

            >>> specifier = baca.Imbrication()
            >>> specifier.truncate_ties is None
            True

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._truncate_ties

    @property
    def voice_name(self):
        """
        Gets voice name.

        Returns string.
        """
        return self._voice_name


class LMRSpecifier(object):
    """
    Left-middle-right specifier.

    ..  container:: example

        Default LMR specifier:

        >>> lmr_specifier = baca.LMRSpecifier()

        >>> parts = lmr_specifier([1])
        >>> for part in parts: part
        Sequence([1])

        >>> parts =lmr_specifier([1, 2])
        >>> for part in parts: part
        Sequence([1, 2])

        >>> parts = lmr_specifier([1, 2, 3])
        >>> for part in parts: part
        Sequence([1, 2, 3])

        >>> parts = lmr_specifier([1, 2, 3, 4])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4])

        >>> parts = lmr_specifier([1, 2, 3, 4, 5])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5])

        >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5, 6])

        >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5, 6, 7])

        >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5, 6, 7, 8])

        >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5, 6, 7, 8, 9])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_left_counts",
        "_left_cyclic",
        "_left_length",
        "_left_reversed",
        "_middle_counts",
        "_middle_cyclic",
        "_middle_reversed",
        "_priority",
        "_right_counts",
        "_right_cyclic",
        "_right_length",
        "_right_reversed",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        left_counts: typing.Sequence[int] = None,
        left_cyclic: bool = None,
        left_length: int = None,
        left_reversed: bool = None,
        middle_counts: typing.Sequence[int] = None,
        middle_cyclic: bool = None,
        middle_reversed: bool = None,
        priority: abjad.HorizontalAlignment = None,
        right_counts: typing.Sequence[int] = None,
        right_cyclic: bool = None,
        right_length: int = None,
        right_reversed: bool = None,
    ) -> None:
        if left_counts is not None:
            assert abjad.mathtools.all_are_positive_integers(left_counts)
        self._left_counts = left_counts
        if left_cyclic is not None:
            left_cyclic = bool(left_cyclic)
        self._left_cyclic = left_cyclic
        if left_length is not None:
            left_length = int(left_length)
            assert 0 <= left_length, repr(left_length)
        self._left_length = left_length
        if left_reversed is not None:
            left_reversed = bool(left_reversed)
        self._left_reversed = left_reversed
        if middle_counts is not None:
            assert abjad.mathtools.all_are_positive_integers(middle_counts)
        self._middle_counts = middle_counts
        if middle_cyclic is not None:
            middle_cyclic = bool(middle_cyclic)
        self._middle_cyclic = middle_cyclic
        if middle_reversed is not None:
            middle_reversed = bool(middle_reversed)
        self._middle_reversed = middle_reversed
        if priority is not None:
            assert priority in (abjad.Left, abjad.Right)
        self._priority = priority
        if right_counts is not None:
            assert abjad.mathtools.all_are_positive_integers(right_counts)
        self._right_counts = right_counts
        if right_cyclic is not None:
            right_cyclic = bool(right_cyclic)
        self._right_cyclic = right_cyclic
        if right_length is not None:
            right_length = int(right_length)
            assert 0 <= right_length, repr(right_length)
        self._right_length = right_length
        if right_reversed is not None:
            right_reversed = bool(right_reversed)
        self._right_reversed = right_reversed

    ### SPECIAL METHODS ###

    def __call__(
        self, sequence: typing.Union[list, abjad.Segment] = None
    ) -> typing.List[abjad.Sequence]:
        """
        Calls LMR specifier on ``sequence``.
        """
        assert isinstance(sequence, (list, abjad.Segment)), repr(sequence)
        top_lengths = self._get_top_lengths(len(sequence))
        top_parts = abjad.sequence(sequence).partition_by_counts(
            top_lengths, cyclic=False, overhang=abjad.Exact
        )
        parts: typing.List[abjad.Sequence] = []
        left_part, middle_part, right_part = top_parts
        if left_part:
            if self.left_counts:
                parts_ = abjad.sequence(left_part).partition_by_counts(
                    self.left_counts,
                    cyclic=self.left_cyclic,
                    overhang=True,
                    reversed_=self.left_reversed,
                )
                parts.extend(parts_)
            else:
                parts.append(left_part)
        if middle_part:
            if self.middle_counts:
                parts_ = abjad.sequence(middle_part).partition_by_counts(
                    self.middle_counts,
                    cyclic=self.middle_cyclic,
                    overhang=True,
                    reversed_=self.middle_reversed,
                )
                parts.extend(parts_)
            else:
                parts.append(middle_part)
        if right_part:
            if self.right_counts:
                parts_ = abjad.sequence(right_part).partition_by_counts(
                    self.right_counts,
                    cyclic=self.right_cyclic,
                    overhang=True,
                    reversed_=self.right_reversed,
                )
                parts.extend(parts_)
            else:
                parts.append(right_part)
        assert isinstance(parts, list), repr(parts)
        assert all(isinstance(_, abjad.Sequence) for _ in parts)
        return parts

    ### PRIVATE METHODS ###

    def _get_priority(self):
        if self.priority is None:
            return abjad.Left
        return self.priority

    def _get_top_lengths(self, total_length):
        left_length, middle_length, right_length = 0, 0, 0
        left_length = self.left_length or 0
        middle_length = 0
        right_length = self.right_length or 0
        if left_length and right_length:
            if self._get_priority() == abjad.Left:
                left_length = self.left_length or 0
                left_length = min([left_length, total_length])
                remaining_length = total_length - left_length
                if self.right_length is None:
                    right_length = remaining_length
                    middle_length = 0
                else:
                    right_length = self.right_length or 0
                    right_length = min([right_length, remaining_length])
                    remaining_length = total_length - (
                        left_length + right_length
                    )
                    middle_length = remaining_length
            else:
                right_length = self.right_length or 0
                right_length = min([right_length, total_length])
                remaining_length = total_length - right_length
                if self.left_length is None:
                    left_length = remaining_length
                    middle_length = 0
                else:
                    left_length = self.left_length or 0
                    left_length = min([left_length, remaining_length])
                    remaining_length = total_length - (
                        right_length + left_length
                    )
                    middle_length = remaining_length
        elif left_length and not right_length:
            left_length = min([left_length, total_length])
            remaining_length = total_length - left_length
            right_length = remaining_length
        elif not left_length and right_length:
            right_length = min([right_length, total_length])
            remaining_length = total_length - right_length
            left_length = remaining_length
        elif not left_length and not right_length:
            middle_length = total_length
        return left_length, middle_length, right_length

    ### PUBLIC PROPERTIES ###

    @property
    def left_counts(self):
        """
        Gets left counts.

        ..  container:: example

            Left counts equal to a single 1:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     left_counts=[1],
            ...     left_cyclic=False,
            ...     left_length=3,
            ...     right_length=2,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4])
            Sequence([5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])
            Sequence([6, 7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5, 6])
            Sequence([7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5, 6, 7])
            Sequence([8, 9])

        ..  container:: example

            Left counts all equal to 1:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     left_counts=[1],
            ...     left_cyclic=True,
            ...     left_length=3,
            ...     right_length=2,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4, 5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4])
            Sequence([5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4, 5])
            Sequence([6, 7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4, 5, 6])
            Sequence([7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4, 5, 6, 7])
            Sequence([8, 9])

        Defaults to none.

        Set to positive integers or none.

        Returns tuple of positive integers or none.
        """
        return self._left_counts

    @property
    def left_cyclic(self):
        """
        Is true when specifier reads left counts cyclically.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._left_cyclic

    @property
    def left_length(self):
        """
        Gets left length.

        ..  container:: example

            Left length equal to 2:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     left_length=2,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7, 8, 9])

        Defaults to none.

        Set to nonnegative integer or none.

        Returns nonnegative integer or none.
        """
        return self._left_length

    @property
    def left_reversed(self):
        """
        Is true when specifier reverses left partition.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._left_reversed

    @property
    def middle_counts(self):
        """
        Gets middle counts.

        Defaults to none.

        Set to positive integers or none.

        Returns positive integers or none.
        """
        return self._middle_counts

    @property
    def middle_cyclic(self):
        """
        Is true when specifier reads middle counts cyclically.

        ..  container:: example

            Cyclic middle counts equal to [2]:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     middle_counts=[2],
            ...     middle_cyclic=True,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])
            Sequence([7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])
            Sequence([7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])
            Sequence([7, 8])
            Sequence([9])

            Odd parity produces length-1 part at right.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._middle_cyclic

    @property
    def middle_reversed(self):
        """
        Is true when specifier reverses middle partition.

        ..  container:: example

            Reversed cyclic middle counts equal to [2]:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     middle_counts=[2],
            ...     middle_cyclic=True,
            ...     middle_reversed=True,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])
            Sequence([6, 7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])
            Sequence([7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])
            Sequence([6, 7])
            Sequence([8, 9])

            Odd parity produces length-1 part at left.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._middle_reversed

    @property
    def priority(self):
        """
        Gets priority.

        ..  container:: example

            Priority to the left:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     left_length=2,
            ...     right_length=1,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])
            Sequence([4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5])
            Sequence([6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6])
            Sequence([7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7])
            Sequence([8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7, 8])
            Sequence([9])

        ..  container:: example

            Priority to the right:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     left_length=2,
            ...     priority=abjad.Right,
            ...     right_length=1,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])
            Sequence([4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5])
            Sequence([6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6])
            Sequence([7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7])
            Sequence([8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7, 8])
            Sequence([9])

        Defaults to none.

        Set to left, right or none.

        Returns left, right or none.
        """
        return self._priority

    @property
    def right_counts(self):
        """
        Gets right counts.

        Defaults to none.

        Set to positive integers or none.

        Returns positive integers or none.
        """
        return self._right_counts

    @property
    def right_cyclic(self):
        """
        Is true when specifier reads right counts cyclically.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._right_cyclic

    @property
    def right_length(self):
        """
        Gets right length.

        ..  container:: example

            Right length equal to 2:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     right_length=2,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2, 3])
            Sequence([4, 5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4])
            Sequence([5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5])
            Sequence([6, 7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5, 6])
            Sequence([7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5, 6, 7])
            Sequence([8, 9])

        ..  container:: example

            Right length equal to 2 and left counts equal to [1]:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     left_counts=[1],
            ...     left_cyclic=False,
            ...     right_length=2,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3, 4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3, 4])
            Sequence([5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3, 4, 5])
            Sequence([6, 7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3, 4, 5, 6])
            Sequence([7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3, 4, 5, 6, 7])
            Sequence([8, 9])

        Defaults to none.

        Set to nonnegative integer or none.

        Returns nonnegative integer or none.
        """
        return self._right_length

    @property
    def right_reversed(self):
        """
        Is true when specifier reverses right partition.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._right_reversed


class MusicAccumulator(object):
    """
    Music-accumulator.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_current_offset",
        "_figure_index",
        "_figure_names",
        "_floating_selections",
        "_music_maker",
        "_score_stop_offset",
        "_score_template",
        "_time_signatures",
        "_voice_names",
    )

    ### INITIALIZER ###

    def __init__(self, score_template: abjad.ScoreTemplate) -> None:
        self._score_template = score_template
        voice_names = []
        dummy_score = score_template()
        for voice in abjad.iterate(dummy_score).components(abjad.Voice):
            voice_names.append(voice.name)
        self._voice_names = voice_names
        self._current_offset = abjad.Offset(0)
        self._figure_index = 0
        self._figure_names: typing.List[str] = []
        self._floating_selections = self._make_voice_dictionary()
        self._score_stop_offset = abjad.Offset(0)
        self._time_signatures: typing.List[abjad.TimeSignature] = []

    ### SPECIAL METHODS ###

    def __call__(
        self,
        voice_name: str,
        collections: typing.Union[
            list, str, abjad.Segment, pitchclasses.CollectionList
        ],
        *specifiers,
        **keywords,
    ) -> None:
        r"""
        Calls music-accumulator.

        Raises exception on duplicate figure name.

        ..  container:: example exception

            >>> accumulator = baca.MusicAccumulator(
            ...     score_template=baca.StringTrioScoreTemplate()
            ...     )
            >>> commands = [
            ...     pitch_first([1], 16, signature=16),
            ...     rmakers.beam(),
            ... ]
            >>> accumulator(
            ...     'Violin_Music_Voice',
            ...     [[0, 1, 2, 3]],
            ...     *commands,
            ...     figure_name='D',
            ... )

            >>> accumulator(
            ...     'Violin_Music_Voice',
            ...     [[4, 5, 6, 7]],
            ...     *commands,
            ...     figure_name='D',
            ... )
            Traceback (most recent call last):
                ...
            Exception: duplicate figure name: 'D'.

        """
        specifiers = specifiers or ()
        specifiers_list = list(specifiers)
        if specifiers_list and isinstance(specifiers_list[0], MusicMaker):
            raise Exception("MMM", specifiers_list)
            music_maker = specifiers_list[0]
            specifiers_list.pop(0)
        else:
            music_maker = MusicMaker()
        assert isinstance(music_maker, MusicMaker)
        for specifier in specifiers_list:
            if isinstance(specifier, MusicMaker):
                message = "must combine music-makers:\n"
                message += f"   {repr(music_maker)}"
                message += f"   {repr(specifier)}"
                raise Exception(message)
        voice_name = self.score_template.voice_abbreviations.get(
            voice_name, voice_name
        )
        first_specifiers = music_maker.commands or []
        all_specifiers = first_specifiers + specifiers_list
        for specifier in all_specifiers:
            if isinstance(specifier, Imbrication):
                voice_name_ = self.score_template.voice_abbreviations.get(
                    specifier.voice_name, specifier.voice_name
                )
                specifier._voice_name = voice_name_
            else:
                assert not hasattr(specifier, "voice_name"), repr(specifier)
                assert not hasattr(specifier, "remote_voice_name"), repr(
                    specifier
                )
        anchor = keywords.pop("anchor", None)
        if anchor is not None:
            voice_name_ = self.score_template.voice_abbreviations.get(
                anchor.remote_voice_name, anchor.remote_voice_name
            )
            anchor._remote_voice_name = voice_name_
        keywords["figure_index"] = self._figure_index
        hide_time_signature = keywords.pop("hide_time_signature", None)
        music_maker = abjad.new(music_maker, *all_specifiers, **keywords)
        contribution = music_maker(voice_name, collections)
        contribution = MusicContribution(
            anchor=anchor,
            color_selector=contribution.color_selector,
            color_selector_result=contribution.color_selector_result,
            figure_name=keywords.get("figure_name", None),
            hide_time_signature=hide_time_signature,
            time_signature=contribution.time_signature,
            voice_to_selection=contribution.voice_to_selection,
        )
        self._cache_figure_name(contribution)
        self._cache_floating_selection(contribution)
        self._cache_time_signature(contribution)
        self._figure_index += 1

    ### PRIVATE METHODS ###

    def _cache_figure_name(self, contribution):
        if contribution.figure_name is None:
            return
        if contribution.figure_name in self._figure_names:
            name = contribution.figure_name
            raise Exception(f"duplicate figure name: {name!r}.")
        self._figure_names.append(contribution.figure_name)

    def _cache_floating_selection(self, contribution):
        for voice_name in contribution:
            voice_name = self.score_template.voice_abbreviations.get(
                voice_name, voice_name
            )
            selection = contribution[voice_name]
            if not selection:
                continue
            start_offset = self._get_start_offset(selection, contribution)
            stop_offset = start_offset + abjad.inspect(selection).duration()
            timespan = abjad.Timespan(start_offset, stop_offset)
            floating_selection = abjad.AnnotatedTimespan(
                timespan.start_offset,
                timespan.stop_offset,
                annotation=selection,
            )
            self._floating_selections[voice_name].append(floating_selection)
        self._current_offset = stop_offset
        self._score_stop_offset = max(self._score_stop_offset, stop_offset)

    def _cache_time_signature(self, contribution):
        if contribution.hide_time_signature:
            return
        if (
            contribution.anchor is None
            or contribution.hide_time_signature is False
            or (
                contribution.anchor
                and contribution.anchor.remote_voice_name is None
            )
        ):
            self.time_signatures.append(contribution.time_signature)

    def _get_figure_start_offset(self, figure_name):
        for voice_name in sorted(self._floating_selections.keys()):
            for floating_selection in self._floating_selections[voice_name]:
                leaf_start_offset = floating_selection.start_offset
                leaves = abjad.iterate(floating_selection.annotation).leaves()
                for leaf in leaves:
                    markup = abjad.inspect(leaf).indicators(abjad.Markup)
                    for markup_ in markup:
                        if isinstance(
                            markup_._annotation, str
                        ) and markup_._annotation.startswith("figure name: "):
                            figure_name_ = markup_._annotation
                            figure_name_ = figure_name_.replace(
                                "figure name: ", ""
                            )
                            if figure_name_ == figure_name:
                                return leaf_start_offset
                    leaf_duration = abjad.inspect(leaf).duration()
                    leaf_start_offset += leaf_duration
        raise Exception(f"can not find figure {figure_name!r}.")

    def _get_leaf_timespan(self, leaf, floating_selections):
        found_leaf = False
        for floating_selection in floating_selections:
            leaf_start_offset = abjad.Offset(0)
            for leaf_ in abjad.iterate(floating_selection.annotation).leaves():
                leaf_duration = abjad.inspect(leaf_).duration()
                if leaf_ is leaf:
                    found_leaf = True
                    break
                leaf_start_offset += leaf_duration
            if found_leaf:
                break
        if not found_leaf:
            raise Exception(f"can not find {leaf!r} in floating selections.")
        selection_start_offset = floating_selection.start_offset
        leaf_start_offset = selection_start_offset + leaf_start_offset
        leaf_stop_offset = leaf_start_offset + leaf_duration
        return abjad.Timespan(leaf_start_offset, leaf_stop_offset)

    def _get_start_offset(self, selection, contribution):
        if (
            contribution.anchor is not None
            and contribution.anchor.figure_name is not None
        ):
            figure_name = contribution.anchor.figure_name
            start_offset = self._get_figure_start_offset(figure_name)
            return start_offset
        anchored = False
        if contribution.anchor is not None:
            remote_voice_name = contribution.anchor.remote_voice_name
            remote_selector = contribution.anchor.remote_selector
            use_remote_stop_offset = contribution.anchor.use_remote_stop_offset
            anchored = True
        else:
            remote_voice_name = None
            remote_selector = None
            use_remote_stop_offset = None
        if not anchored:
            return self._current_offset
        if anchored and remote_voice_name is None:
            return self._score_stop_offset
        remote_selector = remote_selector or classes.selector().leaf(0)
        floating_selections = self._floating_selections[remote_voice_name]
        selections = [_.annotation for _ in floating_selections]
        result = remote_selector(selections)
        selected_leaves = list(abjad.iterate(result).leaves())
        first_selected_leaf = selected_leaves[0]
        timespan = self._get_leaf_timespan(
            first_selected_leaf, floating_selections
        )
        if use_remote_stop_offset:
            remote_anchor_offset = timespan.stop_offset
        else:
            remote_anchor_offset = timespan.start_offset
        local_anchor_offset = abjad.Offset(0)
        if contribution.anchor is not None:
            local_selector = contribution.anchor.local_selector
        else:
            local_selector = None
        if local_selector is not None:
            result = local_selector(selection)
            selected_leaves = list(abjad.iterate(result).leaves())
            first_selected_leaf = selected_leaves[0]
            dummy_container = abjad.Container(selection)
            timespan = abjad.inspect(first_selected_leaf).timespan()
            del dummy_container[:]
            local_anchor_offset = timespan.start_offset
        start_offset = remote_anchor_offset - local_anchor_offset
        return start_offset

    @staticmethod
    def _insert_skips(floating_selections, voice_name):
        for floating_selection in floating_selections:
            assert isinstance(floating_selection, abjad.AnnotatedTimespan)
        floating_selections = list(floating_selections)
        floating_selections.sort()
        try:
            first_start_offset = floating_selections[0].start_offset
        except:
            raise Exception(floating_selections, voice_name)
        timespans = abjad.TimespanList(floating_selections)
        gaps = ~timespans
        if 0 < first_start_offset:
            first_gap = abjad.Timespan(0, first_start_offset)
            gaps.append(first_gap)
        selections = floating_selections + list(gaps)
        selections.sort()
        fused_selection = []
        for selection in selections:
            if isinstance(selection, abjad.AnnotatedTimespan):
                fused_selection.extend(selection.annotation)
            else:
                assert isinstance(selection, abjad.Timespan)
                skip = abjad.Skip(1, multiplier=selection.duration)
                fused_selection.append(skip)
        fused_selection = abjad.select(fused_selection)
        return fused_selection

    def _make_voice_dictionary(self):
        return dict([(_, []) for _ in self._voice_names])

    ### PUBLIC PROPERTIES ###

    @property
    def score_template(self) -> abjad.ScoreTemplate:
        """
        Gets score template.
        """
        return self._score_template

    @property
    def time_signatures(self) -> typing.List[abjad.TimeSignature]:
        """
        Gets time signatures.
        """
        return self._time_signatures

    ### PUBLIC METHODS ###

    def assemble(self, voice_name):
        """
        Assembles complete selection for ``voice_name``.

        Returns selection or none.
        """
        floating_selections = self._floating_selections[voice_name]
        if not floating_selections:
            return
        selection = self._insert_skips(floating_selections, voice_name)
        assert isinstance(selection, abjad.Selection), repr(selection)
        return selection

    def populate_segment_maker(self, segment_maker) -> None:
        """
        Populates ``segment_maker``.
        """
        for voice_name in sorted(self._floating_selections):
            selection = self.assemble(voice_name)
            if not selection:
                continue
            segment_maker(
                (voice_name, 1),
                rhythmcommands.music(
                    selection, do_not_check_total_duration=True, tag=None
                ),
            )


class MusicContribution(object):
    """
    Music contribution.

    ..  container:: example

        >>> baca.MusicContribution()
        MusicContribution()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_anchor",
        "_color_selector",
        "_color_selector_result",
        "_figure_name",
        "_hide_time_signature",
        "_tag",
        "_time_signature",
        "_voice_to_selection",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        anchor: AnchorSpecifier = None,
        color_selector: abjad.Expression = None,
        color_selector_result: typing.Union[
            abjad.Selection, abjad.Tuplet
        ] = None,
        figure_name: str = None,
        hide_time_signature: bool = None,
        time_signature: abjad.TimeSignature = None,
        voice_to_selection: typing.Dict[str, abjad.Selection] = None,
    ):
        if anchor is not None and not isinstance(anchor, AnchorSpecifier):
            raise TypeError(f"anchor specifier only: {anchor!r}.")
        self._anchor = anchor
        if color_selector is not None:
            assert isinstance(color_selector, abjad.Expression)
        self._color_selector = color_selector
        if color_selector_result is not None:
            prototype = (abjad.Selection, abjad.Tuplet)
            assert isinstance(color_selector_result, prototype), repr(
                color_selector_result
            )
        self._color_selector_result = color_selector_result
        if figure_name is not None:
            figure_name = str(figure_name)
        self._figure_name = figure_name
        if hide_time_signature is not None:
            hide_time_signature = bool(hide_time_signature)
        self._hide_time_signature = hide_time_signature
        if time_signature is not None:
            assert isinstance(time_signature, abjad.TimeSignature)
        self._time_signature = time_signature
        if voice_to_selection is not None:
            assert isinstance(voice_to_selection, dict), repr(
                voice_to_selection
            )
        self._voice_to_selection = voice_to_selection

    ### SPECIAL METHODS ###

    def __getitem__(self, voice_name) -> abjad.Selection:
        """
        Gets ``voice_name`` selection list.
        """
        return self.voice_to_selection.__getitem__(voice_name)

    def __iter__(self) -> typing.Generator:
        """
        Iterates figure contribution.
        """
        for voice_name in self.voice_to_selection:
            yield voice_name

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        """
        Gets anchor.

        Returns anchor specifier or none.
        """
        return self._anchor

    @property
    def color_selector(self):
        """
        Gets color selector.

        Returns selector or none.
        """
        return self._color_selector

    @property
    def color_selector_result(self):
        """
        Gets color selector result.

        Returns selector result or none.
        """
        return self._color_selector_result

    @property
    def figure_name(self):
        """
        Gets figure name.

        Returns string or none.
        """
        return self._figure_name

    @property
    def hide_time_signature(self):
        """
        Is true when contribution hides time signature.

        Returns true, false or none.
        """
        return self._hide_time_signature

    @property
    def time_signature(self):
        """
        Gets time signature.

        Returns time signature or none.
        """
        return self._time_signature

    @property
    def voice_to_selection(self):
        """
        Gets voice-to-selection dictionary.
        """
        if self._voice_to_selection is not None:
            assert isinstance(self._voice_to_selection, dict), repr(
                self.voice_to_selection
            )
            for value in self._voice_to_selection.values():
                assert isinstance(value, abjad.Selection), repr(value)
        return self._voice_to_selection

    ### PUBLIC METHODS ###

    def print_color_selector_result(self):
        """
        Prints color selector result.

        Returns none.
        """
        if self.color_selector is None:
            return
        if self.color_selector_result is None:
            return
        self.color_selector.print(self.color_selector_result)


class MusicMaker(object):
    r"""
    Music-maker.

    >>> from abjadext import rmakers

    ..  container:: example

        Default music-maker:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([1], 16),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice_1', collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 9/16
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                bf'16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                e''16                                                                %! baca.MusicMaker.__call__
                                ef''16                                                               %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    ..  container:: example

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([1], 16),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice_1', collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 9/16
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                bf'16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                e''16                                                                %! baca.MusicMaker.__call__
                                ef''16                                                               %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    ..  container:: example

        Calltime counts:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([1, 2], 16),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     collections,
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 3/4
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'8                                                                  %! baca.MusicMaker.__call__
                                bf'16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                e''8                                                                 %! baca.MusicMaker.__call__
                                ef''16                                                               %! baca.MusicMaker.__call__
                                af''8                                                                %! baca.MusicMaker.__call__
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    ..  container:: example

        Calltime denominator:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([1], 32),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     collections,
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 9/32
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                c'32                                                                 %! baca.MusicMaker.__call__
                                [
                                d'32                                                                 %! baca.MusicMaker.__call__
                                bf'32                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                fs''32                                                               %! baca.MusicMaker.__call__
                                [
                                e''32                                                                %! baca.MusicMaker.__call__
                                ef''32                                                               %! baca.MusicMaker.__call__
                                af''32                                                               %! baca.MusicMaker.__call__
                                g''32                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                a'32                                                                 %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    ..  container:: example

        Calltime time treatments:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([1], 16, time_treatments=[1]),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     collections,
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 11/16
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 4/3 {                                                             %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                bf'16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 6/5 {                                                             %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                e''16                                                                %! baca.MusicMaker.__call__
                                ef''16                                                               %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    ..  container:: example

        Rest input:

        >>> music_maker = baca.MusicMaker(
        ...     rmakers.beam(),
        ...     baca.nest('+1/8'),
        ... )

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     "r4. r4.",
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 7/8
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 7/6 {                                                             %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                                    r4.                                                              %! baca.MusicMaker.__call__
                                    r4.                                                              %! baca.MusicMaker.__call__
                                }                                                                    %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    ..  container:: example

        The following negative-valued talea count patterns work:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([2, -1], 16),
        ...     rmakers.beam(),
        ... )

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[18, 16, 15, 20, 19]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 15/16
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                fs''8                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                e''8                                                                 %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                ef''8                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''8                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                g''8                                                                 %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([2, -1, -1], 16),
        ...     rmakers.beam(),
        ... )

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[18, 16, 15, 20, 19]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 5/4
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                fs''8                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                e''8                                                                 %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                ef''8                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''8                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                g''8                                                                 %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([-1, 2], 16),
        ...     rmakers.beam(),
        ... )

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[18, 16, 15, 20, 19]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 15/16
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                fs''8                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                e''8                                                                 %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                ef''8                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''8                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                g''8                                                                 %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([-1, -1, 2], 16),
        ...     rmakers.beam(),
        ... )

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[18, 16, 15, 20, 19]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 5/4
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                fs''8                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                e''8                                                                 %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                ef''8                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''8                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                g''8                                                                 %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([-1, -1, 2, -2, -2], 16),
        ...     rmakers.beam(),
        ... )

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[18, 16, 15, 20, 19]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 5/2
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                fs''8                                                                %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                e''8                                                                 %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                ef''8                                                                %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''8                                                                %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                g''8                                                                 %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    ..  container:: example

        Works with chords:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([1], 16),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     {0, 2, 10},
        ...     [18, 16, 15, 20, 19],
        ...     [9],
        ...     ]
        >>> contribution = music_maker('Voice_1', collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 7/16
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                <c' d' bf'>16
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                e''16                                                                %! baca.MusicMaker.__call__
                                ef''16                                                               %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_commands",
        "_extend_beam",
        "_figure_index",
        "_figure_name",
        "_next_figure",
        "_signature",
        "_tag",
        "_voice_names",
    )

    # to make sure abjad.new() copies commands
    _positional_arguments_name = "commands"

    _publish_storage_format = True

    _state_variables = ("_next_figure",)

    ### INITIALIZER ###

    def __init__(
        self,
        *commands,
        extend_beam: bool = None,
        figure_index: int = None,
        figure_name: str = None,
        signature: int = None,
        tag: str = "baca.MusicMaker.__call__",
    ) -> None:
        self._commands = list(commands)
        if extend_beam is not None:
            extend_beam = bool(extend_beam)
        self._extend_beam = extend_beam
        if figure_index is not None:
            assert isinstance(figure_index, int), repr(figure_index)
        self._figure_index = figure_index
        if figure_name is not None:
            figure_name = str(figure_name)
        self._figure_name = figure_name
        self._next_figure = 0
        if signature is not None:
            assert isinstance(signature, int)
        self._signature = signature
        if tag is not None:
            assert isinstance(tag, str)
        self._tag = tag

    ### SPECIAL METHODS ###

    def __call__(
        self,
        voice_name: str,
        collections: typing.Union[
            list,
            str,
            abjad.Segment,
            abjad.Sequence,
            abjad.Set,
            pitchclasses.CollectionList,
        ],
    ) -> MusicContribution:
        """
        Calls music-maker.
        """
        commands = list(self.commands)
        if any(_ is None for _ in commands):
            message = "commands must not be none:\n"
            message += f"   {repr(commands)}"
            raise Exception(message)
        prototype = (
            list,
            str,
            abjad.Segment,
            abjad.Sequence,
            abjad.Set,
            pitchclasses.CollectionList,
        )
        assert isinstance(collections, prototype), repr(collections)
        assignments = []
        if isinstance(collections, str):
            tuplet = abjad.Tuplet((1, 1), collections, hide=True)
            selections = [abjad.select(tuplet)]
        elif all(isinstance(_, abjad.Rest) for _ in collections):
            tuplet = abjad.Tuplet((1, 1), collections, hide=True)
            selections = [abjad.select(tuplet)]
        else:
            commands_ = []
            for command in commands:
                if isinstance(command, PitchFirstAssignment):
                    assignments.append(command)
                elif isinstance(command, PitchFirstRhythmMaker):
                    assignment = PitchFirstAssignment(command)
                    assignments.append(assignment)
                else:
                    commands_.append(command)
            commands = commands_
            if not assignments:
                raise Exception("must provide pitch-first assignment.")
            # TODO: activate:
            #        if 1 < len(assignments):
            #            assert len(assignments) == 2, repr(assignments)
            #            message = "must combine assignments:\n"
            #            message += f"   {repr(assignments[0])}\n"
            #            message += f"   {repr(assignments[1])}\n"
            #            raise Exception(message)
            collections = self._coerce_collections(collections)
            selections = len(collections) * [None]
            for assignment in assignments:
                assert isinstance(assignment, PitchFirstAssignment)
                assignment(collections=collections, selections=selections)
        container = abjad.Container(selections)
        color_selector, color_selector_result = None, None
        imbricated_selections = {}
        for command in commands:
            if isinstance(command, Imbrication):
                imbricated_selections.update(command(container))
            elif isinstance(command, _commands.ColorCommand):
                color_selector = command.selector
                color_selector_result = command(selections)
            else:
                command(selections)
        self._label_figure_name_(container)
        if self.extend_beam:
            leaf = abjad.select(selections).leaf(-1)
            abjad.attach(abjad.tags.RIGHT_BROKEN_BEAM, leaf)
        selection = abjad.select([container])
        duration = abjad.inspect(selection).duration()
        signature = self.signature
        if signature is None and assignments:
            primary_rhythm_maker = assignments[0].rhythm_maker
            signature = primary_rhythm_maker.signature
        if signature is not None:
            duration = duration.with_denominator(signature)
        time_signature = abjad.TimeSignature(duration)
        voice_to_selection = {voice_name: selection}
        voice_to_selection.update(imbricated_selections)
        for value in voice_to_selection.values():
            assert isinstance(value, abjad.Selection), repr(value)
            if self.tag is not None:
                rhythmcommands.tag_selection(value, self.tag)
        return MusicContribution(
            color_selector=color_selector,
            color_selector_result=color_selector_result,
            time_signature=time_signature,
            voice_to_selection=voice_to_selection,
        )

    def __eq__(self, argument) -> bool:
        """
        Is true when initialization values of music-maker equal
        initialization values of ``argument``.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Formats music-maker.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Hashes music-maker.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation of music-maker.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _coerce_collections(collections) -> pitchclasses.CollectionList:
        prototype = (abjad.Segment, abjad.Set)
        if isinstance(collections, prototype):
            return pitchclasses.CollectionList(collections=[collections])
        item_class: typing.Type = abjad.NumberedPitch
        for collection in collections:
            for item in collection:
                if isinstance(item, str):
                    item_class = abjad.NamedPitch
                    break
        return pitchclasses.CollectionList(
            collections=collections, item_class=item_class
        )

    def _label_figure_name_(self, container):
        if self.figure_name is None:
            return
        figure_name = str(self.figure_name)
        figure_index = self.figure_index
        original_figure_name = figure_name
        parts = figure_name.split("_")
        if len(parts) == 1:
            body = parts[0]
            figure_name = abjad.Markup(body)
        elif len(parts) == 2:
            body, subscript = parts
            figure_name = abjad.Markup.concat(
                [abjad.Markup(body), abjad.Markup(subscript).sub()]
            )
        else:
            raise Exception(f"unrecognized figure name: {figure_name!r}.")
        figure_index = f" ({figure_index})"
        figure_index = abjad.Markup(figure_index).fontsize(-2).raise_(0.25)
        figure_name_markup = abjad.Markup.concat(
            ["[", figure_name, abjad.Markup.hspace(1), figure_index, "]"]
        )
        figure_name_markup = figure_name_markup.fontsize(2)
        figure_name_markup = abjad.Markup(
            figure_name_markup, direction=abjad.Up
        )
        annotation = f"figure name: {original_figure_name}"
        figure_name_markup._annotation = annotation
        leaf = abjad.select(container).leaf(0)
        abjad.attach(
            figure_name_markup,
            leaf,
            deactivate=True,
            tag=abjad.const.FIGURE_NAME,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self) -> typing.List:
        r"""
        Gets commands.

        ..  container:: example

            Register specifier transposes to octave rooted on F#3:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam(),
            ...     baca.register(-6),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 9/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf16                                                                 %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    fs16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    e'16                                                                 %! baca.MusicMaker.__call__
                                    ef'16                                                                %! baca.MusicMaker.__call__
                                    af16                                                                 %! baca.MusicMaker.__call__
                                    g16                                                                  %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Ocatve-transposes to a target interpolated from C4 up to C5:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam(),
            ...     baca.register(0, 12),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 9/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    fs'16                                                                %! baca.MusicMaker.__call__
                                    [
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a''16                                                                %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Hairpin specifier selects all leaves:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam(),
            ...     baca.hairpin('p < f'),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                <<
                    \new GlobalContext
                    {
                        s1 * 11/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    \p                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    \<                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    b''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    \f                                                                   %! baca.hairpin:PiecewiseCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Maps hairpin to each run:

            >>> affix = baca.RestAffixSpecifier(
            ...     pattern=abjad.Pattern(
            ...         indices=[0, -1],
            ...         inverted=True,
            ...         ),
            ...     prefix=[1],
            ... )
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16, affix=affix),
            ...     rmakers.beam(),
            ...     baca.hairpin('p < f', map=baca.runs()),
            ... )
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     [[0, 2, 10, 18], [15, 23], [19, 13, 9, 8]],
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                <<
                    \new GlobalContext
                    {
                        s1 * 11/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    \p                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    \<                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \f                                                                   %! baca.hairpin:PiecewiseCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    r16                                                                  %! baca.MusicMaker.__call__
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    \p                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    \<                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    [
                                    b''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    \f                                                                   %! baca.hairpin:PiecewiseCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Hairpin specifiers select notes of first and last tuplet:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam(),
            ...     baca.new(
            ...         baca.hairpin('p < f'),
            ...         map=baca.tuplet(0),
            ...         ),
            ...     baca.new(
            ...         baca.hairpin('f > p'),
            ...         map=baca.tuplet(-1),
            ...         ),
            ... )
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     [[0, 2, 10, 18], [16, 15, 23], [19, 13, 9, 8]],
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                <<
                    \new GlobalContext
                    {
                        s1 * 11/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    \p                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    \<                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \f                                                                   %! baca.hairpin:PiecewiseCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    b''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    \f                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    \>                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    [
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    \p                                                                   %! baca.hairpin:PiecewiseCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Hairpin specifiers treat first two tuplets and then the rest:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam(),
            ...     baca.new(
            ...         baca.hairpin('p < f'),
            ...         map=baca.tuplets()[:2],
            ...         ),
            ...     baca.new(
            ...         baca.hairpin('f > p'),
            ...         map=baca.tuplet(-1),
            ...         ),
            ... )
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     [[0, 2, 10, 18], [16, 15, 23], [19, 13, 9, 8]],
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 6
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #6
                }
                <<
                    \new GlobalContext
                    {
                        s1 * 11/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    \p                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    \<                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    \f                                                                   %! baca.hairpin:PiecewiseCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    \p                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    \<                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    [
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    b''16                                                                %! baca.MusicMaker.__call__
                                    \f                                                                   %! baca.hairpin:PiecewiseCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    \f                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    \>                                                                   %! baca.hairpin:PiecewiseCommand(1)
                                    [
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    \p                                                                   %! baca.hairpin:PiecewiseCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Spanner specifier selects all leaves by default:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam(),
            ...     baca.slur(),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).stem.direction = abjad.Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Stem.direction = #down
                }
                <<
                    \new GlobalContext
                    {
                        s1 * 11/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    (                                                                    %! baca.slur:SpannerIndicatorCommand(1)
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    b''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    )                                                                    %! baca.slur:SpannerIndicatorCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Maps slur to leaves in each tuplet:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam(),
            ...     baca.slur(map=baca.tuplets()),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).stem.direction = abjad.Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Stem.direction = #down
                }
                <<
                    \new GlobalContext
                    {
                        s1 * 11/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    (                                                                    %! baca.slur:SpannerIndicatorCommand(1)
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    )                                                                    %! baca.slur:SpannerIndicatorCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    (                                                                    %! baca.slur:SpannerIndicatorCommand(1)
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    b''16                                                                %! baca.MusicMaker.__call__
                                    )                                                                    %! baca.slur:SpannerIndicatorCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    (                                                                    %! baca.slur:SpannerIndicatorCommand(1)
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    )                                                                    %! baca.slur:SpannerIndicatorCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Slur specifier selects first two pitched leaves in each tuplet:

            >>> getter = baca.pleaves()[:2]
            >>> selector = baca.tuplets().map(getter)
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam(),
            ...     baca.slur(map=selector),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).stem.direction = abjad.Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Stem.direction = #down
                }
                <<
                    \new GlobalContext
                    {
                        s1 * 11/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    (                                                                    %! baca.slur:SpannerIndicatorCommand(1)
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    )                                                                    %! baca.slur:SpannerIndicatorCommand(2)
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    (                                                                    %! baca.slur:SpannerIndicatorCommand(1)
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    )                                                                    %! baca.slur:SpannerIndicatorCommand(2)
                                    b''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    (                                                                    %! baca.slur:SpannerIndicatorCommand(1)
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    )                                                                    %! baca.slur:SpannerIndicatorCommand(2)
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Slur specifier selects last two pitched leaves in each tuplet:

            >>> getter = baca.pleaves()[-2:]
            >>> selector = baca.tuplets().map(getter)
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam(),
            ...     baca.slur(map=selector),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).stem.direction = abjad.Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Stem.direction = #down
                }
                <<
                    \new GlobalContext
                    {
                        s1 * 11/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    (                                                                    %! baca.slur:SpannerIndicatorCommand(1)
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    )                                                                    %! baca.slur:SpannerIndicatorCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    (                                                                    %! baca.slur:SpannerIndicatorCommand(1)
                                    b''16                                                                %! baca.MusicMaker.__call__
                                    )                                                                    %! baca.slur:SpannerIndicatorCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    (                                                                    %! baca.slur:SpannerIndicatorCommand(1)
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    )                                                                    %! baca.slur:SpannerIndicatorCommand(2)
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Beam specifier beams divisions together:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam_groups(),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                }
                <<
                    \new GlobalContext
                    {
                        s1 * 11/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    b''16                                                                %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Beam specifier beams nothing:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16)
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 11/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    b''16                                                                %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    af'16                                                                %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Nesting specifier augments one sixteenth:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     baca.Nesting(
            ...         time_treatments=['+1/16'],
            ...         ),
            ...     rmakers.beam_groups(),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).beam.positions = (-5.5, -5.5)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Beam.positions = #'(-5.5 . -5.5)
                }
                <<
                    \new GlobalContext
                    {
                        s1 * 3/4
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 12/11 {                                                           %! baca.MusicMaker.__call__
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 0
                                        \set stemRightBeamCount = 2
                                        c'16                                                             %! baca.MusicMaker.__call__
                                        [
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        d'16                                                             %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        bf'16                                                            %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        fs''16                                                           %! baca.MusicMaker.__call__
                                    }                                                                    %! baca.MusicMaker.__call__
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        e''16                                                            %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        ef''16                                                           %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        b''16                                                            %! baca.MusicMaker.__call__
                                    }                                                                    %! baca.MusicMaker.__call__
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        g''16                                                            %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        cs''16                                                           %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        a'16                                                             %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 0
                                        af'16                                                            %! baca.MusicMaker.__call__
                                        ]
                                    }                                                                    %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Nesting specifier augments first two collections one sixteenth:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     baca.Nesting(
            ...         lmr_specifier=baca.LMRSpecifier(
            ...             left_length=2,
            ...             ),
            ...         time_treatments=['+1/16', None],
            ...         ),
            ...     rmakers.beam_groups(),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).beam.positions = (-5.5, -5.5)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Beam.positions = #'(-5.5 . -5.5)
                }
                <<
                    \new GlobalContext
                    {
                        s1 * 3/4
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 8/7 {                                                             %! baca.MusicMaker.__call__
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 0
                                        \set stemRightBeamCount = 2
                                        c'16                                                             %! baca.MusicMaker.__call__
                                        [
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        d'16                                                             %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        bf'16                                                            %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        fs''16                                                           %! baca.MusicMaker.__call__
                                    }                                                                    %! baca.MusicMaker.__call__
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        e''16                                                            %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        ef''16                                                           %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        b''16                                                            %! baca.MusicMaker.__call__
                                    }                                                                    %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Sixteenths followed by eighths:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 8),
            ...     baca.pitch_first([1], 16, pattern=abjad.index_first(1)),
            ...     rmakers.beam(),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 15/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    fs''8                                                                %! baca.MusicMaker.__call__
                                    [
                                    e''8                                                                 %! baca.MusicMaker.__call__
                                    ef''8                                                                %! baca.MusicMaker.__call__
                                    af''8                                                                %! baca.MusicMaker.__call__
                                    g''8                                                                 %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a'8                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Sixteenths surrounding dotted eighths:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([3], 16),
            ...     baca.pitch_first(
            ...         [1], 16,
            ...         pattern=abjad.Pattern(indices=[0, -1]),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 19/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    fs''8.                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''8.                                                                %! baca.MusicMaker.__call__
                                    ef''8.                                                               %! baca.MusicMaker.__call__
                                    af''8.                                                               %! baca.MusicMaker.__call__
                                    g''8.                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Sixteenths surrounding argumented dotted eighths:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([3], 16, time_treatments=[1]),
            ...     baca.pitch_first(
            ...         [1],
            ...         16,
            ...         pattern=abjad.Pattern([0, -1]),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 5/4
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 16/15 {                                                           %! baca.MusicMaker.__call__
                                    fs''8.                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''8.                                                                %! baca.MusicMaker.__call__
                                    ef''8.                                                               %! baca.MusicMaker.__call__
                                    af''8.                                                               %! baca.MusicMaker.__call__
                                    g''8.                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Augmented sixteenths surrounding dotted eighths:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([3], 16),
            ...     baca.pitch_first(
            ...         [1],
            ...         16,
            ...         time_treatments=[1],
            ...         pattern=abjad.Pattern([0, -1]),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 5/4
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 4/3 {                                                             %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    fs''8.                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''8.                                                                %! baca.MusicMaker.__call__
                                    ef''8.                                                               %! baca.MusicMaker.__call__
                                    af''8.                                                               %! baca.MusicMaker.__call__
                                    g''8.                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Diminished sixteenths surrounding dotted eighths:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([3], 16),
            ...     baca.pitch_first(
            ...         [1], 16,
            ...         pattern=abjad.Pattern(indices=[0, -1]),
            ...         time_treatments=[-1],
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 9/8
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \times 2/3 {                                                             %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    fs''8.                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''8.                                                                %! baca.MusicMaker.__call__
                                    ef''8.                                                               %! baca.MusicMaker.__call__
                                    af''8.                                                               %! baca.MusicMaker.__call__
                                    g''8.                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        """
        return self._commands

    @property
    def extend_beam(self) -> typing.Optional[bool]:
        return self._extend_beam

    @property
    def figure_index(self) -> typing.Optional[int]:
        return self._figure_index

    @property
    def figure_name(self) -> typing.Optional[str]:
        return self._figure_name

    @property
    def signature(self) -> typing.Optional[int]:
        """
        Get (time) signature (denominator).
        """
        return self._signature

    @property
    def tag(self) -> typing.Optional[str]:
        return self._tag


class Nesting(object):
    r"""
    Nesting command.

    >>> from abjadext import rmakers

    ..  container:: example

        Augments one sixteenth:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([1], 16),
        ...     baca.Nesting(
        ...         time_treatments=['+1/16'],
        ...         ),
        ...     rmakers.beam_groups(),
        ...     )

        >>> collections = [
        ...     [0, 2, 10, 18],
        ...     [16, 15, 23],
        ...     [19, 13, 9, 8],
        ...     ]
        >>> contribution = music_maker('Voice_1', collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 3/4
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 12/11 {                                                           %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16                                                             %! baca.MusicMaker.__call__
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16                                                             %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16                                                            %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    fs''16                                                           %! baca.MusicMaker.__call__
                                }                                                                    %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    e''16                                                            %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    ef''16                                                           %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    b''16                                                            %! baca.MusicMaker.__call__
                                }                                                                    %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    g''16                                                            %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    cs''16                                                           %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16                                                             %! baca.MusicMaker.__call__
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    af'16                                                            %! baca.MusicMaker.__call__
                                    ]
                                }                                                                    %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_lmr_specifier", "_time_treatments")

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        lmr_specifier: LMRSpecifier = None,
        time_treatments: typing.Sequence[typing.Union[int, str]] = None,
    ) -> None:
        if lmr_specifier is not None:
            assert isinstance(lmr_specifier, LMRSpecifier)
        self._lmr_specifier = lmr_specifier
        if time_treatments is not None:
            assert isinstance(time_treatments, (list, tuple))
            is_time_treatment = PitchFirstRhythmMaker._is_time_treatment
            for time_treatment in time_treatments:
                assert is_time_treatment(time_treatment), repr(time_treatment)
        self._time_treatments = time_treatments

    ### SPECIAL METHODS ###

    def __call__(
        self, selections: typing.List[abjad.Selection] = None
    ) -> typing.Optional[typing.List[abjad.Selection]]:
        r"""
        Calls nesting command on ``selections``.

        ..  container:: example

            With rest affixes:

            >>> affix = baca.RestAffixSpecifier(
            ...     prefix=[2],
            ...     suffix=[3],
            ... )
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16, affix=affix),
            ...     baca.Nesting(time_treatments=['+1/16']),
            ...     rmakers.beam_groups(),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 17/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 17/16 {                                                           %! baca.MusicMaker.__call__
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                                        r8                                                               %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 0
                                        \set stemRightBeamCount = 2
                                        c'16                                                             %! baca.MusicMaker.__call__
                                        [
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        d'16                                                             %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        bf'16                                                            %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        fs''16                                                           %! baca.MusicMaker.__call__
                                    }                                                                    %! baca.MusicMaker.__call__
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        e''16                                                            %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        ef''16                                                           %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        b''16                                                            %! baca.MusicMaker.__call__
                                    }                                                                    %! baca.MusicMaker.__call__
                                    \scaleDurations #'(1 . 1) {                                          %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        g''16                                                            %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        cs''16                                                           %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        a'16                                                             %! baca.MusicMaker.__call__
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 0
                                        af'16                                                            %! baca.MusicMaker.__call__
                                        ]
                                        r8.                                                              %! baca.MusicMaker.__call__
                                    }                                                                    %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        """
        if selections is None:
            return None
        time_treatments = self._get_time_treatments()
        if time_treatments is None:
            return selections
        tuplets = []
        for selection in selections:
            if not isinstance(selection, abjad.Selection):
                raise Exception(f"should be selection: {selection!r}.")
            assert len(selection) == 1, repr(selection)
            assert isinstance(selection[0], abjad.Tuplet)
            tuplets.append(selection[0])
        if self.lmr_specifier is None:
            tuplet_selections = [abjad.select(tuplets)]
        else:
            tuplet_selections = self.lmr_specifier(tuplets)
            tuplet_selections = [
                abjad.select(list(_)) for _ in tuplet_selections
            ]
        selections_ = []
        prototype = abjad.Selection
        for index, tuplet_selection in enumerate(tuplet_selections):
            assert isinstance(tuplet_selection, prototype), repr(
                tuplet_selection
            )
            time_treatment = time_treatments[index]
            if time_treatment is None:
                selections_.append(tuplet_selection)
            else:
                nested_tuplet = self._make_nested_tuplet(
                    tuplet_selection, time_treatment
                )
                selection_ = abjad.Selection([nested_tuplet])
                selections_.append(selection_)
        assert isinstance(selections_, list)
        assert all(isinstance(_, abjad.Selection) for _ in selections_)
        return selections_

    ### PRIVATE METHODS ###

    def _get_time_treatments(self):
        if self.time_treatments:
            return abjad.CyclicTuple(self.time_treatments)

    @staticmethod
    def _make_nested_tuplet(tuplet_selection, time_treatment):
        assert isinstance(tuplet_selection, abjad.Selection)
        for tuplet in tuplet_selection:
            assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
        if isinstance(time_treatment, str):
            addendum = abjad.Duration(time_treatment)
            contents_duration = abjad.inspect(tuplet_selection).duration()
            target_duration = contents_duration + addendum
            multiplier = target_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, [])
            abjad.mutate(tuplet_selection).wrap(tuplet)
        elif time_treatment.__class__ is abjad.Multiplier:
            # tuplet = abjad.Tuplet(time_treatment, tuplet_selection)
            tuplet = abjad.Tuplet(time_treatment, [])
            abjad.mutate(tuplet_selection).wrap(tuplet)
        elif time_treatment.__class__ is abjad.Duration:
            target_duration = time_treatment
            contents_duration = abjad.inspect(tuplet_selection).duration()
            multiplier = target_duration / contents_duration
            # tuplet = abjad.Tuplet(multiplier, tuplet_selection)
            tuplet = abjad.Tuplet(multiplier, [])
            abjad.mutate(tuplet_selection).wrap(tuplet)
        else:
            raise Exception(f"bad time treatment: {time_treatment!r}.")
        return tuplet

    ### PUBLIC PROPERTIES ###

    # TODO: write LMR specifier examples
    @property
    def lmr_specifier(self):
        """
        Gets LMR specifier.

        Defaults to none.

        Set to LMR specifier or none.

        Returns LMR specifier or none.
        """
        return self._lmr_specifier

    @property
    def time_treatments(self):
        """
        Gets time treatments.

        Defaults to none.

        Set to time treatments or none.

        Returns time treatments or none.
        """
        return self._time_treatments


class PitchFirstAssignment(rmakers.MakerAssignment):
    """
    Pitch-first assignment.

    ..  container:: example

        >>> baca.pitch_first([1], 16)
        PitchFirstAssignment(PitchFirstRhythmMaker(Talea([1], 16)))

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = ("_pattern", "_rhythm_maker", "_thread")

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        rhythm_maker: "PitchFirstRhythmMaker",
        *,
        pattern=None,
        thread: bool = None,
    ) -> None:
        assert isinstance(rhythm_maker, PitchFirstRhythmMaker)
        self._rhythm_maker = rhythm_maker
        self._pattern = pattern
        if thread is not None:
            thread = bool(thread)
        self._thread = thread

    ### SPECIAL METHODS ###

    def __call__(
        self,
        collections: pitchclasses.CollectionList,
        selections: typing.Sequence[typing.Union[abjad.Selection, None]],
    ) -> typing.List[abjad.Selection]:
        """
        Calls pitch-first assignment.
        """
        prototype = (pitchclasses.CollectionList,)
        assert isinstance(collections, prototype), repr(collections)
        assert isinstance(selections, list), repr(selections)
        selection_prototype = (abjad.Selection, type(None))
        assert all(
            isinstance(_, selection_prototype) for _ in selections
        ), repr(selections)
        assert len(selections) == len(collections)
        rhythm_maker = self.rhythm_maker
        prototype__ = (PitchFirstRhythmMaker,)
        assert isinstance(rhythm_maker, prototype__), repr(rhythm_maker)
        length = len(selections)
        pattern = self.pattern or abjad.index_all()
        collection_prototype = (abjad.Segment, abjad.Set, list)
        collections_, indices = [], []
        for index, collection in enumerate(collections):
            assert isinstance(collection, collection_prototype), repr(
                collection
            )
            collection_: typing.Union[abjad.Segment, list]
            if isinstance(collection, (abjad.Set, set)):
                collection_ = list(sorted(collection))[:1]
            else:
                collection_ = collection
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
            if not pattern.matches_index(index, length):
                continue
            collections_.append(collection_)
            indices.append(index)
        stage_selections: typing.Union[list, abjad.Selection]
        if self.thread:
            stage_selections = rhythm_maker(collections_)
        else:
            stage_selections = []
            total_collections = len(collections_)
            for collection_index, collection_ in enumerate(collections_):
                stage_selections_ = rhythm_maker(
                    [collection_],
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
                indicators = abjad.detach(object, note)
                abjad.mutate(note).replace([chord])
                for indicator in indicators:
                    abjad.attach(indicator, chord)
            selections[index] = stage_selection
        assert isinstance(selections, list), repr(selections)
        for selection in selections:
            assert isinstance(selection, selection_prototype), repr(selection)
        return selections

    def __eq__(self, argument) -> bool:
        """
        Is true when initialization values of command equal
        initialization values of ``argument``.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Formats command.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Hashes command.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation of command.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(
        self
    ) -> typing.Optional[
        typing.Union[abjad.DurationInequality, abjad.Pattern]
    ]:
        """
        Gets pattern.
        """
        return self._pattern

    @property
    def rhythm_maker(self) -> "PitchFirstRhythmMaker":
        """
        Gets rhythm-maker.
        """
        return self._rhythm_maker

    @property
    def thread(self):
        r"""
        Is true when pitch-first assignment threads over selections.

        ..  container:: example

            Does not thread rhythm-maker over collections:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1, 2, 3], 16),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 1
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'8                                                                  %! baca.MusicMaker.__call__
                                    bf'8.                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''8                                                                 %! baca.MusicMaker.__call__
                                    ef''8.                                                               %! baca.MusicMaker.__call__
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    g''8                                                                 %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

            Threads rhythm-maker over collections:

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1, 2, 3], 16, thread=True),
            ...     rmakers.beam(),
            ... )
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 9/8
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'8                                                                  %! baca.MusicMaker.__call__
                                    bf'8.                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''8                                                                 %! baca.MusicMaker.__call__
                                    ef''8.                                                               %! baca.MusicMaker.__call__
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    g''8                                                                 %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a'8.                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        """
        return self._thread
        self._thread


class PitchFirstCommand(object):
    """
    Pitch-first command.

    ..  container:: example

        >>> command = baca.PitchFirstCommand(baca.pitch_first([1], 16))
        >>> abjad.f(command)
        baca.PitchFirstCommand(
            abjadext.RhythmCommand.MakerAssignments(
                PitchFirstAssignment(PitchFirstRhythmMaker(Talea([1], 16)))
                )
            )

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = ("_commands", "_assignments", "_tag")

    # to make sure abjad.new() copies commands
    _positional_arguments_name = "commands"

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        assignments: typing.Union[
            "PitchFirstAssignment",
            "PitchFirstRhythmMaker",
            rmakers.MakerAssignments,
        ],
        *commands,
        tag: str = None,
    ) -> None:
        if isinstance(assignments, PitchFirstRhythmMaker):
            assignment = PitchFirstAssignment(assignments)
            assignments = rmakers.MakerAssignments(assignment)
        elif isinstance(assignments, PitchFirstAssignment):
            assignments = rmakers.MakerAssignments(assignments)
        if not isinstance(assignments, rmakers.MakerAssignments):
            message = "must be maker assignments:\n"
            message += f"   {repr(assignments)}"
            raise Exception(message)
        self._assignments = assignments
        commands = commands or ()
        commands_ = tuple(commands)
        self._commands = commands_
        if tag is not None:
            assert isinstance(tag, str), repr(tag)
        self._tag = tag

    ### SPECIAL METHODS ###

    def __call__(
        self,
        collections: list,
        collection_index: int = None,
        state: abjad.OrderedDict = None,
        total_collections: int = None,
    ) -> abjad.Selection:
        """
        Calls pitch-first command.
        """
        prototype = (list,)
        assert isinstance(collections, prototype), repr(collections)
        # temporary:
        assert len(self.assignments.assignments) == 1, repr(self)
        rhythm_maker = self.assignments.assignments[0].rhythm_maker
        assert isinstance(rhythm_maker, PitchFirstRhythmMaker), repr(
            rhythm_maker
        )
        tuplets = rhythm_maker(
            collections,
            collection_index=collection_index,
            state=state,
            total_collections=total_collections,
        )
        divisions_consumed = len(tuplets)
        durations = [abjad.inspect(_).duration() for _ in tuplets]
        time_signatures = [abjad.TimeSignature(_) for _ in durations]
        staff = rmakers.RhythmMaker._make_staff(time_signatures)
        voice = staff["MusicVoice"]
        voice.extend(tuplets)
        ###self._call_commands(voice, divisions_consumed, self.rhythm_maker)
        self._call_commands(voice, divisions_consumed, rhythm_maker)
        selections = abjad.select(voice[:]).group_by_measure()
        voice[:] = []
        return selections

    def __eq__(self, argument) -> bool:
        """
        Is true when initialization values of command equal
        initialization values of ``argument``.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Formats command.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Hashes command.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation of command.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _call_commands(self, voice, divisions_consumed, rhythm_maker):
        for command in self.commands or []:
            if isinstance(command, rmakers.CacheStateCommand):
                rhythm_maker._cache_state(voice, divisions_consumed)
                rhythm_maker._already_cached_state = True
                continue
            elif isinstance(command, rmakers.ForceRestCommand):
                command(voice, tag=self.tag)
            else:
                command(voice, tag=self.tag)

    ### PUBLIC PROPERTIES ###

    @property
    def assignments(self):
        """
        Gets assignments.
        """
        return self._assignments

    @property
    def commands(self):
        """
        Gets commands.
        """
        return self._commands

    @property
    def tag(self) -> typing.Optional[str]:
        """
        Gets tag.
        """
        return self._tag


class PitchFirstRhythmMaker(object):
    r"""
    Pitch-first rhythm-maker.

    >>> from abjadext import rmakers

    ..  container:: example

        Sixteenths and eighths:

        >>> rhythm_maker = baca.PitchFirstCommand(
        ...     baca.pitch_first([1, 1, 2], 16),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10, 8]]
        >>> selections = rhythm_maker(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/16
                    s1 * 5/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d'16
                        bf'8
                        af'16
                        ]
                    }
                }
            >>

        >>> collections = [[18, 16, 15, 20, 19]]
        >>> selections = rhythm_maker(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/8
                    s1 * 3/8
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        fs''16
                        [
                        e''16
                        ef''8
                        af''16
                        g''16
                        ]
                    }
                }
            >>

        >>> collections = [[9]]
        >>> selections = rhythm_maker(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 1/16
                    s1 * 1/16
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        a'16
                    }
                }
            >>

        >>> collections = [[0, 2, 10, 8], [18, 16, 15, 20, 19], [9]]
        >>> selections = rhythm_maker(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 13/16
                    s1 * 13/16
                }
                \new Staff
                {
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
                }
            >>

    ..  container:: example

        Silences every third logical tie:

        >>> rhythm_maker = baca.PitchFirstCommand(
        ...     baca.pitch_first([1, 1, 2], 16),
        ...     rmakers.force_rest(baca.lts().get([2], 3)),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selections = rhythm_maker(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/4
                    s1 * 3/4
                }
                \new Staff
                {
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
                }
            >>

    ..  container:: example

        Silences first and last logical ties:

        >>> rhythm_maker = baca.PitchFirstCommand(
        ...     baca.pitch_first([1, 1, 2], 16),
        ...     rmakers.force_rest(baca.lt(0)),
        ...     rmakers.force_rest(baca.lt(-1)),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selections = rhythm_maker(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/4
                    s1 * 3/4
                }
                \new Staff
                {
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
                }
            >>

    ..  container:: example

        No rest commands:

        >>> rhythm_maker = baca.PitchFirstCommand(
        ...     baca.pitch_first([1, 1, 2], 16),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selections = rhythm_maker(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/4
                    s1 * 3/4
                }
                \new Staff
                {
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
                }
            >>

    ..  container:: example

        Silences every other division:

        >>> rhythm_maker = baca.PitchFirstCommand(
        ...     baca.pitch_first([1, 1, 2], 16),
        ...     rmakers.force_rest(baca.tuplets().get([1], 2)),
        ...     rmakers.rewrite_rest_filled(),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selections = rhythm_maker(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/4
                    s1 * 3/4
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d'16
                        bf'8
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        r4.
                    }
                    \scaleDurations #'(1 . 1) {
                        a'8
                    }
                }
            >>

    ..  container:: example

        Sustains every other division:

        >>> tuplets = selector=baca.tuplets().get([1], 2)
        >>> rhythm_maker = baca.PitchFirstCommand(
        ...     baca.pitch_first([1, 1, 2], 16),
        ...     rmakers.tie(tuplets.map(baca.leaves()[:-1])),
        ...     rmakers.rewrite_sustained(),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selections = rhythm_maker(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/4
                    s1 * 3/4
                }
                \new Staff
                {
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d'16
                        bf'8
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        fs''4.
                    }
                    \scaleDurations #'(1 . 1) {
                        a'8
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Classes"

    __slots__ = (
        "_acciaccatura",
        "_affix",
        "_next_attack",
        "_next_segment",
        "_signature",
        "_spelling",
        "_state",
        "_talea",
        "_time_treatments",
    )

    _state_variables = ("_next_attack", "_next_segment")

    ### INITIALIZER ###

    def __init__(
        self,
        talea: rmakers.Talea,
        acciaccatura: AcciaccaturaSpecifier = None,
        affix: "RestAffixSpecifier" = None,
        signature: int = None,
        spelling: rmakers.Spelling = None,
        time_treatments: typing.Sequence[
            typing.Union[int, str, abjad.Duration]
        ] = None,
    ):
        if acciaccatura is not None:
            assert isinstance(acciaccatura, AcciaccaturaSpecifier), repr(
                acciaccatura
            )
        self._acciaccatura = acciaccatura
        if affix is not None:
            if not isinstance(affix, RestAffixSpecifier):
                message = "must be rest affix specifier:\n"
                message += f"   {repr(affix)}"
                raise Exception(message)
        self._affix = affix
        self._next_attack = 0
        self._next_segment = 0
        if signature is not None:
            assert isinstance(signature, int), repr(signature)
        self._signature = signature
        if spelling is not None:
            assert isinstance(spelling, rmakers.Spelling)
        self._spelling = spelling
        self._state = abjad.OrderedDict()
        if not isinstance(talea, rmakers.Talea):
            raise TypeError(f"must be talea: {talea!r}.")
        self._talea = talea
        if time_treatments is not None:
            for time_treatment in time_treatments:
                if not self._is_time_treatment(time_treatment):
                    raise Exception(f"bad time treatment: {time_treatment!r}.")
        self._time_treatments = time_treatments

    ### SPECIAL METHODS ###

    def __call__(
        self,
        collections: list,
        collection_index: int = None,
        state: abjad.OrderedDict = None,
        total_collections: int = None,
    ) -> abjad.Selection:
        r"""
        Calls rhythm-maker on ``collections``.

        ..  container:: example

            Without state manifest:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1, 1, 2], 16),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            With state manifest:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1, 1, 2], 16),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> state = {'_next_attack': 2}
            >>> selections = rhythm_maker(
            ...     collections,
            ...     state=state,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
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
                    }
                >>

        """
        prototype = (list,)
        assert isinstance(collections, prototype), repr(collections)
        self._state = state or abjad.OrderedDict()
        self._apply_state(state=state)
        tuplets = self._make_music(
            collections,
            collection_index=collection_index,
            total_collections=total_collections,
        )
        selections = [abjad.select(_) for _ in tuplets]
        ###return selections
        ###raise Exception(selections, "SSS")
        divisions_consumed = len(tuplets)
        durations = [abjad.inspect(_).duration() for _ in tuplets]
        time_signatures = [abjad.TimeSignature(_) for _ in durations]
        staff = rmakers.RhythmMaker._make_staff(time_signatures)
        voice = staff["MusicVoice"]
        voice.extend(tuplets)
        # self._check_wellformedness(selections)
        selections = abjad.select(voice[:]).group_by_measure()
        assert isinstance(selections, abjad.Selection)
        voice[:] = []
        assert isinstance(selections, abjad.Selection)
        return selections

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of rhythm-maker equal
        initialization values of ``argument``.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes rhythm-maker.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __format__(self, format_specification="") -> str:
        """
        Formats rhythm-maker.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _add_rest_affixes(
        leaves,
        talea,
        rest_prefix,
        rest_suffix,
        affix_skips_instead_of_rests,
        increase_durations,
    ):
        if rest_prefix:
            durations = [(_, talea.denominator) for _ in rest_prefix]
            maker = abjad.LeafMaker(
                increase_monotonic=increase_durations,
                skips_instead_of_rests=affix_skips_instead_of_rests,
            )
            leaves_ = maker([None], durations)
            leaves[0:0] = leaves_
        if rest_suffix:
            durations = [(_, talea.denominator) for _ in rest_suffix]
            maker = abjad.LeafMaker(
                increase_monotonic=increase_durations,
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
        if not self.acciaccatura:
            return
        pattern = self.acciaccatura._get_pattern()
        if pattern.matches_index(collection_index, total_collections):
            return self.acciaccatura

    def _get_spelling_specifier(self):
        if self.spelling is not None:
            return self.spelling
        return rmakers.Spelling()

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
        elif argument in ("accel", "rit"):
            return True
        return False

    @classmethod
    def _make_accelerando(class_, leaf_selection, accelerando_indicator):
        assert accelerando_indicator in ("accel", "rit")
        tuplet = abjad.Tuplet((1, 1), leaf_selection, hide=True)
        if len(tuplet) == 1:
            return tuplet
        durations = [abjad.inspect(_).duration() for _ in leaf_selection]
        if accelerando_indicator == "accel":
            exponent = 0.625
        elif accelerando_indicator == "rit":
            exponent = 1.625
        multipliers = class_._make_accelerando_multipliers(durations, exponent)
        assert len(leaf_selection) == len(multipliers)
        for multiplier, leaf in zip(multipliers, leaf_selection):
            leaf.multiplier = multiplier
        if rmakers.FeatherBeamCommand._is_accelerando(leaf_selection):
            abjad.override(leaf_selection[0]).beam.grow_direction = abjad.Right
        elif rmakers.FeatherBeamCommand._is_ritardando(leaf_selection):
            abjad.override(leaf_selection[0]).beam.grow_direction = abjad.Left
        duration = abjad.inspect(tuplet).duration()
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
        # print(total_duration, start_offsets)
        start_offsets = [_ / total_duration for _ in start_offsets]
        # print(total_duration, start_offsets)
        start_offsets_ = []
        rhythm_maker_class = rmakers.AccelerandoRhythmMaker
        for start_offset in start_offsets:
            start_offset_ = rhythm_maker_class._interpolate_exponential(
                0, total_duration, start_offset, exponent
            )
            start_offsets_.append(start_offset_)
        # print(start_offsets_)
        # start_offsets_ = [float(total_duration * _) for _ in start_offsets_]
        start_offsets_.append(float(total_duration))
        durations_ = abjad.mathtools.difference_series(start_offsets_)
        durations_ = rhythm_maker_class._round_durations(durations_, 2 ** 10)
        durations_ = class_._fix_rounding_error(durations_, total_duration)
        multipliers = []
        assert len(durations) == len(durations_)
        for duration_, duration in zip(durations_, durations):
            multiplier = duration_ / duration
            multiplier = abjad.Multiplier(multiplier)
            multiplier = multiplier.with_denominator(2 ** 10)
            multipliers.append(multiplier)
        return multipliers

    def _make_music(
        self, collections, collection_index=None, total_collections=None
    ) -> typing.List[abjad.Tuplet]:
        segment_count = len(collections)
        tuplets = []
        if collection_index is None:
            for i, segment in enumerate(collections):
                if self.affix is not None:
                    result = self.affix(i, segment_count)
                    rest_prefix, rest_suffix = result
                    affix_skips_instead_of_rests = (
                        self.affix.skips_instead_of_rests
                    )
                else:
                    rest_prefix, rest_suffix = None, None
                    affix_skips_instead_of_rests = None
                tuplet = self._make_tuplet(
                    segment,
                    rest_prefix=rest_prefix,
                    rest_suffix=rest_suffix,
                    affix_skips_instead_of_rests=affix_skips_instead_of_rests,
                )
                tuplets.append(tuplet)
        else:
            assert len(collections) == 1, repr(collections)
            segment = collections[0]
            if self.affix is not None:
                result = self.affix(collection_index, total_collections)
                rest_prefix, rest_suffix = result
                affix_skips_instead_of_rests = (
                    self.affix.skips_instead_of_rests
                )
            else:
                rest_prefix, rest_suffix = None, None
                affix_skips_instead_of_rests = None
            tuplet = self._make_tuplet(
                segment,
                rest_prefix=rest_prefix,
                rest_suffix=rest_suffix,
                affix_skips_instead_of_rests=affix_skips_instead_of_rests,
            )
            tuplets.append(tuplet)
        assert all(isinstance(_, abjad.Tuplet) for _ in tuplets)
        return tuplets

    def _make_tuplet(
        self,
        segment,
        rest_prefix=None,
        rest_suffix=None,
        affix_skips_instead_of_rests=None,
    ):
        collection_index = self._next_segment
        acciaccatura = self.acciaccatura
        self._next_segment += 1
        talea = self._get_talea()
        leaves = []
        specifier = self._get_spelling_specifier()
        increase_durations = specifier.increase_monotonic
        current_selection = self._next_segment - 1
        time_treatment = self._get_time_treatments()[current_selection]
        if time_treatment is None:
            time_treatment = 0
        grace_containers = None
        if acciaccatura is not None:
            grace_containers, segment = acciaccatura(segment)
            assert len(grace_containers) == len(segment)
        for pitch_expression in segment:
            prototype = abjad.NumberedPitchClass
            if isinstance(pitch_expression, prototype):
                pitch_expression = pitch_expression.number
            count = self._next_attack
            while talea[count] < 0:
                self._next_attack += 1
                duration = -talea[count]
                maker = abjad.LeafMaker(increase_monotonic=increase_durations)
                leaves_ = maker([None], [duration])
                leaves.extend(leaves_)
                count = self._next_attack
            self._next_attack += 1
            duration = talea[count]
            assert 0 < duration, repr(duration)
            skips_instead_of_rests = False
            if (
                isinstance(pitch_expression, tuple)
                and len(pitch_expression) == 2
                and pitch_expression[-1] in (None, "skip")
            ):
                multiplier = pitch_expression[0]
                duration = abjad.Duration(1, talea.denominator)
                duration *= multiplier
                if pitch_expression[-1] == "skip":
                    skips_instead_of_rests = True
                pitch_expression = None
            maker = abjad.LeafMaker(
                increase_monotonic=increase_durations,
                skips_instead_of_rests=skips_instead_of_rests,
            )
            leaves_ = maker([pitch_expression], [duration])
            leaves.extend(leaves_)
            count = self._next_attack
            while talea[count] < 0 and not count % len(talea) == 0:
                self._next_attack += 1
                duration = -talea[count]
                maker = abjad.LeafMaker(increase_monotonic=increase_durations)
                leaves_ = maker([None], [duration])
                leaves.extend(leaves_)
                count = self._next_attack
        leaves = self._add_rest_affixes(
            leaves,
            talea,
            rest_prefix,
            rest_suffix,
            affix_skips_instead_of_rests,
            increase_durations,
        )
        leaf_selection = abjad.select(leaves)
        if isinstance(time_treatment, int):
            tuplet = self._make_tuplet_with_extra_count(
                leaf_selection, time_treatment, talea.denominator
            )
        elif time_treatment in ("accel", "rit"):
            tuplet = self._make_accelerando(leaf_selection, time_treatment)
        elif isinstance(time_treatment, abjad.Ratio):
            numerator, denominator = time_treatment.numbers
            multiplier = abjad.NonreducedFraction((denominator, numerator))
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
        elif isinstance(time_treatment, abjad.Multiplier):
            tuplet = abjad.Tuplet(time_treatment, leaf_selection)
        elif time_treatment.__class__ is abjad.Duration:
            tuplet_duration = time_treatment
            contents_duration = abjad.inspect(leaf_selection).duration()
            multiplier = tuplet_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
            if not tuplet.multiplier.normalized():
                tuplet.normalize_multiplier()
        else:
            raise Exception(f"bad time treatment: {time_treatment!r}.")
        assert isinstance(tuplet, abjad.Tuplet)
        if grace_containers is not None:
            logical_ties = abjad.iterate(tuplet).logical_ties()
            pairs = zip(grace_containers, logical_ties)
            for grace_container, logical_tie in pairs:
                if grace_container is None:
                    continue
                abjad.attach(grace_container, logical_tie.head, tag="PFRM_1")
        if tuplet.trivial():
            tuplet.hide = True
        assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
        return tuplet

    @staticmethod
    def _make_tuplet_with_extra_count(
        leaf_selection, extra_count, denominator
    ):
        contents_duration = abjad.inspect(leaf_selection).duration()
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
            new_contents_count, contents_count
        )
        if not tuplet_multiplier.normalized():
            message = f"{leaf_selection!r} gives {tuplet_multiplier}"
            message += " with {contents_count} and {new_contents_count}."
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
    def acciaccatura(self) -> typing.Optional[AcciaccaturaSpecifier]:
        r"""
        Gets acciaccatura specifier.

        ..  container:: example

            Graced quarters:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1],
            ...         4,
            ...         acciaccatura=baca.AcciaccaturaSpecifier(),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
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
                                fs''16
                                [                                                                        %! AcciaccaturaSpecifier
                                e''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            ef''4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! AcciaccaturaSpecifier
                                g''16
                                a'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            c'4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! AcciaccaturaSpecifier
                                bf'16
                                fs''16
                                e''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            ef''4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! AcciaccaturaSpecifier
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            bf'4
                        }
                    }
                >>

        ..  container:: example

            Graced rests:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1],
            ...         4,
            ...         acciaccatura=baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier()
            ...             ),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [None],
            ...     [0, None],
            ...     [2, 10, None],
            ...     [18, 16, 15, None],
            ...     [20, 19, 9, 0, None],
            ...     [2, 10, 18, 16, 15, None],
            ...     [20, 19, 9, 0, 2, 10, None],
            ...     ]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 7/4
                        s1 * 7/4
                    }
                    \new Staff
                    {
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
                                d'16
                                [                                                                        %! AcciaccaturaSpecifier
                                bf'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! AcciaccaturaSpecifier
                                e''16
                                ef''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! AcciaccaturaSpecifier
                                g''16
                                a'16
                                c'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! AcciaccaturaSpecifier
                                bf'16
                                fs''16
                                e''16
                                ef''16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! AcciaccaturaSpecifier
                                g''16
                                a'16
                                c'16
                                d'16
                                bf'16
                                ]                                                                        %! AcciaccaturaSpecifier
                            }
                            r4
                        }
                    }
                >>

        """
        return self._acciaccatura

    @property
    def affix(self) -> typing.Optional["RestAffixSpecifier"]:
        """
        Gets rest affix specifier.
        """
        return self._affix

    @property
    def signature(self) -> typing.Optional[int]:
        r"""
        Gets (time) signature (denominator).

        ..  container:: example

            No denominator by default:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23, 17],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 3/4
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    b''16                                                                %! baca.MusicMaker.__call__
                                    f''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Denominator supplied at configuration time:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16, signature=16),
            ...     rmakers.beam(),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23, 17],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice_1', collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ...     time_signatures=[contribution.time_signature],
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 12/16
                        s1 * 3/4
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    b''16                                                                %! baca.MusicMaker.__call__
                                    f''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Denominator supplied at call time:

            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16, signature=8),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23, 17],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ...     time_signatures=[contribution.time_signature],
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 6/8
                        s1 * 3/4
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    b''16                                                                %! baca.MusicMaker.__call__
                                    f''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    [
                                    cs''16                                                               %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    af'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        """
        return self._signature

    @property
    def spelling(self) -> typing.Optional[rmakers.Spelling]:
        r"""
        Gets duration specifier.

        ..  container:: example

            Spells nonassignable durations with monontonically decreasing
            durations by default:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([4, 4, 5], 32),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 39/32
                        s1 * 39/32
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            Spells nonassignable durations with monontonically increasing
            durations:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [4, 4, 5],
            ...         32,
            ...         spelling=rmakers.Spelling(increase_monotonic=True),
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 39/32
                        s1 * 39/32
                    }
                    \new Staff
                    {
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
                    }
                >>

        """
        return self._spelling

    @property
    def talea(self) -> rmakers.Talea:
        r"""
        Gets talea.

        ..  container:: example

            With rests:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([3, -1, 2, 2], 16),
            ...     rmakers.beam(
            ...         beam_rests=True,
            ...         stemlet_length=1.5,
            ...     ),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
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
                            a'8
                        }
                    }
                >>

        ..  container:: example

            With very large nonassignable counts:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([29], 64),
            ...     rmakers.beam(),
            ...     rmakers.force_repeat_tie(),
            ... )

            >>> collections = [[0, 2]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 29/32
                        s1 * 29/32
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'4..
                            c'64
                            \repeatTie
                            d'4..
                            d'64
                            \repeatTie
                        }
                    }
                >>

        """
        return self._talea

    @property
    def time_treatments(
        self
    ) -> typing.Optional[
        typing.Sequence[typing.Union[int, str, abjad.Duration]]
    ]:
        r"""
        Gets time treatments.

        ..  container:: example

            One extra count per division:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1, 1, 2], 16, time_treatments=[1]),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            One missing count per division:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1, 1, 2], 16, time_treatments=[-1]),
            ...     rmakers.beam(),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 5/8
                        s1 * 5/8
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            Accelerandi:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1], 16, time_treatments=["accel"]),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 5/8
                        s1 * 5/8
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            Ritardandi:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1], 16, time_treatments=["rit"]),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 5/8
                        s1 * 5/8
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            Accelerandi followed by ritardandi:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first([1], 16, time_treatments=["accel", "rit"]),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0, 2],
            ...     [10, 18, 16, 15, 20],
            ...     [19, 9, 0, 2, 10, 18],
            ...     ]
            >>> selections = rhythm_maker(collections)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 5/8
                        s1 * 5/8
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            Mixed accelerandi, ritardandi and prolation:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1],
            ...         16,
            ...         time_treatments=['accel', -2, 'rit'],
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2],
            ...     [10, 18, 16, 15, 20],
            ...     [19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 5/8
                        s1 * 5/8
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            Specified by tuplet multiplier:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1],
            ...         8,
            ...         time_treatments=[abjad.Ratio((3, 2))],
            ...     ),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.override(staff).stem.direction = abjad.Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                <<
                    \new GlobalContext
                    {
                        \time 7/4
                        s1 * 7/4
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            Segment durations equal to a quarter:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1],
            ...         8,
            ...         time_treatments=[abjad.Duration(1, 4)],
            ...     ),
            ...     rmakers.denominator((1, 16)),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.override(staff).stem.direction = abjad.Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
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
                    }
                >>

        ..  container:: example

            Segment durations alternating between a quarter and a dotted
            quarter:

            >>> rhythm_maker = baca.PitchFirstCommand(
            ...     baca.pitch_first(
            ...         [1, 1, 2],
            ...         8,
            ...         time_treatments=[abjad.Duration(1, 4), abjad.Duration(3, 8)],
            ...     ),
            ...     rmakers.denominator((1, 16)),
            ...     rmakers.beam(),
            ... )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2],
            ...     [10, 18, 16, 15, 20],
            ...     [19, 9, 0, 2, 10],
            ...     ]
            >>> selections = rhythm_maker(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.override(staff).stem.direction = abjad.Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                <<
                    \new GlobalContext
                    {
                        \time 15/8
                        s1 * 15/8
                    }
                    \new Staff
                    {
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
                    }
                >>

        Time treatments defined equal to integers; positive multipliers;
        positive durations; and the strings ``'accel'`` and ``'rit'``.
        """
        return self._time_treatments


class RestAffixSpecifier(object):
    r"""
    Rest affix specifier.

    ..  container:: example

        Works together with negative-valued talea:

        >>> affix = baca.RestAffixSpecifier(
        ...     prefix=[2],
        ...     suffix=[3],
        ... )
        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([1, -1], 16, affix=affix, time_treatments=[1]),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     collections,
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> staff = lilypond_file[abjad.Score]
        >>> abjad.override(staff).tuplet_bracket.staff_padding = 4
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override TupletBracket.staff-padding = #4
            }
            <<
                \new GlobalContext
                {
                    s1 * 13/8
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/8 {                                                             %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                d'16                                                                 %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                bf'16                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 11/10 {                                                           %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                e''16                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                ef''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                g''16                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 6/5 {                                                             %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                r8.                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> affix = baca.RestAffixSpecifier(
        ...     prefix=[2],
        ...     suffix=[3],
        ... )
        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first([-1, 1], 16, affix=affix, time_treatments=[1]),
        ...     rmakers.beam(),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     collections,
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> staff = lilypond_file[abjad.Score]
        >>> abjad.override(staff).tuplet_bracket.staff_padding = 4
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override TupletBracket.staff-padding = #4
            }
            <<
                \new GlobalContext
                {
                    s1 * 13/8
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/8 {                                                             %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                d'16                                                                 %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                bf'16                                                                %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 11/10 {                                                           %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                e''16                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                ef''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                g''16                                                                %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 6/5 {                                                             %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                                r8.                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    ..  container:: example

        >>> baca.RestAffixSpecifier()
        RestAffixSpecifier()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_pattern", "_prefix", "_skips_instead_of_rests", "_suffix")

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        pattern: abjad.Pattern = None,
        prefix: typing.Sequence[int] = None,
        skips_instead_of_rests: bool = None,
        suffix: typing.Sequence[int] = None,
    ):
        if pattern is not None and not isinstance(pattern, abjad.Pattern):
            raise TypeError(f"pattern or none: {pattern!r}.")
        self._pattern = pattern
        if prefix is not None:
            assert all(isinstance(_, int) for _ in prefix)
        self._prefix = prefix
        if skips_instead_of_rests is not None:
            skips_instead_of_rests = bool(skips_instead_of_rests)
        self._skips_instead_of_rests = skips_instead_of_rests
        if suffix is not None:
            assert all(isinstance(_, int) for _ in suffix)
        self._suffix = suffix

    ### SPECIAL METHODS ###

    def __call__(
        self, collection_index: int, total_collections: int
    ) -> typing.Tuple[
        typing.Optional[abjad.IntegerSequence],
        typing.Optional[abjad.IntegerSequence],
    ]:
        r"""
        Calls rest affix specifier on ``collection_index`` and
        ``total_collections``.

        ..  container:: example

            With time treatments:

            >>> affix = baca.RestAffixSpecifier(prefix=[1], suffix=[1])
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16, affix=affix, time_treatments=[-1]),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 9/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 3/4 {                                                             %! baca.MusicMaker.__call__
                                    r16                                                                  %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \times 4/5 {                                                             %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    r16                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        """
        if self.pattern is None:
            if (
                collection_index == 0
                and collection_index == total_collections - 1
            ):
                return self.prefix, self.suffix
            if collection_index == 0:
                return self.prefix, None
            if collection_index == total_collections - 1:
                return None, self.suffix
        elif self.pattern.matches_index(collection_index, total_collections):
            return self.prefix, self.suffix
        return None, None

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Formats Abjad object.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r"""
        Gets pattern.

        ..  container:: example

            Treats entire figure when pattern is none:

            >>> affix = baca.RestAffixSpecifier(
            ...     prefix=[1],
            ...     suffix=[2],
            ... )
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16, affix=affix, time_treatments=[1]),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 15/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 5/4 {                                                             %! baca.MusicMaker.__call__
                                    r16                                                                  %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 6/5 {                                                             %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 4/3 {                                                             %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    r8                                                                   %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Treats entire figure (of only one segment) when pattern is none:

            >>> affix = baca.RestAffixSpecifier(
            ...     prefix=[1],
            ...     suffix=[2],
            ... )
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16, affix=affix, time_treatments=[1]),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[18, 16, 15, 20, 19]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 9/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 9/8 {                                                             %! baca.MusicMaker.__call__
                                    r16                                                                  %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                    r8                                                                   %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Treats first segment and last segment in figure:

            >>> affix = baca.RestAffixSpecifier(
            ...     pattern=abjad.Pattern(indices=[0, -1]),
            ...     prefix=[1],
            ...     suffix=[2],
            ... )
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16, affix=affix, time_treatments=[1]),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 9/8
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 7/6 {                                                             %! baca.MusicMaker.__call__
                                    r16                                                                  %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                    r8                                                                   %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 6/5 {                                                             %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 5/4 {                                                             %! baca.MusicMaker.__call__
                                    r16                                                                  %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    r8                                                                   %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        ..  container:: example

            Treats every segment in figure:

            >>> affix = baca.RestAffixSpecifier(
            ...     pattern=abjad.index_all(),
            ...     prefix=[1],
            ...     suffix=[2],
            ... )
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16, affix=affix, time_treatments=[1]),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 21/16
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 7/6 {                                                             %! baca.MusicMaker.__call__
                                    r16                                                                  %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                    r8                                                                   %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 9/8 {                                                             %! baca.MusicMaker.__call__
                                    r16                                                                  %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                    r8                                                                   %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                                \times 5/4 {                                                             %! baca.MusicMaker.__call__
                                    r16                                                                  %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    r8                                                                   %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        Set to pattern or none.

        Defaults to none.

        Returns pattern or none.
        """
        return self._pattern

    @property
    def prefix(self):
        r"""
        Gets prefix.

        ..  container:: example

            >>> affix = baca.RestAffixSpecifier(prefix=[3])
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16, affix=affix),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 3/4
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    r8.                                                                  %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        Set to list of positive integers or none.

        Defaults to none.

        Returns list of positive integers or none.
        """
        return self._prefix

    @property
    def skips_instead_of_rests(self):
        """
        Is true when command makes skips instead of rests.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        """
        return self._skips_instead_of_rests

    @property
    def suffix(self):
        r"""
        Gets suffix.

        ..  container:: example

            >>> affix = baca.RestAffixSpecifier(suffix=[3])
            >>> music_maker = baca.MusicMaker(
            ...     baca.pitch_first([1], 16, affix=affix),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     )
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     contribution.voice_to_selection,
            ...     attach_lilypond_voice_commands=True,
            ... )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        s1 * 3/4
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice_1"
                        {
                            \voiceOne
                            {                                                                            %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    c'16                                                                 %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                                 %! baca.MusicMaker.__call__
                                    bf'16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    fs''16                                                               %! baca.MusicMaker.__call__
                                    [
                                    e''16                                                                %! baca.MusicMaker.__call__
                                    ef''16                                                               %! baca.MusicMaker.__call__
                                    af''16                                                               %! baca.MusicMaker.__call__
                                    g''16                                                                %! baca.MusicMaker.__call__
                                    ]
                                }                                                                        %! baca.MusicMaker.__call__
                                \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                    a'16                                                                 %! baca.MusicMaker.__call__
                                    r8.                                                                  %! baca.MusicMaker.__call__
                                }                                                                        %! baca.MusicMaker.__call__
                            }                                                                            %! baca.MusicMaker.__call__
                        }
                    >>
                >>

        Set to list of positive integers or none.

        Defaults to none.

        Returns list of positive integers or none.
        """
        return self._suffix


### FACTORY FUNCTIONS ###


def anchor(
    remote_voice_name: str,
    remote_selector: abjad.SelectorTyping = None,
    local_selector: abjad.SelectorTyping = None,
) -> AnchorSpecifier:
    """
    Anchors music in this figure (filtered by ``local_selector``) to
    start offset of ``remote_voice_name`` (filtered by
    ``remote_selector``).
    """
    return AnchorSpecifier(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
    )


def anchor_after(
    remote_voice_name: str,
    remote_selector: abjad.SelectorTyping = None,
    local_selector: abjad.SelectorTyping = None,
) -> AnchorSpecifier:
    """
    Anchors music in this figure (filtered by ``local_selector``) to
    stop offset of ``remote_voice_name`` (filtered by ``remote_selector``).
    """
    return AnchorSpecifier(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
    )


def anchor_to_figure(figure_name: str) -> AnchorSpecifier:
    """
    Anchors music in this figure to start of ``figure_name``.

    :param figure_name: figure name.
    """
    return AnchorSpecifier(figure_name=figure_name)


def coat(pitch: typing.Union[int, str, abjad.Pitch]) -> Coat:
    r"""
    Coats ``pitch``.

    ..  container:: example

        Coats pitches:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.imbricate(
        ...         'Voice_2',
        ...         [baca.coat(0), baca.coat(2), 10, 0, 2],
        ...         rmakers.beam_groups(),
        ...     ),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     3 * [[0, 2, 10]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 3/4
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \times 4/5 {                                                             %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                bf'16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \times 2/3 {                                                             %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                bf'16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 6/7 {                                                             %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                bf'16                                                                %! baca.MusicMaker.__call__
                                ]
                                r4                                                                   %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                    \context Voice = "Voice_2"
                    {
                        \voiceTwo
                        {                                                                            %! baca.MusicMaker.__call__
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \times 4/5 {                                                             %! baca.MusicMaker.__call__
                                s8                                                                   %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                bf'16                                                                %! baca.MusicMaker.__call__
                                [
                            }                                                                        %! baca.MusicMaker.__call__
                            \times 2/3 {                                                             %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                c'16                                                                 %! baca.MusicMaker.__call__
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                d'16                                                                 %! baca.MusicMaker.__call__
                                ]
                                s16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 6/7 {                                                             %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s4                                                                   %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    """
    return Coat(pitch)


def imbricate(
    voice_name: str,
    segment: typing.List,
    *specifiers: typing.Any,
    allow_unused_pitches: bool = None,
    by_pitch_class: bool = None,
    extend_beam: bool = None,
    hocket: bool = None,
    selector: abjad.SelectorTyping = None,
    truncate_ties: bool = None,
):
    r"""
    Imbricates ``segment`` in voice with ``voice_name``.

    ..  container:: example

        Imbricates segment:

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...         ),
        ...     rmakers.beam(),
        ...     baca.imbricate('Voice_2', [10, 20, 19]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 11/8
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.staff-padding = #5                           %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                                r8                                                                   %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                ]
                                bf'4                                                                 %! baca.MusicMaker.__call__
                                ~
                                bf'16                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                e''16                                                                %! baca.MusicMaker.__call__
                                ]
                                ef''4                                                                %! baca.MusicMaker.__call__
                                ~
                                ef''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                [
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \times 4/5 {                                                             %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                                r4                                                                   %! baca.MusicMaker.__call__
                                \revert TupletBracket.staff-padding                                  %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                    \context Voice = "Voice_2"
                    {
                        \voiceTwo
                        {                                                                            %! baca.MusicMaker.__call__
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                s8                                                                   %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                bf'4                                                                 %! baca.MusicMaker.__call__
                                ~
                                bf'16                                                                %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s4                                                                   %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                [
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \times 4/5 {                                                             %! baca.MusicMaker.__call__
                                s16                                                                  %! baca.MusicMaker.__call__
                                s4                                                                   %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    """
    return Imbrication(
        voice_name,
        segment,
        *specifiers,
        allow_unused_pitches=allow_unused_pitches,
        by_pitch_class=by_pitch_class,
        extend_beam=extend_beam,
        hocket=hocket,
        selector=selector,
        truncate_ties=truncate_ties,
    )


def nest(time_treatments: typing.Sequence = None,) -> Nesting:
    r"""
    Nests music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.nest('+4/16'),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 13/8
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 13/11 {                                                           %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                       %! baca.MusicMaker.__call__
                                \times 9/10 {                                                        %! baca.MusicMaker.__call__
                                    \override TupletBracket.staff-padding = #5                       %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                                    r8                                                               %! baca.MusicMaker.__call__
                                    c'16                                                             %! baca.MusicMaker.__call__
                                    [
                                    d'16                                                             %! baca.MusicMaker.__call__
                                    ]
                                    bf'4                                                             %! baca.MusicMaker.__call__
                                    ~
                                    bf'16                                                            %! baca.MusicMaker.__call__
                                    r16                                                              %! baca.MusicMaker.__call__
                                }                                                                    %! baca.MusicMaker.__call__
                                \tweak text #tuplet-number::calc-fraction-text                       %! baca.MusicMaker.__call__
                                \times 9/10 {                                                        %! baca.MusicMaker.__call__
                                    fs''16                                                           %! baca.MusicMaker.__call__
                                    [
                                    e''16                                                            %! baca.MusicMaker.__call__
                                    ]
                                    ef''4                                                            %! baca.MusicMaker.__call__
                                    ~
                                    ef''16                                                           %! baca.MusicMaker.__call__
                                    r16                                                              %! baca.MusicMaker.__call__
                                    af''16                                                           %! baca.MusicMaker.__call__
                                    [
                                    g''16                                                            %! baca.MusicMaker.__call__
                                    ]
                                }                                                                    %! baca.MusicMaker.__call__
                                \times 4/5 {                                                         %! baca.MusicMaker.__call__
                                    a'16                                                             %! baca.MusicMaker.__call__
                                    r4                                                               %! baca.MusicMaker.__call__
                                    \revert TupletBracket.staff-padding                              %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                                }                                                                    %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    """
    if not isinstance(time_treatments, list):
        time_treatments = [time_treatments]
    return Nesting(lmr_specifier=None, time_treatments=time_treatments)


def pitch_first(
    counts: abjad.IntegerSequence,
    denominator: int,
    *,
    acciaccatura=None,
    affix: RestAffixSpecifier = None,
    pattern=None,
    signature: int = None,
    spelling: rmakers.Spelling = None,
    thread: bool = None,
    time_treatments=None,
) -> PitchFirstAssignment:
    """
    Makes pitch-first assignment.
    """
    return PitchFirstAssignment(
        PitchFirstRhythmMaker(
            rmakers.Talea(counts=counts, denominator=denominator),
            acciaccatura=acciaccatura,
            affix=affix,
            signature=signature,
            spelling=spelling,
            time_treatments=time_treatments,
        ),
        pattern=pattern,
        thread=thread,
    )


def rests_after(counts: typing.Sequence[int]) -> RestAffixSpecifier:
    r"""
    Makes rests after music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_after([2]),
        ...         time_treatments=[-1],
        ...         ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 9/8
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 7/8 {                                                             %! baca.MusicMaker.__call__
                                \override TupletBracket.staff-padding = #5                           %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                ]
                                bf'4                                                                 %! baca.MusicMaker.__call__
                                ~
                                bf'16                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                e''16                                                                %! baca.MusicMaker.__call__
                                ]
                                ef''4                                                                %! baca.MusicMaker.__call__
                                ~
                                ef''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                [
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \times 2/3 {                                                             %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                \revert TupletBracket.staff-padding                                  %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    """
    return RestAffixSpecifier(suffix=counts)


def rests_around(
    prefix: typing.List[int], suffix: typing.List[int]
) -> RestAffixSpecifier:
    r"""
    Makes rests around music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [2]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 5/4
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.staff-padding = #5                           %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                                r8                                                                   %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                ]
                                bf'4                                                                 %! baca.MusicMaker.__call__
                                ~
                                bf'16                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                e''16                                                                %! baca.MusicMaker.__call__
                                ]
                                ef''4                                                                %! baca.MusicMaker.__call__
                                ~
                                ef''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                [
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \times 2/3 {                                                             %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                                r8                                                                   %! baca.MusicMaker.__call__
                                \revert TupletBracket.staff-padding                                  %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    """
    return RestAffixSpecifier(prefix=prefix, suffix=suffix)


def rests_before(counts: typing.List[int]) -> RestAffixSpecifier:
    r"""
    Makes rests before music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_before([2]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 19/16
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.staff-padding = #5                           %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                                r8                                                                   %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                ]
                                bf'4                                                                 %! baca.MusicMaker.__call__
                                ~
                                bf'16                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                e''16                                                                %! baca.MusicMaker.__call__
                                ]
                                ef''4                                                                %! baca.MusicMaker.__call__
                                ~
                                ef''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                [
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                                \revert TupletBracket.staff-padding                                  %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    """
    return RestAffixSpecifier(prefix=counts)


def resume() -> AnchorSpecifier:
    """
    Resumes music at next offset across all voices in score.
    """
    return AnchorSpecifier()


def resume_after(remote_voice_name) -> AnchorSpecifier:
    """
    Resumes music after remote selection.
    """
    return AnchorSpecifier(
        remote_selector="baca.leaf(-1)",
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
    )


def skips_after(counts: typing.List[int]) -> RestAffixSpecifier:
    r"""
    Makes skips after music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.skips_after([2]),
        ...         time_treatments=[-1],
        ...         ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 9/8
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 7/8 {                                                             %! baca.MusicMaker.__call__
                                \override TupletBracket.staff-padding = #5                           %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                ]
                                bf'4                                                                 %! baca.MusicMaker.__call__
                                ~
                                bf'16                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                e''16                                                                %! baca.MusicMaker.__call__
                                ]
                                ef''4                                                                %! baca.MusicMaker.__call__
                                ~
                                ef''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                [
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \times 2/3 {                                                             %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                                s8                                                                   %! baca.MusicMaker.__call__
                                \revert TupletBracket.staff-padding                                  %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    """
    return RestAffixSpecifier(skips_instead_of_rests=True, suffix=counts)


def skips_around(
    prefix: typing.List[int], suffix: typing.List[int]
) -> RestAffixSpecifier:
    r"""
    Makes skips around music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.skips_around([2], [2]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 5/4
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.staff-padding = #5                           %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                                s8                                                                   %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                ]
                                bf'4                                                                 %! baca.MusicMaker.__call__
                                ~
                                bf'16                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                e''16                                                                %! baca.MusicMaker.__call__
                                ]
                                ef''4                                                                %! baca.MusicMaker.__call__
                                ~
                                ef''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                [
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \times 2/3 {                                                             %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                                s8                                                                   %! baca.MusicMaker.__call__
                                \revert TupletBracket.staff-padding                                  %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    """
    return RestAffixSpecifier(
        prefix=prefix, skips_instead_of_rests=True, suffix=suffix
    )


def skips_before(counts: typing.List[int],) -> RestAffixSpecifier:
    r"""
    Makes skips before music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker(
        ...     baca.pitch_first(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.skips_before([2]),
        ...         time_treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(5),
        ... )
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     )
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     contribution.voice_to_selection,
        ...     attach_lilypond_voice_commands=True,
        ... )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    s1 * 19/16
                }
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {                                                                            %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                \override TupletBracket.staff-padding = #5                           %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                                s8                                                                   %! baca.MusicMaker.__call__
                                c'16                                                                 %! baca.MusicMaker.__call__
                                [
                                d'16                                                                 %! baca.MusicMaker.__call__
                                ]
                                bf'4                                                                 %! baca.MusicMaker.__call__
                                ~
                                bf'16                                                                %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                            }                                                                        %! baca.MusicMaker.__call__
                            \tweak text #tuplet-number::calc-fraction-text                           %! baca.MusicMaker.__call__
                            \times 9/10 {                                                            %! baca.MusicMaker.__call__
                                fs''16                                                               %! baca.MusicMaker.__call__
                                [
                                e''16                                                                %! baca.MusicMaker.__call__
                                ]
                                ef''4                                                                %! baca.MusicMaker.__call__
                                ~
                                ef''16                                                               %! baca.MusicMaker.__call__
                                r16                                                                  %! baca.MusicMaker.__call__
                                af''16                                                               %! baca.MusicMaker.__call__
                                [
                                g''16                                                                %! baca.MusicMaker.__call__
                                ]
                            }                                                                        %! baca.MusicMaker.__call__
                            \scaleDurations #'(1 . 1) {                                              %! baca.MusicMaker.__call__
                                a'16                                                                 %! baca.MusicMaker.__call__
                                \revert TupletBracket.staff-padding                                  %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                            }                                                                        %! baca.MusicMaker.__call__
                        }                                                                            %! baca.MusicMaker.__call__
                    }
                >>
            >>

    """
    return RestAffixSpecifier(prefix=counts, skips_instead_of_rests=True)
