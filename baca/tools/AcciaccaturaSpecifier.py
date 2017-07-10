# -*- coding: utf-8 -*-
import abjad
import baca


class AcciaccaturaSpecifier(abjad.abctools.AbjadObject):
    r'''Acciaccatura specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Default acciaccatura specifier:

        ::

            >>> rhythm_maker = baca.MusicRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier()
            ...         ],
            ...     talea=abjad.rhythmmakertools.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

        ::

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
            >>> show(lilypond_file) # doctest: +SKIP 

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff {
                {
                    \time 3/4
                    {
                        c'8
                    }
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    {
                        \acciaccatura {
                            fs''16 [
                            e''16 ]
                        }
                        ef''8
                    }
                    {
                        \acciaccatura {
                            af''16 [
                            g''16
                            a'16 ]
                        }
                        c'8
                    }
                    {
                        \acciaccatura {
                            d'16 [
                            bf'16
                            fs''16
                            e''16 ]
                        }
                        ef''8
                    }
                    {
                        \acciaccatura {
                            af''16 [
                            g''16
                            a'16
                            c'16
                            d'16 ]
                        }
                        bf'8
                    }
                }
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_durations',
        '_lmr_specifier',
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        durations=None,
        lmr_specifier=None,
        pattern=None,
        ):
        if durations is not None:
            assert isinstance(durations, list), repr(durations)
            durations = [abjad.Duration(_) for _ in durations]
        self._durations = durations
        if lmr_specifier is not None:
            prototype = baca.LMRSpecifier
            assert isinstance(lmr_specifier, prototype)
        self._lmr_specifier = lmr_specifier
        if pattern is not None:
            prototype = (
                abjad.Pattern,
                abjad.CompoundPattern,
                )
            assert isinstance(pattern, prototype), repr(pattern)
        self._pattern = pattern

    ### SPECIAL METHODS ###

    def __call__(self, collection=None):
        r'''Calls acciaccatura specifier on `collection`.

        Returns acciaccatura container together with new collection.
        '''
        prototype = (list, abjad.pitchtools.Segment)
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
                abjad.attach(abjad.Beam(), acciaccatura_container[:])
            acciaccatura_containers.append(acciaccatura_container)
        assert len(acciaccatura_containers) == len(collection)
        return acciaccatura_containers, collection

    ### PRIVATE METHODS ###

    def _get_durations(self):
        return self.durations or [abjad.Duration(1, 16)]

    def _get_lmr_specifier(self):
        if self.lmr_specifier is not None:
            return self.lmr_specifier
        return baca.LMRSpecifier()

    def _get_pattern(self):
        return self.pattern or abjad.index_all()

    ### PUBLIC PROPERTIES ###

    @property
    def durations(self):
        r'''Gets durations.

        ..  container:: example

            Sixteenth-note acciaccaturas by default:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     acciaccatura_specifiers=[
                ...         baca.AcciaccaturaSpecifier()
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=8,
                ...         ),
                ...     )

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'8
                        }
                        {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        {
                            \acciaccatura {
                                fs''16 [
                                e''16 ]
                            }
                            ef''8
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16 ]
                            }
                            c'8
                        }
                        {
                            \acciaccatura {
                                d'16 [
                                bf'16
                                fs''16
                                e''16 ]
                            }
                            ef''8
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16
                                c'16
                                d'16 ]
                            }
                            bf'8
                        }
                    }
                }

        ..  container:: example

            Eighth-note acciaccaturas:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     acciaccatura_specifiers=[
                ...         baca.AcciaccaturaSpecifier(
                ...             durations=[(1, 8)],
                ...             ),
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=8,
                ...         ),
                ...     )

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'8
                        }
                        {
                            \acciaccatura {
                                d'8
                            }
                            bf'8
                        }
                        {
                            \acciaccatura {
                                fs''8 [
                                e''8 ]
                            }
                            ef''8
                        }
                        {
                            \acciaccatura {
                                af''8 [
                                g''8
                                a'8 ]
                            }
                            c'8
                        }
                        {
                            \acciaccatura {
                                d'8 [
                                bf'8
                                fs''8
                                e''8 ]
                            }
                            ef''8
                        }
                        {
                            \acciaccatura {
                                af''8 [
                                g''8
                                a'8
                                c'8
                                d'8 ]
                            }
                            bf'8
                        }
                    }
                }

        Defaults to none.

        Set to durations or none.

        Returns durations or none.
        '''
        return self._durations

    @property
    def lmr_specifier(self):
        r'''Gets LMR specifier.

        ..  container:: example

            As many acciaccaturas as possible per collection:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     acciaccatura_specifiers=[
                ...         baca.AcciaccaturaSpecifier()
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=8,
                ...         ),
                ...     )

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'8
                        }
                        {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        {
                            \acciaccatura {
                                fs''16 [
                                e''16 ]
                            }
                            ef''8
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16 ]
                            }
                            c'8
                        }
                        {
                            \acciaccatura {
                                d'16 [
                                bf'16
                                fs''16
                                e''16 ]
                            }
                            ef''8
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16
                                c'16
                                d'16 ]
                            }
                            bf'8
                        }
                    }
                }

        ..  container:: example

            At most two acciaccaturas at the beginning of every collection:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     acciaccatura_specifiers=[
                ...         baca.AcciaccaturaSpecifier(
                ...             lmr_specifier=baca.LMRSpecifier(
                ...                 left_length=3,
                ...                 right_counts=[1],
                ...                 right_cyclic=True,
                ...                 ),
                ...             ),
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=8,
                ...         ),
                ...     )

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/2
                        {
                            c'8
                        }
                        {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        {
                            \acciaccatura {
                                fs''16 [
                                e''16 ]
                            }
                            ef''8
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16 ]
                            }
                            a'8 [
                            c'8 ]
                        }
                        {
                            \acciaccatura {
                                d'16 [
                                bf'16 ]
                            }
                            fs''8 [
                            e''8
                            ef''8 ]
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16 ]
                            }
                            a'8 [
                            c'8
                            d'8
                            bf'8 ]
                        }
                    }
                }

        ..  container:: example

            At most two acciaccaturas at the end of every collection:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     acciaccatura_specifiers=[
                ...         baca.AcciaccaturaSpecifier(
                ...             lmr_specifier=baca.LMRSpecifier(
                ...                 right_length=3,
                ...                 left_counts=[1],
                ...                 left_cyclic=True,
                ...                 ),
                ...             ),
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=8,
                ...         ),
                ...     )

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/2
                        {
                            c'8
                        }
                        {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        {
                            \acciaccatura {
                                fs''16 [
                                e''16 ]
                            }
                            ef''8
                        }
                        {
                            af''8 [
                            \acciaccatura {
                                g''16 [
                                a'16 ]
                            }
                            c'8 ]
                        }
                        {
                            d'8 [
                            bf'8
                            \acciaccatura {
                                fs''16 [
                                e''16 ]
                            }
                            ef''8 ]
                        }
                        {
                            af''8 [
                            g''8
                            a'8
                            \acciaccatura {
                                c'16 [
                                d'16 ]
                            }
                            bf'8 ]
                        }
                    }
                }

        ..  container:: example

            At most two acciaccaturas at the beginning of every collection and
            then at most two acciaccaturas at the end of every collection:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
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
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=8,
                ...         ),
                ...     )

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 9/8
                        {
                            c'8
                        }
                        {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        {
                            \acciaccatura {
                                fs''16 [
                                e''16 ]
                            }
                            ef''8
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16 ]
                            }
                            a'8 [
                            c'8 ]
                        }
                        {
                            \acciaccatura {
                                d'16 [
                                bf'16 ]
                            }
                            fs''8 [
                            \acciaccatura {
                                e''16
                            }
                            ef''8 ]
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16 ]
                            }
                            a'8 [
                            \acciaccatura {
                                c'16 [
                                d'16 ]
                            }
                            bf'8 ]
                        }
                    }
                }

        ..  container:: example

            As many acciaccaturas as possible in the middle of every collection:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     acciaccatura_specifiers=[
                ...         baca.AcciaccaturaSpecifier(
                ...             lmr_specifier=baca.LMRSpecifier(
                ...                 left_length=1,
                ...                 ),
                ...             ),
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=8,
                ...         ),
                ...     )

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 11/8
                        {
                            c'8
                        }
                        {
                            d'8 [
                            bf'8 ]
                        }
                        {
                            fs''8 [
                            \acciaccatura {
                                e''16
                            }
                            ef''8 ]
                        }
                        {
                            af''8 [
                            \acciaccatura {
                                g''16 [
                                a'16 ]
                            }
                            c'8 ]
                        }
                        {
                            d'8 [
                            \acciaccatura {
                                bf'16 [
                                fs''16
                                e''16 ]
                            }
                            ef''8 ]
                        }
                        {
                            af''8 [
                            \acciaccatura {
                                g''16 [
                                a'16
                                c'16
                                d'16 ]
                            }
                            bf'8 ]
                        }
                    }
                }

        Defaults to none.

        Set to LMR specifier or none.

        Returns LMR specifier or none.
        '''
        return self._lmr_specifier

    @property
    def pattern(self):
        r'''Gets pattern.

        ..  container:: example

            Applies to all collections by default:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     acciaccatura_specifiers=[
                ...         baca.AcciaccaturaSpecifier()
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=8,
                ...         ),
                ...     )

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/4
                        {
                            c'8
                        }
                        {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        {
                            \acciaccatura {
                                fs''16 [
                                e''16 ]
                            }
                            ef''8
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16 ]
                            }
                            c'8
                        }
                        {
                            \acciaccatura {
                                d'16 [
                                bf'16
                                fs''16
                                e''16 ]
                            }
                            ef''8
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16
                                c'16
                                d'16 ]
                            }
                            bf'8
                        }
                    }
                }

        ..  container:: example

            Applies to last collection:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     acciaccatura_specifiers=[
                ...         baca.AcciaccaturaSpecifier(
                ...             pattern=abjad.index_last(),
                ...             ),
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=8,
                ...         ),
                ...     )

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 2/1
                        {
                            c'8
                        }
                        {
                            d'8 [
                            bf'8 ]
                        }
                        {
                            fs''8 [
                            e''8
                            ef''8 ]
                        }
                        {
                            af''8 [
                            g''8
                            a'8
                            c'8 ]
                        }
                        {
                            d'8 [
                            bf'8
                            fs''8
                            e''8
                            ef''8 ]
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16
                                c'16
                                d'16 ]
                            }
                            bf'8
                        }
                    }
                }

        ..  container:: example

            Applies to every other collection:

            ::

                >>> rhythm_maker = baca.MusicRhythmMaker(
                ...     acciaccatura_specifiers=[
                ...         baca.AcciaccaturaSpecifier(
                ...             pattern=abjad.index_every([1], period=2),
                ...             ),
                ...         ],
                ...     talea=abjad.rhythmmakertools.Talea(
                ...         counts=[1],
                ...         denominator=8,
                ...         ),
                ...     )

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff {
                    {
                        \time 3/2
                        {
                            c'8
                        }
                        {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        {
                            fs''8 [
                            e''8
                            ef''8 ]
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16 ]
                            }
                            c'8
                        }
                        {
                            d'8 [
                            bf'8
                            fs''8
                            e''8
                            ef''8 ]
                        }
                        {
                            \acciaccatura {
                                af''16 [
                                g''16
                                a'16
                                c'16
                                d'16 ]
                            }
                            bf'8
                        }
                    }
                }

        Defaults to none.

        Set to pattern or none.

        Returns pattern or none.
        '''
        return self._pattern
