# -*- coding: utf-8 -*-
import abjad
import baca
import copy


class ImbricationSpecifier(abjad.abctools.AbjadObject):
    r'''Imbrication specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Defaults:

        ::

            >>> figure_maker = baca.tools.FigureMaker(
            ...     baca.tools.RhythmSpecifier(
            ...         rhythm_maker=baca.tools.FigureRhythmMaker(
            ...             talea=abjad.rhythmmakertools.Talea(
            ...                 counts=[1],
            ...                 denominator=16,
            ...                 ),
            ...             ),
            ...         ),
            ...     abjad.rhythmmakertools.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

        ::

            >>> segments = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = figure_maker(
            ...     'Voice 2',
            ...     segments,
            ...     baca.tools.ImbricationSpecifier(
            ...         segment=[2, 19, 9, 18, 16],
            ...         voice_name='Voice 1',
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Score])
            \new Score <<
                \new TimeSignatureContext {
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                }
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            {
                                s16
                                d'16
                                s16
                                s16
                                s16
                            }
                            {
                                s16
                                s16
                                g''16 [
                                a'16 ]
                                s16
                            }
                            {
                                s16
                                s16
                                fs''16 [
                                e''16 ]
                                s16
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        {
                            {
                                \set stemLeftBeamCount = #0
                                \set stemRightBeamCount = #2
                                c'16 [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                e''16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                ef''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                af''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                g''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                a'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                c'16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                d'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                e''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #0
                                ef''16 ]
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Multiple imbricated voices:

        ::

            >>> figure_maker = baca.tools.FigureMaker(
            ...     baca.tools.RhythmSpecifier(
            ...         rhythm_maker=baca.tools.FigureRhythmMaker(
            ...             talea=abjad.rhythmmakertools.Talea(
            ...                 counts=[1],
            ...                 denominator=16,
            ...                 ),
            ...             ),
            ...         ),
            ...     abjad.rhythmmakertools.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

        ::

            >>> segments = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = figure_maker(
            ...     'Voice 2',
            ...     segments,
            ...     baca.tools.ImbricationSpecifier(
            ...         'Voice 1',
            ...         [2, 19, 9],
            ...         baca.beam_everything(),
            ...         baca.staccati(),
            ...         ),
            ...     baca.tools.ImbricationSpecifier(
            ...         'Voice 3',
            ...         [16, 10, 18],
            ...         baca.beam_everything(),
            ...         baca.accents(),
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Score])
            \new Score <<
                \new TimeSignatureContext {
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                }
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            {
                                s16 [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16 -\staccato
                                s16
                                s16
                                s16
                            }
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                g''16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                a'16 -\staccato
                                s16
                            }
                            {
                                s16
                                s16
                                s16
                                s16
                                s16 ]
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        {
                            {
                                \set stemLeftBeamCount = #0
                                \set stemRightBeamCount = #2
                                c'16 [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                e''16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                ef''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                af''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                g''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                a'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                c'16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                d'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                e''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #0
                                ef''16 ]
                            }
                        }
                    }
                    \context Voice = "Voice 3" {
                        \voiceThree
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            {
                                s16 [
                                s16
                                s16
                                s16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                e''16 -\accent
                            }
                            {
                                s16
                                s16
                                s16
                                s16
                                s16
                            }
                            {
                                s16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16 -\accent
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16 -\accent
                                s16
                                s16 ]
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                >>
            >>

    ..  container:: example

        Hides tuplet brackets above imbricated voice:

        ::

            >>> figure_maker = baca.tools.FigureMaker(
            ...     baca.tools.ArticulationSpecifier(
            ...         articulations=['.'],
            ...     ),
            ...     baca.tools.RhythmSpecifier(
            ...         rhythm_maker=baca.tools.FigureRhythmMaker(
            ...             talea=abjad.rhythmmakertools.Talea(
            ...                 counts=[1],
            ...                 denominator=16,
            ...                 ),
            ...             time_treatments=[1],
            ...             ),
            ...         ),
            ...     abjad.rhythmmakertools.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         beam_rests=True,
            ...         ),
            ...     )

        ::

            >>> segments = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = figure_maker(
            ...     'Voice 2',
            ...     segments,
            ...     baca.tools.ImbricationSpecifier(
            ...         'Voice 1',
            ...         [2, 19, 9, 18, 16],
            ...         baca.accents(),
            ...         baca.beam_everything(),
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Score])
            \new Score <<
                \new TimeSignatureContext {
                    {
                        \time 9/8
                        s1 * 9/8
                    }
                }
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                s16 [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16 -\accent
                                s16
                                s16
                                s16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                s16
                                s16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                g''16 -\accent
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                a'16 -\accent
                                s16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                s16
                                s16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16 -\accent
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                e''16 -\accent
                                s16 ]
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                \set stemLeftBeamCount = #0
                                \set stemRightBeamCount = #2
                                c'16 -\staccato [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                e''16 -\staccato
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                ef''16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                af''16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                g''16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                a'16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                c'16 -\staccato
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                d'16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                fs''16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                e''16 -\staccato
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #0
                                ef''16 -\staccato ]
                            }
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_allow_unused_pitches',
        '_extend_beam',
        '_hocket',
        '_segment',
        '_selector',
        '_specifiers',
        '_truncate_ties',
        '_voice_name',
        )

    _extend_beam_tag = 'extend beam'

    ### INITIALIZER ###

    def __init__(
        self,
        voice_name=None,
        segment=None,
        *specifiers,
        allow_unused_pitches=None,
        extend_beam=None,
        hocket=None,
        selector=None,
        truncate_ties=None
        ):
        if voice_name is not None:
            assert isinstance(voice_name, str), repr(voice_name)
        self._voice_name = voice_name
        self._segment = segment
        self._specifiers = specifiers
        if allow_unused_pitches is not None:
            allow_unused_pitches = bool(allow_unused_pitches)
        self._allow_unused_pitches = allow_unused_pitches
        if extend_beam is not None:
            extend_beam = bool(extend_beam)
        self._extend_beam = extend_beam
        if hocket is not None:
            hocket = bool(hocket)
        self._hocket = hocket
        if selector is not None:
            if not isinstance(selector, abjad.selectortools.Selector):
                message = 'must be selector or none: {!r}.'
                message = message.format(selector)
                raise TypeError(selector)
        self._selector = selector
        if truncate_ties is not None:
            truncate_ties = bool(truncate_ties)
        self._truncate_ties = truncate_ties

    ### SPECIAL METHODS ###

    def __call__(
        self,
        container,
        #imbrication_token,
        #extend_beam=False,
        ):
        r'''Calls specifier on `container` with `imbrication_token`.

        ..  container:: example

            Imbrication together with polyphony:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     )
                >>> polyphony_specifier = baca.tools.PolyphonySpecifier(
                ...      figure_maker=baca.tools.FigureMaker(
                ...         baca.tools.ArticulationSpecifier(
                ...             articulations=['.'],
                ...             ),
                ...         baca.tools.RhythmSpecifier(
                ...             rhythm_maker=baca.tools.FigureRhythmMaker(
                ...                 talea=abjad.rhythmmakertools.Talea(
                ...                     counts=[2],
                ...                     denominator=16,
                ...                     ),
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> polyphony_map = [
                ...     ('Voice 1', [[18, 16, 15, 20, 19], [9]], polyphony_specifier),
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     segments,
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 3',
                ...         [2, 15, 20],
                ...         baca.accents(),
                ...         baca.beam_everything(),
                ...         ),
                ...     polyphony_map=polyphony_map,
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 27/16
                            s1 * 27/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                {
                                    fs''8 -\staccato [
                                    e''8 -\staccato
                                    ef''8 -\staccato
                                    af''8 -\staccato
                                    g''8 -\staccato ]
                                }
                                {
                                    a'8 -\staccato
                                }
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    c'8. [
                                    d'8.
                                    bf'8. ]
                                }
                                {
                                    fs''8. [
                                    e''8.
                                    ef''8.
                                    af''8.
                                    g''8. ]
                                }
                                {
                                    a'8.
                                }
                            }
                        }
                        \context Voice = "Voice 3" {
                            \voiceThree
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                {
                                    s8. [
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    d'8. -\accent
                                    s8.
                                }
                                {
                                    s8.
                                    s8.
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    ef''8. -\accent
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    af''8. -\accent
                                    s8.
                                }
                                {
                                    s8. ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                    >>
                >>

        ..  container:: example

            Works with pitch-classes:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> segment = [
                ...     abjad.NumberedPitchClass(10),
                ...     abjad.NumberedPitchClass(6),
                ...     abjad.NumberedPitchClass(4),
                ...     abjad.NumberedPitchClass(3),
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     segments,
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         segment,
                ...         baca.accents(),
                ...         baca.beam_everything(),
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 27/16
                            s1 * 27/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                {
                                    s8. [
                                    s8.
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    bf'8. -\accent
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    fs''8. -\accent
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    e''8. -\accent
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    ef''8. -\accent
                                    s8.
                                    s8.
                                }
                                {
                                    s8. ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    c'8. [
                                    d'8.
                                    bf'8. ]
                                }
                                {
                                    fs''8. [
                                    e''8.
                                    ef''8.
                                    af''8.
                                    g''8. ]
                                }
                                {
                                    a'8.
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Skips wrapped pitches:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
                ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
                ...     ]
                >>> imbricated_pitches = [
                ...     0,
                ...     baca.coat(10),
                ...     baca.coat(18),
                ...     10, 18,
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     segments,
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         imbricated_pitches,
                ...         baca.accents(),
                ...         baca.beam_everything(),
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 9/8
                            s1 * 9/8
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 -\accent [
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16 -\accent
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\accent
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    s16
                                    s16 ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    c'16 [
                                    d'16
                                    bf'16
                                    fs''16
                                    e''16 ]
                                }
                                {
                                    ef''16 [
                                    af''16
                                    g''16
                                    a'16 ]
                                }
                                {
                                    c'16 [
                                    d'16
                                    bf'16
                                    fs''16
                                    e''16 ]
                                }
                                {
                                    ef''16 [
                                    af''16
                                    g''16
                                    a'16 ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Segment-maker allows for beam extension.
            
            Extends beam across figures:

                >>> figure_maker = baca.tools.FigureMaker(
                ...     abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> voice_1_selections = []
                >>> voice_2_selections = []
                >>> time_signatures = []
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     [[0, 2, 10, 18], [16, 15, 23]],
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         [2, 10],
                ...         baca.staccati(),
                ...         baca.beam_everything(),
                ...         extend_beam=True,
                ...         ),
                ...     )
                >>> dictionary = contribution.selections
                >>> voice_1_selections.append(dictionary['Voice 1'])
                >>> voice_2_selections.append(dictionary['Voice 2'])
                >>> time_signatures.append(contribution.time_signature)    
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     [[19, 13, 9, 8]],
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         [13, 9],
                ...         baca.staccati(),
                ...         baca.beam_everything(),
                ...         ),
                ...     )
                >>> dictionary = contribution.selections
                >>> voice_1_selections.append(dictionary['Voice 1'])
                >>> voice_2_selections.append(dictionary['Voice 2'])
                >>> time_signatures.append(contribution.time_signature)    

            ::

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     ignore_duplicate_pitch_classes=True,
                ...     measures_per_stage=[1, 1],
                ...     score_template=baca.tools.TwoVoiceStaffScoreTemplate(),
                ...     spacing_specifier=baca.tools.HorizontalSpacingSpecifier(
                ...         minimum_width=abjad.Duration(1, 24),
                ...         ),
                ...     time_signatures=time_signatures,
                ...     )
                >>> specifiers = segment_maker.append_specifiers(
                ...     ('v2', baca.select.stages(1)),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=voice_2_selections[0],
                ...         ),
                ...     )
                >>> specifiers = segment_maker.append_specifiers(
                ...     ('v2', baca.select.stages(2)),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=voice_2_selections[1],
                ...         ),
                ...     )
                >>> specifiers = segment_maker.append_specifiers(
                ...     ('v1', baca.select.stages(1)),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=voice_1_selections[0],
                ...         ),
                ...     )
                >>> specifiers = segment_maker.append_specifiers(
                ...     ('v1', baca.select.stages(2)),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=voice_1_selections[1],
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> voice = lilypond_file['Music Voice 2']
                >>> abjad.override(voice).beam.positions = (-5, -5)
                >>> show(lilypond_file) # doctest: +SKIP


            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context TimeSignatureContext = "Time Signature Context" <<
                        \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
                            {
                                \time 7/16
                                R1 * 7/16
                            }
                            {
                                \time 1/4
                                R1 * 1/4
                            }
                        }
                        \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                            {
                                \time 7/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 7/16
                            }
                            {
                                \time 1/4
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 1/4
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \context MusicStaff = "Music Staff" <<
                            \context MusicVoiceOne = "Music Voice 1" {
                                {
                                    \override TupletBracket.stencil = ##f
                                    \override TupletNumber.stencil = ##f
                                    {
                                        s16 [
                                        \set stemLeftBeamCount = #2
                                        \set stemRightBeamCount = #2
                                        d'16 -\staccato
                                        \set stemLeftBeamCount = #2
                                        \set stemRightBeamCount = #2
                                        bf'16 -\staccato
                                        s16
                                    }
                                    {
                                        s16
                                        s16
                                        s16
                                    }
                                    \revert TupletBracket.stencil
                                    \revert TupletNumber.stencil
                                }
                                {
                                    \override TupletBracket.stencil = ##f
                                    \override TupletNumber.stencil = ##f
                                    {
                                        s16
                                        \set stemLeftBeamCount = #2
                                        \set stemRightBeamCount = #2
                                        cs''16 -\staccato
                                        \set stemLeftBeamCount = #2
                                        \set stemRightBeamCount = #2
                                        a'16 -\staccato
                                        s16 ]
                                        \bar "|"
                                    }
                                    \revert TupletBracket.stencil
                                    \revert TupletNumber.stencil
                                }
                            }
                            \context MusicVoiceTwo = "Music Voice 2" \with {
                                \override Beam.positions = #'(-5 . -5)
                            } {
                                {
                                    {
                                        \set stemLeftBeamCount = #0
                                        \set stemRightBeamCount = #2
                                        c'16 [
                                        \set stemLeftBeamCount = #2
                                        \set stemRightBeamCount = #2
                                        d'16
                                        \set stemLeftBeamCount = #2
                                        \set stemRightBeamCount = #2
                                        bf'16
                                        \set stemLeftBeamCount = #2
                                        \set stemRightBeamCount = #1
                                        fs''16
                                    }
                                    {
                                        \set stemLeftBeamCount = #1
                                        \set stemRightBeamCount = #2
                                        e''16
                                        \set stemLeftBeamCount = #2
                                        \set stemRightBeamCount = #2
                                        ef''16
                                        \set stemLeftBeamCount = #2
                                        \set stemRightBeamCount = #0
                                        b''16 ]
                                    }
                                }
                                {
                                    {
                                        \set stemLeftBeamCount = #0
                                        \set stemRightBeamCount = #2
                                        g''16 [
                                        \set stemLeftBeamCount = #2
                                        \set stemRightBeamCount = #2
                                        cs''16
                                        \set stemLeftBeamCount = #2
                                        \set stemRightBeamCount = #2
                                        a'16
                                        \set stemLeftBeamCount = #2
                                        \set stemRightBeamCount = #0
                                        af'16 ]
                                        \bar "|"
                                    }
                                }
                            }
                        >>
                    >>
                >>

        Returns new container.
        '''
        original_container = container
        container = copy.deepcopy(container)
        abjad.override(container).tuplet_bracket.stencil = False
        abjad.override(container).tuplet_number.stencil = False
        segment = baca.sequence(self.segment).flatten()
        cursor = baca.tools.Cursor(
            segment,
            singletons=True,
            suppress_exception=True,
            )
        pitch_number = cursor.next()
        if self.selector is not None:
            selection = self.selector(original_container)
        selected_logical_ties = None
        if self.selector is not None:
            selection = self.selector(container)
            agent = abjad.iterate(selection)
            selected_logical_ties = agent.by_logical_tie(pitched=True)
            selected_logical_ties = list(selected_logical_ties)
        agent = abjad.iterate(original_container)
        original_logical_ties = agent.by_logical_tie(pitched=True)
        logical_ties = abjad.iterate(container).by_logical_tie(pitched=True)
        pairs = zip(logical_ties, original_logical_ties)
        for logical_tie, original_logical_tie in pairs:
            if (selected_logical_ties is not None and
                logical_tie not in selected_logical_ties):
                for note in logical_tie:
                    duration = note.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(note).replace([skip])
            elif self._matches_pitch(logical_tie.head, pitch_number):
                if isinstance(pitch_number, baca.tools.Coat):
                    for note in logical_tie:
                        duration = note.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(note).replace([skip])
                    pitch_number = cursor.next()
                    continue
                pitch_number = cursor.next()
                if self.truncate_ties:
                    for note in logical_tie[1:]:
                        duration = note.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(note).replace([skip])
                if self.hocket:
                    for note in original_logical_tie:
                        duration = note.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(note).replace([skip])
            else:
                for note in logical_tie:
                    duration = note.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(note).replace([skip])
        if not self.allow_unused_pitches and not cursor.is_exhausted:
            message = '{!r} used only {} of {} pitches.'
            message = message.format(cursor, cursor.position-1, len(cursor))
            raise Exception(message)
        self._apply_specifiers(container)
        if self.extend_beam:
            leaves = list(abjad.iterate(container).by_leaf())
            last_leaf = leaves[-1]
            abjad.attach(self._extend_beam_tag, last_leaf)
        selection = abjad.select(container)
        return {self.voice_name: selection}

    ### PRIVATE METHODS ###

    def _apply_specifiers(self, container):
        assert isinstance(container, abjad.Container), repr(container)
        nested_selections = None
        specifiers = self.specifiers or []
        selections = container[:]
        for specifier in specifiers:
            if isinstance(specifier, baca.tools.RhythmSpecifier):
                continue
            if isinstance(specifier, baca.tools.ImbricationSpecifier):
                continue
            if isinstance(specifier, abjad.rhythmmakertools.BeamSpecifier):
                specifier._detach_all_beams(selections)
            if isinstance(specifier, baca.tools.NestingSpecifier):
                nested_selections = specifier(selections)
            else:
                specifier(selections)
        if nested_selections is not None:
            return nested_selections
        return selections

    @staticmethod
    def _matches_pitch(note, pitch_object):
        if isinstance(pitch_object, baca.tools.Coat):
            pitch_object = pitch_object.argument
        if pitch_object is None:
            return False
        elif isinstance(pitch_object, (int, float)):
            source = note.written_pitch.pitch_number
        elif isinstance(pitch_object, abjad.NamedPitch):
            source = note.written_pitch
        elif isinstance(pitch_object, abjad.NumberedPitch):
            source = note.written_pitch
            source = abjad.NumberedPitch(source)
        elif isinstance(pitch_object, abjad.NamedPitchClass):
            source = note.written_pitch
            source = abjad.NamedPitchClass(source)
        elif isinstance(pitch_object, abjad.NumberedPitchClass):
            source = note.written_pitch
            source = abjad.NumberedPitchClass(source)
        else:
            message = 'unknown pitch object: {!r}.'
            message = message.format(pitch_object)
            raise TypeError(message)
        if not type(source) is type(pitch_object):
            message = 'type of {!r} must match type of {!r}.'
            message = message.format(source, pitch_object)
            raise TypeError(message)
        return source == pitch_object

    ### PUBLIC PROPERTIES ###

    @property
    def allow_unused_pitches(self):
        r'''Is true when specifier allows unused pitches.

        ..  container:: example

            Allows unused pitches:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...     ),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     segments,
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         [2, 19, 9, 18, 16],
                ...         baca.accents(),
                ...         baca.beam_everything(),
                ...         allow_unused_pitches=True,
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 5/8
                            s1 * 5/8
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                {
                                    s16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 -\accent
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16 -\accent
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16 -\accent
                                    s16 ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 -\staccato [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16 -\staccato
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    c'16 -\staccato ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Raises exception on unused pitches:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...     ),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     ]
                >>> result = figure_maker(
                ...     'Voice 2',
                ...     segments,
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         [2, 19, 9, 18, 16],
                ...         baca.accents(),
                ...         baca.beam_everything(),
                ...         ),
                ...     )
                Traceback (most recent call last):
                    ...
                Exception: Cursor(source=Sequence(items=(2, 19, 9, 18, 16)),
                position=4, singletons=True, suppress_exception=True)
                used only 3 of 5 pitches.

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = baca.tools.ImbricationSpecifier()
                >>> specifier.allow_unused_pitches is None
                True

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._allow_unused_pitches

    @property
    def extend_beam(self):
        r'''Is true when specifier extends beam.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._extend_beam

    @property
    def hocket(self):
        r'''Is true when specifier hockets voices.

        ..  container:: example

            Hockets voices:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...     ),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     segments,
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         [2, 19, 9, 18, 16],
                ...         baca.accents(),
                ...         baca.beam_everything(),
                ...         hocket=True,
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 15/16
                            s1 * 15/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                {
                                    s16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 -\accent
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16 -\accent
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16 -\accent
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\accent
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16 -\accent
                                    s16 ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 -\staccato [
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16 -\staccato
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16 -\staccato
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    c'16 -\staccato
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    d'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16 -\staccato
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    ef''16 -\staccato ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = baca.tools.ImbricationSpecifier()
                >>> specifier.hocket is None
                True

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._hocket

    @property
    def segment(self):
        r'''Gets segment.

        Returns pitch or pitch-class segment.
        '''
        return self._segment
        
    @property
    def selector(self):
        r'''Gets selector.

        ..  container:: example

            Selects last nine notes:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.ArticulationSpecifier(
                ...         articulations=['.'],
                ...     ),
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         beam_rests=True,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
                ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     segments,
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         [2, 18, 16, 15],
                ...         baca.accents(),
                ...         baca.beam_everything(),
                ...         selector=baca.select.pitched_logical_ties(-9),
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 9/8
                            s1 * 9/8
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                {
                                    s16 [
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 -\accent
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\accent
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16 -\accent
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16 -\accent
                                    s16
                                    s16
                                    s16 ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 -\staccato [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16 -\staccato
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    a'16 -\staccato
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    c'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16 -\staccato
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16 -\staccato
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    a'16 -\staccato ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = baca.tools.ImbricationSpecifier()
                >>> specifier.selector is None
                True

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector

    @property
    def specifiers(self):
        r'''Gets specifiers.

        ..  container:: example

            Beams nothing:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     segments,
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         [2, 19, 9, 18, 16],
                ...         abjad.rhythmmakertools.BeamSpecifier(
                ...             beam_each_division=False,
                ...             ),
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 15/16
                            s1 * 15/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                {
                                    s16
                                    d'16
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    g''16
                                    a'16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    fs''16
                                    e''16
                                    s16
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    c'16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    ef''16 ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Beams divisions together but excludes skips:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     segments,
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         [2, 19, 9, 18, 16],
                ...         abjad.rhythmmakertools.BeamSpecifier(
                ...             beam_divisions_together=True,
                ...             ),
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 15/16
                            s1 * 15/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                {
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16 [ ]
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16 ]
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16 ]
                                    s16
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    c'16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    ef''16 ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Beams divisions together and includes skips:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     segments,
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         [2, 19, 9, 18, 16],
                ...         baca.beam_everything(),
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 15/16
                            s1 * 15/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                {
                                    s16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16
                                    s16
                                    s16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16
                                    s16
                                }
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16
                                    s16 ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    c'16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    ef''16 ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Beams each division and includes skips:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[1],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     abjad.rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> segments = [
                ...     [0, 2, 10, 18, 16],
                ...     [15, 20, 19, 9, 0],
                ...     [2, 10, 18, 16, 15],
                ...     ]
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     segments,
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         [2, 19, 9, 18, 16],
                ...         abjad.rhythmmakertools.BeamSpecifier(
                ...             beam_rests=True,
                ...             ),
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 15/16
                            s1 * 15/16
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                {
                                    s16 [
                                    d'16
                                    s16
                                    s16
                                    s16 ]
                                }
                                {
                                    s16 [
                                    s16
                                    g''16
                                    a'16
                                    s16 ]
                                }
                                {
                                    s16 [
                                    s16
                                    fs''16
                                    e''16
                                    s16 ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    \set stemLeftBeamCount = #0
                                    \set stemRightBeamCount = #2
                                    c'16 [
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    e''16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    ef''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    af''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    g''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    a'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #1
                                    c'16
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #2
                                    d'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    bf'16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    fs''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #2
                                    e''16
                                    \set stemLeftBeamCount = #2
                                    \set stemRightBeamCount = #0
                                    ef''16 ]
                                }
                            }
                        }
                    >>
                >>

        Returns specifiers or none.
        '''
        return list(self._specifiers)

    @property
    def truncate_ties(self):
        r'''Is true when specifier truncates ties.

        ..  container:: example

            Truncates ties:

            ::

                >>> figure_maker = baca.tools.FigureMaker(
                ...     baca.tools.RhythmSpecifier(
                ...         rhythm_maker=baca.tools.FigureRhythmMaker(
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[5],
                ...                 denominator=32,
                ...                 ),
                ...             ),
                ...         ),
                ...     )

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(
                ...     'Voice 2',
                ...     segments,
                ...     baca.tools.ImbricationSpecifier(
                ...         'Voice 1',
                ...         [2, 10, 18, 19, 9],
                ...         baca.beam_everything(),
                ...         truncate_ties=True,
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 45/32
                            s1 * 45/32
                        }
                    }
                    \new Staff <<
                        \context Voice = "Voice 1" {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                {
                                    s8 [
                                    s32
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    d'8
                                    s32
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    bf'8
                                    s32
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    fs''8
                                    s32
                                    s8
                                    s32
                                    s8
                                    s32
                                    s8
                                    s32
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    g''8
                                    s32
                                }
                                {
                                    \set stemLeftBeamCount = #1
                                    \set stemRightBeamCount = #1
                                    a'8
                                    s32 ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2" {
                            \voiceTwo
                            {
                                {
                                    c'8 ~ [
                                    c'32
                                    d'8 ~
                                    d'32
                                    bf'8 ~
                                    bf'32 ]
                                }
                                {
                                    fs''8 ~ [
                                    fs''32
                                    e''8 ~
                                    e''32
                                    ef''8 ~
                                    ef''32
                                    af''8 ~
                                    af''32
                                    g''8 ~
                                    g''32 ]
                                }
                                {
                                    a'8 ~ [
                                    a'32 ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Defaults to none:

            ::

                >>> specifier = baca.tools.ImbricationSpecifier()
                >>> specifier.truncate_ties is None
                True

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._truncate_ties

    @property
    def voice_name(self):
        r'''Gets voice name.

        Returns string.
        '''
        return self._voice_name
