import abjad
import baca
from abjad import rhythmmakertools as rhythmos


class LibraryAF(abjad.AbjadObject):
    r'''Library A - F.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(1) Library'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def accents(selector='baca.pheads()'):
        r'''Attaches accents to pitched heads.

        ..  container:: example

            Attaches accents to all pitched heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accents(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                -\accent
                                [
                                d'16
                                -\accent
                                ]
                                bf'4
                                -\accent
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\accent
                                [
                                e''16
                                -\accent
                                ]
                                ef''4
                                -\accent
                                ~
                                ef''16
                                r16
                                af''16
                                -\accent
                                [
                                g''16
                                -\accent
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\accent
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches accents to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.accents(), baca.tuplet(1)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                -\accent
                                [
                                e''16
                                -\accent
                                ]
                                ef''4
                                -\accent
                                ~
                                ef''16
                                r16
                                af''16
                                -\accent
                                [
                                g''16
                                -\accent
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('>')],
            selector=selector,
            )

    @staticmethod
    def alternate_bow_strokes(downbow_first=True, selector='baca.pheads()'):
        r'''Attaches alternate bow strokes.

        ..  container:: example

            Attaches alternate bow strokes to all pitched heads (down-bow
            first):

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.alternate_bow_strokes(downbow_first=True),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                -\downbow
                                [
                                d'16
                                -\upbow
                                ]
                                bf'4
                                -\downbow
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\upbow
                                [
                                e''16
                                -\downbow
                                ]
                                ef''4
                                -\upbow
                                ~
                                ef''16
                                r16
                                af''16
                                -\downbow
                                [
                                g''16
                                -\upbow
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\downbow
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches alternate bow strokes to all pitched heads (up-bow first):

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.alternate_bow_strokes(downbow_first=False),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(6),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #6
                                r8
                                c'16
                                -\upbow
                                [
                                d'16
                                -\downbow
                                ]
                                bf'4
                                -\upbow
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\downbow
                                [
                                e''16
                                -\upbow
                                ]
                                ef''4
                                -\downbow
                                ~
                                ef''16
                                r16
                                af''16
                                -\upbow
                                [
                                g''16
                                -\downbow
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\upbow
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches alternate bow strokes to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.alternate_bow_strokes(),
            ...         baca.tuplet(1),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(6),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #6
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
                                -\downbow
                                [
                                e''16
                                -\upbow
                                ]
                                ef''4
                                -\downbow
                                ~
                                ef''16
                                r16
                                af''16
                                -\upbow
                                [
                                g''16
                                -\downbow
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if downbow_first:
            articulations = ['downbow', 'upbow']
        else:
            articulations = ['upbow', 'downbow']
        articulations = [abjad.Articulation(_) for _ in articulations]
        return baca.IndicatorCommand(
            indicators=articulations,
            selector=selector,
            )

    @staticmethod
    def anchor(remote_voice_name, remote_selector=None, local_selector=None):
        r'''Anchors music to start of remote selection.
        '''
        return baca.AnchorSpecifier(
            local_selector=local_selector,
            remote_selector=remote_selector,
            remote_voice_name=remote_voice_name,
            )

    @staticmethod
    def anchor_after(
        remote_voice_name,
        remote_selector=None,
        local_selector=None,
        ):
        r'''Anchors music to stop of remote selection.
        '''
        return baca.AnchorSpecifier(
            local_selector=local_selector,
            remote_selector=remote_selector,
            remote_voice_name=remote_voice_name,
            use_remote_stop_offset=True,
            )

    @staticmethod
    def anchor_to_figure(figure_name):
        r'''Anchors music to start of figure.
        '''
        return baca.AnchorSpecifier(
            figure_name=figure_name,
            )

    @staticmethod
    def ancora_dynamic(
        dynamic,
        selector='baca.phead(0)',
        direction=abjad.Down,
        ):
        r'''Attaches ancora dynamic pitched head 0.

        ..  container:: example

            Attaches ancora dynamic to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.ancora_dynamic('ff'),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                [
                                _ \markup {
                                    \dynamic
                                        ff
                                    \upright
                                        ancora
                                    }
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches ancora dynamic to pitched head 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.ancora_dynamic(
            ...         'ff',
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                _ \markup {
                                    \dynamic
                                        ff
                                    \upright
                                        ancora
                                    }
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        markup = abjad.Markup(dynamic).dynamic()
        markup += abjad.Markup('ancora').upright()
        markup = abjad.new(markup, direction=direction)
        return baca.IndicatorCommand(
            indicators=[markup],
            selector=selector,
            )

    @staticmethod
    def arpeggios(selector='baca.cheads()'):
        r"""Attaches arpeggios.

        ..  container:: example

            Attaches arpeggios to all chord heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.arpeggios(),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                <c' d' bf'>8
                                -\arpeggio
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            {
                                <ef'' e'' fs'''>8
                                -\arpeggio
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            {
                                <g' af''>8
                                -\arpeggio
                                ~
                                [
                                <g' af''>32
                                ]
                                r16.
                            }
                            {
                                a'8
                                ~
                                [
                                a'32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches arpeggios to last two chord heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.arpeggios(baca.cheads()[-2:]),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                <c' d' bf'>8
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            {
                                <ef'' e'' fs'''>8
                                -\arpeggio
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            {
                                <g' af''>8
                                -\arpeggio
                                ~
                                [
                                <g' af''>32
                                ]
                                r16.
                            }
                            {
                                a'8
                                ~
                                [
                                a'32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        """
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('arpeggio')],
            selector=selector,
            )

    @staticmethod
    def articulations(articulations, selector='baca.pheads()'):
        r'''Attaches articulations.
        '''
        return baca.IndicatorCommand(indicators=articulations)

    @staticmethod
    def bar_extent(pair, selector='baca.leaf(0)', after=False, tag=None):
        r'''Overrides bar line bar extent.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing_specifier=baca.minimum_width((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.bar_extent((-4, 4), baca.group_by_measure()[1]),
            ...     baca.bar_extent((-4, 4), baca.leaf(-1), after=True),
            ...     baca.make_even_runs(),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     )

            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     remove=[
            ...         baca.Tags.FIGURE_NAME_MARKUP,
            ...         baca.Tags.STAGE_NUMBER_MARKUP,
            ...         baca.Tags.build(baca.Tags.SPACING_MARKUP),
            ...         ],
            ...     )
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=79)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % GlobalSkips [measure 1]
                            \time 4/8                                                          %%! SM1
                            \bar ""                                                            %%! EMPTY_START_BAR:SM2
                            \newSpacingSection
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)   %%! SEGMENT:SPACING
                            s1 * 1/2
                <BLANKLINE>
                            % GlobalSkips [measure 2]
                            \time 3/8                                                          %%! SM1
                            \newSpacingSection
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)   %%! SEGMENT:SPACING
                            s1 * 3/8
                <BLANKLINE>
                            % GlobalSkips [measure 3]
                            \time 4/8                                                          %%! SM1
                            \newSpacingSection
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)   %%! SEGMENT:SPACING
                            s1 * 1/2
                <BLANKLINE>
                            % GlobalSkips [measure 4]
                            \time 3/8                                                          %%! SM1
                            \newSpacingSection
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)   %%! SEGMENT:SPACING
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    % MusicVoice [measure 1]
                                    e'8
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
                                    % MusicVoice [measure 2]
                                    \override Staff.BarLine.bar-extent = #'(-4 . 4)
                                    g'8
                                    [
                <BLANKLINE>
                                    f''8
                <BLANKLINE>
                                    e'8
                                    ]
                                    \revert Staff.BarLine.bar-extent
                                }
                                {
                <BLANKLINE>
                                    % MusicVoice [measure 3]
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
                                    % MusicVoice [measure 4]
                                    f''8
                                    [
                <BLANKLINE>
                                    e'8
                <BLANKLINE>
                                    d''8
                                    ]
                                    \bar "|"
                                    \once \override Staff.BarLine.bar-extent = #'(-4 . 4)
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        '''
        return baca.OverrideCommand(
            after=after,
            attribute='bar_extent',
            value=pair,
            context='Staff',
            grob='bar_line',
            selector=selector,
            tag=tag,
            )

    @staticmethod
    def bass_to_octave(n, selector='baca.plts()'):
        r"""Octave-transposes music.

        ..  container:: example

            Octave-transposes music such that the lowest note in the entire
            selection appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.bass_to_octave(3),
            ...     baca.color(baca.plts().group()),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <c d bf>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <c d bf>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f'8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f'32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <ef' e' fs''>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <ef' e' fs''>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <g af'>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <g af'>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music such that the lowest pitch in each pitched
            logical tie appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.map(baca.bass_to_octave(3), baca.plts()),
            ...     baca.color(baca.plts()),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c d bf>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c d bf>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f8
                                ~
                                [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <g af'>8
                                ~
                                [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <g af'>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music such that the lowest pitch in each of the
            last two pitched logical ties appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.map(baca.bass_to_octave(3), baca.plts()[-2:]),
            ...     baca.color(baca.plts()[-2:]),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                <c' d' bf'>8
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            {
                                <ef'' e'' fs'''>8
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g af'>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g af'>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a8
                                ~
                                [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        """
        return baca.RegisterToOctaveCommand(
            anchor=abjad.Bottom,
            octave_number=n,
            selector=selector,
            )

    @staticmethod
    def beam_divisions(stemlets=None):
        r'''Beams divisions.

        ..  container:: example

            Beams divisions:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_divisions(),
            ...     baca.rests_around([2], [2]),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                r8
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            {
                                a'16
                                r8
                            }
                        }
                    }
                >>

        ..  container:: example

            Beams divisions with stemlets:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_divisions(stemlets=2),
            ...     baca.rests_around([2], [2]),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \override Staff.Stem.stemlet-length = #2
                                r8
                                [
                                c'16
                                d'16
                                \revert Staff.Stem.stemlet-length
                                bf'16
                                ]
                            }
                            {
                                \override Staff.Stem.stemlet-length = #2
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                \revert Staff.Stem.stemlet-length
                                g''16
                                ]
                            }
                            {
                                \override Staff.Stem.stemlet-length = #2
                                a'16
                                [
                                \revert Staff.Stem.stemlet-length
                                r8
                                ]
                            }
                        }
                    }
                >>

        '''
        return rhythmos.BeamSpecifier(
            beam_each_division=True,
            beam_rests=bool(stemlets),
            stemlet_length=stemlets,
            )

    @staticmethod
    def beam_everything(hide_nibs=None, stemlets=None):
        r'''Beams everything.

        ..  container:: example

            Beams everything:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_everything(),
            ...     baca.rests_around([2], [2]),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                r8
                                [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                c'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                bf'16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                fs''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                e''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                ef''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                af''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                g''16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                a'16
                                r8
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Beams everything with stemlets:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_everything(stemlets=2),
            ...     baca.rests_around([2], [2]),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \override Staff.Stem.stemlet-length = #2
                                r8
                                [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                c'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                bf'16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                fs''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                e''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                ef''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                af''16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                g''16
                            }
                            {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                a'16
                                \revert Staff.Stem.stemlet-length
                                r8
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Beams everything without nibs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_everything(hide_nibs=True),
            ...     baca.rests_around([2], [2]),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                r8
                                [
                                c'16
                                d'16
                                bf'16
                            }
                            {
                                fs''16
                                e''16
                                ef''16
                                af''16
                                g''16
                            }
                            {
                                a'16
                                r8
                                ]
                            }
                        }
                    }
                >>

        '''
        return rhythmos.BeamSpecifier(
            beam_divisions_together=True,
            beam_each_division=True,
            beam_rests=True,
            hide_nibs=hide_nibs,
            stemlet_length=stemlets,
            )

    @staticmethod
    def beam_positions(n=None, selector='baca.leaves()'):
        r'''Overrides beam positions.

        ..  container:: example

            Overrides beam positions on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_positions(6),
            ...     baca.rests_around([2], [4]),
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \times 4/5 {
                                \override Beam.positions = #'(6 . 6)
                                r8
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \times 4/5 {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Beam.positions
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides beam positions on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_positions(6, baca.tuplet(1)),
            ...     baca.rests_around([2], [4]),
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \times 4/5 {
                                r8
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \times 4/5 {
                                \override Beam.positions = #'(6 . 6)
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                                \revert Beam.positions
                            }
                            \times 4/5 {
                                a'16
                                r4
                            }
                        }
                    }
                >>

        '''
        assert isinstance(n, (int, float)), repr(n)
        return baca.OverrideCommand(
            attribute='positions',
            value=(n, n),
            grob='beam',
            selector=selector,
            )

    @staticmethod
    def beam_runs(hide_nibs=None):
        r'''Beams PLT runs.

        ..  container:: example

            Beams PLT runs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_runs(),
            ...     baca.rests_around([2], [2]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                c'16
                                [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16
                                ]
                                bf'4
                                ~
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16
                                [
                                ]
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                fs''16
                                [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                e''16
                                ]
                                ef''4
                                ~
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                ef''16
                                [
                                ]
                                r16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                af''16
                                [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                g''16
                            }
                            \times 2/3 {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                a'16
                                ]
                                r8
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Beams PLT runs without nibs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_runs(hide_nibs=True),
            ...     baca.rests_around([2], [2]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                            }
                            \times 2/3 {
                                a'16
                                ]
                                r8
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return rhythmos.BeamSpecifier(
            beam_divisions_together=True,
            beam_each_division=True,
            beam_rests=False,
            hide_nibs=hide_nibs,
            )

    @staticmethod
    def center_to_octave(n, selector='baca.plts()'):
        r"""Octave-transposes music.

        ..  container:: example

            Octave-transposes music such that the centroid of all PLTs appears
            in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.center_to_octave(3),
            ...     baca.color(baca.plts().group()),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <c, d, bf,>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <c, d, bf,>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <ef e fs'>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <ef e fs'>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <g, af>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <g, af>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a,8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a,32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music such that the centroid of each pitched
            logical tie appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.map(baca.center_to_octave(3), baca.plts()),
            ...     baca.color(baca.plts()),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c d bf>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c d bf>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f8
                                ~
                                [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <g, af>8
                                ~
                                [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <g, af>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music such that the centroid of each of the last
            two pitched logical ties appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.map(baca.center_to_octave(3), baca.plts()[-2:]),
            ...     baca.color(baca.plts()[-2:]),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                <c' d' bf'>8
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            {
                                <ef'' e'' fs'''>8
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g, af>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g, af>32
                                ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a8
                                ~
                                [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        """
        return baca.RegisterToOctaveCommand(
            anchor=abjad.Center,
            octave_number=n,
            selector=selector,
            )

    @staticmethod
    def clef(clef='treble', selector='baca.leaf(0)'):
        r'''Attaches clef to leaf 0.

        ..  container:: example

            Attaches clef to leaf 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.clef('alto'),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(7),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #7
                                \clef "alto"
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches clef to leaf 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.clef(
            ...         clef='alto',
            ...         selector=baca.tuplets()[1:2].leaf(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(7),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #7
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
                                \clef "alto"
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.Clef(clef)],
            selector=selector,
            )

    @staticmethod
    def clef_extra_offset(pair, selector='baca.leaf(0)'):
        r'''Overrides clef extra offset.
        '''
        return baca.OverrideCommand(
            attribute='extra_offset',
            context='Staff',
            grob='clef',
            selector=selector,
            value=pair,
            )

    @staticmethod
    def clef_x_extent_false(selector='baca.leaf(0)'):
        r'''Overrides clef x-extent.
        '''
        return baca.OverrideCommand(
            attribute='X_extent',
            context='Staff',
            grob='clef',
            selector=selector,
            value=False,
            )

    @staticmethod
    def clusters(widths, selector='baca.plts()', start_pitch=None):
        r'''Makes clusters.
        '''
        return baca.ClusterCommand(
            selector=selector,
            start_pitch=start_pitch,
            widths=widths,
            )

    @staticmethod
    def coat(pitch):
        r'''Coats `pitch`.

        ..  container:: example

            Coats pitches:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     3 * [[0, 2, 10]],
            ...     baca.imbricate(
            ...         'Voice 2',
            ...         [baca.coat(0), baca.coat(2), 10, 0, 2],
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \times 4/5 {
                                r8
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \times 2/3 {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/7 {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                                r4
                            }
                        }
                    }
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \times 4/5 {
                                s8
                                s16
                                s16
                                bf'16
                            }
                            \times 2/3 {
                                c'16
                                [
                                d'16
                                ]
                                s16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/7 {
                                s16
                                s16
                                s16
                                s4
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                >>

        '''
        return baca.Coat(pitch)

    @staticmethod
    def color(selector='baca.leaves()'):
        r'''Colors leaves.

        ..  container:: example

            Colors all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.color(),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r8
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                d'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'4
                                ~
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'16
                                \once \override Dots.color = #blue
                                \once \override Rest.color = #blue
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                ef''4
                                ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                ef''16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                g''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a'16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Colors leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.color(selector=baca.tuplets()[1:2].leaves()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                d'16
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                ef''4
                                ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                ef''16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                g''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.ColorCommand(selector=selector)

    @staticmethod
    def color_fingerings(numbers, selector='baca.pheads()'):
        r'''Color fingerings.

        Returns color fingering command.
        '''
        return baca.ColorFingeringCommand(numbers=numbers, selector=selector)

    @staticmethod
    def compound_quarter_divisions():
        r'''Makes compound quarter divisions.

        Returns division sequence expression.
        '''
        expression = baca.DivisionSequenceExpression()
        expression = expression.split_by_durations(
            compound_meter_multiplier=abjad.Multiplier((3, 2)),
            durations=[abjad.Duration(1, 4)],
            )
        expression = expression.flatten(depth=-1)
        return expression

    @staticmethod
    def cross_note_heads(selector='baca.tleaves()'):
        r'''Overrides note-head style on pitched leaves.

        ..  container:: example

            Overrides note-head style on all pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.cross_note_heads(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override NoteHead.style = #'cross
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
                                \revert NoteHead.style
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides note-head style on pitched leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.cross_note_heads(baca.tuplet(1)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                \override NoteHead.style = #'cross
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
                                \revert NoteHead.style
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute='style',
            value='cross',
            grob='note_head',
            selector=selector,
            )

    @staticmethod
    def cross_staff(selector='baca.pheads()'):
        r'''Attaches cross-staff command to leaves.

        ..  container:: example

            Attaches cross-staff command to all leaves:

            >>> score_template = baca.StringTrioScoreTemplate()
            >>> accumulator = baca.MusicAccumulator(score_template)
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolinMusicVoice',
            ...         [[9, 11, 12, 14, 16]],
            ...         baca.flags(),
            ...         baca.stems_up(),
            ...         denominator=8,
            ...         figure_name='vn.1',
            ...         talea_denominator=8,
            ...         ),
            ...     )
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolaMusicVoice',
            ...         [[0, 2, 4, 5, 7]],
            ...         baca.anchor('ViolinMusicVoice'),
            ...         baca.cross_staff(),
            ...         baca.flags(),
            ...         baca.stems_up(),
            ...         figure_name='va.1',
            ...         talea_denominator=8,
            ...         ),
            ...     )
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolinMusicVoice',
            ...         [[15]],
            ...         baca.flags(),
            ...         figure_name='vn.2',
            ...         talea_denominator=8,
            ...         ),
            ...     )

            >>> maker = baca.SegmentMaker(
            ...     ignore_repeat_pitch_classes=True,
            ...     ignore_unregistered_pitches=True,
            ...     score_template=accumulator.score_template,
            ...     spacing_specifier=baca.minimum_width((1, 12)),
            ...     time_signatures=accumulator.time_signatures,
            ...     )
            >>> accumulator.populate_segment_maker(maker)
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     remove=[
            ...         baca.Tags.FIGURE_NAME_MARKUP,
            ...         baca.Tags.STAGE_NUMBER_MARKUP,
            ...         baca.Tags.build(baca.Tags.SPACING_MARKUP),
            ...         ],
            ...     )
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=79)
                \context Score = "Score" <<
                    \tag violin.viola.cello
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % GlobalSkips [measure 1]
                            \time 5/8                                                          %%! SM1
                            \bar ""                                                            %%! EMPTY_START_BAR:SM2
                            \newSpacingSection
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)   %%! SEGMENT:SPACING
                            s1 * 5/8
                <BLANKLINE>
                            % GlobalSkips [measure 2]
                            \time 2/16                                                         %%! SM1
                            \newSpacingSection
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)   %%! SEGMENT:SPACING
                            s1 * 1/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context StringSectionStaffGroup = "String Section Staff Group" <<
                            \tag violin
                            \context ViolinMusicStaff = "ViolinMusicStaff" {
                                \context ViolinMusicVoice = "ViolinMusicVoice" {
                                    {
                                        {
                <BLANKLINE>
                                            % ViolinMusicVoice [measure 1]
                                            \override Stem.direction = #up
                                            \set ViolinMusicStaff.instrumentName = \markup {   %%! DEFAULT_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_INSTRUMENT
                                                    #10                                        %%! DEFAULT_INSTRUMENT
                                                    Violin                                     %%! DEFAULT_INSTRUMENT
                                                }                                              %%! DEFAULT_INSTRUMENT
                                            \set ViolinMusicStaff.shortInstrumentName = \markup { %%! DEFAULT_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_INSTRUMENT
                                                    #10                                        %%! DEFAULT_INSTRUMENT
                                                    Vn.                                        %%! DEFAULT_INSTRUMENT
                                                }                                              %%! DEFAULT_INSTRUMENT
                                            \set ViolinMusicStaff.forceClef = ##t              %%! DEFAULT_CLEF
                                            \clef "treble"                                     %%! DEFAULT_CLEF
                                            \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! DEFAULT_INSTRUMENT_COLOR
                                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! DEFAULT_CLEF_COLOR
                                            %%% \override ViolinMusicStaff.Clef.color = ##f    %%! DEFAULT_CLEF_UNCOLOR
                                            a'8
                                            ^ \markup {
                                                \column
                                                    {
                                                        %%% \line                              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%     {                              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%         \vcenter                   %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             (Violin                %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%         \vcenter                   %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             \hcenter-in            %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 #10                %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 Violin             %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%         \concat                    %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             {                      %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 \vcenter           %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                     \hcenter-in    %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                         #10        %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                         Vn.        %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 \vcenter           %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                     )              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             }                      %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%     }                              %%! DEFAULT_INSTRUMENT_ALERT
                                                        \line                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            {                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \with-color                    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    #(x11-color 'DarkViolet)   %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    {                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter               %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            (Violin            %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter               %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            \hcenter-in        %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                #10            %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                Violin         %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \concat                %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            {                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                \vcenter       %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                    \hcenter-in %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                        #10    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                        Vn.    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                \vcenter       %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                    )          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            }                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    }                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            }                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    }
                                                }
                                            \set ViolinMusicStaff.instrumentName = \markup {   %%! DEFAULT_REDRAW_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_REDRAW_INSTRUMENT
                                                    #10                                        %%! DEFAULT_REDRAW_INSTRUMENT
                                                    Violin                                     %%! DEFAULT_REDRAW_INSTRUMENT
                                                }                                              %%! DEFAULT_REDRAW_INSTRUMENT
                                            \set ViolinMusicStaff.shortInstrumentName = \markup { %%! DEFAULT_REDRAW_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_REDRAW_INSTRUMENT
                                                    #10                                        %%! DEFAULT_REDRAW_INSTRUMENT
                                                    Vn.                                        %%! DEFAULT_REDRAW_INSTRUMENT
                                                }                                              %%! DEFAULT_REDRAW_INSTRUMENT
                                            \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! DEFAULT_REDRAW_INSTRUMENT_COLOR
                                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %%! DEFAULT_CLEF_COLOR_REDRAW
                <BLANKLINE>
                                            b'8
                <BLANKLINE>
                                            c''8
                <BLANKLINE>
                                            d''8
                <BLANKLINE>
                                            e''8
                                            \revert Stem.direction
                                        }
                                    }
                                    {
                                        {
                <BLANKLINE>
                                            % ViolinMusicVoice [measure 2]
                                            ef''8
                                            \bar "|"
                <BLANKLINE>
                                        }
                                    }
                                }
                            }
                            \tag viola
                            \context ViolaMusicStaff = "ViolaMusicStaff" {
                                \context ViolaMusicVoice = "ViolaMusicVoice" {
                                    {
                                        {
                <BLANKLINE>
                                            % ViolaMusicVoice [measure 1]
                                            \override Stem.direction = #up
                                            \set ViolaMusicStaff.instrumentName = \markup {    %%! DEFAULT_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_INSTRUMENT
                                                    #10                                        %%! DEFAULT_INSTRUMENT
                                                    Viola                                      %%! DEFAULT_INSTRUMENT
                                                }                                              %%! DEFAULT_INSTRUMENT
                                            \set ViolaMusicStaff.shortInstrumentName = \markup { %%! DEFAULT_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_INSTRUMENT
                                                    #10                                        %%! DEFAULT_INSTRUMENT
                                                    Va.                                        %%! DEFAULT_INSTRUMENT
                                                }                                              %%! DEFAULT_INSTRUMENT
                                            \set ViolaMusicStaff.forceClef = ##t               %%! DEFAULT_CLEF
                                            \clef "alto"                                       %%! DEFAULT_CLEF
                                            \crossStaff
                                            \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! DEFAULT_INSTRUMENT_COLOR
                                            \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! DEFAULT_CLEF_COLOR
                                            %%% \override ViolaMusicStaff.Clef.color = ##f     %%! DEFAULT_CLEF_UNCOLOR
                                            c'8
                                            ^ \markup {
                                                \column
                                                    {
                                                        %%% \line                              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%     {                              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%         \vcenter                   %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             (Viola                 %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%         \vcenter                   %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             \hcenter-in            %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 #10                %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 Viola              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%         \concat                    %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             {                      %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 \vcenter           %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                     \hcenter-in    %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                         #10        %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                         Va.        %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 \vcenter           %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                     )              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             }                      %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%     }                              %%! DEFAULT_INSTRUMENT_ALERT
                                                        \line                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            {                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \with-color                    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    #(x11-color 'DarkViolet)   %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    {                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter               %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            (Viola             %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter               %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            \hcenter-in        %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                #10            %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                Viola          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \concat                %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            {                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                \vcenter       %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                    \hcenter-in %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                        #10    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                        Va.    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                \vcenter       %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                    )          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            }                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    }                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            }                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    }
                                                }
                                            \set ViolaMusicStaff.instrumentName = \markup {    %%! DEFAULT_REDRAW_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_REDRAW_INSTRUMENT
                                                    #10                                        %%! DEFAULT_REDRAW_INSTRUMENT
                                                    Viola                                      %%! DEFAULT_REDRAW_INSTRUMENT
                                                }                                              %%! DEFAULT_REDRAW_INSTRUMENT
                                            \set ViolaMusicStaff.shortInstrumentName = \markup { %%! DEFAULT_REDRAW_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_REDRAW_INSTRUMENT
                                                    #10                                        %%! DEFAULT_REDRAW_INSTRUMENT
                                                    Va.                                        %%! DEFAULT_REDRAW_INSTRUMENT
                                                }                                              %%! DEFAULT_REDRAW_INSTRUMENT
                                            \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! DEFAULT_REDRAW_INSTRUMENT_COLOR
                                            \override ViolaMusicStaff.Clef.color = #(x11-color 'violet) %%! DEFAULT_CLEF_COLOR_REDRAW
                <BLANKLINE>
                                            \crossStaff
                                            d'8
                <BLANKLINE>
                                            \crossStaff
                                            e'8
                <BLANKLINE>
                                            \crossStaff
                                            f'8
                <BLANKLINE>
                                            \crossStaff
                                            g'8
                                            \revert Stem.direction
                                        }
                                    }
                <BLANKLINE>
                                    % ViolaMusicVoice [measure 2]
                                    R1 * 1/8
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                            \tag cello
                            \context CelloMusicStaff = "CelloMusicStaff" {
                                \context CelloMusicVoice = "CelloMusicVoice" {
                <BLANKLINE>
                                    % CelloMusicVoice [measure 1]
                                    \set CelloMusicStaff.instrumentName = \markup {            %%! DEFAULT_INSTRUMENT
                                        \hcenter-in                                            %%! DEFAULT_INSTRUMENT
                                            #10                                                %%! DEFAULT_INSTRUMENT
                                            Cello                                              %%! DEFAULT_INSTRUMENT
                                        }                                                      %%! DEFAULT_INSTRUMENT
                                    \set CelloMusicStaff.shortInstrumentName = \markup {       %%! DEFAULT_INSTRUMENT
                                        \hcenter-in                                            %%! DEFAULT_INSTRUMENT
                                            #10                                                %%! DEFAULT_INSTRUMENT
                                            Vc.                                                %%! DEFAULT_INSTRUMENT
                                        }                                                      %%! DEFAULT_INSTRUMENT
                                    \set CelloMusicStaff.forceClef = ##t                       %%! DEFAULT_CLEF
                                    \clef "bass"                                               %%! DEFAULT_CLEF
                                    \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! DEFAULT_INSTRUMENT_COLOR
                                    \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! DEFAULT_CLEF_COLOR
                                    %%% \override CelloMusicStaff.Clef.color = ##f             %%! DEFAULT_CLEF_UNCOLOR
                                    R1 * 5/8
                                    ^ \markup {
                                        \column
                                            {
                                                %%% \line                                      %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%     {                                      %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%         \vcenter                           %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%             (Cello                         %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%         \vcenter                           %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%             \hcenter-in                    %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                 #10                        %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                 Cello                      %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%         \concat                            %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%             {                              %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                 \vcenter                   %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                     \hcenter-in            %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                         #10                %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                         Vc.                %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                 \vcenter                   %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                     )                      %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%             }                              %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%     }                                      %%! DEFAULT_INSTRUMENT_ALERT
                                                \line                                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    {                                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        \with-color                            %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            #(x11-color 'DarkViolet)           %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            {                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \vcenter                       %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    (Cello                     %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \vcenter                       %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \hcenter-in                %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        #10                    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        Cello                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \concat                        %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    {                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter               %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            \hcenter-in        %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                #10            %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                Vc.            %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter               %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            )                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    }                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            }                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    }                                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                            }
                                        }
                                    \set CelloMusicStaff.instrumentName = \markup {            %%! DEFAULT_REDRAW_INSTRUMENT
                                        \hcenter-in                                            %%! DEFAULT_REDRAW_INSTRUMENT
                                            #10                                                %%! DEFAULT_REDRAW_INSTRUMENT
                                            Cello                                              %%! DEFAULT_REDRAW_INSTRUMENT
                                        }                                                      %%! DEFAULT_REDRAW_INSTRUMENT
                                    \set CelloMusicStaff.shortInstrumentName = \markup {       %%! DEFAULT_REDRAW_INSTRUMENT
                                        \hcenter-in                                            %%! DEFAULT_REDRAW_INSTRUMENT
                                            #10                                                %%! DEFAULT_REDRAW_INSTRUMENT
                                            Vc.                                                %%! DEFAULT_REDRAW_INSTRUMENT
                                        }                                                      %%! DEFAULT_REDRAW_INSTRUMENT
                                    \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! DEFAULT_REDRAW_INSTRUMENT_COLOR
                                    \override CelloMusicStaff.Clef.color = #(x11-color 'violet) %%! DEFAULT_CLEF_COLOR_REDRAW
                <BLANKLINE>
                                    % CelloMusicVoice [measure 2]
                                    R1 * 1/8
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                        >>
                    >>
                >>

        ..  container:: example

            Attaches cross-staff command to last two pitched leaves:

            >>> score_template = baca.StringTrioScoreTemplate()
            >>> accumulator = baca.MusicAccumulator(score_template)
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolinMusicVoice',
            ...         [[9, 11, 12, 14, 16]],
            ...         baca.flags(),
            ...         baca.stems_up(),
            ...         denominator=8,
            ...         figure_name='vn.1',
            ...         talea_denominator=8,
            ...         ),
            ...     )
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolaMusicVoice',
            ...         [[0, 2, 4, 5, 7]],
            ...         baca.anchor('ViolinMusicVoice'),
            ...         baca.cross_staff(selector=baca.pleaves()[-2:]),
            ...         baca.flags(),
            ...         baca.stems_up(),
            ...         figure_name='va.1',
            ...         talea_denominator=8,
            ...         ),
            ...     )
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolinMusicVoice',
            ...         [[15]],
            ...         baca.flags(),
            ...         figure_name='vn.2',
            ...         talea_denominator=8,
            ...         ),
            ...     )

            >>> maker = baca.SegmentMaker(
            ...     ignore_repeat_pitch_classes=True,
            ...     ignore_unregistered_pitches=True,
            ...     score_template=accumulator.score_template,
            ...     spacing_specifier=baca.minimum_width((1, 12)),
            ...     time_signatures=accumulator.time_signatures,
            ...     )
            >>> accumulator.populate_segment_maker(maker)
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     remove=[
            ...         baca.Tags.FIGURE_NAME_MARKUP,
            ...         baca.Tags.STAGE_NUMBER_MARKUP,
            ...         baca.Tags.build(baca.Tags.SPACING_MARKUP),
            ...         ],
            ...     )
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=79)
                \context Score = "Score" <<
                    \tag violin.viola.cello
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % GlobalSkips [measure 1]
                            \time 5/8                                                          %%! SM1
                            \bar ""                                                            %%! EMPTY_START_BAR:SM2
                            \newSpacingSection
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)   %%! SEGMENT:SPACING
                            s1 * 5/8
                <BLANKLINE>
                            % GlobalSkips [measure 2]
                            \time 2/16                                                         %%! SM1
                            \newSpacingSection
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)   %%! SEGMENT:SPACING
                            s1 * 1/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context StringSectionStaffGroup = "String Section Staff Group" <<
                            \tag violin
                            \context ViolinMusicStaff = "ViolinMusicStaff" {
                                \context ViolinMusicVoice = "ViolinMusicVoice" {
                                    {
                                        {
                <BLANKLINE>
                                            % ViolinMusicVoice [measure 1]
                                            \override Stem.direction = #up
                                            \set ViolinMusicStaff.instrumentName = \markup {   %%! DEFAULT_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_INSTRUMENT
                                                    #10                                        %%! DEFAULT_INSTRUMENT
                                                    Violin                                     %%! DEFAULT_INSTRUMENT
                                                }                                              %%! DEFAULT_INSTRUMENT
                                            \set ViolinMusicStaff.shortInstrumentName = \markup { %%! DEFAULT_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_INSTRUMENT
                                                    #10                                        %%! DEFAULT_INSTRUMENT
                                                    Vn.                                        %%! DEFAULT_INSTRUMENT
                                                }                                              %%! DEFAULT_INSTRUMENT
                                            \set ViolinMusicStaff.forceClef = ##t              %%! DEFAULT_CLEF
                                            \clef "treble"                                     %%! DEFAULT_CLEF
                                            \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! DEFAULT_INSTRUMENT_COLOR
                                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! DEFAULT_CLEF_COLOR
                                            %%% \override ViolinMusicStaff.Clef.color = ##f    %%! DEFAULT_CLEF_UNCOLOR
                                            a'8
                                            ^ \markup {
                                                \column
                                                    {
                                                        %%% \line                              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%     {                              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%         \vcenter                   %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             (Violin                %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%         \vcenter                   %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             \hcenter-in            %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 #10                %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 Violin             %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%         \concat                    %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             {                      %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 \vcenter           %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                     \hcenter-in    %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                         #10        %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                         Vn.        %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 \vcenter           %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                     )              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             }                      %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%     }                              %%! DEFAULT_INSTRUMENT_ALERT
                                                        \line                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            {                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \with-color                    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    #(x11-color 'DarkViolet)   %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    {                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter               %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            (Violin            %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter               %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            \hcenter-in        %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                #10            %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                Violin         %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \concat                %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            {                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                \vcenter       %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                    \hcenter-in %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                        #10    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                        Vn.    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                \vcenter       %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                    )          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            }                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    }                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            }                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    }
                                                }
                                            \set ViolinMusicStaff.instrumentName = \markup {   %%! DEFAULT_REDRAW_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_REDRAW_INSTRUMENT
                                                    #10                                        %%! DEFAULT_REDRAW_INSTRUMENT
                                                    Violin                                     %%! DEFAULT_REDRAW_INSTRUMENT
                                                }                                              %%! DEFAULT_REDRAW_INSTRUMENT
                                            \set ViolinMusicStaff.shortInstrumentName = \markup { %%! DEFAULT_REDRAW_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_REDRAW_INSTRUMENT
                                                    #10                                        %%! DEFAULT_REDRAW_INSTRUMENT
                                                    Vn.                                        %%! DEFAULT_REDRAW_INSTRUMENT
                                                }                                              %%! DEFAULT_REDRAW_INSTRUMENT
                                            \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! DEFAULT_REDRAW_INSTRUMENT_COLOR
                                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %%! DEFAULT_CLEF_COLOR_REDRAW
                <BLANKLINE>
                                            b'8
                <BLANKLINE>
                                            c''8
                <BLANKLINE>
                                            d''8
                <BLANKLINE>
                                            e''8
                                            \revert Stem.direction
                                        }
                                    }
                                    {
                                        {
                <BLANKLINE>
                                            % ViolinMusicVoice [measure 2]
                                            ef''8
                                            \bar "|"
                <BLANKLINE>
                                        }
                                    }
                                }
                            }
                            \tag viola
                            \context ViolaMusicStaff = "ViolaMusicStaff" {
                                \context ViolaMusicVoice = "ViolaMusicVoice" {
                                    {
                                        {
                <BLANKLINE>
                                            % ViolaMusicVoice [measure 1]
                                            \override Stem.direction = #up
                                            \set ViolaMusicStaff.instrumentName = \markup {    %%! DEFAULT_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_INSTRUMENT
                                                    #10                                        %%! DEFAULT_INSTRUMENT
                                                    Viola                                      %%! DEFAULT_INSTRUMENT
                                                }                                              %%! DEFAULT_INSTRUMENT
                                            \set ViolaMusicStaff.shortInstrumentName = \markup { %%! DEFAULT_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_INSTRUMENT
                                                    #10                                        %%! DEFAULT_INSTRUMENT
                                                    Va.                                        %%! DEFAULT_INSTRUMENT
                                                }                                              %%! DEFAULT_INSTRUMENT
                                            \set ViolaMusicStaff.forceClef = ##t               %%! DEFAULT_CLEF
                                            \clef "alto"                                       %%! DEFAULT_CLEF
                                            \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! DEFAULT_INSTRUMENT_COLOR
                                            \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! DEFAULT_CLEF_COLOR
                                            %%% \override ViolaMusicStaff.Clef.color = ##f     %%! DEFAULT_CLEF_UNCOLOR
                                            c'8
                                            ^ \markup {
                                                \column
                                                    {
                                                        %%% \line                              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%     {                              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%         \vcenter                   %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             (Viola                 %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%         \vcenter                   %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             \hcenter-in            %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 #10                %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 Viola              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%         \concat                    %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             {                      %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 \vcenter           %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                     \hcenter-in    %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                         #10        %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                         Va.        %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                 \vcenter           %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%                     )              %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%             }                      %%! DEFAULT_INSTRUMENT_ALERT
                                                        %%%     }                              %%! DEFAULT_INSTRUMENT_ALERT
                                                        \line                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            {                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \with-color                    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    #(x11-color 'DarkViolet)   %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    {                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter               %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            (Viola             %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter               %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            \hcenter-in        %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                #10            %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                Viola          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \concat                %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            {                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                \vcenter       %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                    \hcenter-in %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                        #10    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                        Va.    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                \vcenter       %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                    )          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            }                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    }                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            }                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    }
                                                }
                                            \set ViolaMusicStaff.instrumentName = \markup {    %%! DEFAULT_REDRAW_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_REDRAW_INSTRUMENT
                                                    #10                                        %%! DEFAULT_REDRAW_INSTRUMENT
                                                    Viola                                      %%! DEFAULT_REDRAW_INSTRUMENT
                                                }                                              %%! DEFAULT_REDRAW_INSTRUMENT
                                            \set ViolaMusicStaff.shortInstrumentName = \markup { %%! DEFAULT_REDRAW_INSTRUMENT
                                                \hcenter-in                                    %%! DEFAULT_REDRAW_INSTRUMENT
                                                    #10                                        %%! DEFAULT_REDRAW_INSTRUMENT
                                                    Va.                                        %%! DEFAULT_REDRAW_INSTRUMENT
                                                }                                              %%! DEFAULT_REDRAW_INSTRUMENT
                                            \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! DEFAULT_REDRAW_INSTRUMENT_COLOR
                                            \override ViolaMusicStaff.Clef.color = #(x11-color 'violet) %%! DEFAULT_CLEF_COLOR_REDRAW
                <BLANKLINE>
                                            d'8
                <BLANKLINE>
                                            e'8
                <BLANKLINE>
                                            \crossStaff
                                            f'8
                <BLANKLINE>
                                            \crossStaff
                                            g'8
                                            \revert Stem.direction
                                        }
                                    }
                <BLANKLINE>
                                    % ViolaMusicVoice [measure 2]
                                    R1 * 1/8
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                            \tag cello
                            \context CelloMusicStaff = "CelloMusicStaff" {
                                \context CelloMusicVoice = "CelloMusicVoice" {
                <BLANKLINE>
                                    % CelloMusicVoice [measure 1]
                                    \set CelloMusicStaff.instrumentName = \markup {            %%! DEFAULT_INSTRUMENT
                                        \hcenter-in                                            %%! DEFAULT_INSTRUMENT
                                            #10                                                %%! DEFAULT_INSTRUMENT
                                            Cello                                              %%! DEFAULT_INSTRUMENT
                                        }                                                      %%! DEFAULT_INSTRUMENT
                                    \set CelloMusicStaff.shortInstrumentName = \markup {       %%! DEFAULT_INSTRUMENT
                                        \hcenter-in                                            %%! DEFAULT_INSTRUMENT
                                            #10                                                %%! DEFAULT_INSTRUMENT
                                            Vc.                                                %%! DEFAULT_INSTRUMENT
                                        }                                                      %%! DEFAULT_INSTRUMENT
                                    \set CelloMusicStaff.forceClef = ##t                       %%! DEFAULT_CLEF
                                    \clef "bass"                                               %%! DEFAULT_CLEF
                                    \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! DEFAULT_INSTRUMENT_COLOR
                                    \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! DEFAULT_CLEF_COLOR
                                    %%% \override CelloMusicStaff.Clef.color = ##f             %%! DEFAULT_CLEF_UNCOLOR
                                    R1 * 5/8
                                    ^ \markup {
                                        \column
                                            {
                                                %%% \line                                      %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%     {                                      %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%         \vcenter                           %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%             (Cello                         %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%         \vcenter                           %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%             \hcenter-in                    %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                 #10                        %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                 Cello                      %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%         \concat                            %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%             {                              %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                 \vcenter                   %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                     \hcenter-in            %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                         #10                %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                         Vc.                %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                 \vcenter                   %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%                     )                      %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%             }                              %%! DEFAULT_INSTRUMENT_ALERT
                                                %%%     }                                      %%! DEFAULT_INSTRUMENT_ALERT
                                                \line                                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    {                                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        \with-color                            %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            #(x11-color 'DarkViolet)           %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            {                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \vcenter                       %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    (Cello                     %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \vcenter                       %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \hcenter-in                %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        #10                    %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        Cello                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \concat                        %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    {                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter               %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            \hcenter-in        %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                #10            %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                                Vc.            %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter               %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            )                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    }                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            }                                  %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    }                                          %%! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                            }
                                        }
                                    \set CelloMusicStaff.instrumentName = \markup {            %%! DEFAULT_REDRAW_INSTRUMENT
                                        \hcenter-in                                            %%! DEFAULT_REDRAW_INSTRUMENT
                                            #10                                                %%! DEFAULT_REDRAW_INSTRUMENT
                                            Cello                                              %%! DEFAULT_REDRAW_INSTRUMENT
                                        }                                                      %%! DEFAULT_REDRAW_INSTRUMENT
                                    \set CelloMusicStaff.shortInstrumentName = \markup {       %%! DEFAULT_REDRAW_INSTRUMENT
                                        \hcenter-in                                            %%! DEFAULT_REDRAW_INSTRUMENT
                                            #10                                                %%! DEFAULT_REDRAW_INSTRUMENT
                                            Vc.                                                %%! DEFAULT_REDRAW_INSTRUMENT
                                        }                                                      %%! DEFAULT_REDRAW_INSTRUMENT
                                    \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! DEFAULT_REDRAW_INSTRUMENT_COLOR
                                    \override CelloMusicStaff.Clef.color = #(x11-color 'violet) %%! DEFAULT_CLEF_COLOR_REDRAW
                <BLANKLINE>
                                    % CelloMusicVoice [measure 2]
                                    R1 * 1/8
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                        >>
                    >>
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.LilyPondCommand(r'\crossStaff')],
            selector=selector,
            )

    @staticmethod
    def dashed_arrow():
        r'''Makes dashed arrow line segment.

        Returns arrow line segment.
        '''
        return abjad.ArrowLineSegment(
            dash_fraction=0.25,
            dash_period=1.5,
            left_broken_text=False,
            left_hspace=0.5,
            right_broken_arrow=False,
            right_broken_padding=0,
            right_padding=1.75,
            )

    @staticmethod
    def deviation(deviations, selector='baca.plts()'):
        r''''Makes microtone deviation.
        '''
        return baca.MicrotoneDeviationCommand(
            deviations=deviations,
            selector=selector,
            )

    @staticmethod
    def diatonic_clusters(widths, selector='baca.plts()'):
        r'''Makes diatonic clusters.
        '''
        return baca.DiatonicClusterCommand(
            selector=selector,
            widths=widths,
            )

    @staticmethod
    def displacement(displacements, selector='baca.plts()'):
        r'''Octave-displaces PLTs.

        ..  container:: example

            Octave-displaces PLTs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     3 * [[0, 2, 3]],
            ...     baca.displacement([0, 0, -1, -1, 1, 1]),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                [
                                d'16
                                ]
                                ef4
                                ~
                                ef16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                c16
                                [
                                d''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 11/12 {
                                c'16
                                [
                                d'16
                                ]
                                ef4
                                ~
                                ef16
                                r16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-displaces chords:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     6 * [{0, 2, 3}],
            ...     baca.displacement([0, 0, -1, -1, 1, 1]),
            ...     baca.rests_around([2], [4]),
            ...     counts=[4],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                r8
                                <c' d' ef'>4
                            }
                            {
                                <c' d' ef'>4
                            }
                            {
                                <c d ef>4
                            }
                            {
                                <c d ef>4
                            }
                            {
                                <c'' d'' ef''>4
                            }
                            {
                                <c'' d'' ef''>4
                                r4
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-displaces last six pitched logical ties:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     3 * [[0, 2, 3]],
            ...     baca.displacement([0, 0, -1, -1, 1, 1], baca.plts()[-6:]),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                [
                                d'16
                                ]
                                ef'4
                                ~
                                ef'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                c'16
                                [
                                d'16
                                ]
                                ef4
                                ~
                                ef16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 11/12 {
                                c16
                                [
                                d''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OctaveDisplacementCommand(
            displacements=displacements,
            selector=selector,
            )

    @staticmethod
    def double_tonguing(selector='baca.pheads()'):
        r'''Attaches double-staccati to pitched heads.

        ..  container:: example

            Attaches double-staccati to all pitched heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.double_tonguing(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                -\tongue #2
                                [
                                d'16
                                -\tongue #2
                                ]
                                bf'4
                                -\tongue #2
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\tongue #2
                                [
                                e''16
                                -\tongue #2
                                ]
                                ef''4
                                -\tongue #2
                                ~
                                ef''16
                                r16
                                af''16
                                -\tongue #2
                                [
                                g''16
                                -\tongue #2
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\tongue #2
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches double-staccati to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.double_tonguing(
            ...         baca.tuplets()[1:2].pheads(),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                -\tongue #2
                                [
                                e''16
                                -\tongue #2
                                ]
                                ef''4
                                -\tongue #2
                                ~
                                ef''16
                                r16
                                af''16
                                -\tongue #2
                                [
                                g''16
                                -\tongue #2
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('tongue #2')],
            selector=selector,
            )

    @staticmethod
    def down_arpeggios(selector='baca.cheads()'):
        r"""Attaches down-arpeggios to chord heads.

        ..  container:: example

            Attaches down-arpeggios to all chord heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.down_arpeggios(),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \arpeggioArrowDown
                                <c' d' bf'>8
                                \arpeggio
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            {
                                \arpeggioArrowDown
                                <ef'' e'' fs'''>8
                                \arpeggio
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            {
                                \arpeggioArrowDown
                                <g' af''>8
                                \arpeggio
                                ~
                                [
                                <g' af''>32
                                ]
                                r16.
                            }
                            {
                                a'8
                                ~
                                [
                                a'32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches down-arpeggios to last two chord heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.down_arpeggios(baca.cheads()[-2:]),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                <c' d' bf'>8
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            {
                                \arpeggioArrowDown
                                <ef'' e'' fs'''>8
                                \arpeggio
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            {
                                \arpeggioArrowDown
                                <g' af''>8
                                \arpeggio
                                ~
                                [
                                <g' af''>32
                                ]
                                r16.
                            }
                            {
                                a'8
                                ~
                                [
                                a'32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        """
        return baca.IndicatorCommand(
            indicators=[abjad.Arpeggio(direction=abjad.Down)],
            selector=selector,
            )

    @staticmethod
    def down_bows(selector='baca.pheads()'):
        r'''Attaches down-bows to pitched heads.

        ..  container:: example

            Attaches down-bows to all pitched heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.down_bows(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                -\downbow
                                [
                                d'16
                                -\downbow
                                ]
                                bf'4
                                -\downbow
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\downbow
                                [
                                e''16
                                -\downbow
                                ]
                                ef''4
                                -\downbow
                                ~
                                ef''16
                                r16
                                af''16
                                -\downbow
                                [
                                g''16
                                -\downbow
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\downbow
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches down-bows to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.down_bows(
            ...         baca.tuplets()[1:2].pheads(),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                -\downbow
                                [
                                e''16
                                -\downbow
                                ]
                                ef''4
                                -\downbow
                                ~
                                ef''16
                                r16
                                af''16
                                -\downbow
                                [
                                g''16
                                -\downbow
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('downbow')],
            selector=selector,
            )

    @staticmethod
    def dynamic(dynamic=None, selector='baca.phead(0)'):
        r'''Attaches dynamic to pitched head 0.

        ..  container:: example

            Attaches dynamic to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('f'),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                \f
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches dynamic to pitched head 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('f', baca.tuplets()[1:2].phead(0)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                \f
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            context='Voice',
            indicators=[abjad.Dynamic(dynamic)],
            selector=selector,
            )

    @staticmethod
    def dynamic_line_spanner_staff_padding(n, selector='baca.leaves()'):
        r'''Overrides dynamic line spanner staff padding on leaves.

        ..  container:: example

            Overrides dynamic line spanner staff padding on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic_line_spanner_staff_padding(4),
            ...     baca.map(baca.hairpin('p < f'), baca.tuplets()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override DynamicLineSpanner.staff-padding = #'4
                                \override TupletBracket.staff-padding = #5
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
                                \revert DynamicLineSpanner.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides dynamic line spanner staff padding on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic_line_spanner_staff_padding(4, baca.tuplet(1)),
            ...     baca.map(baca.hairpin('p < f'), baca.tuplets()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                \override DynamicLineSpanner.staff-padding = #'4
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
                                \revert DynamicLineSpanner.staff-padding
                            }
                            \times 4/5 {
                                a'16
                                \p
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute='staff_padding',
            value=str(n),
            grob='dynamic_line_spanner',
            selector=selector,
            )

    @staticmethod
    def dynamic_line_spanner_up(selector='baca.leaves()'):
        r'''Up-overrides dynamic line spanner direction.

        ..  container:: example

            Up-overrides dynamic line spanner direction on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic_line_spanner_up(),
            ...     baca.map(baca.hairpin('p < f'), baca.tuplets()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override DynamicLineSpanner.direction = #up
                                \override TupletBracket.staff-padding = #5
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
                                \revert DynamicLineSpanner.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides dynamic line spanner direction on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic_line_spanner_up(baca.tuplet(1)),
            ...     baca.map(baca.hairpin('p < f'), baca.tuplets()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                \override DynamicLineSpanner.direction = #up
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
                                \revert DynamicLineSpanner.direction
                            }
                            \times 4/5 {
                                a'16
                                \p
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute='direction',
            value=abjad.Up,
            grob='dynamic_line_spanner',
            selector=selector,
            )

    @staticmethod
    def dynamic_text_extra_offset(pair, selector='baca.pleaf(0)'):
        r'''Overrides dynamic text extra offset.

        ..  container:: example

            Overrides dynamic text extra offset on pitched leaf 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('p'),
            ...     baca.dynamic('f', baca.tuplets()[1:2].pleaf(0)),
            ...     baca.dynamic_text_extra_offset((-3, 0)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override DynamicText.extra-offset = #'(-3 . 0)
                                c'16
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
                                \f
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides dynamic text extra offset on leaf 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('p'),
            ...     baca.dynamic('f', baca.tuplets()[1:2].leaf(0)),
            ...     baca.dynamic_text_extra_offset(
            ...         (-3, 0),
            ...         baca.tuplets()[1:2].leaf(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP


            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
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
                                \once \override DynamicText.extra-offset = #'(-3 . 0)
                                fs''16
                                \f
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute='extra_offset',
            value=pair,
            grob='dynamic_text',
            selector=selector,
            )

    @staticmethod
    def dynamics(string):
        r'''Makes dynamics from `string`.

        ..  container::

            >>> baca.dynamics('ff p f pp')
            [Dynamic('ff'), Dynamic('p'), Dynamic('f'), Dynamic('pp')]

        Returns list of dynamics.
        '''
        return [abjad.Dynamic(_) for _ in string.split()]

    @staticmethod
    def dynamics_down(selector='baca.leaf(0)'):
        r'''Attaches dynamic-down command to leaf 0.

        ..  container:: example

            Attaches dynamic-down command to leaf 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('p'),
            ...     baca.dynamic('f', baca.tuplets()[1:2].phead(0)),
            ...     baca.dynamics_down(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                \dynamicDown
                                r8
                                c'16
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
                                \f
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches dynamic-down command to leaf 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('p'),
            ...     baca.dynamic('f', baca.tuplets()[1:2].phead(0)),
            ...     baca.dynamics_down(baca.tuplets()[1:2].leaf(0)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
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
                                \dynamicDown
                                fs''16
                                \f
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.LilyPondCommand('dynamicDown')],
            selector=selector,
            )

    @staticmethod
    def dynamics_up(selector='baca.leaf(0)'):
        r'''Attaches dynamic-up command to leaf 0.

        ..  container:: example

            Attaches dynamic-up command to leaf 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('p'),
            ...     baca.dynamic('f', baca.tuplets()[1:2].phead(0)),
            ...     baca.dynamics_up(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                \dynamicUp
                                r8
                                c'16
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
                                \f
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches dynamic-up command to leaf 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('p'),
            ...     baca.dynamic('f', baca.tuplets()[1:2].phead(0)),
            ...     baca.dynamics_up(baca.tuplets()[1:2].leaf(0)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
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
                                \dynamicUp
                                fs''16
                                \f
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.LilyPondCommand('dynamicUp')],
            selector=selector,
            )

    @staticmethod
    def effort_dynamic(
        dynamic=None,
        selector='baca.phead(0)',
        direction=abjad.Down,
        ):
        r'''Attaches effort dynamic to pitched head 0.

        ..  container:: example

            Attaches effort dynamic to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.effort_dynamic('f'),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                [
                                _ \markup {
                                    \larger
                                        \italic
                                            “
                                    \dynamic
                                        \override
                                            #'(font-name . #f)
                                            f
                                    \larger
                                        \italic
                                            ”
                                    }
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches effort dynamic to pitched head 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.effort_dynamic(
            ...         'f',
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                _ \markup {
                                    \larger
                                        \italic
                                            “
                                    \dynamic
                                        \override
                                            #'(font-name . #f)
                                            f
                                    \larger
                                        \italic
                                            ”
                                    }
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        # overriding font-name to false makes sure that
        # the LilyPond \dynamic command works correctly
        # in the case that TextScript.font-name is overridden score-globally
        left_quotes = abjad.Markup('“').italic().larger()
        dynamic_markup = abjad.Markup(dynamic)
        dynamic_markup = dynamic_markup.override(('font-name', False))
        dynamic_markup = dynamic_markup.dynamic()
        right_quotes = abjad.Markup('”').italic().larger()
        markup = left_quotes + dynamic_markup + right_quotes
        markup = abjad.new(markup, direction=direction)
        return baca.IndicatorCommand(
            indicators=[markup],
            selector=selector,
            )

    @staticmethod
    def fermata(selector='baca.leaf(0)'):
        r'''Attaches fermata to leaf.

        ..  container:: example

            Attaches fermata to first leaf:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.fermata(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                -\fermata
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches fermata to first leaf in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.fermata(baca.tuplets()[1:2].phead(0)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                -\fermata
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('fermata')],
            selector=selector,
            )

    @staticmethod
    def flageolets(selector='baca.pheads()'):
        r'''Attaches flageolets to pitched heads.

        ..  container:: example

            Attaches flageolets to all pitched heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.flageolets(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                -\flageolet
                                [
                                d'16
                                -\flageolet
                                ]
                                bf'4
                                -\flageolet
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\flageolet
                                [
                                e''16
                                -\flageolet
                                ]
                                ef''4
                                -\flageolet
                                ~
                                ef''16
                                r16
                                af''16
                                -\flageolet
                                [
                                g''16
                                -\flageolet
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\flageolet
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches flageolets to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.flageolets(baca.tuplets()[1:2].pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                -\flageolet
                                [
                                e''16
                                -\flageolet
                                ]
                                ef''4
                                -\flageolet
                                ~
                                ef''16
                                r16
                                af''16
                                -\flageolet
                                [
                                g''16
                                -\flageolet
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('flageolet')],
            selector=selector,
            )

    @staticmethod
    def flags():
        r'''Flags music.

        ..  container:: example

            Flags music:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=79)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                d'16
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                e''16
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                g''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return rhythmos.BeamSpecifier(
            beam_divisions_together=False,
            beam_each_division=False,
            )

    @staticmethod
    def fuse_compound_quarter_divisions(counts):
        r'''Fuses compound quarter divisions.

        ..  container:: example

            >>> expression = baca.fuse_compound_quarter_divisions([1])

            >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
            ...     item
            ...
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))

            >>> for item in expression([(3, 8), (3, 8), (3, 8)]):
            ...     item
            ...
            Division((1, 4))
            Division((1, 8))
            Division((1, 4))
            Division((1, 8))
            Division((1, 4))
            Division((1, 8))

        ..  container:: example

            >>> expression = baca.fuse_compound_quarter_divisions([2])

            >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
            ...     item
            ...
            Division((2, 4))
            Division((1, 4))

            >>> for item in expression([(3, 8), (3, 8), (3, 8)]):
            ...     item
            ...
            Division((3, 8))
            Division((3, 8))
            Division((3, 8))

        Returns division sequence expression.
        '''
        if not all(isinstance(_, int) for _ in counts):
            raise Exception(counts)
        expression = baca.DivisionSequenceExpression()
        expression = expression.division_sequence()
        expression = expression.split_by_durations(
            compound_meter_multiplier=abjad.Multiplier((3, 2)),
            durations=[abjad.Duration(1, 4)],
            )
        expression = expression.flatten(depth=-1)
        expression = expression.partition_by_counts(
            counts=counts,
            cyclic=True,
            overhang=True,
            )
        expression = expression.map(baca.sequence().sum())
        expression = expression.flatten(depth=-1)
        return expression
