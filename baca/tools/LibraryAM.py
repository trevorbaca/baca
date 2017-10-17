import abjad
import baca


class LibraryAM(object):
    r'''Library A - M.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Libraries'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def accents(selector=None):
        r'''Attaches accents to PLT heads.

        ..  container:: example

            ::

                >>> abjad.f(baca.accents())
                baca.AttachCommand(
                    arguments=[
                        abjad.Articulation('>'),
                        ],
                    target=baca.select().plt_heads(),
                    )

        ..  container:: example

            Attaches accents to all pitched heads:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 -\accent [
                                d'16 -\accent ]
                                bf'4 -\accent ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\accent [
                                e''16 -\accent ]
                                ef''4 -\accent ~
                                ef''16
                                r16
                                af''16 -\accent [
                                g''16 -\accent ]
                            }
                            \times 4/5 {
                                a'16 -\accent
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches accents to pitched heads in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.accents(baca.select().plt_heads_in_tuplet(n=1)),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\accent [
                                e''16 -\accent ]
                                ef''4 -\accent ~
                                ef''16
                                r16
                                af''16 -\accent [
                                g''16 -\accent ]
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
        return baca.AttachCommand(
            arguments=[abjad.Articulation('>')],
            selector=selector,
            )

    @staticmethod
    def alternate_bow_strokes(downbow_first=True, selector=None):
        r'''Attaches alternate bow strokes.

        ..  container:: example

            ::

                >>> abjad.f(baca.alternate_bow_strokes())
                baca.AttachCommand(
                    arguments=[
                        abjad.Articulation('downbow'),
                        abjad.Articulation('upbow'),
                        ],
                    target=baca.select().plt_heads(),
                    )

        ..  container:: example

            Attaches alternate bow strokes to all pitched heads (down-bow
            first):

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 -\downbow [
                                d'16 -\upbow ]
                                bf'4 -\downbow ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\upbow [
                                e''16 -\downbow ]
                                ef''4 -\upbow ~
                                ef''16
                                r16
                                af''16 -\downbow [
                                g''16 -\upbow ]
                            }
                            \times 4/5 {
                                a'16 -\downbow
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches alternate bow strokes to all pitched heads (up-bow first):

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #6
                                r8
                                c'16 -\upbow [
                                d'16 -\downbow ]
                                bf'4 -\upbow ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\downbow [
                                e''16 -\upbow ]
                                ef''4 -\downbow ~
                                ef''16
                                r16
                                af''16 -\upbow [
                                g''16 -\downbow ]
                            }
                            \times 4/5 {
                                a'16 -\upbow
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches alternate bow strokes to pitched heads in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.alternate_bow_strokes(
                ...         selector=baca.select().plt_heads_in_tuplet(1),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(6),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #6
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\downbow [
                                e''16 -\upbow ]
                                ef''4 -\downbow ~
                                ef''16
                                r16
                                af''16 -\upbow [
                                g''16 -\downbow ]
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
        return baca.AttachCommand(
            arguments=articulations,
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
    def ancora_dynamic(dynamic, selector=None, direction=abjad.Down):
        r'''Attaches ancora dynamic pitched head 0.

        ..  container::

            ::

                >>> abjad.f(baca.ancora_dynamic('f'))
                baca.AttachCommand(
                    arguments=[
                        abjad.Markup(
                            contents=[
                                abjad.MarkupCommand(
                                    'dynamic',
                                    'f'
                                    ),
                                abjad.MarkupCommand(
                                    'upright',
                                    'ancora'
                                    ),
                                ],
                            direction=Down,
                            ),
                        ],
                    target=baca.select().plt_head(),
                    )

        ..  container:: example

            Attaches ancora dynamic to pitched head 0:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                    _ \markup {
                                        \dynamic
                                            ff
                                        \upright
                                            ancora
                                        }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.ancora_dynamic(
                ...         'ff',
                ...         baca.select().plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                    _ \markup {
                                        \dynamic
                                            ff
                                        \upright
                                            ancora
                                        }
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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
        return baca.AttachCommand(
            arguments=[markup],
            selector=selector,
            target=baca.select().plt_head(0),
            )

    @staticmethod
    def arpeggios(selector=None):
        r"""Attaches arpeggios.

        ..  container:: example

            Attaches arpeggios to all chord heads:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.arpeggios(),
                ...     counts=[5, -3],
                ...     talea_denominator=32,
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                <c' d' bf'>8 -\arpeggio ~ [
                                <c' d' bf'>32 ]
                                r16.
                            }
                            {
                                f''8 ~ [
                                f''32 ]
                                r16.
                            }
                            {
                                <ef'' e'' fs'''>8 -\arpeggio ~ [
                                <ef'' e'' fs'''>32 ]
                                r16.
                            }
                            {
                                <g' af''>8 -\arpeggio ~ [
                                <g' af''>32 ]
                                r16.
                            }
                            {
                                a'8 ~ [
                                a'32 ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches arpeggios to last two chord heads:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.arpeggios(baca.select().chord_heads()[-2:]),
                ...     counts=[5, -3],
                ...     talea_denominator=32,
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                <c' d' bf'>8 ~ [
                                <c' d' bf'>32 ]
                                r16.
                            }
                            {
                                f''8 ~ [
                                f''32 ]
                                r16.
                            }
                            {
                                <ef'' e'' fs'''>8 -\arpeggio ~ [
                                <ef'' e'' fs'''>32 ]
                                r16.
                            }
                            {
                                <g' af''>8 -\arpeggio ~ [
                                <g' af''>32 ]
                                r16.
                            }
                            {
                                a'8 ~ [
                                a'32 ]
                                r16.
                            }
                        }
                    }
                >>

        """
        return baca.AttachCommand(
            arguments=[abjad.Articulation('arpeggio')],
            selector=selector,
            target=baca.select().chord_heads(),
            )

    @staticmethod
    def bass_to_octave(n=4, selector=None):
        r"""Octave-transposes music.

        ..  container:: example

            Octave-transposes music such that the lowest note in the entire
            selection appears in octave 3:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.bass_to_octave(3, baca.select().plts().wrap()),
                ...     baca.color(baca.select().plts().wrap()),
                ...     counts=[5, -3],
                ...     talea_denominator=32,
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
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
                                <c d bf>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c d bf>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                f'8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                f'32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef' e' fs''>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef' e' fs''>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g af'>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g af'>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a32 ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music such that the lowest pitch in each pitched
            logical tie appears in octave 3:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.bass_to_octave(
                ...         n=3,
                ...         selector=baca.select().leaves_in_each_plt(),
                ...         ),
                ...     baca.color(baca.select().leaves_in_each_plt()),
                ...     counts=[5, -3],
                ...     talea_denominator=32,
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
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
                                <c d bf>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c d bf>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f8 ~ [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <g af'>8 ~ [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <g af'>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a32 ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music such that the lowest pitch in each of the
            last two pitched logical ties appears in octave 3:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.bass_to_octave(
                ...         n=3,
                ...         selector=baca.select().leaves_in_each_plt(start=-2),
                ...         ),
                ...     baca.color(baca.select().leaves_in_each_plt(start=-2)),
                ...     counts=[5, -3],
                ...     talea_denominator=32,
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                <c' d' bf'>8 ~ [
                                <c' d' bf'>32 ]
                                r16.
                            }
                            {
                                f''8 ~ [
                                f''32 ]
                                r16.
                            }
                            {
                                <ef'' e'' fs'''>8 ~ [
                                <ef'' e'' fs'''>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g af'>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g af'>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a8 ~ [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a32 ]
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.beam_divisions(),
                ...     baca.rests_around([2], [2]),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                r8
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            {
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                g''16 ]
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.beam_divisions(stemlets=2),
                ...     baca.rests_around([2], [2]),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \override Staff.Stem.stemlet-length = #2
                                r8 [
                                c'16
                                d'16
                                \revert Staff.Stem.stemlet-length
                                bf'16 ]
                            }
                            {
                                \override Staff.Stem.stemlet-length = #2
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                \revert Staff.Stem.stemlet-length
                                g''16 ]
                            }
                            {
                                \override Staff.Stem.stemlet-length = #2
                                a'16 [
                                \revert Staff.Stem.stemlet-length
                                r8 ]
                            }
                        }
                    }
                >>

        '''
        return abjad.rhythmmakertools.BeamSpecifier(
            beam_each_division=True,
            beam_rests=bool(stemlets),
            stemlet_length=stemlets,
            )

    @staticmethod
    def beam_everything(hide_nibs=None, stemlets=None):
        r'''Beams everything.

        ..  container:: example

            Beams everything:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.beam_everything(),
                ...     baca.rests_around([2], [2]),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                r8 [
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
                                r8 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Beams everything with stemlets:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.beam_everything(stemlets=2),
                ...     baca.rests_around([2], [2]),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \override Staff.Stem.stemlet-length = #2
                                r8 [
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
                                r8 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Beams everything without nibs:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.beam_everything(hide_nibs=True),
                ...     baca.rests_around([2], [2]),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                r8 [
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
                                r8 ]
                            }
                        }
                    }
                >>

        '''
        return abjad.rhythmmakertools.BeamSpecifier(
            beam_divisions_together=True,
            beam_each_division=True,
            beam_rests=True,
            hide_nibs=hide_nibs,
            stemlet_length=stemlets,
            )

    @staticmethod
    def beam_plt_runs(hide_nibs=None):
        r'''Beams PLT runs.

        ..  container:: example

            Beams PLT runs:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.beam_plt_runs(),
                ...     baca.rests_around([2], [2]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
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
                                c'16 [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                d'16 ]
                                bf'4 ~
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                bf'16 [ ]
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                fs''16 [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                e''16 ]
                                ef''4 ~
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                ef''16 [ ]
                                r16
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #2
                                af''16 [
                                \set stemLeftBeamCount = #2
                                \set stemRightBeamCount = #1
                                g''16
                            }
                            \times 2/3 {
                                \set stemLeftBeamCount = #1
                                \set stemRightBeamCount = #2
                                a'16 ]
                                r8
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Beams PLT runs without nibs:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.beam_plt_runs(hide_nibs=True),
                ...     baca.rests_around([2], [2]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16
                            }
                            \times 2/3 {
                                a'16 ]
                                r8
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return abjad.rhythmmakertools.BeamSpecifier(
            beam_divisions_together=True,
            beam_each_division=True,
            beam_rests=False,
            hide_nibs=hide_nibs,
            )

    @staticmethod
    def beam_positions(n=None, selector=None):
        r'''Overrides beam positions.

        ..  container:: example

            Overrides beam positions on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.beam_positions(6),
                ...     baca.rests_around([2], [4]),
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \times 4/5 {
                                \override Beam.positions = #'(6 . 6)
                                r8
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            \times 4/5 {
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                g''16 ]
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.beam_positions(
                ...         n=6,
                ...         selector=baca.select().leaves_in_tuplet(1),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \times 4/5 {
                                r8
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            \times 4/5 {
                                \override Beam.positions = #'(6 . 6)
                                fs''16 [
                                e''16
                                ef''16
                                af''16
                                g''16 ]
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
            attribute_name='positions',
            attribute_value=(n, n),
            grob_name='beam',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def center_to_octave(n=4, selector=None):
        r"""Octave-transposes music.

        ..  container:: example

            Octave-transposes music such that the centroid of the entire
            selection appears in octave 3:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.center_to_octave(3, baca.select().plts().wrap()),
                ...     baca.color(baca.select().plts().wrap()),
                ...     counts=[5, -3],
                ...     talea_denominator=32,
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
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
                                <c, d, bf,>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c, d, bf,>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                f8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                f32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g, af>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g, af>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a,8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a,32 ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music such that the centroid of each pitched
            logical tie appears in octave 3:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.center_to_octave(3, baca.select().plts()),
                ...     baca.color(baca.select().plts()),
                ...     counts=[5, -3],
                ...     talea_denominator=32,
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
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
                                <c d bf>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c d bf>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f8 ~ [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <g, af>8 ~ [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <g, af>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a32 ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music such that the centroid of each of the last
            two pitched logical ties appears in octave 3:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.center_to_octave(
                ...         n=3,
                ...         selector=baca.select().leaves_in_each_plt(start=-2),
                ...         ),
                ...     baca.color(baca.select().leaves_in_each_plt(start=-2)),
                ...     counts=[5, -3],
                ...     talea_denominator=32,
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                <c' d' bf'>8 ~ [
                                <c' d' bf'>32 ]
                                r16.
                            }
                            {
                                f''8 ~ [
                                f''32 ]
                                r16.
                            }
                            {
                                <ef'' e'' fs'''>8 ~ [
                                <ef'' e'' fs'''>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g, af>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g, af>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a8 ~ [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a32 ]
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
    def clef(clef='treble', selector=None):
        r'''Attaches clef to leaf 0.

        ..  container:: example

            Attaches clef to leaf 0:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \clef "alto"
                                \override TupletBracket.staff-padding = #7
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.clef(
                ...         clef='alto',
                ...         selector=baca.select().leaf_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(7),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #7
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \clef "alto"
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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
        return baca.AttachCommand(
            arguments=[abjad.Clef(clef)],
            selector=selector,
            target=baca.select().leaf(),
            )

    @staticmethod
    def clef_spanner(clef='percussion', selector=None):
        r'''Attaches clef spanner to leaves.

        ..  container:: example

            Attaches clef spanner and one-line spanner to all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.clef_spanner(),
                ...     baca.one_line_staff(),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(9),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \stopStaff
                                \once \override Staff.StaffSymbol.line-count = 1
                                \startStaff
                                \clef "percussion"
                                \override TupletBracket.staff-padding = #9
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                                \stopStaff
                                \startStaff
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches clef spanner and one-line spanner to leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.clef_spanner(
                ...         clef='percussion',
                ...         selector=baca.select().leaves_in_tuplet(1),
                ...         ),
                ...     baca.one_line_staff(
                ...         selector=baca.select().leaves_in_tuplet(1),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(9),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #9
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \stopStaff
                                \once \override Staff.StaffSymbol.line-count = 1
                                \startStaff
                                \clef "percussion"
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \stopStaff
                                \startStaff
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
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.ClefSpanner(clef=clef),
            )

    @staticmethod
    def clusters(widths, start_pitch=None, selector='baca.select().plts()'):
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

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \times 4/5 {
                                r8
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            \times 2/3 {
                                c'16 [
                                d'16
                                bf'16 ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/7 {
                                c'16 [
                                d'16
                                bf'16 ]
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
                                c'16 [
                                d'16 ]
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
    def color(selector=None):
        r'''Colors leaves.

        ..  container:: example

            Colors all leaves:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                \override TupletBracket.staff-padding = #5
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
                                bf'4 ~
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
                                ef''4 ~
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.color(selector=baca.select().leaves_in_tuplet(1)),
                ...     baca.flags(),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
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
                                bf'4 ~
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
                                ef''4 ~
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
    def color_fingerings(numbers, selector='baca.select().plt_heads()'):
        r'''Color fingerings.

        Returns color fingering command.
        '''
        return baca.ColorFingeringCommand(
            numbers=numbers,
            selector=selector,
            )

    @staticmethod
    def compound(scopes):
        r'''Makes compound scope.

        Returns compound scope.
        '''
        return baca.CompoundScope(scopes=scopes)

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
        expression = expression.flatten()
        return expression

    @staticmethod
    def constellate(cells, range, flatten=True):
        '''Constellates `cells`.

        ..  container:: example

            ::

                >>> pitches = [[0, 2, 10], [16, 19, 20]]
                >>> range_ = abjad.PitchRange('[C4, C#7]')
                >>> segments = baca.constellate(pitches, range_)
                >>> for segment in segments:
                ...     segment
                Sequence([0, 2, 4, 7, 8, 10])
                Sequence([0, 2, 10, 16, 19, 20])
                Sequence([0, 2, 10, 28, 31, 32])
                Sequence([4, 7, 8, 12, 14, 22])
                Sequence([12, 14, 16, 19, 20, 22])
                Sequence([12, 14, 22, 28, 31, 32])
                Sequence([4, 7, 8, 24, 26, 34])
                Sequence([16, 19, 20, 24, 26, 34])
                Sequence([24, 26, 28, 31, 32, 34])

        ..  container:: example

            ::

                >>> pitches = [[4, 8, 11], [7, 15, 17]]
                >>> range_ = abjad.PitchRange('[C4, C#7]')
                >>> segments = baca.constellate(pitches, range_)
                >>> for segment in segments:
                ...     segment
                Sequence([4, 7, 8, 11, 15, 17])
                Sequence([4, 8, 11, 19, 27, 29])
                Sequence([7, 15, 16, 17, 20, 23])
                Sequence([16, 19, 20, 23, 27, 29])
                Sequence([7, 15, 17, 28, 32, 35])
                Sequence([19, 27, 28, 29, 32, 35])

        Returns outer product of octave transpositions of `cells` in `range`.
        '''
        if not isinstance(range, abjad.PitchRange):
            raise TypeError(f'pitch range only: {range!r}.')
        transposition_list = []
        for cell in cells:
            transpositions = range.list_octave_transpositions(cell)
            transposition_list.append(transpositions)
        enumerator = abjad.Enumerator(transposition_list)
        result = enumerator.yield_outer_product()
        result = list(result)
        if flatten:
            for i, part in enumerate(result):
                result[i] = baca.Sequence(part).flatten()
        for i, cell in enumerate(result[:]):
            result[i] = cell.sort()
        return result

    @staticmethod
    def cross_note_heads(selector=None):
        r'''Overrides note-head style on pitched leaves.

        ..  container:: example

            Overrides note-head style on all pitched leaves:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override NoteHead.style = #'cross
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.cross_note_heads(
                ...         baca.select().pls_in_tuplet(1),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override NoteHead.style = #'cross
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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
            attribute_name='style',
            attribute_value='cross',
            grob_name='note_head',
            revert=True,
            selector=selector,
            target=baca.select().pls().wrap(),
            )

    @staticmethod
    def cross_staff(selector=None):
        r'''Attaches cross-staff command to leaves.

        ..  container:: example

            Attaches cross-staff command to all leaves:

            ::

                >>> score_template = baca.StringTrioScoreTemplate()
                >>> accumulator = baca.MusicAccumulator(score_template)
                >>> accumulator(
                ...     accumulator.music_maker(
                ...         'Violin Music Voice',
                ...         [[9, 11, 12, 14, 16]],
                ...         baca.flags(),
                ...         baca.stems_up(),
                ...         denominator=8,
                ...         figure_name='vn 1',
                ...         talea_denominator=8,
                ...         ),
                ...     )
                >>> accumulator(
                ...     accumulator.music_maker(
                ...         'Viola Music Voice',
                ...         [[0, 2, 4, 5, 7]],
                ...         baca.anchor('Violin Music Voice'),
                ...         baca.cross_staff(),
                ...         baca.flags(),
                ...         baca.stems_up(),
                ...         figure_name='vn 2',
                ...         talea_denominator=8,
                ...         ),
                ...     )

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     allow_figure_names=False,
                ...     ignore_repeat_pitch_classes=True,
                ...     ignore_unregistered_pitches=True,
                ...     score_template=accumulator.score_template,
                ...     time_signatures=accumulator.time_signatures,
                ...     )
                >>> accumulator.populate_segment_maker(segment_maker)
                >>> result = segment_maker.run(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin.viola.cello
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
                            {
                                \time 5/8
                                R1 * 5/8
                            }
                        }
                        \context GlobalSkips = "Global Skips" {
                            {
                                s1 * 5/8
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \context StringSectionStaffGroup = "String Section Staff Group" <<
                            \tag violin
                            \context ViolinMusicStaff = "Violin Music Staff" {
                                \context ViolinMusicVoice = "Violin Music Voice" {
                                    {
                                        {
                                            \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                            \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                            \clef "treble"
                                            \override Stem.direction = #up
                                            a'8
                                            b'8
                                            c''8
                                            d''8
                                            e''8
                                            \bar "|"
                                            \revert Stem.direction
                                        }
                                    }
                                }
                            }
                            \tag viola
                            \context ViolaMusicStaff = "Viola Music Staff" {
                                \context ViolaMusicVoice = "Viola Music Voice" {
                                    {
                                        {
                                            \set ViolaMusicStaff.instrumentName = \markup { Viola }
                                            \set ViolaMusicStaff.shortInstrumentName = \markup { Va. }
                                            \clef "alto"
                                            \crossStaff
                                            \override Stem.direction = #up
                                            c'8
                                            \crossStaff
                                            d'8
                                            \crossStaff
                                            e'8
                                            \crossStaff
                                            f'8
                                            \crossStaff
                                            g'8
                                            \bar "|"
                                            \revert Stem.direction
                                        }
                                    }
                                }
                            }
                            \tag cello
                            \context CelloMusicStaff = "Cello Music Staff" {
                                \context CelloMusicVoice = "Cello Music Voice" {
                                    \set CelloMusicStaff.instrumentName = \markup { Cello }
                                    \set CelloMusicStaff.shortInstrumentName = \markup { Vc. }
                                    \clef "bass"
                                    R1 * 5/8
                                    \bar "|"
                                }
                            }
                        >>
                    >>
                >>

        ..  container:: example

            Attaches cross-staff command to last two pitched leaves:

            ::

                >>> score_template = baca.StringTrioScoreTemplate()
                >>> accumulator = baca.MusicAccumulator(score_template)
                >>> accumulator(
                ...     accumulator.music_maker(
                ...         'Violin Music Voice',
                ...         [[9, 11, 12, 14, 16]],
                ...         baca.flags(),
                ...         baca.stems_up(),
                ...         denominator=8,
                ...         figure_name='vn 1',
                ...         talea_denominator=8,
                ...         ),
                ...     )
                >>> accumulator(
                ...     accumulator.music_maker(
                ...         'Viola Music Voice',
                ...         [[0, 2, 4, 5, 7]],
                ...         baca.anchor('Violin Music Voice'),
                ...         baca.cross_staff(selector=baca.select().pls()[-2:]),
                ...         baca.flags(),
                ...         baca.stems_up(),
                ...         figure_name='vn 2',
                ...         talea_denominator=8,
                ...         ),
                ...     )

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     allow_figure_names=False,
                ...     ignore_repeat_pitch_classes=True,
                ...     ignore_unregistered_pitches=True,
                ...     score_template=accumulator.score_template,
                ...     time_signatures=accumulator.time_signatures,
                ...     )
                >>> accumulator.populate_segment_maker(segment_maker)
                >>> result = segment_maker.run(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin.viola.cello
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
                            {
                                \time 5/8
                                R1 * 5/8
                            }
                        }
                        \context GlobalSkips = "Global Skips" {
                            {
                                s1 * 5/8
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \context StringSectionStaffGroup = "String Section Staff Group" <<
                            \tag violin
                            \context ViolinMusicStaff = "Violin Music Staff" {
                                \context ViolinMusicVoice = "Violin Music Voice" {
                                    {
                                        {
                                            \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                            \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                            \clef "treble"
                                            \override Stem.direction = #up
                                            a'8
                                            b'8
                                            c''8
                                            d''8
                                            e''8
                                            \bar "|"
                                            \revert Stem.direction
                                        }
                                    }
                                }
                            }
                            \tag viola
                            \context ViolaMusicStaff = "Viola Music Staff" {
                                \context ViolaMusicVoice = "Viola Music Voice" {
                                    {
                                        {
                                            \set ViolaMusicStaff.instrumentName = \markup { Viola }
                                            \set ViolaMusicStaff.shortInstrumentName = \markup { Va. }
                                            \clef "alto"
                                            \override Stem.direction = #up
                                            c'8
                                            d'8
                                            e'8
                                            \crossStaff
                                            f'8
                                            \crossStaff
                                            g'8
                                            \bar "|"
                                            \revert Stem.direction
                                        }
                                    }
                                }
                            }
                            \tag cello
                            \context CelloMusicStaff = "Cello Music Staff" {
                                \context CelloMusicVoice = "Cello Music Voice" {
                                    \set CelloMusicStaff.instrumentName = \markup { Cello }
                                    \set CelloMusicStaff.shortInstrumentName = \markup { Vc. }
                                    \clef "bass"
                                    R1 * 5/8
                                    \bar "|"
                                }
                            }
                        >>
                    >>
                >>

        '''
        return baca.AttachCommand(
            arguments=[abjad.LilyPondCommand(r'\crossStaff')],
            selector=selector,
            target=baca.select().plt_heads(),
            )

    @staticmethod
    def diatonic_clusters(widths, selector='baca.select().plts()'):
        r'''Makes diatonic clusters.
        '''
        return baca.DiatonicClusterCommand(
            selector=selector,
            widths=widths,
            )

    @staticmethod
    def displacements(displacements, selector=None):
        r'''Octave-displaces pitched logical ties.

        ..  container:: example

            Octave-displaces all pitched logical ties:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     3 * [[0, 2, 3]],
                ...     baca.displacements([0, 0, -1, -1, 1, 1]),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                ef4 ~
                                ef16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                c16 [
                                d''16 ]
                                ef''4 ~
                                ef''16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 11/12 {
                                c'16 [
                                d'16 ]
                                ef4 ~
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     6 * [{0, 2, 3}],
                ...     baca.displacements([0, 0, -1, -1, 1, 1]),
                ...     baca.rests_around([2], [4]),
                ...     counts=[4],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     3 * [[0, 2, 3]],
                ...     baca.displacements(
                ...         [0, 0, -1, -1, 1, 1],
                ...         baca.select().plts()[-6:],
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                ef'4 ~
                                ef'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                c'16 [
                                d'16 ]
                                ef4 ~
                                ef16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 11/12 {
                                c16 [
                                d''16 ]
                                ef''4 ~
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
    def double_tonguing(selector=None):
        r'''Attaches double-staccati to pitched heads.

        ..  container:: example

            Attaches double-staccati to all pitched heads:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 -\tongue #2 [
                                d'16 -\tongue #2 ]
                                bf'4 -\tongue #2 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\tongue #2 [
                                e''16 -\tongue #2 ]
                                ef''4 -\tongue #2 ~
                                ef''16
                                r16
                                af''16 -\tongue #2 [
                                g''16 -\tongue #2 ]
                            }
                            \times 4/5 {
                                a'16 -\tongue #2
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches double-staccati to pitched heads in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.double_tonguing(
                ...         baca.select().plt_heads_in_tuplet(1),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\tongue #2 [
                                e''16 -\tongue #2 ]
                                ef''4 -\tongue #2 ~
                                ef''16
                                r16
                                af''16 -\tongue #2 [
                                g''16 -\tongue #2 ]
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
        return baca.AttachCommand(
            arguments=[abjad.Articulation('tongue #2')],
            selector=selector,
            target=baca.select().plt_heads(),
            )

    @staticmethod
    def down_arpeggios(selector=None):
        r"""Attaches down-arpeggios to chord heads.

        ..  container:: example

            Attaches down-arpeggios to all chord heads:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.down_arpeggios(),
                ...     counts=[5, -3],
                ...     talea_denominator=32,
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \arpeggioArrowDown
                                <c' d' bf'>8 \arpeggio ~ [
                                <c' d' bf'>32 ]
                                r16.
                            }
                            {
                                f''8 ~ [
                                f''32 ]
                                r16.
                            }
                            {
                                \arpeggioArrowDown
                                <ef'' e'' fs'''>8 \arpeggio ~ [
                                <ef'' e'' fs'''>32 ]
                                r16.
                            }
                            {
                                \arpeggioArrowDown
                                <g' af''>8 \arpeggio ~ [
                                <g' af''>32 ]
                                r16.
                            }
                            {
                                a'8 ~ [
                                a'32 ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches down-arpeggios to last two chord heads:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.down_arpeggios(baca.select().chord_heads()[-2:]),
                ...     counts=[5, -3],
                ...     talea_denominator=32,
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                <c' d' bf'>8 ~ [
                                <c' d' bf'>32 ]
                                r16.
                            }
                            {
                                f''8 ~ [
                                f''32 ]
                                r16.
                            }
                            {
                                \arpeggioArrowDown
                                <ef'' e'' fs'''>8 \arpeggio ~ [
                                <ef'' e'' fs'''>32 ]
                                r16.
                            }
                            {
                                \arpeggioArrowDown
                                <g' af''>8 \arpeggio ~ [
                                <g' af''>32 ]
                                r16.
                            }
                            {
                                a'8 ~ [
                                a'32 ]
                                r16.
                            }
                        }
                    }
                >>

        """
        return baca.AttachCommand(
            arguments=[abjad.Arpeggio(direction=abjad.Down)],
            selector=selector,
            target=baca.select().chord_heads(),
            )

    @staticmethod
    def down_bows(selector=None):
        r'''Attaches down-bows to pitched heads.

        ..  container:: example

            Attaches down-bows to all pitched heads:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 -\downbow [
                                d'16 -\downbow ]
                                bf'4 -\downbow ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\downbow [
                                e''16 -\downbow ]
                                ef''4 -\downbow ~
                                ef''16
                                r16
                                af''16 -\downbow [
                                g''16 -\downbow ]
                            }
                            \times 4/5 {
                                a'16 -\downbow
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches down-bows to pitched heads in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.down_bows(
                ...         baca.select().plt_heads_in_tuplet(1),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\downbow [
                                e''16 -\downbow ]
                                ef''4 -\downbow ~
                                ef''16
                                r16
                                af''16 -\downbow [
                                g''16 -\downbow ]
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
        return baca.AttachCommand(
            arguments=[abjad.Articulation('downbow')],
            selector=selector,
            target=baca.select().plt_heads(),
            )

    @staticmethod
    def dynamic(dynamic=None, selector=None, target='baca.select().plt_head()'):
        r'''Attaches dynamic to pitched head 0.

        ..  container:: example

            Attaches dynamic to pitched head 0:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \f [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.dynamic(
                ...         'f',
                ...         baca.select().plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 \f [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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
        return baca.AttachCommand(
            arguments=[abjad.Dynamic(dynamic)],
            selector=selector,
            target=target,
            )

    @staticmethod
    def dynamic_line_spanner_staff_padding(n=None, selector=None):
        r'''Overrides dynamic line spanner staff padding on leaves.

        ..  container:: example

            Overrides dynamic line spanner staff padding on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.dynamic_line_spanner_staff_padding(4),
                ...     baca.hairpins(
                ...         hairpins=['p < f'],
                ...         target=baca.select().trimmed_run_in_each_tuplet()
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override DynamicLineSpanner.staff-padding = #'4
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \< \p [
                                d'16 ]
                                bf'4 ~
                                bf'16 \f
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 \< \p [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 \f ]
                            }
                            \times 4/5 {
                                a'16 \p
                                r4
                                \revert DynamicLineSpanner.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides dynamic line spanner staff padding on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.dynamic_line_spanner_staff_padding(
                ...         n=4,
                ...         selector=baca.select().leaves_in_tuplet(1),
                ...         ),
                ...     baca.hairpins(
                ...         hairpins=['p < f'],
                ...         target=baca.select().trimmed_run_in_each_tuplet()
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \< \p [
                                d'16 ]
                                bf'4 ~
                                bf'16 \f
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override DynamicLineSpanner.staff-padding = #'4
                                fs''16 \< \p [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 \f ]
                                \revert DynamicLineSpanner.staff-padding
                            }
                            \times 4/5 {
                                a'16 \p
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='staff_padding',
            attribute_value=str(n),
            grob_name='dynamic_line_spanner',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def dynamic_line_spanner_up(selector=None):
        r'''Up-overrides dynamic line spanner direction.

        ..  container:: example

            Up-overrides dynamic line spanner direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.dynamic_line_spanner_up(),
                ...     baca.hairpins(
                ...         hairpins=['p < f'],
                ...         target=baca.select().trimmed_run_in_each_tuplet()
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override DynamicLineSpanner.direction = #up
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \< \p [
                                d'16 ]
                                bf'4 ~
                                bf'16 \f
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 \< \p [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 \f ]
                            }
                            \times 4/5 {
                                a'16 \p
                                r4
                                \revert DynamicLineSpanner.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides dynamic line spanner direction on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.dynamic_line_spanner_up(
                ...         baca.select().leaves_in_tuplet(1),
                ...         ),
                ...     baca.hairpins(
                ...         hairpins=['p < f'],
                ...         target=baca.select().trimmed_run_in_each_tuplet()
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \< \p [
                                d'16 ]
                                bf'4 ~
                                bf'16 \f
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override DynamicLineSpanner.direction = #up
                                fs''16 \< \p [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 \f ]
                                \revert DynamicLineSpanner.direction
                            }
                            \times 4/5 {
                                a'16 \p
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=abjad.Up,
            grob_name='dynamic_line_spanner',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def dynamic_text_extra_offset(pair, selector=None):
        r'''Overrides dynamic text extra offset.

        ..  container:: example

            Overrides dynamic text extra offset on PL 0:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.dynamic('p'),
                ...     baca.dynamic(
                ...         'f',
                ...         baca.select().leaf_in_tuplet(1, 0),
                ...         ),
                ...     baca.dynamic_text_extra_offset((-3, 0)),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override DynamicText.extra-offset = #'(-3 . 0)
                                c'16 \p [
                                \revert DynamicText.extra-offset
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 \f [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.dynamic('p'),
                ...     baca.dynamic(
                ...         'f',
                ...         baca.select().leaf_in_tuplet(1, 0),
                ...         ),
                ...     baca.dynamic_text_extra_offset(
                ...         (-3, 0),
                ...         baca.select().leaf_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP


            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \p [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override DynamicText.extra-offset = #'(-3 . 0)
                                fs''16 \f [
                                \revert DynamicText.extra-offset
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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
            attribute_name='extra_offset',
            attribute_value=pair,
            grob_name='dynamic_text',
            revert=True,
            selector=selector,
            target=baca.select().pl(),
            )

    @staticmethod
    def dynamics_down(selector=None):
        r'''Attaches dynamic-down command to leaf 0.

        ..  container:: example

            Attaches dynamic-down command to leaf 0:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.dynamic('p'),
                ...     baca.dynamic(
                ...         'f',
                ...         baca.select().plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.dynamics_down(),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \dynamicDown
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \p [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 \f [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.dynamic('p'),
                ...     baca.dynamic(
                ...         'f',
                ...         baca.select().plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.dynamics_down(baca.select().leaf_in_tuplet(1, 0)),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \p [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \dynamicDown
                                fs''16 \f [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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
        return baca.AttachCommand(
            arguments=[abjad.LilyPondCommand('dynamicDown')],
            selector=selector,
            target=baca.select().leaf(),
            )

    @staticmethod
    def dynamics_up(selector=None):
        r'''Attaches dynamic-up command to leaf 0.

        ..  container:: example

            Attaches dynamic-up command to leaf 0:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.dynamic('p'),
                ...     baca.dynamic(
                ...         'f',
                ...         baca.select().plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.dynamics_up(),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \dynamicUp
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \p [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 \f [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.dynamic('p'),
                ...     baca.dynamic(
                ...         'f',
                ...         baca.select().plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.dynamics_up(baca.select().leaf_in_tuplet(1, 0)),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \p [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \dynamicUp
                                fs''16 \f [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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
        return baca.AttachCommand(
            arguments=[abjad.LilyPondCommand('dynamicUp')],
            selector=selector,
            target=baca.select().leaf(),
            )

    @staticmethod
    def effort_dynamic(dynamic=None, selector=None, direction=abjad.Down):
        r'''Attaches effort dynamic to pitched head 0.

        ..  container:: example

            Attaches effort dynamic to pitched head 0:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
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
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.effort_dynamic(
                ...         'f',
                ...         baca.select().plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
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
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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
        return baca.AttachCommand(
            arguments=[markup],
            selector=selector,
            target=baca.select().plt_head(),
            )

    @staticmethod
    def even_runs():
        r'''Makes even runs.
        '''
        return baca.RhythmBuilder(
            rhythm_maker=abjad.rhythmmakertools.EvenRunRhythmMaker()
            )

    @staticmethod
    def fermata(selector=None):
        r'''Attaches fermata to leaf.

        ..  container:: example

            Attaches fermata to first leaf:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8 -\fermata
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.fermata(baca.select().plt_head_in_tuplet(1, 0)),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\fermata [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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
        return baca.AttachCommand(
            arguments=[abjad.Articulation('fermata')],
            selector=selector,
            target=baca.select().leaf(),
            )

    @staticmethod
    def five_line_staff(selector=None):
        r'''Attaches five-line staff spanner to leaves.

        ..  container:: example

            Attaches five-line staff to leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.clef_spanner(clef='percussion'),
                ...     baca.clef_spanner(
                ...         clef='treble',
                ...         selector=baca.select().leaves_in_tuplet(1),
                ...         ),
                ...     baca.five_line_staff(
                ...         selector=baca.select().leaves_in_tuplet(1),
                ...         ),
                ...     baca.one_line_staff(),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(9),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \stopStaff
                                \once \override Staff.StaffSymbol.line-count = 1
                                \startStaff
                                \clef "percussion"
                                \override TupletBracket.staff-padding = #9
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \stopStaff
                                \once \override Staff.StaffSymbol.line-count = 5
                                \startStaff
                                \clef "treble"
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \stopStaff
                                \startStaff
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                                \stopStaff
                                \startStaff
                            }
                        }
                    }
                >>

        '''
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.StaffLinesSpanner(lines=5),
            )

    @staticmethod
    def fixed_pitches(source):
        r'''Sets fixed pitches.
        '''
        return baca.ScorePitchCommand(
            acyclic=True,
            source=source,
            )

    @staticmethod
    def flageolets(selector=None):
        r'''Attaches flageolets to pitched heads.

        ..  container:: example

            Attaches flageolets to all pitched heads:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 -\flageolet [
                                d'16 -\flageolet ]
                                bf'4 -\flageolet ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\flageolet [
                                e''16 -\flageolet ]
                                ef''4 -\flageolet ~
                                ef''16
                                r16
                                af''16 -\flageolet [
                                g''16 -\flageolet ]
                            }
                            \times 4/5 {
                                a'16 -\flageolet
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches flageolets to pitched heads in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.flageolets(
                ...         baca.select().plt_heads_in_tuplet(1),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\flageolet [
                                e''16 -\flageolet ]
                                ef''4 -\flageolet ~
                                ef''16
                                r16
                                af''16 -\flageolet [
                                g''16 -\flageolet ]
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
        return baca.AttachCommand(
            arguments=[abjad.Articulation('flageolet')],
            selector=selector,
            target=baca.select().plt_heads(),
            )

    @staticmethod
    def flags():
        r'''Flags music.

        ..  container:: example

            Flags music:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
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
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                e''16
                                ef''4 ~
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
        return abjad.rhythmmakertools.BeamSpecifier(
            beam_divisions_together=False,
            beam_each_division=False,
            )

    @staticmethod
    def fuse_compound_quarter_divisions(counts):
        r'''Fuses compound quarter divisions.

        ..  container:: example

            ::

                >>> expression = baca.fuse_compound_quarter_divisions([1])

            ::

                >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
                ...     item
                ...
                Division((1, 4))
                Division((1, 4))
                Division((1, 4))

            ::

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

            ::

                >>> expression = baca.fuse_compound_quarter_divisions([2])

            ::

                >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
                ...     item
                ...
                Division((2, 4))
                Division((1, 4))

            ::

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
        expression = expression.flatten()
        expression = expression.partition_by_counts(
            counts=counts,
            cyclic=True,
            overhang=True,
            )
        expression = expression.map(baca.sequence().sum())
        expression = expression.flatten()
        return expression

    @staticmethod
    def fused_tuplet_monads(tuplet_ratio=None):
        r'''Makes fused tuplet monads.
        '''
        if tuplet_ratio is None:
            tuplet_ratios = [(1,)]
        else:
            tuplet_ratios = [tuplet_ratio]
        return baca.RhythmBuilder(
            division_expression=abjad.sequence()
                .sum()
                .sequence(),
            rhythm_maker=abjad.rhythmmakertools.TupletRhythmMaker(
                tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                    use_messiaen_style_ties=True,
                    ),
                tuplet_ratios=tuplet_ratios,
                ),
            )

    @staticmethod
    def glissandi(selector='baca.select().plt_runs()'):
        r'''Attaches glissandi to PLT runs.

        ..  container:: example

            Attaches glissandi to PLT runs:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.glissandi(),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \glissando [
                                d'16 ] \glissando
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 \glissando [
                                e''16 ] \glissando
                                ef''4 ~
                                ef''16
                                r16
                                af''16 \glissando [
                                g''16 ] \glissando
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

            Attaches glissandi to PLT runs in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> selector = abjad.select().by_class(abjad.Tuplet)[1]
                >>> selector = selector.by_leaf(pitched=True).by_contiguity()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.glissandi(selector=selector),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 \glissando [
                                e''16 ] \glissando
                                ef''4 ~
                                ef''16
                                r16
                                af''16 \glissando [
                                g''16 ]
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
        return baca.GlissandoCommand(selector=selector)

    @staticmethod
    def grid_poss_to_flaut_poss():
        r'''Makes color transition spanner.

        Returns text spanner.
        '''
        left_text = abjad.Markup('grid. possibile').italic().larger()
        left_text += abjad.Markup.hspace(1)
        right_text = abjad.Markup.hspace(1) + abjad.Markup('flaut. possibile')
        right_text = right_text.italic().larger()
        spanner = abjad.TextSpanner(
            overrides={
                'text_spanner__bound_details__left__padding': -1,
                'text_spanner__bound_details__left__stencil_align_dir_y': 0,
                'text_spanner__bound_details__left__text': left_text,
                'text_spanner__bound_details__left_broken__text': None,
                'text_spanner__bound_details__right__arrow': True,
                'text_spanner__bound_details__right__padding': 1,
                'text_spanner__bound_details__right__stencil_align_dir_y': 0,
                'text_spanner__bound_details__right__text': right_text,
                'text_spanner__bound_details__right_broken__padding': 0,
                'text_spanner__bound_details__right_broken__text': None,
                'text_spanner__dash_fraction': 0.25,
                'text_spanner__dash_period': 1.5,
            }
        )
        return spanner

    @staticmethod
    def hairpins(
        hairpins,
        selector=None,
        target='baca.select().leaves_in_trimmed_run()',
        flare=None,
        include_rests=None,
        omit_lone_note_dynamic=None,
        ):
        r'''Attaches hairpins to pitched logical ties.

        ..  container:: example

            Attaches hairpins to all pitched logical ties:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.hairpins(['p < f']),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \< \p [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                            }
                            \times 4/5 {
                                a'16 \f
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches hairpins to trimmed leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.hairpins(
                ...         hairpins=['p < f'],
                ...         target=baca.select().trimmed_run_in_tuplet(1),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 \< \p [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 \f ]
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

            Attaches hairpins to trimmed leaves in tuplets:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.hairpins(
                ...         hairpins=['p < f'],
                ...         target=baca.select().trimmed_run_in_each_tuplet(),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 \< \p [
                                d'16 ]
                                bf'4 ~
                                bf'16 \f
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 \< \p [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 \f ]
                            }
                            \times 4/5 {
                                a'16 \p
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        hairpin_tokens_ = []
        for hairpin_token in hairpins:
            if isinstance(hairpin_token, str):
                hairpin_token = hairpin_token.split()
                hairpin_token = tuple(hairpin_token)
            hairpin_tokens_.append(hairpin_token)
        hairpin_tokens = hairpin_tokens_
        return baca.HairpinCommand(
            flare=flare,
            hairpin_tokens=hairpin_tokens,
            include_rests=include_rests,
            omit_lone_note_dynamic=omit_lone_note_dynamic,
            selector=selector,
            target=target,
            )

    @staticmethod
    def helianthate(sequence, n=0, m=0):
        '''Helianthates `sequence` by outer index of rotation `n` and inner
        index of rotation `m`.

        ..  container:: example

            Helianthates list of lists:

            ::

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

            ::

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

            ::

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

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
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
                                bf'4 ~
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
                                af''16 [
                                g''16 ]
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
        return baca.ImbricateBuilder(
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
    def infinite_pitches(source, repetition_intervals):
        r'''Sets infinite pitches.
        '''
        return baca.ScorePitchCommand(
            repetition_intervals=repetition_intervals,
            source=source,
            )

    @staticmethod
    def instrument(instrument, selector=None):
        r'''Attaches instrument.
        '''
        assert isinstance(instrument, abjad.Instrument)
        return baca.AttachCommand(
            arguments=[instrument],
            selector=selector,
            target=baca.select().leaf(),
            )

    @staticmethod
    def invert(axis=None):
        r'''Inverts pitches.
        '''
        return baca.ScorePitchCommand(
            operators=[
                abjad.Inversion(axis=axis),
                ]
            )

    @staticmethod
    def invert_segments(axis=None):
        r'''Inverts pitch-class segments.
        '''
        operator = baca.pitch_class_segment().invert(axis=axis)
        expression = baca.sequence().map(operator)
        return baca.MusicPitchSpecifier(
            expressions=[expression],
            to_pitch_classes=True,
            )

    @staticmethod
    def label(expression, selector=None):
        r'''Labels selection with label `expression`.

        ..  container:: example

            Labels pitch names:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                    ^ \markup {
                                        \small
                                            C4
                                        }
                                d'16 ]
                                    ^ \markup {
                                        \small
                                            D4
                                        }
                                bf'4 ~
                                    ^ \markup {
                                        \small
                                            Bb4
                                        }
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                    ^ \markup {
                                        \small
                                            "F#5"
                                        }
                                e''16 ]
                                    ^ \markup {
                                        \small
                                            E5
                                        }
                                ef''4 ~
                                    ^ \markup {
                                        \small
                                            Eb5
                                        }
                                ef''16
                                r16
                                af''16 [
                                    ^ \markup {
                                        \small
                                            Ab5
                                        }
                                g''16 ]
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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Labels pitch names in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.label(
                ...         expression=abjad.label().with_pitches(locale='us'),
                ...         selector=baca.select().plt_heads_in_tuplet(n=1),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                    ^ \markup {
                                        \small
                                            "F#5"
                                        }
                                e''16 ]
                                    ^ \markup {
                                        \small
                                            E5
                                        }
                                ef''4 ~
                                    ^ \markup {
                                        \small
                                            Eb5
                                        }
                                ef''16
                                r16
                                af''16 [
                                    ^ \markup {
                                        \small
                                            Ab5
                                        }
                                g''16 ]
                                    ^ \markup {
                                        \small
                                            G5
                                        }
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
        return baca.LabelCommand(
            expression=expression,
            selector=selector,
            )

    @staticmethod
    def laissez_vibrer(selector=None):
        r'''Attaches laissez vibrer to PLT tails.

        ..  container:: example

            Attaches laissez vibrer to all PLT tails:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs:: 
                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 -\laissezVibrer [
                                d'16 -\laissezVibrer ]
                                bf'4 ~
                                bf'16 -\laissezVibrer
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\laissezVibrer [
                                e''16 -\laissezVibrer ]
                                ef''4 ~
                                ef''16 -\laissezVibrer
                                r16
                                af''16 -\laissezVibrer [
                                g''16 -\laissezVibrer ]
                            }
                            \times 4/5 {
                                a'16 -\laissezVibrer
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches laissez vibrer to pitched tails in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.laissez_vibrer(baca.select().tuplet(1)),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\laissezVibrer [
                                e''16 -\laissezVibrer ]
                                ef''4 ~
                                ef''16 -\laissezVibrer
                                r16
                                af''16 -\laissezVibrer [
                                g''16 -\laissezVibrer ]
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
        return baca.AttachCommand(
            arguments=[abjad.Articulation('laissezVibrer')],
            selector=selector,
            target=baca.select().plt_tails(),
            )

    @staticmethod
    def line_break(selector=None):
        r'''Attaches line break command after last leaf.

        ..  container:: example

            Attaches line break after last leaf:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \break
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches line break after last leaf in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.line_break(baca.select().leaf_in_tuplet(1, -1)),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \break
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
        command = abjad.LilyPondCommand('break', format_slot='after')
        return baca.AttachCommand(
            arguments=[command],
            selector=selector,
            target=baca.select().leaf(-1),
            )

    @staticmethod
    def long_fermata(selector=None):
        r'''Attaches long fermata to leaf.

        ..  container:: example

            Attaches long fermata to first leaf:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8 -\longfermata
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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

            Attaches long fermata to first leaf in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.long_fermata(
                ...         baca.select().plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\longfermata [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
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
        return baca.AttachCommand(
            arguments=[abjad.Articulation('longfermata')],
            selector=selector,
            target=baca.select().leaf(),
            )

    @staticmethod
    def marcati(selector=None):
        r'''Attaches marcati to pitched heads.

        ..  container:: example

            Attaches marcati to all pitched heads:

            ::

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
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 -\marcato [
                                d'16 -\marcato ]
                                bf'4 -\marcato ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\marcato [
                                e''16 -\marcato ]
                                ef''4 -\marcato ~
                                ef''16
                                r16
                                af''16 -\marcato [
                                g''16 -\marcato ]
                            }
                            \times 4/5 {
                                a'16 -\marcato
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches marcati to pitched heads in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.marcati(
                ...         selector=baca.select().plt_heads_in_tuplet(1),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\marcato [
                                e''16 -\marcato ]
                                ef''4 -\marcato ~
                                ef''16
                                r16
                                af''16 -\marcato [
                                g''16 -\marcato ]
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
        return baca.AttachCommand(
            arguments=[abjad.Articulation('marcato')],
            selector=selector,
            target=baca.select().plt_heads(),
            )

    @staticmethod
    def messiaen_notes():
        r'''Makes notes.
        '''
        return baca.RhythmBuilder(
            rewrite_meter=True,
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker(
                tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                    use_messiaen_style_ties=True,
                    ),
                ),
            )

    @staticmethod
    def messiaen_tie_each(selector=None):
        r'''Attaches Messaien ties to each PLT p-run.

        ..  container:: example

            Attaches Messiaen ties to each PLT p-run:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
                ...     baca.messiaen_tie_each(),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                c'16 \repeatTie ]
                                bf'4
                                bf'16 \repeatTie
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16 [
                                e''16 ]
                                e''4 \repeatTie
                                e''16 \repeatTie
                                r16
                                fs''16 [
                                af''16 ]
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

            Attaches Messiaen tie to PLT p-run 0:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
                ...     baca.messiaen_tie_each(baca.select().plt_prun()),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                c'16 \repeatTie ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16 [
                                e''16 ]
                                e''4 ~
                                e''16
                                r16
                                fs''16 [
                                af''16 ]
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
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.Tie(use_messiaen_style_ties=True),
            target=baca.select().plt_pruns(),
            )

    @staticmethod
    def messiaen_tied_notes():
        r'''Makes tied notes.
        '''
        return baca.RhythmBuilder(
            rewrite_meter=True,
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker(
                tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                    tie_across_divisions=True,
                    use_messiaen_style_ties=True,
                    ),
                ),
            )

    @staticmethod
    def molto_flaut_to_molto_grid(selector=None):
        r'''Makes color transition spanner.
        '''
        left_text = abjad.Markup('molto flautando').italic().larger() + abjad.Markup.hspace(1)
        right_text = abjad.Markup.hspace(1) + abjad.Markup('molto gridato').italic().larger()
        spanner = abjad.TextSpanner(
            overrides={
                'text_spanner__bound_details__left__padding': -1,
                'text_spanner__bound_details__left__stencil_align_dir_y': 0,
                'text_spanner__bound_details__left__text': left_text,
                'text_spanner__bound_details__left_broken__text': None,
                'text_spanner__bound_details__right__arrow': True,
                'text_spanner__bound_details__right__padding': 1,
                'text_spanner__bound_details__right__stencil_align_dir_y': 0,
                'text_spanner__bound_details__right__text': right_text,
                'text_spanner__bound_details__right_broken__padding': 0,
                'text_spanner__bound_details__right_broken__text': None,
                'text_spanner__dash_fraction': 0.25,
                'text_spanner__dash_period': 1.5,
            }
        )
        return baca.SpannerCommand(
            selector=selector,
            spanner=spanner
            )

    @staticmethod
    def multimeasure_rests():
        r'''Makes multimeasure rests.
        '''
        mask = abjad.rhythmmakertools.SilenceMask(
            pattern=abjad.index_all(),
            use_multimeasure_rests=True,
            )
        return baca.RhythmBuilder(
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker(
                division_masks=[mask],
                ),
            )
