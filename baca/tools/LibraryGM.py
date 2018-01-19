import abjad
import baca
from abjad import rhythmmakertools as rhythmos


class LibraryGM(abjad.AbjadObject):
    r'''Library G - M.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(1) Library'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def glissando(selector='baca.tleaves()'):
        r'''Attaches glissando to trimmed leaves.

        ..  container:: example

            With segment-maker:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.glissando()
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % GlobalSkips [measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % GlobalSkips [measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % GlobalSkips [measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % GlobalSkips [measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    % MusicVoice [measure 1]                                             %! SM4
                                    e'8
                                    \glissando                                                           %! SC
                                    [
                <BLANKLINE>
                                    d''8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    f'8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    e''8
                                    ]
                                    \glissando                                                           %! SC
                                }
                                {
                <BLANKLINE>
                                    % MusicVoice [measure 2]                                             %! SM4
                                    g'8
                                    \glissando                                                           %! SC
                                    [
                <BLANKLINE>
                                    f''8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    e'8
                                    ]
                                    \glissando                                                           %! SC
                                }
                                {
                <BLANKLINE>
                                    % MusicVoice [measure 3]                                             %! SM4
                                    d''8
                                    \glissando                                                           %! SC
                                    [
                <BLANKLINE>
                                    f'8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    e''8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    g'8
                                    ]
                                    \glissando                                                           %! SC
                                }
                                {
                <BLANKLINE>
                                    % MusicVoice [measure 4]                                             %! SM4
                                    f''8
                                    \glissando                                                           %! SC
                                    [
                <BLANKLINE>
                                    e'8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    d''8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            First and last PLTs:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.make_even_runs(),
            ...     baca.glissando(baca.plts()[:2]),
            ...     baca.glissando(baca.plts()[-2:]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % GlobalSkips [measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % GlobalSkips [measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % GlobalSkips [measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % GlobalSkips [measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    % MusicVoice [measure 1]                                             %! SM4
                                    e'8
                                    \glissando                                                           %! SC
                                    [
                <BLANKLINE>
                                    d''8
                <BLANKLINE>
                                    f'8
                <BLANKLINE>
                                    e''8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % MusicVoice [measure 2]                                             %! SM4
                                    g'8
                                    [
                <BLANKLINE>
                                    f''8
                <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % MusicVoice [measure 3]                                             %! SM4
                                    d''8
                                    [
                <BLANKLINE>
                                    f'8
                <BLANKLINE>
                                    e''8
                <BLANKLINE>
                                    g'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % MusicVoice [measure 4]                                             %! SM4
                                    f''8
                                    [
                <BLANKLINE>
                                    e'8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    d''8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            With music-maker:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.glissando(),
            ...         baca.tuplets()[1:2].runs(),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                \glissando                                                               %! SC
                                [
                                e''16
                                ]
                                \glissando                                                               %! SC
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                \glissando                                                               %! SC
                                [
                                g''16
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        '''
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.Glissando(),
            )

    @staticmethod
    def hairpin(hairpin=None, selector='baca.tleaves()'):
        r'''Attaches hairpin to trimmed leaves.

        ..  container:: example

            Attaches hairpin to trimmed leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.hairpin('p < f'),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                \<
                                \p
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                e''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                [
                                g''16
                                ]
                            }
                            \times 4/5 {
                                a'16
                                \f
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches hairpin to trimmed leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.hairpin('p < f'), baca.tuplet(1)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                \<
                                \p
                                [
                                e''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                [
                                g''16
                                \f
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches hairpin to trimmed leaves in each tuplets:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.hairpin('p < f'), baca.tuplets()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                \<
                                \p
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                \f
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                \<
                                \p
                                [
                                e''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                [
                                g''16
                                \f
                                ]
                            }
                            \times 4/5 {
                                a'16
                                \p
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        '''
        hairpin = abjad.Hairpin(hairpin)
        return baca.HairpinCommand(
            selector=selector,
            start=hairpin.start_dynamic,
            stop=hairpin.stop_dynamic,
            )

    @staticmethod
    def hairpin_shorten_pair(pair:tuple, selector='baca.leaf(0)'):
        r'''Overrides hairpin shorten pair.

        Returns override command.
        '''
        return baca.OverrideCommand(
            attribute='shorten_pair',
            value=pair,
            grob='hairpin',
            selector=selector,
            )

    @staticmethod
    def helianthate(sequence, n=0, m=0):
        '''Helianthates `sequence` by outer index of rotation `n` and inner
        index of rotation `m`.

        ..  container:: example

            Helianthates list of lists:

            >>> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
            >>> sequence = baca.helianthate(sequence, n=-1, m=1)
            >>> for item in sequence:
            ...     item
            [1, 2, 3]
            [4, 5]
            [6, 7, 8]
            [5, 4]
            [8, 6, 7]
            [3, 1, 2]
            [7, 8, 6]
            [2, 3, 1]
            [4, 5]
            [1, 2, 3]
            [5, 4]
            [6, 7, 8]
            [4, 5]
            [8, 6, 7]
            [3, 1, 2]
            [7, 8, 6]
            [2, 3, 1]
            [5, 4]

        ..  container:: example

            Helianthates list of segments:

            >>> J = abjad.PitchClassSegment(items=[0, 2, 4])
            >>> K = abjad.PitchClassSegment(items=[5, 6])
            >>> L = abjad.PitchClassSegment(items=[7, 9, 11])
            >>> sequence = baca.helianthate([J, K, L], n=-1, m=1)
            >>> for item in sequence:
            ...     item
            ...
            PitchClassSegment([0, 2, 4])
            PitchClassSegment([5, 6])
            PitchClassSegment([7, 9, 11])
            PitchClassSegment([6, 5])
            PitchClassSegment([11, 7, 9])
            PitchClassSegment([4, 0, 2])
            PitchClassSegment([9, 11, 7])
            PitchClassSegment([2, 4, 0])
            PitchClassSegment([5, 6])
            PitchClassSegment([0, 2, 4])
            PitchClassSegment([6, 5])
            PitchClassSegment([7, 9, 11])
            PitchClassSegment([5, 6])
            PitchClassSegment([11, 7, 9])
            PitchClassSegment([4, 0, 2])
            PitchClassSegment([9, 11, 7])
            PitchClassSegment([2, 4, 0])
            PitchClassSegment([6, 5])

        ..  container:: example

            Helianthates trivially:

            >>> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
            >>> baca.helianthate(sequence)
            [[1, 2, 3], [4, 5], [6, 7, 8]]

        Returns new object with type equal to that of `sequence`.
        '''
        sequence_type = type(sequence)
        start = list(sequence[:])
        result = list(sequence[:])
        assert isinstance(n, int), repr(n)
        assert isinstance(m, int), repr(m)
        original_n = n
        original_m = m

        def _generalized_rotate(argument, n=0):
            if hasattr(argument, 'rotate'):
                return argument.rotate(n=n)
            argument_type = type(argument)
            argument = baca.Sequence(argument).rotate(n=n)
            return argument_type(argument)
        while True:
            inner = [_generalized_rotate(_, m) for _ in sequence]
            candidate = _generalized_rotate(inner, n)
            if candidate == start:
                break
            result.extend(candidate)
            n += original_n
            m += original_m
        result = sequence_type(result)
        return result

    @staticmethod
    def imbricate(
        voice_name,
        segment,
        *specifiers,
        allow_unused_pitches=None,
        by_pitch_class=None,
        extend_beam=None,
        hocket=None,
        selector=None,
        truncate_ties=None
        ):
        r'''Imbricates `segment` in `voice_name`.

        ..  container:: example

            Imbricates segment:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.imbricate('Voice 2', [10, 20, 19]),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                e''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                [
                                g''16
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                s8
                                s16
                                s16
                                bf'4
                                ~
                                bf'16
                                s16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                s16
                                s16
                                s4
                                s16
                                s16
                                af''16
                                [
                                g''16
                                ]
                            }
                            \times 4/5 {
                                s16
                                s4
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                >>

        '''
        return baca.ImbricationCommand(
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

    @staticmethod
    def instrument(instrument, selector='baca.leaf(0)'):
        r'''Attaches instrument.
        '''
        assert isinstance(instrument, abjad.Instrument)
        return baca.IndicatorCommand(
            indicators=[instrument],
            selector=selector,
            )

    @staticmethod
    def invisible_line_segment():
        r'''Makes invisible line segment.

        ..  container:: example

            >>> abjad.f(baca.invisible_line_segment())
            abjad.LineSegment(
                dash_period=0,
                left_broken_text=False,
                left_hspace=0.25,
                left_stencil_align_direction_y=Center,
                right_broken_padding=0,
                right_broken_text=False,
                right_padding=1.5,
                right_stencil_align_direction_y=Center,
                )

        Returns line segment.
        '''
        return abjad.LineSegment(
            dash_period=0,
            left_broken_text=False,
            left_hspace=0.25,
            left_stencil_align_direction_y=abjad.Center,
            right_broken_padding=0,
            right_broken_text=False,
            right_padding=1.5,
            right_stencil_align_direction_y=abjad.Center,
            )

    @staticmethod
    def label(expression, selector='baca.leaves()'):
        r'''Labels selections with label `expression`.

        ..  container:: example

            Labels pitch names:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.label(abjad.label().with_pitches(locale='us')),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                ^ \markup {
                                    \small
                                        C4
                                    }
                                d'16
                                ]
                                ^ \markup {
                                    \small
                                        D4
                                    }
                                bf'4
                                ~
                                ^ \markup {
                                    \small
                                        Bb4
                                    }
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                ^ \markup {
                                    \small
                                        "F#5"
                                    }
                                e''16
                                ]
                                ^ \markup {
                                    \small
                                        E5
                                    }
                                ef''4
                                ~
                                ^ \markup {
                                    \small
                                        Eb5
                                    }
                                ef''16
                                r16
                                af''16
                                [
                                ^ \markup {
                                    \small
                                        Ab5
                                    }
                                g''16
                                ]
                                ^ \markup {
                                    \small
                                        G5
                                    }
                            }
                            \times 4/5 {
                                a'16
                                ^ \markup {
                                    \small
                                        A4
                                    }
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        ..  container:: example

            Labels pitch names in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.label(
            ...         abjad.label().with_pitches(locale='us'),
            ...         baca.tuplet(1),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                ^ \markup {
                                    \small
                                        "F#5"
                                    }
                                e''16
                                ]
                                ^ \markup {
                                    \small
                                        E5
                                    }
                                ef''4
                                ~
                                ^ \markup {
                                    \small
                                        Eb5
                                    }
                                ef''16
                                r16
                                af''16
                                [
                                ^ \markup {
                                    \small
                                        Ab5
                                    }
                                g''16
                                ]
                                ^ \markup {
                                    \small
                                        G5
                                    }
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        '''
        return baca.LabelCommand(expression=expression, selector=selector)

    @staticmethod
    def laissez_vibrer(selector='baca.ptails()'):
        r'''Attaches laissez vibrer to PLT tails.

        ..  container:: example

            Attaches laissez vibrer to all PLT tails:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.laissez_vibrer(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs:: 

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                -\laissezVibrer                                                          %! IC
                                [
                                d'16
                                -\laissezVibrer                                                          %! IC
                                ]
                                bf'4
                                ~
                                bf'16
                                -\laissezVibrer                                                          %! IC
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\laissezVibrer                                                          %! IC
                                [
                                e''16
                                -\laissezVibrer                                                          %! IC
                                ]
                                ef''4
                                ~
                                ef''16
                                -\laissezVibrer                                                          %! IC
                                r16
                                af''16
                                -\laissezVibrer                                                          %! IC
                                [
                                g''16
                                -\laissezVibrer                                                          %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\laissezVibrer                                                          %! IC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches laissez vibrer to pitched tails in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.laissez_vibrer(baca.tuplets()[1:2].ptails()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\laissezVibrer                                                          %! IC
                                [
                                e''16
                                -\laissezVibrer                                                          %! IC
                                ]
                                ef''4
                                ~
                                ef''16
                                -\laissezVibrer                                                          %! IC
                                r16
                                af''16
                                -\laissezVibrer                                                          %! IC
                                [
                                g''16
                                -\laissezVibrer                                                          %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('laissezVibrer')],
            selector=selector,
            )

    @staticmethod
    def lbsd(y_offset, alignment_distances, selector='baca.leaf(0)'):
        r'''Makes line-break system details.

        Returns indicator command.
        '''
        alignment_distances = baca.sequence(alignment_distances).flatten()
        lbsd = baca.LBSD(
            alignment_distances=alignment_distances,
            y_offset=y_offset,
            )
        return baca.IndicatorCommand(
            indicators=[lbsd],
            selector=selector,
            )

    @staticmethod
    def lilypond_tag(tag, selector='baca.leaves()'):
        r'''Attaches LilyPond tag command to leaves.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.pitches('E4 F4'),
            ...     baca.lilypond_tag('ViolinI', baca.leaves()[:2]),
            ...     baca.lilypond_tag('ViolinI.ViolinII', baca.leaves()[2:]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        % GlobalSkips [measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            \tag ViolinI
                            {
            <BLANKLINE>
                                % MusicVoice [measure 1]                                             %! SM4
                                e'2
            <BLANKLINE>
                                % MusicVoice [measure 2]                                             %! SM4
                                f'4.
                            }
                            \tag ViolinI.ViolinII
                            {
            <BLANKLINE>
                                % MusicVoice [measure 3]                                             %! SM4
                                e'2
            <BLANKLINE>
                                % MusicVoice [measure 4]                                             %! SM4
                                f'4.
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

        Returns tag command.
        '''
        return baca.LilyPondTagCommand(selector=selector, tag=tag)

    @staticmethod
    def line_break(selector='baca.leaf(-1)'):
        r'''Attaches line break after last leaf.

        ..  container:: example

            Attaches line break after last leaf:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.line_break(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                e''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                [
                                g''16
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \break                                                                   %! IC
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches line break after last leaf in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.line_break(baca.tuplets()[1:2].leaf(-1)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                e''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                [
                                g''16
                                ]
                                \break                                                                   %! IC
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            #indicators=[abjad.LineBreak()],
            indicators=[abjad.LilyPondLiteral(r'\break', 'after')],
            selector=selector,
            )

    @staticmethod
    def literal(string, selector='baca.leaf(0)'):
        r'''Makes LilyPond literal.
        '''
        literal = abjad.LilyPondLiteral(string)
        return baca.IndicatorCommand(
            indicators=[literal],
            selector=selector,
            )

    @staticmethod
    def long_fermata(selector='baca.leaf(0)'):
        r'''Attaches long fermata to leaf.

        ..  container:: example

            Attaches long fermata to first leaf:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.long_fermata(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                -\longfermata                                                            %! IC
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                e''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                [
                                g''16
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches long fermata to first leaf in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.long_fermata(baca.tuplets()[1:2].phead(0)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\longfermata                                                            %! IC
                                [
                                e''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                [
                                g''16
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('longfermata')],
            selector=selector,
            )

    @staticmethod
    def loop(pitches, intervals):
        r'''Loops `pitches` at `intervals`.

        Returns loop.
        '''
        loop = baca.Loop(items=pitches, intervals=intervals)
        return baca.pitches(loop)

    @staticmethod
    def make_even_runs():
        r'''Makes even runs.
        '''
        return baca.RhythmCommand(
            rhythm_maker=rhythmos.EvenRunRhythmMaker()
            )

    @staticmethod
    def make_fused_tuplet_monads(tuplet_ratio=None):
        r'''Makes fused tuplet monads.
        '''
        if tuplet_ratio is None:
            tuplet_ratios = [(1,)]
        else:
            tuplet_ratios = [tuplet_ratio]
        return baca.RhythmCommand(
            division_expression=abjad.sequence()
                .sum()
                .sequence(),
            rhythm_maker=rhythmos.TupletRhythmMaker(
                tie_specifier=rhythmos.TieSpecifier(
                    repeat_ties=True,
                    ),
                tuplet_ratios=tuplet_ratios,
                ),
            )

    @staticmethod
    def make_multimeasure_rests():
        r'''Makes multimeasure rests.
        '''
        mask = rhythmos.SilenceMask(
            pattern=abjad.index_all(),
            use_multimeasure_rests=True,
            )
        return baca.RhythmCommand(
            rhythm_maker=rhythmos.NoteRhythmMaker(
                division_masks=[mask],
                ),
            )

    @staticmethod
    def make_notes(repeat_ties=False):
        r'''Makes notes; rewrites meter.
        '''
        if repeat_ties:
            tie_specifier = rhythmos.TieSpecifier(repeat_ties=True)
        else:
            tie_specifier = None
        return baca.RhythmCommand(
            rewrite_meter=True,
            rhythm_maker=rhythmos.NoteRhythmMaker(
                tie_specifier=tie_specifier,
                )
            )

    @staticmethod
    def make_repeated_durations(durations):
        r'''Makes repeated durations.
        '''
        if isinstance(durations, abjad.Duration):
            durations = [durations]
        elif isinstance(durations, tuple):
            assert len(durations) == 2
            durations = [abjad.Duration(durations)]
        return baca.RhythmCommand(
            division_expression=baca.split_by_durations(durations=durations),
            rewrite_meter=True,
            rhythm_maker=rhythmos.NoteRhythmMaker(
                tie_specifier=rhythmos.TieSpecifier(
                    repeat_ties=True,
                    ),
                ),
            )

    @staticmethod
    def make_rests():
        r'''Makes rests.
        '''
        return baca.RhythmCommand(
            rhythm_maker=rhythmos.NoteRhythmMaker(
                division_masks=[abjad.silence([0], 1)],
                ),
            )
    
    @staticmethod
    def make_rhythm(selection):
        r'''Set rhythm to `selection`.

        Return rhythm command.
        '''
        assert isinstance(selection, abjad.Selection), repr(selection)
        assert all(isinstance(_,  abjad.Component) for _ in selection)
        return baca.RhythmCommand(
            rhythm_maker=selection,
            )

    @staticmethod
    def make_scopes(voices, stages):
        r'''Makes scope crossproduct of `voices` against `stages`.

        Returns list of scopes.
        '''
        assert isinstance(voices, list), repr(voices)
        assert isinstance(stages, list), repr(stages)
        scopes = []
        for voice in voices:
            for item in stages:
                if isinstance(item, int):
                    scope = baca.scope(voice, item)
                else:
                    assert isinstance(item, tuple), repr(item)
                    scope = baca.scope(voice, *item)
                scopes.append(scope)
        return scopes

    @staticmethod
    def make_single_attack(duration):
        r'''Makes single attacks with `duration`.
        '''
        duration = abjad.Duration(duration)
        numerator, denominator = duration.pair
        rhythm_maker = rhythmos.IncisedRhythmMaker(
            incise_specifier=rhythmos.InciseSpecifier(
                fill_with_notes=False,
                outer_divisions_only=True,
                prefix_talea=[numerator],
                prefix_counts=[1],
                talea_denominator=denominator,
                ),
            )
        return baca.RhythmCommand(
            rhythm_maker=rhythm_maker,
            )

    @staticmethod
    def make_tied_notes(repeat_ties=False):
        r'''Makes tied notes; rewrites meter.
        '''
        return baca.RhythmCommand(
            rewrite_meter=True,
            rhythm_maker=rhythmos.NoteRhythmMaker(
                tie_specifier=rhythmos.TieSpecifier(
                    tie_across_divisions=True,
                    repeat_ties=repeat_ties,
                    ),
                ),
            )

    @staticmethod
    def make_tied_repeated_durations(durations):
        r'''Makes tied repeated durations.
        '''
        command = baca.make_repeated_durations(durations)
        return abjad.new(
            command,
            rewrite_meter=False,
            rhythm_maker__tie_specifier__tie_across_divisions=True,
            )

    @staticmethod
    def marcati(selector='baca.pheads()'):
        r'''Attaches marcati to pitched heads.

        ..  container:: example

            Attaches marcati to all pitched heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.marcati(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                -\marcato                                                                %! IC
                                [
                                d'16
                                -\marcato                                                                %! IC
                                ]
                                bf'4
                                -\marcato                                                                %! IC
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\marcato                                                                %! IC
                                [
                                e''16
                                -\marcato                                                                %! IC
                                ]
                                ef''4
                                -\marcato                                                                %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\marcato                                                                %! IC
                                [
                                g''16
                                -\marcato                                                                %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\marcato                                                                %! IC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches marcati to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.marcati(baca.tuplets()[1:2].pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\marcato                                                                %! IC
                                [
                                e''16
                                -\marcato                                                                %! IC
                                ]
                                ef''4
                                -\marcato                                                                %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\marcato                                                                %! IC
                                [
                                g''16
                                -\marcato                                                                %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('marcato')],
            selector=selector,
            )

    @staticmethod
    def margin_markup(
        argument,
        context='Staff',
        selector='baca.leaf(0)',
        ):
        r'''Sets margin markup on leaf.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.margin_markup(('Flute', 'Fl.')),
            ...     baca.pitches('E4 F4'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % GlobalSkips [measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % GlobalSkips [measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % GlobalSkips [measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % GlobalSkips [measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % MusicVoice [measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! EXPLICIT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                                e'2
                                ^ \markup {
                                    \column
                                        {
                                        %@% \line                                                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%     {                                                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%         \vcenter                                             %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%             [MarginMarkup                                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%         \vcenter                                             %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%             Flute                                            %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%         \concat                                              %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%             {                                                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%                 \vcenter                                     %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%                     Fl.                                      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%                 \vcenter                                     %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%                     ]                                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%             }                                                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                        %@%     }                                                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM10
                                            \line                                                        %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                {                                                        %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                    \with-color                                          %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                        #(x11-color 'blue)                               %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                        {                                                %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                            \vcenter                                     %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                                [MarginMarkup                            %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                            \vcenter                                     %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                                Flute                                    %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                            \concat                                      %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                                {                                        %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                                    \vcenter                             %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                                        Fl.                              %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                                    \vcenter                             %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                                        ]                                %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                                }                                        %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                        }                                                %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                                }                                                        %! EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR:SM11
                                        }
                                    }
                                \set Staff.instrumentName = \markup { Flute }                            %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % MusicVoice [measure 2]                                                 %! SM4
                                f'4.
                <BLANKLINE>
                                % MusicVoice [measure 3]                                                 %! SM4
                                e'2
                <BLANKLINE>
                                % MusicVoice [measure 4]                                                 %! SM4
                                f'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        Returns indicator command.
        '''
        if isinstance(argument, tuple):
            assert len(argument) == 2, repr(argument)
            markup, short_markup = argument
            if isinstance(markup, str):
                markup = abjad.Markup(markup)
            if isinstance(short_markup, str):
                short_markup = abjad.Markup(short_markup)
            margin_markup = baca.MarginMarkup(
                context=context,
                markup=markup,
                short_markup=short_markup,
                )
        elif isinstance(argument, (str, abjad.Markup)):
            margin_markup = baca.MarginMarkup(
                context=context,
                markup=argument,
                short_markup=argument,
                )
        elif isinstance(argument, baca.MarginMarkup):
            margin_markup = abjad.new(
                argument,
                context=context,
                )
        else:
            raise TypeError(argument)
        return baca.IndicatorCommand(
            indicators=[margin_markup],
            selector=selector,
            )

    @staticmethod
    def metronome_mark(key, selector='baca.leaf(0)'):
        r'''Attaches metronome mark with `key`.

        Returns metronome mark command.
        '''
        return baca.MetronomeMarkCommand(
            key=key,
            selector=selector,
            )

    @staticmethod
    def minimum_width(duration):
        r'''Makes horizontal spacing specifier with `duration` minimum width.
        '''
        return baca.HorizontalSpacingSpecifier(
            minimum_width=duration,
            )
