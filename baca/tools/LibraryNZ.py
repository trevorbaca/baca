# -*- coding: utf-8 -*-
import abjad
import baca


class LibraryNZ(object):
    r'''Library N - Z.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Library'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def natural_harmonics(selector=None):
        r'''Overrides note-head style on pitched logical ties.

        ..  container:: example

            Overrides note-head style on all pitched logical ties:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.natural_harmonics(),
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
                                \override NoteHead.style = #'harmonic
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

            Overrides note-head style on pitched logical ties in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.natural_harmonics(
                ...         baca.select_plts_in_tuplet(1),
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
                                \override NoteHead.style = #'harmonic
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
        selector = selector or baca.select_plts()
        return baca.OverrideCommand(
            attribute_name='style',
            attribute_value='harmonic',
            grob_name='note_head',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def nest(time_treatments=None):
        r'''Nests music.

        ..  container:: example

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.nest('+4/16'),
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
                            \times 13/11 {
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
                    }
                >>

        '''
        if not isinstance(time_treatments, list):
            time_treatments = [time_treatments]
        return baca.NestCommand(
            lmr_specifier=None,
            time_treatments=time_treatments,
            )

    @staticmethod
    def niente_swell(dynamic, selector=None):
        r'''Attaches niente swell to pitched logical ties:

        ..  container:: example

            Attaches niente swell to all pitched logical ties:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.niente_swell('p'),
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
                                \once \override Hairpin.circled-tip = ##t
                                c'16 \< [
                                d'16 \p ]
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
                                \once \override Hairpin.circled-tip = ##t
                                g''16 ] \> \p
                            }
                            \times 4/5 {
                                a'16 \!
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches niente swell to pitched logical ties in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.niente_swell(
                ...         'p',
                ...         baca.select_pls_in_tuplet(1),
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
                                \once \override Hairpin.circled-tip = ##t
                                fs''16 \< [
                                e''16 \p ]
                                ef''4 ~
                                ef''16
                                r16
                                \once \override Hairpin.circled-tip = ##t
                                af''16 \> \p [
                                g''16 \! ]
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
        start_token = 'niente < {}'
        start_token = start_token.format(dynamic)
        stop_token = '{} > niente'
        stop_token = stop_token.format(dynamic)
        return baca.SwellSpecifier(
            selector=selector,
            start_count=2,
            start_token=start_token,
            stop_count=2,
            stop_token=stop_token,
            )

    @staticmethod
    def notes():
        r'''Makes notes.
        '''
        return baca.RhythmSpecifier(
            rewrite_meter=True,
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker()
            )

    @staticmethod
    def one_line_staff(selector=None):
        r'''Attaches one-line staff to leaves.

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
                ...         selector=baca.select_leaves_in_tuplet(1),
                ...         ),
                ...     baca.one_line_staff(
                ...         selector=baca.select_leaves_in_tuplet(1),
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
            spanner=abjad.StaffLinesSpanner(lines=1),
            )

    @staticmethod
    def ottava(selector=None):
        r'''Attaches ottava spanner to trimmed leaves.

        ..  container:: example

            Attaches ottava spanner to all trimmed leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.ottava(),
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
                                \ottava #1
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
                                \ottava #0
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches ottava spanner to pitched runs:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.ottava(baca.select_each_plt_run()),
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
                                \ottava #1
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                \ottava #0
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \ottava #1
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                \ottava #0
                                r16
                                \ottava #1
                                af''16 [
                                g''16 ]
                            }
                            \times 4/5 {
                                a'16
                                \ottava #0
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        selector = selector or baca.select_leaves_in_trimmed_run()
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.OctavationSpanner(start=1, stop=0),
            )

    @staticmethod
    def ottava_bassa(selector=None):
        r'''Attaches ottava bassa spanner to trimmed leaves.

        ..  container:: example

            Attaches ottava bassa spanner to all trimmed leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.ottava_bassa(),
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
                                \ottava #-1
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
                                \ottava #0
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches ottava bassa spanner to pitched runs:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.ottava_bassa(baca.select_each_plt_run()),
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
                                \ottava #-1
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                \ottava #0
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \ottava #-1
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                \ottava #0
                                r16
                                \ottava #-1
                                af''16 [
                                g''16 ]
                            }
                            \times 4/5 {
                                a'16
                                \ottava #0
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        selector = selector or baca.select_leaves_in_trimmed_run()
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.OctavationSpanner(start=-1, stop=0),
            )

    @staticmethod
    def percussion_staff(selector=None):
        r'''Attaches percussion staff spanner to leaves.

        ..  container:: example

            Attaches percussion staff spanner to all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.percussion_staff(),
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

            Attaches percussion staff spanner to leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.one_line_staff(
                ...         baca.select_leaves_in_tuplet(1),
                ...         ),
                ...     baca.percussion_staff(
                ...         baca.select_leaves_in_tuplet(1),
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
            spanner=abjad.ClefSpanner(clef='percussion'),
            )

    @staticmethod
    def pervasive_trills(selector=None):
        r'''Attaches pervasive trills to notes and chords.

        ..  container:: example

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.pervasive_trills(),
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
                                c'16 [ \startTrillSpan
                                d'16 ] \stopTrillSpan \startTrillSpan
                                bf'4 ~ \stopTrillSpan \startTrillSpan
                                bf'16
                                r16 \stopTrillSpan
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ \startTrillSpan
                                e''16 ] \stopTrillSpan \startTrillSpan
                                ef''4 ~ \stopTrillSpan \startTrillSpan
                                ef''16
                                r16 \stopTrillSpan
                                af''16 [ \startTrillSpan
                                g''16 ] \stopTrillSpan \startTrillSpan
                            }
                            \times 4/5 {
                                a'16 \stopTrillSpan \startTrillSpan
                                r4 \stopTrillSpan
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches pervasive trills to pitched logical ties in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.pervasive_trills(
                ...         baca.select_pls_in_tuplet(1),
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
                                fs''16 [ \startTrillSpan
                                e''16 ] \stopTrillSpan \startTrillSpan
                                ef''4 ~ \stopTrillSpan \startTrillSpan
                                ef''16
                                r16 \stopTrillSpan
                                af''16 [ \startTrillSpan
                                g''16 ] \stopTrillSpan \startTrillSpan
                            }
                            \times 4/5 {
                                a'16 \stopTrillSpan
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.TrillCommand(
            minimum_written_duration=None,
            selector=selector,
            )

    @staticmethod
    def pervasive_trills_at_interval(interval, selector=None):
        r'''Attaches pervasive trills at `interval` to pitched logical ties.

        ..  container:: example

            Attaches pervasive trills to all pitched logical ties:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.pervasive_trills_at_interval(2),
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
                                \pitchedTrill
                                c'16 [ \startTrillSpan d'
                                \pitchedTrill
                                d'16 ] \stopTrillSpan \startTrillSpan e'
                                \pitchedTrill
                                bf'4 ~ \stopTrillSpan \startTrillSpan c''
                                bf'16
                                r16 \stopTrillSpan
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \pitchedTrill
                                fs''16 [ \startTrillSpan gs''
                                \pitchedTrill
                                e''16 ] \stopTrillSpan \startTrillSpan fs''
                                \pitchedTrill
                                ef''4 ~ \stopTrillSpan \startTrillSpan f''
                                ef''16
                                r16 \stopTrillSpan
                                \pitchedTrill
                                af''16 [ \startTrillSpan bf''
                                \pitchedTrill
                                g''16 ] \stopTrillSpan \startTrillSpan a''
                            }
                            \times 4/5 {
                                \pitchedTrill
                                a'16 \stopTrillSpan \startTrillSpan b'
                                r4 \stopTrillSpan
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches pervasive trills to pitched leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.pervasive_trills_at_interval(
                ...         2,
                ...         baca.select_pls_in_tuplet(1),
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
                                \pitchedTrill
                                fs''16 [ \startTrillSpan gs''
                                \pitchedTrill
                                e''16 ] \stopTrillSpan \startTrillSpan fs''
                                \pitchedTrill
                                ef''4 ~ \stopTrillSpan \startTrillSpan f''
                                ef''16
                                r16 \stopTrillSpan
                                \pitchedTrill
                                af''16 [ \startTrillSpan bf''
                                \pitchedTrill
                                g''16 ] \stopTrillSpan \startTrillSpan a''
                            }
                            \times 4/5 {
                                a'16 \stopTrillSpan
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.TrillCommand(
            interval=interval,
            minimum_written_duration=None,
            selector=selector,
            )

    @staticmethod
    def pervasive_trills_at_pitch(pitch, harmonic=None, selector=None):
        r'''Attaches pervasive trills at `pitch` to pitched logical ties.

        ..  container:: example

            Attaches pervasive trills to all pitched logical ties:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.pervasive_trills_at_pitch(1),
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
                                \pitchedTrill
                                c'16 [ \startTrillSpan cs'
                                \pitchedTrill
                                d'16 ] \stopTrillSpan \startTrillSpan cs'
                                \pitchedTrill
                                bf'4 ~ \stopTrillSpan \startTrillSpan cs'
                                bf'16
                                r16 \stopTrillSpan
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \pitchedTrill
                                fs''16 [ \startTrillSpan cs'
                                \pitchedTrill
                                e''16 ] \stopTrillSpan \startTrillSpan cs'
                                \pitchedTrill
                                ef''4 ~ \stopTrillSpan \startTrillSpan cs'
                                ef''16
                                r16 \stopTrillSpan
                                \pitchedTrill
                                af''16 [ \startTrillSpan cs'
                                \pitchedTrill
                                g''16 ] \stopTrillSpan \startTrillSpan cs'
                            }
                            \times 4/5 {
                                \pitchedTrill
                                a'16 \stopTrillSpan \startTrillSpan cs'
                                r4 \stopTrillSpan
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches pervasive trills to all pitched leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.pervasive_trills_at_pitch(
                ...         pitch=1,
                ...         selector=baca.select_pls_in_tuplet(1),
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
                                \pitchedTrill
                                fs''16 [ \startTrillSpan cs'
                                \pitchedTrill
                                e''16 ] \stopTrillSpan \startTrillSpan cs'
                                \pitchedTrill
                                ef''4 ~ \stopTrillSpan \startTrillSpan cs'
                                ef''16
                                r16 \stopTrillSpan
                                \pitchedTrill
                                af''16 [ \startTrillSpan cs'
                                \pitchedTrill
                                g''16 ] \stopTrillSpan \startTrillSpan cs'
                            }
                            \times 4/5 {
                                a'16 \stopTrillSpan
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.TrillCommand(
            harmonic=harmonic,
            minimum_written_duration=None,
            pitch=pitch,
            selector=selector,
            )

    @staticmethod
    def pitches(
        source,
        allow_repeat_pitches=True,
        operators=None,
        start_index=None,
        ):
        r'''Sets pitches.
        '''
        return baca.ScorePitchCommand(
            allow_repeat_pitches=allow_repeat_pitches,
            operators=operators,
            source=source,
            start_index=start_index,
            )

    @staticmethod
    def possibile_dynamic(dynamic, selector=None, direction=Down):
        r'''Attaches possibile dynamic to pitched head 0.

        ..  container:: example

            Attaches possibilie dynamic to pitched head 0:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.possibile_dynamic('ff'),
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
                                            possibile
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

            Attaches possibile dynamic to pitched head 0 of tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.possibile_dynamic(
                ...         'ff',
                ...         baca.select_plt_head_in_tuplet(1, 0),
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
                                            possibile
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
        markup += abjad.Markup('possibile').upright()
        markup = abjad.new(markup, direction=direction)
        selector = selector or baca.select_plt_head(n=0)
        return baca.AttachCommand(
            arguments=[markup],
            selector=selector,
            )

    @staticmethod
    def proportional_notation_duration(duration=None, selector=None):
        r'''Sets proportional notation duration on leaf 0:

        ..  container:: example

            Sets proportional notation duration on leaf 0:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.proportional_notation_duration((1, 8)),
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
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 8)
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
                >>

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.proportional_notation_duration((1, 12)),
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
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)
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
                >>

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.proportional_notation_duration((1, 16)),
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
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)
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
                >>

        '''
        assert isinstance(duration, tuple), repr(duration)
        assert len(duration) == 2, repr(duration)
        moment = abjad.SchemeMoment(duration)
        selector = selector or baca.select_leaf(0)
        return baca.SetCommand(
            context_name='score',
            selector=selector,
            setting_name='proportional_notation_duration',
            setting_value=moment,
            )

    @staticmethod
    def register(start, stop=None, selector=None):
        r'''Octave-transposes pitched logical ties.

        ..  container:: example

            Octave-transposes all pitched logical ties to the octave rooted at
            -6:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.register(-6),
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
                                bf4 ~
                                bf16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs16 [
                                e'16 ]
                                ef'4 ~
                                ef'16
                                r16
                                af16 [
                                g16 ]
                            }
                            \times 4/5 {
                                a16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

            Octave-transposes pitched logical ties in tuplet 1 to the octave
            rooted at -6:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.color('red', baca.select_leaves_in_tuplet(1)),
                ...     baca.register(
                ...         -6,
                ...         selector=baca.select_leaves_in_tuplet(1),
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
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs16 [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e'16 ]
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                ef'4 ~
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                ef'16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                af16 [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                g16 ]
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

            Octave-transposes all pitched logical ties to an octave
            interpolated from -6 to 10:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.register(-6, 10),
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
                                bf4 ~
                                bf16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs'16 [
                                e'16 ]
                                ef'4 ~
                                ef'16
                                r16
                                af'16 [
                                g'16 ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

            Octave-transposes pitched logical ties in tuplet 1 to an octave
            interpolated from -6 to 10:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.color('red', baca.select_leaves_in_tuplet(1)),
                ...     baca.register(
                ...         start=-6,
                ...         stop=10,
                ...         selector=baca.select_leaves_in_tuplet(1),
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
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs16 [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e'16 ]
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                ef'4 ~
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                ef'16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                af'16 [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                g'16 ]
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
        if stop is None:
            return baca.RegisterCommand(
                registration=abjad.Registration(
                    [('[A0, C8]', start)],
                    ),
                selector=selector,
                )
        return baca.RegisterInterpolationCommand(
            selector=selector,
            start_pitch=start,
            stop_pitch=stop,
            )

    @staticmethod
    def reiterated_dynamic(dynamic=None, selector=None):
        r'''Attaches `dynamic` to pitched heads.

        ..  container:: example

            Attaches dynamic to all pitched heads:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.reiterated_dynamic('f'),
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
                                c'16 -\f [
                                d'16 -\f ]
                                bf'4 -\f ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\f [
                                e''16 -\f ]
                                ef''4 -\f ~
                                ef''16
                                r16
                                af''16 -\f [
                                g''16 -\f ]
                            }
                            \times 4/5 {
                                a'16 -\f
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches dynamic to pitched heads in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.reiterated_dynamic(
                ...         'f',
                ...         selector=baca.select_plt_heads_in_tuplet(1),
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
                                fs''16 -\f [
                                e''16 -\f ]
                                ef''4 -\f ~
                                ef''16
                                r16
                                af''16 -\f [
                                g''16 -\f ]
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
        selector = selector or baca.select_plt_heads()
        return baca.AttachCommand(
            arguments=[abjad.Articulation(dynamic)],
            selector=selector,
            )

    @staticmethod
    def repeat_ties_down(selector=None):
        r'''Overrides repeat tie direction on leaves.

        ..  container:: example

            Overrides repeat tie direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[11, 11, 12], [11, 11, 11], [11]],
                ...     baca.messiaen_tie_each(),
                ...     baca.repeat_ties_down(),
                ...     baca.rests_around([2], [4]),
                ...     baca.stems_up(),
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
                                \override Stem.direction = #up
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override RepeatTie.direction = #down
                                b'16 [
                                b'16 \repeatTie ]
                                c''4
                                c''16 \repeatTie
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                b'16 [
                                b'16 \repeatTie ]
                                b'4 \repeatTie
                                b'16 \repeatTie
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert RepeatTie.direction
                                r4
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides repeat tie direction on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[11, 11, 12], [11, 11, 11], [11]],
                ...     baca.messiaen_tie_each(),
                ...     baca.repeat_ties_down(baca.select_leaves_in_tuplet(1)),
                ...     baca.rests_around([2], [4]),
                ...     baca.stems_up(),
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
                                \override Stem.direction = #up
                                \override TupletBracket.staff-padding = #5
                                r8
                                b'16 [
                                b'16 \repeatTie ]
                                c''4
                                c''16 \repeatTie
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                \override RepeatTie.direction = #down
                                b'16 [
                                b'16 \repeatTie ]
                                b'4 \repeatTie
                                b'16 \repeatTie
                                r16
                                \revert RepeatTie.direction
                            }
                            \times 4/5 {
                                b'16
                                r4
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        selector = selector or baca.select_leaves_in_trimmed_run()
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=Down,
            grob_name='repeat_tie',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def repeat_ties_up(selector=None):
        r'''Overrides repeat tie direction on leaves.

        ..  container:: example

            Overrides repeat tie direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[11, 11, 12], [11, 11, 11], [11]],
                ...     baca.messiaen_tie_each(),
                ...     baca.repeat_ties_up(),
                ...     baca.rests_around([2], [4]),
                ...     baca.stems_down(),
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
                                \override Stem.direction = #down
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override RepeatTie.direction = #up
                                b'16 [
                                b'16 \repeatTie ]
                                c''4
                                c''16 \repeatTie
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                b'16 [
                                b'16 \repeatTie ]
                                b'4 \repeatTie
                                b'16 \repeatTie
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert RepeatTie.direction
                                r4
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides repeat tie direction on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[11, 11, 12], [11, 11, 11], [11]],
                ...     baca.messiaen_tie_each(),
                ...     baca.repeat_ties_up(baca.select_leaves_in_tuplet(1)),
                ...     baca.rests_around([2], [4]),
                ...     baca.stems_down(),
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
                                \override Stem.direction = #down
                                \override TupletBracket.staff-padding = #5
                                r8
                                b'16 [
                                b'16 \repeatTie ]
                                c''4
                                c''16 \repeatTie
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                \override RepeatTie.direction = #up
                                b'16 [
                                b'16 \repeatTie ]
                                b'4 \repeatTie
                                b'16 \repeatTie
                                r16
                                \revert RepeatTie.direction
                            }
                            \times 4/5 {
                                b'16
                                r4
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        selector = selector or baca.select_leaves_in_trimmed_run()
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=Up,
            grob_name='repeat_tie',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def repeated_durations(durations):
        r'''Makes repeated durations.
        '''
        if isinstance(durations, abjad.Duration):
            durations = [durations]
        elif isinstance(durations, tuple):
            assert len(durations) == 2
            durations = [abjad.Duration(durations)]
        return baca.RhythmSpecifier(
            division_expression=baca.split_by_durations(durations=durations),
            rewrite_meter=True,
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker(
                tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                    use_messiaen_style_ties=True,
                    ),
                ),
            )

    @staticmethod
    def rest_position(n=None, selector=None):
        r'''Overrides position of rests.

        ..  container:: example

            Overrides position of all rests:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rest_position(-6),
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
                                \override Rest.staff-position = #-6
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
                                \revert Rest.staff-position
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides position of rests in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rest_position(
                ...         -6,
                ...         baca.select_leaves_in_tuplet(1)
                ...         .by_leaf(pitched=False),
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
                                \override Rest.staff-position = #-6
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert Rest.staff-position
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
        selector = selector or baca.select_rests()
        return baca.OverrideCommand(
            attribute_name='staff_position',
            attribute_value=n,
            grob_name='rest',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def rests():
        r'''Makes rests.
        '''
        mask = abjad.rhythmmakertools.SilenceMask(
            pattern=abjad.index_all(),
            )
        return baca.RhythmSpecifier(
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker(
                division_masks=[mask],
                ),
            )

    @staticmethod
    def rests_after(counts):
        r'''Makes rests after music.

        ..  container:: example

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_after([2]),
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
                            \times 7/8 {
                                \override TupletBracket.staff-padding = #5
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
                            \times 2/3 {
                                a'16
                                r8
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.RestAffixCommand(
            suffix=counts,
            )

    @staticmethod
    def rests_around(prefix, suffix):
        r'''Makes rests around music.

        ..  container:: example

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
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
                                g''16 ]
                            }
                            \times 2/3 {
                                a'16
                                r8
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.RestAffixCommand(
            prefix=prefix,
            suffix=suffix,
            )

    @staticmethod
    def rests_before(counts):
        r'''Makes rests before music.

        ..  container:: example

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_before([2]),
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
                            {
                                a'16
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.RestAffixCommand(
            prefix=counts,
            )

    @staticmethod
    def rests_down(selector=None):
        r'''Overrides direction of rests.

        ..  container:: example

            Overrides direction of all rests:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_down(),
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
                                \override Rest.direction = #down
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
                                \revert Rest.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides direction of rests in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_down(
                ...         baca.select_leaves_in_tuplet(1)
                ...         .by_leaf(pitched=False)
                ...         ,
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
                                \override Rest.direction = #down
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
                                \revert Rest.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        selector = selector or baca.select_rests()
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=Down,
            grob_name='rest',
            revert=True,
            )

    @staticmethod
    def rests_up(selector=None):
        r'''Up-overrides direction of rests.

        ..  container:: example

            Up-overrides direction of all rests:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_up(),
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
                                \override Rest.direction = #up
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
                                \revert Rest.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides direction of rests in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_up(
                ...         baca.select_leaves_in_tuplet(1)
                ...         .by_leaf(pitched=False)
                ...         ,
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
                                \override Rest.direction = #up
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert Rest.direction
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
        selector = selector or baca.select_rests()
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=Up,
            grob_name='rest',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def resume():
        r'''Resumes music at next offset across all voices in score.
        '''
        return baca.AnchorCommand()

    @staticmethod
    def resume_after(remote_voice_name):
        r'''Resumes music after remote selection.
        '''
        return baca.AnchorCommand(
            remote_selector=baca.select_leaf(-1),
            remote_voice_name=remote_voice_name,
            use_remote_stop_offset=True,
            )

    @staticmethod
    def script_color(color='red', selector=None):
        r'''Overrides script color.

        ..  container:: example

            Overrides script color on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.accents(),
                ...     baca.rests_around([2], [4]),
                ...     baca.script_color('red'),
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
                                \override Script.color = #red
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
                                \revert Script.color
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides script color on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.accents(),
                ...     baca.rests_around([2], [4]),
                ...     baca.script_color(
                ...         'red',
                ...         baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                \override Script.color = #red
                                fs''16 -\accent [
                                e''16 -\accent ]
                                ef''4 -\accent ~
                                ef''16
                                r16
                                af''16 -\accent [
                                g''16 -\accent ]
                                \revert Script.color
                            }
                            \times 4/5 {
                                a'16 -\accent
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        selector = selector or baca.select_leaves()
        return baca.OverrideCommand(
            attribute_name='color',
            attribute_value=color,
            grob_name='script',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def script_extra_offset(pair=None, selector=None):
        r'''Overrides script extra offset.

        ..  container:: example

            Overrides script extra offset on leaf 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.accents(),
                ...     baca.rests_around([2], [4]),
                ...     baca.script_extra_offset((-1.5, 0)),
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
                                \override Script.extra-offset = #'(-1.5 . 0)
                                \override TupletBracket.staff-padding = #5
                                r8
                                \revert Script.extra-offset
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

            Overrides script extra offset on leaf 0 in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.accents(),
                ...     baca.rests_around([2], [4]),
                ...     baca.script_extra_offset(
                ...         (-1.5, 0),
                ...         baca.select_leaf_in_tuplet(1, 0),
                ...         ),
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
                                \override Script.extra-offset = #'(-1.5 . 0)
                                fs''16 -\accent [
                                \revert Script.extra-offset
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

        '''
        selector = selector or baca.select_leaf(n=0)
        return baca.OverrideCommand(
            attribute_name='extra_offset',
            attribute_value=pair,
            grob_name='script',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def scripts_down(selector=None):
        r'''Down-overrides script direction on leaves.

        ..  container:: example

            Down-overrides script direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.accents(),
                ...     baca.rests_around([2], [4]),
                ...     baca.scripts_down(),
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
                                \override Script.direction = #down
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
                                \revert Script.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Down-overrides script direction all leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.accents(),
                ...     baca.rests_around([2], [4]),
                ...     baca.scripts_down(baca.select_leaves_in_tuplet(1)),
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
                                \override Script.direction = #down
                                fs''16 -\accent [
                                e''16 -\accent ]
                                ef''4 -\accent ~
                                ef''16
                                r16
                                af''16 -\accent [
                                g''16 -\accent ]
                                \revert Script.direction
                            }
                            \times 4/5 {
                                a'16 -\accent
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=Down,
            grob_name='script',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def scripts_up(selector=None):
        r'''Up-overrides script direction on leaves.

        ..  container:: example

            Up-overrides script direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.accents(),
                ...     baca.rests_around([2], [4]),
                ...     baca.scripts_up(),
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
                                \override Script.direction = #up
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
                                \revert Script.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides script direction on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.accents(),
                ...     baca.rests_around([2], [4]),
                ...     baca.scripts_up(baca.select_leaves_in_tuplet(1)),
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
                                \override Script.direction = #up
                                fs''16 -\accent [
                                e''16 -\accent ]
                                ef''4 -\accent ~
                                ef''16
                                r16
                                af''16 -\accent [
                                g''16 -\accent ]
                                \revert Script.direction
                            }
                            \times 4/5 {
                                a'16 -\accent
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=Up,
            grob_name='script',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def short_fermata(selector=None):
        r'''Attaches short fermata to leaf.

        ..  container:: example

            Attaches short fermata to first leaf:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.short_fermata(),
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
                                r8 -\shortfermata
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

            Attaches short fermata to first leaf in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.short_fermata(
                ...         baca.select_plt_head_in_tuplet(1, 0),
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
                                fs''16 -\shortfermata [
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
        selector = selector or baca.select_leaf(n=0)
        return baca.AttachCommand(
            arguments=[abjad.Articulation('shortfermata')],
            selector=selector,
            )

    @staticmethod
    def single_attack(duration):
        r'''Makes single attacks with `duration`.
        '''
        duration = abjad.Duration(duration)
        numerator, denominator = duration.pair
        rhythm_maker = abjad.rhythmmakertools.IncisedRhythmMaker(
            incise_specifier=abjad.rhythmmakertools.InciseSpecifier(
                fill_with_notes=False,
                outer_divisions_only=True,
                prefix_talea=[numerator],
                prefix_counts=[1],
                talea_denominator=denominator,
                ),
            )
        return baca.RhythmSpecifier(
            rhythm_maker=rhythm_maker,
            )

    @staticmethod
    def single_taper(
        denominator=16,
        start_talea=[4],
        stop_talea=[3, -1],
        ):
        r'''Makes single tapers.
        '''
        return baca.RhythmSpecifier(
            rhythm_maker=abjad.rhythmmakertools.IncisedRhythmMaker(
                incise_specifier=abjad.rhythmmakertools.InciseSpecifier(
                    outer_divisions_only=True,
                    prefix_talea=start_talea,
                    prefix_counts=[len(start_talea)],
                    suffix_talea=stop_talea,
                    suffix_counts=[len(stop_talea)],
                    talea_denominator=denominator,
                    ),
                tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                    tie_consecutive_notes=True,
                    use_messiaen_style_ties=True,
                    ),
                ),
            )

    @staticmethod
    def skips_after(counts):
        r'''Makes skips after music.

        ..  container:: example

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.skips_after([2]),
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
                            \times 7/8 {
                                \override TupletBracket.staff-padding = #5
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
                            \times 2/3 {
                                a'16
                                s8
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.RestAffixCommand(
            skips_instead_of_rests=True,
            suffix=counts,
            )

    @staticmethod
    def skips_around(prefix, suffix):
        r'''Makes skips around music.

        ..  container:: example

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.skips_around([2], [2]),
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
                                s8
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
                            \times 2/3 {
                                a'16
                                s8
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.RestAffixCommand(
            prefix=prefix,
            skips_instead_of_rests=True,
            suffix=suffix,
            )

    @staticmethod
    def skips_before(counts):
        r'''Makes skips before music.

        ..  container:: example

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.skips_before([2]),
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
                                s8
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
                            {
                                a'16
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.RestAffixCommand(
            prefix=counts,
            skips_instead_of_rests=True,
            )

    @staticmethod
    def slur(selector=None):
        r'''Slurs trimmed leaves.

        ..  container:: example

            Slurs all trimmed leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.slur(),
                ...     baca.slurs_down(),
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
                                \override Slur.direction = #down
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [ (
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
                                a'16 )
                                r4
                                \revert Slur.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Slurs trimmed leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.slur(baca.select_trimmed_run_in_tuplet(1)),
                ...     baca.slurs_down(),
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
                                \override Slur.direction = #down
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
                                fs''16 [ (
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] )
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Slur.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        selector = selector or baca.select_leaves_in_trimmed_run()
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.Slur(),
            )

    @staticmethod
    def slur_each_plt_run(start=None, stop=None):
        r'''Slurs pitched runs.

        ..  container:: example

            Slurs all pitched runs:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.slur_each_plt_run(),
                ...     baca.slurs_down(),
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
                                \override Slur.direction = #down
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [ (
                                d'16 ]
                                bf'4 ~
                                bf'16 )
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ (
                                e''16 ]
                                ef''4 ~
                                ef''16 )
                                r16
                                af''16 [ (
                                g''16 ]
                            }
                            \times 4/5 {
                                a'16 )
                                r4
                                \revert Slur.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Slurs last two pitched runs:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.slur_each_plt_run(start=-2),
                ...     baca.slurs_down(),
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
                                \override Slur.direction = #down
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
                                fs''16 [ (
                                e''16 ]
                                ef''4 ~
                                ef''16 )
                                r16
                                af''16 [ (
                                g''16 ]
                            }
                            \times 4/5 {
                                a'16 )
                                r4
                                \revert Slur.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.SpannerCommand(
            selector=baca.select_each_plt_run(start=start, stop=stop),
            spanner=abjad.Slur(),
            )

    @staticmethod
    def slur_trimmed_run_in_each_tuplet(start=None, stop=None):
        r'''Slurs trimmed leaves in tuplets.

        ..  container:: example

            Slurs trimmed leaves in all tuplets:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.slur_trimmed_run_in_each_tuplet(),
                ...     baca.slurs_down(),
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
                                \override Slur.direction = #down
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [ (
                                d'16 ]
                                bf'4 ~
                                bf'16 )
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ (
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] )
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Slur.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Slurs trimmed leaves in last two tuplets:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.slur_trimmed_run_in_each_tuplet(start=-2),
                ...     baca.slurs_down(),
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
                                \override Slur.direction = #down
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
                                fs''16 [ (
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] )
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Slur.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.SpannerCommand(
            selector=baca.select_trimmed_run_in_each_tuplet(
                start=start,
                stop=stop,
                ),
            spanner=abjad.Slur(),
            )

    @staticmethod
    def slurs_down(selector=None):
        r'''Overrides slur direction for leaves.

        ..  container:: example

            Overrides slur direction for all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.slur_trimmed_run_in_each_tuplet(),
                ...     baca.slurs_down(),
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
                                \override Slur.direction = #down
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [ (
                                d'16 ]
                                bf'4 ~
                                bf'16 )
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ (
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] )
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Slur.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides slur direction leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.slur_trimmed_run_in_each_tuplet(),
                ...     baca.slurs_down(baca.select_leaves_in_tuplet(1)),
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
                                c'16 [ (
                                d'16 ]
                                bf'4 ~
                                bf'16 )
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override Slur.direction = #down
                                fs''16 [ (
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] )
                                \revert Slur.direction
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
            attribute_name='direction',
            attribute_value=Down,
            grob_name='slur',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def slurs_up(selector=None):
        r'''Overrides slur direction for leaves.

        ..  container:: example

            Overrides slur direction for all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.slur_trimmed_run_in_each_tuplet(),
                ...     baca.slurs_up(),
                ...     baca.stems_down(),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     baca.tuplet_brackets_down(),
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
                                \override Slur.direction = #up
                                \override Stem.direction = #down
                                \override TupletBracket.staff-padding = #5
                                \override TupletBracket.direction = #down
                                r8
                                c'16 [ (
                                d'16 ]
                                bf'4 ~
                                bf'16 )
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ (
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] )
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Slur.direction
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                                \revert TupletBracket.direction
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides slur direction all leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.slur_trimmed_run_in_each_tuplet(),
                ...     baca.slurs_up(baca.select_leaves_in_tuplet(1)),
                ...     baca.stems_down(),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     baca.tuplet_brackets_down(),
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
                                \override Stem.direction = #down
                                \override TupletBracket.staff-padding = #5
                                \override TupletBracket.direction = #down
                                r8
                                c'16 [ (
                                d'16 ]
                                bf'4 ~
                                bf'16 )
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override Slur.direction = #up
                                fs''16 [ (
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] )
                                \revert Slur.direction
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                                \revert TupletBracket.direction
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=Up,
            grob_name='slur',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def soprano_to_octave(n=4, selector=None):
        r"""Octave-transposes music.

        ..  container:: example

            Octave-transposes music such that the highest note in the entire
            selection appears in octave 3:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.color('red', baca.select_plts()),
                ...     baca.soprano_to_octave(3),
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
                                <c,, d,, bf,,>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c,, d,, bf,,>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                f,8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                f,32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef, e, fs>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef, e, fs>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g,, af,>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g,, af,>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a,,8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a,,32 ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music that such that the highest note in each
            pitched logical tie appears in octave 3:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.soprano_to_octave(
                ...         n=3,
                ...         selector=baca.select_each_plt(),
                ...         ),
                ...     baca.color('red', baca.select_each_plt()),
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
                                <ef, e, fs>8 ~ [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef, e, fs>32 ]
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

            Octave-transposes music that such that the highest note in each
            of the last two pitched logical ties appears in octave 3:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.soprano_to_octave(
                ...         3,
                ...         selector=baca.select_each_plt(start=-2),
                ...         ),
                ...     baca.color('red', baca.select_each_plt(start=-2)),
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

        """
        return baca.RegisterToOctaveCommand(
            anchor=Top,
            octave_number=n,
            selector=selector,
            )

    @staticmethod
    def split_by_durations(durations):
        r'''Splits divisions by `durations`.

        ..  container:: example

            ::

                >>> expression = baca.split_by_durations([(3, 8)])

            ::

                >>> for item in expression([(2, 8), (2, 8)]):
                ...     item
                ...
                Division((3, 8))
                Division((1, 8))

            ::

                >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
                ...     item
                ...
                Division((3, 8))
                Division((3, 8))

            ::

                >>> for item in expression([(2, 8), (2, 8), (2, 8), (2, 8)]):
                ...     item
                ...
                Division((3, 8))
                Division((3, 8))
                Division((2, 8))

        '''
        expression = baca.DivisionSequenceExpression()
        expression = expression.division_sequence()
        expression = expression.flatten()
        expression = expression.sum()
        expression = expression.division_sequence()
        expression = expression.split_by_durations(
            cyclic=True,
            durations=durations,
            )
        expression = expression.flatten()
        return expression

    @staticmethod
    def staccati(selector=None):
        r'''Attaches staccati to pitched heads.

        ..  container:: example

            Attaches staccati to all pitched heads:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.staccati(),
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
                                c'16 -\staccato [
                                d'16 -\staccato ]
                                bf'4 -\staccato ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\staccato [
                                e''16 -\staccato ]
                                ef''4 -\staccato ~
                                ef''16
                                r16
                                af''16 -\staccato [
                                g''16 -\staccato ]
                            }
                            \times 4/5 {
                                a'16 -\staccato
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches staccati to pitched heads in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.staccati(baca.select_plt_heads_in_tuplet(1)),
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
                                fs''16 -\staccato [
                                e''16 -\staccato ]
                                ef''4 -\staccato ~
                                ef''16
                                r16
                                af''16 -\staccato [
                                g''16 -\staccato ]
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
        selector = selector or baca.select_plt_heads()
        return baca.AttachCommand(
            arguments=[abjad.Articulation('staccato')],
            selector=selector,
            )

    @staticmethod
    def staccatissimi(selector=None):
        r'''Attaches staccatissimi to pitched heads.

        ..  container:: example

            Attaches staccatissimi to all pitched heads:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.staccatissimi(),
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
                                c'16 -\staccatissimo [
                                d'16 -\staccatissimo ]
                                bf'4 -\staccatissimo ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\staccatissimo [
                                e''16 -\staccatissimo ]
                                ef''4 -\staccatissimo ~
                                ef''16
                                r16
                                af''16 -\staccatissimo [
                                g''16 -\staccatissimo ]
                            }
                            \times 4/5 {
                                a'16 -\staccatissimo
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches staccatissimi to pitched heads in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.staccatissimi(baca.select_leaves_in_tuplet(1)),
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
                                fs''16 -\staccatissimo [
                                e''16 -\staccatissimo ]
                                ef''4 -\staccatissimo ~
                                ef''16 -\staccatissimo
                                r16 -\staccatissimo
                                af''16 -\staccatissimo [
                                g''16 -\staccatissimo ]
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
        selector = selector or baca.select_plt_heads()
        return baca.AttachCommand(
            arguments=[abjad.Articulation('staccatissimo')],
            selector=selector,
            )

    @staticmethod
    def stem_color(color='red', context_name=None, selector=None):
        r'''Overrides stem color on trimmed leaves.

        ..  container:: example

            Overrides stem color on all trimmed leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.stem_color(color='red'),
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
                                \override Stem.color = #red
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
                                \revert Stem.color
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides stem color on trimmed leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.stem_color(
                ...         color='red',
                ...         selector=baca.select_trimmed_run_in_tuplet(1),
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
                                \override Stem.color = #red
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert Stem.color
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
        selector = selector or baca.select_leaves_in_trimmed_run()
        return baca.OverrideCommand(
            attribute_name='color',
            attribute_value=color,
            context_name=context_name,
            grob_name='stem',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def stem_tremolo(selector=None):
        r'''Attaches stem tremolo to pitched leaves.

        ..  container:: example

            Attaches stem tremolo to all pitched leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.stem_tremolo(),
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
                                c'16 :32 [
                                d'16 :32 ]
                                bf'4 :32 ~
                                bf'16 :32
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 :32 [
                                e''16 :32 ]
                                ef''4 :32 ~
                                ef''16 :32
                                r16
                                af''16 :32 [
                                g''16 :32 ]
                            }
                            \times 4/5 {
                                a'16 :32
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches stem tremolo to pitched leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.stem_tremolo(
                ...         baca.select_pls_in_tuplet(n=1),
                ...         ),
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
                                fs''16 :32 [
                                e''16 :32 ]
                                ef''4 :32 ~
                                ef''16 :32
                                r16
                                af''16 :32 [
                                g''16 :32 ]
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
        selector = selector or baca.select_pls()
        return baca.StemTremoloCommand(
            selector=selector,
            tremolo_flags=32,
            )

    @staticmethod
    def stems_down(selector=None):
        r'''Down-overrides stem direction on leaves:

        ..  container:: example

            Down-overrides stem direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.stems_down(),
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
                                \override Stem.direction = #down
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
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Down-overrides stem direction for leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.stems_down(baca.select_leaves_in_tuplet(1)),
                ...     baca.stems_up(),
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
                                \override Stem.direction = #up
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
                                \override Stem.direction = #down
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert Stem.direction
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=Down,
            grob_name='stem',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def stems_up(selector=None):
        r'''Up-overrides stem direction on leaves.

        ..  container:: example

            Overrides stem direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 2',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.stems_up(),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override Stem.direction = #up
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
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides stem direction on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 2',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [10]],
                ...     baca.rests_around([2], [4]),
                ...     baca.stems_down(),
                ...     baca.stems_up(baca.select_leaves_in_tuplet(n=1)),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override Stem.direction = #down
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
                                \override Stem.direction = #up
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert Stem.direction
                            }
                            \times 4/5 {
                                bf'16
                                r4
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=Up,
            grob_name='stem',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def strict_note_spacing_off(selector=None):
        r'''Turns strict note spacing off on first leaf.

        ..  container:: example

            Turns strict note spacing off on first leaf:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.strict_note_spacing_off(),
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
                                \override Score.SpacingSpanner.strict-note-spacing = ##f
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
                                \revert Score.SpacingSpanner.strict-note-spacing
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='strict_note_spacing',
            attribute_value=False,
            context_name='score',
            grob_name='spacing_spanner',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def strict_quarter_divisions():
        r'''Makes strict quarter divisions.

        ..  container:: example

            ::

                >>> expression = baca.strict_quarter_divisions()
                >>> for item in expression([(2, 4), (2, 4)]):
                ...     item
                ...
                Division((1, 4))
                Division((1, 4))
                Division((1, 4))
                Division((1, 4))

        '''
        expression = baca.DivisionSequenceExpression()
        expression = expression.division_sequence()
        expression = expression.split_by_durations(
            durations=[abjad.Duration(1, 4)]
            )
        expression = expression.sequence()
        expression = expression.flatten()
        return expression

    @staticmethod
    def sustain_pedal(selector=None):
        r'''Pedals selection.

        ..  container:: example

            Pedals leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.sustain_pedal(),
                ...     baca.sustain_pedal_staff_padding(4),
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
                                \set Staff.pedalSustainStyle = #'bracket
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4
                                \override TupletBracket.staff-padding = #5
                                r8 \sustainOn
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
                                r4 \sustainOff
                                \revert Staff.SustainPedalLineSpanner.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.sustain_pedal(
                ...         selector=baca.select_leaves_in_tuplet(n=1),
                ...         ),
                ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4
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
                                \set Staff.pedalSustainStyle = #'bracket
                                fs''16 [ \sustainOn
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] \sustainOff
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Staff.SustainPedalLineSpanner.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplet 1 (leaked to the left):

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.sustain_pedal(
                ...         selector=baca.select_leaves_in_tuplet(
                ...             n=1,
                ...             leak=Left,
                ...             ),
                ...         ),
                ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                \set Staff.pedalSustainStyle = #'bracket
                                r16 \sustainOn
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] \sustainOff
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Staff.SustainPedalLineSpanner.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplet 1 (leaked to the right):

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.sustain_pedal(
                ...         selector=baca.select_leaves_in_tuplet(
                ...             n=1,
                ...             leak=Right,
                ...             ),
                ...         ),
                ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4
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
                                \set Staff.pedalSustainStyle = #'bracket
                                fs''16 [ \sustainOn
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                            }
                            \times 4/5 {
                                a'16 \sustainOff
                                r4
                                \revert Staff.SustainPedalLineSpanner.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplet 1 (leaked both left and right):

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.sustain_pedal(
                ...         selector=baca.select_leaves_in_tuplet(
                ...             n=1,
                ...             leak=Both,
                ...             ),
                ...         ),
                ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                \set Staff.pedalSustainStyle = #'bracket
                                r16 \sustainOn
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
                                a'16 \sustainOff
                                r4
                                \revert Staff.SustainPedalLineSpanner.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplets:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.sustain_pedal(
                ...         selector=baca.select_leaves_in_each_tuplet(),
                ...         ),
                ...     baca.sustain_pedal_staff_padding(4),
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
                                \set Staff.pedalSustainStyle = #'bracket
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4
                                \override TupletBracket.staff-padding = #5
                                r8 \sustainOn
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16 \sustainOff
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \set Staff.pedalSustainStyle = #'bracket
                                fs''16 [ \sustainOn
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] \sustainOff
                            }
                            \times 4/5 {
                                \set Staff.pedalSustainStyle = #'bracket
                                a'16 \sustainOn
                                r4 \sustainOff
                                \revert Staff.SustainPedalLineSpanner.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplets (leaked to the left):

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.sustain_pedal(
                ...         selector=baca.select_leaves_in_each_tuplet(leak=Left),
                ...         ),
                ...     baca.sustain_pedal_staff_padding(4),
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
                                \set Staff.pedalSustainStyle = #'bracket
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4
                                \override TupletBracket.staff-padding = #5
                                r8 \sustainOn
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                \set Staff.pedalSustainStyle = #'bracket
                                r16 \sustainOff \sustainOn
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                \set Staff.pedalSustainStyle = #'bracket
                                g''16 ] \sustainOff \sustainOn
                            }
                            \times 4/5 {
                                a'16
                                r4 \sustainOff
                                \revert Staff.SustainPedalLineSpanner.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplets (leaked to the right):

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.sustain_pedal(
                ...         selector=baca.select_leaves_in_each_tuplet(leak=Right),
                ...         ),
                ...     baca.sustain_pedal_staff_padding(4),
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
                                \set Staff.pedalSustainStyle = #'bracket
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4
                                \override TupletBracket.staff-padding = #5
                                r8 \sustainOn
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \set Staff.pedalSustainStyle = #'bracket
                                fs''16 \sustainOff [ \sustainOn
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                            }
                            \times 4/5 {
                                \set Staff.pedalSustainStyle = #'bracket
                                a'16 \sustainOff \sustainOn
                                r4 \sustainOff
                                \revert Staff.SustainPedalLineSpanner.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.PianoPedalSpanner(
                style='bracket',
                ),
            )

    @staticmethod
    def sustain_pedal_staff_padding(n=None, context='Staff', selector=None):
        r'''Overrides sustain pedal staff padding on leaves.

        ..  container:: example

            Overrides sustain pedal staff padding on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.sustain_pedal(
                ...         selector=baca.select_leaves_in_each_tuplet(leak=Right),
                ...         ),
                ...     baca.sustain_pedal_staff_padding(4),
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
                                \set Staff.pedalSustainStyle = #'bracket
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4
                                \override TupletBracket.staff-padding = #5
                                r8 \sustainOn
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \set Staff.pedalSustainStyle = #'bracket
                                fs''16 \sustainOff [ \sustainOn
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                            }
                            \times 4/5 {
                                \set Staff.pedalSustainStyle = #'bracket
                                a'16 \sustainOff \sustainOn
                                r4 \sustainOff
                                \revert Staff.SustainPedalLineSpanner.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides sustain pedal staff padding on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.sustain_pedal(
                ...         selector=baca.select_leaves_in_each_tuplet(),
                ...         ),
                ...     baca.sustain_pedal_staff_padding(
                ...         n=4,
                ...         selector=baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                \set Staff.pedalSustainStyle = #'bracket
                                \override TupletBracket.staff-padding = #5
                                r8 \sustainOn
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16 \sustainOff
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \set Staff.pedalSustainStyle = #'bracket
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4
                                fs''16 [ \sustainOn
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] \sustainOff
                                \revert Staff.SustainPedalLineSpanner.staff-padding
                            }
                            \times 4/5 {
                                \set Staff.pedalSustainStyle = #'bracket
                                a'16 \sustainOn
                                r4 \sustainOff
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='staff_padding',
            attribute_value=n,
            context_name=context,
            grob_name='sustain_pedal_line_spanner',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def tenuti(selector=None):
        r'''Attaches tenuti to pitched heads.

        ..  container:: example

            Attaches tenuti to all pitched heads:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.tenuti(),
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
                                c'16 -\tenuto [
                                d'16 -\tenuto ]
                                bf'4 -\tenuto ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\tenuto [
                                e''16 -\tenuto ]
                                ef''4 -\tenuto ~
                                ef''16
                                r16
                                af''16 -\tenuto [
                                g''16 -\tenuto ]
                            }
                            \times 4/5 {
                                a'16 -\tenuto
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches tenuti to pitched heads in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.tenuti(baca.select_plt_heads_in_tuplet(n=1)),
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
                                fs''16 -\tenuto [
                                e''16 -\tenuto ]
                                ef''4 -\tenuto ~
                                ef''16
                                r16
                                af''16 -\tenuto [
                                g''16 -\tenuto ]
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
        selector = selector or baca.select_plt_heads()
        return baca.AttachCommand(
            arguments=[abjad.Articulation('tenuto')],
            selector=selector,
            )

    @staticmethod
    def text_script_color(color='red', selector=None):
        r'''Overrides text script color on leaves.

        ..  container:: example

            Overrides text script color on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup('più mosso'),
                ...     baca.markup(
                ...         'lo stesso tempo',
                ...         baca.select_plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.text_script_color(color='red'),
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
                                \override TextScript.color = #red
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [ - \markup { "più mosso" }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ - \markup { "lo stesso tempo" }
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
                                \revert TextScript.color
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides text script color on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup('più mosso'),
                ...     baca.markup(
                ...         'lo stesso tempo',
                ...         baca.select_plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.text_script_color(
                ...         color='red',
                ...         selector=baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                c'16 [ - \markup { "più mosso" }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.color = #red
                                fs''16 [ - \markup { "lo stesso tempo" }
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert TextScript.color
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
            attribute_name='color',
            attribute_value=color,
            grob_name='text_script',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def text_script_padding(n=0, selector=None):
        r'''Overrides text script padding on leaves.

        ..  container:: example

            Overrides text script padding on all leaves:

            ::


                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup('più mosso'),
                ...     baca.markup(
                ...         'lo stesso tempo',
                ...         baca.select_plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.text_script_padding(n=4),
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
                                \override TextScript.padding = #4
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [ - \markup { "più mosso" }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ - \markup { "lo stesso tempo" }
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
                                \revert TextScript.padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides text script padding on leaves in tuplet 1:

            ::


                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup('più mosso'),
                ...     baca.markup(
                ...         'lo stesso tempo',
                ...         baca.select_plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.text_script_padding(
                ...         n=4,
                ...         selector=baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                c'16 [ - \markup { "più mosso" }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.padding = #4
                                fs''16 [ - \markup { "lo stesso tempo" }
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert TextScript.padding
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
            attribute_name='padding',
            attribute_value=n,
            grob_name='text_script',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def text_script_staff_padding(n=0, selector=None):
        r'''Overrides text script staff padding on leaves.

        ..  container:: example

            Overrides text script staff padding on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup('più mosso'),
                ...     baca.markup(
                ...         'lo stesso tempo',
                ...         baca.select_plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.text_script_staff_padding(n=4),
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
                                \override TextScript.staff-padding = #4
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [ - \markup { "più mosso" }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ - \markup { "lo stesso tempo" }
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
                                \revert TextScript.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides text script staff padding on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup('più mosso'),
                ...     baca.markup(
                ...         'lo stesso tempo',
                ...         baca.select_plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.text_script_staff_padding(
                ...         n=4,
                ...         selector=baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                c'16 [ - \markup { "più mosso" }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.staff-padding = #4
                                fs''16 [ - \markup { "lo stesso tempo" }
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert TextScript.staff-padding
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
            attribute_name='staff_padding',
            attribute_value=n,
            grob_name='text_script',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def text_scripts_down(selector=None):
        r'''Down-overrides text script on leaves.

        ..  container:: example

            Down-overrides text script direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup('più mosso'),
                ...     baca.markup(
                ...         'lo stesso tempo',
                ...         baca.select_plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.text_scripts_down(),
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
                                \override TextScript.direction = #down
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [ - \markup { "più mosso" }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ - \markup { "lo stesso tempo" }
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
                                \revert TextScript.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Down-overrides text script direction on leaves in tuplet 1:

            ::


                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup('più mosso'),
                ...     baca.markup(
                ...         'lo stesso tempo',
                ...         baca.select_plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.text_scripts_down(
                ...         selector=baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                c'16 [ - \markup { "più mosso" }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.direction = #down
                                fs''16 [ - \markup { "lo stesso tempo" }
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert TextScript.direction
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
            attribute_name='direction',
            attribute_value=Down,
            grob_name='text_script',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def text_scripts_up(selector=None):
        r'''Up-overrides text script direction on leaves.

        ..  container:: example

            Up-overrides text script direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup('più mosso'),
                ...     baca.markup(
                ...         'lo stesso tempo',
                ...         baca.select_plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.text_scripts_up(),
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
                                \override TextScript.direction = #up
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [ - \markup { "più mosso" }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ - \markup { "lo stesso tempo" }
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
                                \revert TextScript.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides text script direction on leaves in tuplet 1:

            ::


                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup('più mosso'),
                ...     baca.markup(
                ...         'lo stesso tempo',
                ...         baca.select_plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.text_scripts_up(
                ...         selector=baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                c'16 [ - \markup { "più mosso" }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.direction = #up
                                fs''16 [ - \markup { "lo stesso tempo" }
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert TextScript.direction
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
            attribute_name='direction',
            attribute_value=Up,
            grob_name='text_script',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def text_spanner_staff_padding(n=0, selector=None):
        r'''Overrides text spanner staff padding on trimmed leaves.

        ..  container:: example

            Overrides text spanner staff padding on all trimmed leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.text_spanner_staff_padding(6),
                ...     baca.text_script_staff_padding(6),
                ...     baca.transition_spanner(
                ...         baca.markup.pont(),
                ...         baca.markup.ord_(),
                ...         ),
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
                                \once \override TextSpanner.arrow-width = 0.25
                                \once \override TextSpanner.bound-details.left-broken.text = ##f
                                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                                \once \override TextSpanner.bound-details.left.text = \markup {
                                    \concat
                                        {
                                            \override
                                                #'(font-name . "Palatino")
                                                \whiteout
                                                    \upright
                                                        pont.
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                                \once \override TextSpanner.bound-details.right-broken.padding = 0
                                \once \override TextSpanner.bound-details.right.arrow = ##t
                                \once \override TextSpanner.bound-details.right.padding = 1.75
                                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                                \once \override TextSpanner.dash-fraction = 0.25
                                \once \override TextSpanner.dash-period = 1.5
                                \override TextSpanner.staff-padding = #6
                                \override TextScript.staff-padding = #6
                                \override TupletBracket.staff-padding = #5
                                r8 \startTextSpan
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
                                r4 \stopTextSpan ^ \markup {
                                    \override
                                        #'(font-name . "Palatino")
                                        \whiteout
                                            \upright
                                                ord.
                                    }
                                \revert TextSpanner.staff-padding
                                \revert TextScript.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides text spanner staff padding on trimmed leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.text_spanner_staff_padding(
                ...         n=6,
                ...         selector=baca.select_trimmed_run_in_tuplet(1),
                ...         ),
                ...     baca.text_script_staff_padding(6),
                ...     baca.transition_spanner(
                ...         baca.markup.pont(),
                ...         baca.markup.ord_(),
                ...         selector=baca.select_trimmed_run_in_tuplet(1),
                ...         ),
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
                                \override TextScript.staff-padding = #6
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
                                \once \override TextSpanner.arrow-width = 0.25
                                \once \override TextSpanner.bound-details.left-broken.text = ##f
                                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                                \once \override TextSpanner.bound-details.left.text = \markup {
                                    \concat
                                        {
                                            \override
                                                #'(font-name . "Palatino")
                                                \whiteout
                                                    \upright
                                                        pont.
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                                \once \override TextSpanner.bound-details.right-broken.padding = 0
                                \once \override TextSpanner.bound-details.right.arrow = ##t
                                \once \override TextSpanner.bound-details.right.padding = 1.75
                                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                                \once \override TextSpanner.dash-fraction = 0.25
                                \once \override TextSpanner.dash-period = 1.5
                                \override TextSpanner.staff-padding = #6
                                fs''16 [ \startTextSpan
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] \stopTextSpan ^ \markup {
                                    \override
                                        #'(font-name . "Palatino")
                                        \whiteout
                                            \upright
                                                ord.
                                    }
                                \revert TextSpanner.staff-padding
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TextScript.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='staff_padding',
            attribute_value=n,
            grob_name='text_spanner',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def tie_each(selector=None):
        r'''Ties each PLT p-run.

        ..  container:: example

            Ties all PLT p-runs:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
                ...     baca.tie_each(),
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
                                c'16 ~ [
                                c'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16 [
                                e''16 ~ ]
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

        ..  container:: example

            Ties PLT p-run 0:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
                ...     baca.tie_each(baca.select_plt_prun()),
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
                                c'16 ~ [
                                c'16 ]
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
        selector = selector or baca.select_each_plt_prun()
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.Tie(),
            )

    @staticmethod
    def tied_repeated_durations(durations):
        r'''Makes tied repeated durations.
        '''
        #specifier = make_repeated_duration_rhythm_specifier(durations)
        specifier = baca.repeated_durations(durations)
        specifier = abjad.new(
            specifier,
            rewrite_meter=False,
            rhythm_maker__tie_specifier__tie_across_divisions=True,
            )
        return specifier

    @staticmethod
    def ties_down(selector=None):
        r'''Overrides tie direction on leaves.

        ..  container:: example

            Overrides tie direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[11, 11, 12], [11, 11, 11], [11]],
                ...     baca.rests_around([2], [4]),
                ...     baca.stems_up(),
                ...     baca.tie_each(),
                ...     baca.ties_down(),
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
                                \override Stem.direction = #up
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override Tie.direction = #down
                                b'16 ~ [
                                b'16 ]
                                c''4 ~
                                c''16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                b'16 ~ [
                                b'16 ~ ]
                                b'4 ~
                                b'16
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert Tie.direction
                                r4
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides tie direction on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[11, 11, 12], [11, 11, 11], [11]],
                ...     baca.rests_around([2], [4]),
                ...     baca.stems_up(),
                ...     baca.tie_each(),
                ...     baca.ties_down(baca.select_leaves_in_tuplet(1)),
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
                                \override Stem.direction = #up
                                \override TupletBracket.staff-padding = #5
                                r8
                                b'16 ~ [
                                b'16 ]
                                c''4 ~
                                c''16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                \override Tie.direction = #down
                                b'16 ~ [
                                b'16 ~ ]
                                b'4 ~
                                b'16
                                r16
                                \revert Tie.direction
                            }
                            \times 4/5 {
                                b'16
                                r4
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        selector = selector or baca.select_leaves_in_trimmed_run()
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=Down,
            grob_name='tie',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def ties_up(selector=None):
        r'''Overrides tie direction on leaves.

        ..  container:: example

            Overrides tie direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[11, 11, 12], [11, 11, 11], [11]],
                ...     baca.rests_around([2], [4]),
                ...     baca.stems_down(),
                ...     baca.tie_each(),
                ...     baca.ties_up(),
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
                                \override Stem.direction = #down
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override Tie.direction = #up
                                b'16 ~ [
                                b'16 ]
                                c''4 ~
                                c''16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                b'16 ~ [
                                b'16 ~ ]
                                b'4 ~
                                b'16
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert Tie.direction
                                r4
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides tie direction on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[11, 11, 12], [11, 11, 11], [11]],
                ...     baca.rests_around([2], [4]),
                ...     baca.stems_down(),
                ...     baca.tie_each(),
                ...     baca.ties_up(baca.select_leaves_in_tuplet(1)),
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
                                \override Stem.direction = #down
                                \override TupletBracket.staff-padding = #5
                                r8
                                b'16 ~ [
                                b'16 ]
                                c''4 ~
                                c''16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                \override Tie.direction = #up
                                b'16 ~ [
                                b'16 ~ ]
                                b'4 ~
                                b'16
                                r16
                                \revert Tie.direction
                            }
                            \times 4/5 {
                                b'16
                                r4
                                \revert Stem.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        selector = selector or baca.select_leaves_in_trimmed_run()
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=Up,
            grob_name='tie',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def time_signature_extra_offset(pair=None, selector=None):
        r'''Overrides time signature extra offset on leaves.

        ..  container:: example

            Overrides time signature extra offset on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.time_signature_extra_offset((-6, 0)),
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
                                \override Score.TimeSignature.extra-offset = #'(-6 . 0)
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
                                \revert Score.TimeSignature.extra-offset
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        assert isinstance(pair, tuple), repr(pair)
        return baca.OverrideCommand(
            attribute_name='extra_offset',
            attribute_value=pair,
            context_name='score',
            grob_name='time_signature',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def transition_spanner(start_markup=None, stop_markup=None, selector=None):
        r'''Attaches transition spanner to trimmed leaves.

        ..  container:: example

            Attaches transition spanner to all trimmed leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.text_spanner_staff_padding(6),
                ...     baca.text_script_staff_padding(6),
                ...     baca.transition_spanner(
                ...         baca.markup.pont(),
                ...         baca.markup.ord_(),
                ...         ),
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
                                \once \override TextSpanner.arrow-width = 0.25
                                \once \override TextSpanner.bound-details.left-broken.text = ##f
                                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                                \once \override TextSpanner.bound-details.left.text = \markup {
                                    \concat
                                        {
                                            \override
                                                #'(font-name . "Palatino")
                                                \whiteout
                                                    \upright
                                                        pont.
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                                \once \override TextSpanner.bound-details.right-broken.padding = 0
                                \once \override TextSpanner.bound-details.right.arrow = ##t
                                \once \override TextSpanner.bound-details.right.padding = 1.75
                                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                                \once \override TextSpanner.dash-fraction = 0.25
                                \once \override TextSpanner.dash-period = 1.5
                                \override TextSpanner.staff-padding = #6
                                \override TextScript.staff-padding = #6
                                \override TupletBracket.staff-padding = #5
                                r8 \startTextSpan
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
                                r4 \stopTextSpan ^ \markup {
                                    \override
                                        #'(font-name . "Palatino")
                                        \whiteout
                                            \upright
                                                ord.
                                    }
                                \revert TextSpanner.staff-padding
                                \revert TextScript.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches transition spanner to trimmed leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.text_spanner_staff_padding(6),
                ...     baca.text_script_staff_padding(6),
                ...     baca.transition_spanner(
                ...         baca.markup.pont(),
                ...         baca.markup.ord_(),
                ...         selector=baca.select_trimmed_run_in_tuplet(1),
                ...         ),
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
                                \override TextSpanner.staff-padding = #6
                                \override TextScript.staff-padding = #6
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
                                \once \override TextSpanner.arrow-width = 0.25
                                \once \override TextSpanner.bound-details.left-broken.text = ##f
                                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                                \once \override TextSpanner.bound-details.left.text = \markup {
                                    \concat
                                        {
                                            \override
                                                #'(font-name . "Palatino")
                                                \whiteout
                                                    \upright
                                                        pont.
                                            \hspace
                                                #0.5
                                        }
                                    }
                                \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                                \once \override TextSpanner.bound-details.right-broken.padding = 0
                                \once \override TextSpanner.bound-details.right.arrow = ##t
                                \once \override TextSpanner.bound-details.right.padding = 1.75
                                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                                \once \override TextSpanner.dash-fraction = 0.25
                                \once \override TextSpanner.dash-period = 1.5
                                fs''16 [ \startTextSpan
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ] \stopTextSpan ^ \markup {
                                    \override
                                        #'(font-name . "Palatino")
                                        \whiteout
                                            \upright
                                                ord.
                                    }
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TextSpanner.staff-padding
                                \revert TextScript.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.TransitionCommand(
            selector=selector,
            start_markup=start_markup,
            stop_markup=stop_markup,
            )

    @staticmethod
    def transparent_bar_lines(selector=None):
        r'''Makes bar lines transparent.

        ..  container:: example

            Makes bar lines before leaf 0 transparent:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.transparent_bar_lines(),
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
                                \once \override Score.BarLine.transparent = ##t
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
                >>

        '''
        selector = selector or baca.select_leaf()
        return baca.OverrideCommand(
            attribute_name='transparent',
            attribute_value=True,
            context_name='Score',
            grob_name='bar_line',
            revert=False,
            selector=selector,
            )

    @staticmethod
    def transparent_rests(selector=None):
        r'''Makes rests transparent.

        ..  container:: example

            Makes all rests transparent:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.transparent_rests(),
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
                                \override Rest.transparent = ##t
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
                                \revert Rest.transparent
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Makes rests in tuplet 1 transparent:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.transparent_rests(
                ...         baca.select_rests_in_tuplet(1),
                ...         ),
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
                                \override Rest.transparent = ##t
                                r16
                                \revert Rest.transparent
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
        selector = selector or baca.select_rests()
        return baca.OverrideCommand(
            attribute_name='transparent',
            attribute_value=True,
            grob_name='rest',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def transparent_span_bars(selector=None):
        r'''Makes span bars transparent.

        ..  container:: example

            Makes span bar before leaf 0 transparent:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.transparent_span_bars(),
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
                                \once \override Score.SpanBar.transparent = ##t
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
                >>

        '''
        selector = selector or baca.select_leaf()
        return baca.OverrideCommand(
            attribute_name='transparent',
            attribute_value=True,
            context_name='Score',
            grob_name='span_bar',
            revert=False,
            selector=selector,
            )

    @staticmethod
    def transparent_time_signatures(selector=None):
        r'''Makes time signatures transparent.

        ..  container:: example

            Makes all time signatures transparent:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.transparent_time_signatures(),
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
                                \override GlobalContext.TimeSignature.transparent = ##t
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
                                \revert GlobalContext.TimeSignature.transparent
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        selector = selector or baca.select_rests()
        return baca.OverrideCommand(
            attribute_name='transparent',
            attribute_value=True,
            context_name='GlobalContext',
            grob_name='time_signature',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def transpose(n=0):
        r'''Transposes pitches.
        '''
        return baca.ScorePitchCommand(
            operators=[abjad.Transposition(n=n)],
            )

    @staticmethod
    def transpose_segments(n=0):
        r'''Transposes segments.
        '''
        operator = baca.pitch_class_segment().transpose(n=n)
        expression = baca.sequence().map(operator)
        return baca.MusicPitchSpecifier(
            expressions=[expression],
            to_pitch_classes=True,
            )

    @staticmethod
    def tremolo_down(n, maximum_adjustment=-1.5):
        r'''Overrides stem tremolo extra offset on leaves.
        '''
        pair = (0, -n)
        return baca.OverrideCommand(
            attribute_name='extra_offset',
            attribute_value=str(pair),
            grob_name='stem_tremolo',
            maximum_written_duration=abjad.Duration(1),
            maximum_settings={
                'grob_name': 'stem_tremolo',
                'attribute_name': 'extra_offset',
                'attribute_value': str((0, maximum_adjustment)),
                },
            )

    @staticmethod
    def trill_quarter_notes(selector=None):
        r'''Trills quarter notes.

        ..  container:: example

            Trills all quarter notes:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.trill_quarter_notes(),
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
                                bf'4 ~ \startTrillSpan
                                bf'16
                                r16 \stopTrillSpan
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~ \startTrillSpan
                                ef''16
                                r16 \stopTrillSpan
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

            Trills quarter notes in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.trill_quarter_notes(
                ...         baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                ef''4 ~ \startTrillSpan
                                ef''16
                                r16 \stopTrillSpan
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
        return baca.TrillCommand(
            forbidden_annotations=['color fingering', 'color microtone'],
            minimum_written_duration=abjad.Duration(1, 4),
            selector=selector,
            )

    @staticmethod
    def tuplet_bracket_extra_offset(pair=None, selector=None):
        r'''Overrides tuplet bracket extra offset on leaves.

        ..  container:: example

            Overrides tuplet bracket extra offset on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_extra_offset((-1, 0)),
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
                                \override TupletBracket.extra-offset = #'(-1 . 0)
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
                                \revert TupletBracket.extra-offset
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides tuplet bracket extra offset on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_extra_offset(
                ...         (-1, 0),
                ...         baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                \override TupletBracket.extra-offset = #'(-1 . 0)
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert TupletBracket.extra-offset
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
            grob_name='tuplet_bracket',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def tuplet_bracket_staff_padding(n=None, selector=None):
        r'''Overrides tuplet bracket staff padding on leaves.

        ..  container:: example

            Overrides tuplet bracket staff padding on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
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
                >>

        ..  container:: example

            Overrides tuplet bracket staff padding on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(
                ...         n=5,
                ...         selector=baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert TupletBracket.staff-padding
                            }
                            \times 4/5 {
                                a'16
                                r4
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='staff_padding',
            attribute_value=n,
            grob_name='tuplet_bracket',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def tuplet_brackets_down(selector=None):
        r'''Overrides tuplet bracket direction on leaves.

        ..  container:: example

            Overrides tuplet bracket direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     baca.tuplet_brackets_down(),
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
                                \override TupletBracket.direction = #down
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
                                \revert TupletBracket.direction
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides tuplet bracket direction on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     baca.tuplet_brackets_down(
                ...         baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                \override TupletBracket.direction = #down
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert TupletBracket.direction
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
            attribute_name='direction',
            attribute_value=Down,
            grob_name='tuplet_bracket',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def tuplet_brackets_up(selector=None):
        r'''Overrides tuplet bracket direction on leaves.

        ..  container:: example

            Override tuplet bracket direction on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     baca.tuplet_brackets_up(),
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
                                \override TupletBracket.direction = #up
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
                                \revert TupletBracket.direction
                            }
                        }
                    }
                >>

        ..  container:: example

            Override tuplet bracket direction on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     baca.tuplet_brackets_up(
                ...         baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                \override TupletBracket.direction = #up
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert TupletBracket.direction
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
            attribute_name='direction',
            attribute_value=Up,
            grob_name='tuplet_bracket',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def tuplet_number_extra_offset(pair=None, selector=None):
        r'''Overrides tuplet number extra offset on leaves.

        ..  container:: example

            Overrides tuplet number extra offset on all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     baca.tuplet_number_extra_offset((-1, 0)),
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
                                \override TupletNumber.extra-offset = #'(-1 . 0)
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
                                \revert TupletNumber.extra-offset
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides tuplet number extra offset on leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     baca.tuplet_number_extra_offset(
                ...         (-1, 0),
                ...         baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                \override TupletNumber.extra-offset = #'(-1 . 0)
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                                \revert TupletNumber.extra-offset
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
            grob_name='tuplet_number',
            revert=True,
            selector=selector,
            )

    @staticmethod
    def two_line_staff(selector=None):
        r'''Attaches two-line staff spanner to leaves.

        ..  container:: example

            Attaches two-line percussion staff spanner to all leaves:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.percussion_staff(),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(9),
                ...     baca.two_line_staff(),
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
                                \once \override Staff.StaffSymbol.line-count = 2
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

            Attaches two-line percussion staff spanner to leaves in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.percussion_staff(
                ...         baca.select_leaves_in_tuplet(1),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(9),
                ...     baca.two_line_staff(
                ...         baca.select_leaves_in_tuplet(1),
                ...         ),
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
                                \once \override Staff.StaffSymbol.line-count = 2
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
            spanner=abjad.StaffLinesSpanner(lines=2),
            )

    @staticmethod
    def up_arpeggios(selector=None):
        r"""Attaches up-arpeggios to chord heads.

        ..  container:: example

            Attaches up-arpeggios to all chord heads:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.up_arpeggios(),
                ...     counts=[5, -3],
                ...     talea_denominator=32,
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \arpeggioArrowUp
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
                                \arpeggioArrowUp
                                <ef'' e'' fs'''>8 \arpeggio ~ [
                                <ef'' e'' fs'''>32 ]
                                r16.
                            }
                            {
                                \arpeggioArrowUp
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

            Attaches up-arpeggios to last two chord heads:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
                ...     baca.up_arpeggios(
                ...         baca.select_chord_heads(start=-2),
                ...         ),
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
                                \arpeggioArrowUp
                                <ef'' e'' fs'''>8 \arpeggio ~ [
                                <ef'' e'' fs'''>32 ]
                                r16.
                            }
                            {
                                \arpeggioArrowUp
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
        selector = selector or baca.select_chord_heads()
        return baca.AttachCommand(
            arguments=[abjad.Arpeggio(direction=Up)],
            selector=selector,
            )

    @staticmethod
    def up_bows(selector=None):
        r'''Attaches up-bows to pitched heads.

        ..  container:: example

            Attaches up-bows to all pitched heads:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     baca.up_bows(),
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
                                c'16 -\upbow [
                                d'16 -\upbow ]
                                bf'4 -\upbow ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 -\upbow [
                                e''16 -\upbow ]
                                ef''4 -\upbow ~
                                ef''16
                                r16
                                af''16 -\upbow [
                                g''16 -\upbow ]
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

            Attaches up-bows to pitched heads in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     baca.up_bows(
                ...         baca.select_plt_heads_in_tuplet(1),
                ...         ),
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
                                fs''16 -\upbow [
                                e''16 -\upbow ]
                                ef''4 -\upbow ~
                                ef''16
                                r16
                                af''16 -\upbow [
                                g''16 -\upbow ]
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
        selector = selector or baca.select_plt_heads()
        return baca.AttachCommand(
            arguments=[abjad.Articulation('upbow')],
            selector=selector,
            )

    @staticmethod
    def very_long_fermata(selector=None):
        r'''Attaches very long fermata to leaf.

        ..  container:: example

            Attaches very long fermata to first leaf:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.very_long_fermata(),
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
                                r8 -\verylongfermata
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

            Attaches very long fermata to first leaf in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.very_long_fermata(
                ...         baca.select_plt_head_in_tuplet(1, 0),
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
                                fs''16 -\verylongfermata [
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
        selector = selector or baca.select_leaf(n=0)
        return baca.AttachCommand(
            arguments=[abjad.Articulation('verylongfermata')],
            selector=selector,
            )
