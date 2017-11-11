import abjad
import baca
import collections
from abjad import rhythmmakertools as rhythmos


class LibraryNS(abjad.AbjadObject):
    r'''Library N - S.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(1) Library'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def natural_clusters(widths, selector='baca.plts()', start_pitch=None):
        r'''Makes natural clusters.
        '''
        return baca.ClusterCommand(
            hide_flat_markup=True,
            selector=selector,
            start_pitch=start_pitch,
            widths=widths,
            )

    @staticmethod
    def natural_harmonics(selector='baca.tleaves()'):
        r'''Overrides note-head style on PLTs.

        ..  container:: example

            Overrides note-head style on all PLTs:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            Overrides note-head style on PLTs in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.natural_harmonics(
            ...         baca.tuplets()[1:2].plts().group(),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.OverrideCommand(
            attribute_name='style',
            attribute_value='harmonic',
            grob_name='note_head',
            selector=selector,
            )

    @staticmethod
    def nest(time_treatments=None):
        r'''Nests music.

        ..  container:: example

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.NestBuilder(
            lmr_specifier=None,
            time_treatments=time_treatments,
            )

    @staticmethod
    def ottava(selector='baca.tleaves()'):
        r'''Attaches ottava spanner to trimmed leaves.

        ..  container:: example

            Attaches ottava spanner to trimmed leaves:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

        '''
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.OctavationSpanner(start=1, stop=0),
            )

    @staticmethod
    def ottava_bassa(selector='baca.tleaves()'):
        r'''Attaches ottava bassa spanner to trimmed leaves.

        ..  container:: example

            Attaches ottava bassa spanner to trimmed leaves:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

        '''
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.OctavationSpanner(start=-1, stop=0),
            )

    @staticmethod
    def page_break(selector='baca.leaf(-1)'):
        r'''Attaches page break command after last leaf.

        ..  container:: example

            Attaches page break after last leaf:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.page_break(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
                                \pageBreak
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.IndicatorCommand(
            indicators=[abjad.PageBreak()],
            selector=selector,
            )

    @staticmethod
    def piecewise(spanner, indicators, selector, bookend=False, preamble=None):
        r'''Makes piecewise command from `spanner` command, `indicators` and
        indicator `selector`.
        '''
        return baca.PiecewiseCommand(
            bookend=bookend,
            indicators=indicators,
            preamble=preamble,
            selector=selector,
            spanner=spanner,
            )

    @staticmethod
    def pitches(pitches, exact=None, repeats=None):
        r'''Sets pitches.
        '''
        if bool(exact):
            cyclic = False
        else:
            cyclic = True
        return baca.PitchCommand(
            allow_repeat_pitches=repeats,
            cyclic=cyclic,
            pitches=pitches,
            )

    @staticmethod
    def possibile_dynamic(
        dynamic,
        selector='baca.phead(0)',
        direction=abjad.Down,
        ):
        r'''Attaches possibile dynamic to pitched head 0.

        ..  container:: example

            Attaches possibilie dynamic to pitched head 0:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.possibile_dynamic(
            ...         'ff',
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.IndicatorCommand(
            indicators=[markup],
            selector=selector,
            )

    @staticmethod
    def proportional_notation_duration(duration, selector='baca.leaf(0)'):
        r'''Sets proportional notation duration.

        ..  container:: example

            Sets proportional notation duration on leaf 0:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.SettingCommand(
            context_name='Score',
            selector=selector,
            setting_name='proportional_notation_duration',
            setting_value=moment,
            )

    @staticmethod
    def register(start, stop=None, selector='baca.plts()'):
        r'''Octave-transposes PLTs.

        ..  container:: example

            Octave-transposes all PLTs to the octave rooted at -6:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            Octave-transposes PLTs in tuplet 1 to the octave rooted at -6:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.color(baca.tuplet(1)),
            ...     baca.register(-6, selector=baca.tuplet(1)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                fs16 [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                e'16 ]
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                ef'4 ~
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                ef'16
                                \once \override Dots.color = #green
                                \once \override Rest.color = #green
                                r16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                af16 [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
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

            Octave-transposes all PLTs to an octave interpolated from -6 to 18:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.register(-6, 18),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
                                fs'16 [
                                e'16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                            }
                            \times 4/5 {
                                a''16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

            Octave-transposes PLTs in tuplet 1 to an octave interpolated from
            -6 to 18:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.color(baca.tuplet(1)),
            ...     baca.register(-6, 18, baca.tuplet(1)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                fs16 [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                e'16 ]
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                ef'4 ~
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                ef'16
                                \once \override Dots.color = #green
                                \once \override Rest.color = #green
                                r16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                af'16 [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
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
        if stop is None:
            return baca.RegisterCommand(
                registration=baca.Registration([('[A0, C8]', start)]),
                selector=selector,
                )
        return baca.RegisterInterpolationCommand(
            selector=selector,
            start_pitch=start,
            stop_pitch=stop,
            )

    @staticmethod
    def reiterated_dynamic(dynamic, selector='baca.pheads()'):
        r'''Attaches `dynamic` to pitched heads.

        ..  container:: example

            Attaches dynamic to all pitched heads:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.reiterated_dynamic(
            ...         'f',
            ...         selector=baca.tuplets()[1:2].pheads(),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation(dynamic)],
            selector=selector,
            )

    @staticmethod
    def repeat_ties_down(selector='baca.tleaves()'):
        r'''Overrides repeat tie direction.

        ..  container:: example

            Overrides repeat tie direction on pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.map(baca.tie(repeat=True), baca.qruns()),
            ...     baca.repeat_ties_down(),
            ...     baca.rests_around([2], [4]),
            ...     baca.stems_up(),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override RepeatTie.direction = #down
                                \override Stem.direction = #up
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
                                \revert Stem.direction
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides repeat tie direction on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.map(baca.tie(repeat=True), baca.qruns()),
            ...     baca.repeat_ties_down(
            ...         baca.tuplets()[1:2].pleaves().group()
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.stems_up(),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override Stem.direction = #up
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
                                \revert RepeatTie.direction
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert Stem.direction
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=abjad.Down,
            grob_name='repeat_tie',
            selector=selector,
            )

    @staticmethod
    def repeat_ties_up(selector='baca.tleaves()'):
        r'''Overrides repeat tie direction on leaves.

        ..  container:: example

            Overrides repeat tie direction on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.map(baca.tie(repeat=True), baca.qruns()),
            ...     baca.repeat_ties_up(),
            ...     baca.rests_around([2], [4]),
            ...     baca.stems_down(),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override RepeatTie.direction = #up
                                \override Stem.direction = #down
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
                                \revert Stem.direction
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides repeat tie direction on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.map(baca.tie(repeat=True), baca.qruns()),
            ...     baca.repeat_ties_up(
            ...         baca.tuplets()[1:2].pleaves().group()
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.stems_down(),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override Stem.direction = #down
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
                                \revert RepeatTie.direction
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert Stem.direction
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
            grob_name='repeat_tie',
            selector=selector,
            )

    @staticmethod
    def rest_position(n, selector='baca.rests()'):
        r'''Overrides position of rests.

        ..  container:: example

            Overrides position of all rests:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rest_position(
            ...         -6,
            ...         baca.tuplets()[1:2].rests().group(),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
                                \once \override Rest.staff-position = #-6
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
            attribute_name='staff_position',
            attribute_value=n,
            grob_name='rest',
            selector=selector,
            )

    @staticmethod
    def rests_after(counts):
        r'''Makes rests after music.

        ..  container:: example

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.RestAffixSpecifier(
            suffix=counts,
            )

    @staticmethod
    def rests_around(prefix, suffix):
        r'''Makes rests around music.

        ..  container:: example

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.RestAffixSpecifier(
            prefix=prefix,
            suffix=suffix,
            )

    @staticmethod
    def rests_before(counts):
        r'''Makes rests before music.

        ..  container:: example

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.RestAffixSpecifier(
            prefix=counts,
            )

    @staticmethod
    def rests_down(selector='baca.rests()'):
        r'''Overrides direction of rests.

        ..  container:: example

            Down-overrides direction of rests:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            Down-overrides direction of rests in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_down(
            ...         baca.tuplets()[1:2].rests().group(),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
                                \once \override Rest.direction = #down
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
            attribute_name='direction',
            attribute_value=abjad.Down,
            grob_name='rest',
            selector=selector,
            )

    @staticmethod
    def rests_up(selector='baca.rests()'):
        r'''Up-overrides direction of rests.

        ..  container:: example

            Up-overrides direction of rests:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_up(baca.tuplets()[1:2].rests().group()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
                                \once \override Rest.direction = #up
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
            attribute_name='direction',
            attribute_value=abjad.Up,
            grob_name='rest',
            selector=selector,
            )

    @staticmethod
    def resume():
        r'''Resumes music at next offset across all voices in score.
        '''
        return baca.AnchorSpecifier()

    @staticmethod
    def resume_after(remote_voice_name):
        r'''Resumes music after remote selection.
        '''
        return baca.AnchorSpecifier(
            remote_selector=baca.leaf(-1),
            remote_voice_name=remote_voice_name,
            use_remote_stop_offset=True,
            )

    @staticmethod
    def scope(voice, start, stop=None):
        r'''Scopes `voice` from `start` to `stop`.

        Returns simple scope.
        '''
        assert isinstance(start, int), repr(start)
        if stop is None:
            stages = baca.StageSpecifier(start, start)
        else:
            stages = baca.StageSpecifier(start, stop)
        return baca.Scope(
            voice_name=voice,
            stages=stages,
            )

    @staticmethod
    def scopes(*arguments):
        r'''Makes scopes from `arguments`.

        Returns list of scopes.
        '''
        scopes = []
        for argument in arguments:
            scope = baca.Scope(*argument)
            scopes.append(scope)
        return scopes

    @staticmethod
    def script_color(color='red', selector='baca.leaves()'):
        r'''Overrides script color.

        ..  container:: example

            Overrides script color on all leaves:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accents(),
            ...     baca.rests_around([2], [4]),
            ...     baca.script_color(
            ...         'red',
            ...         baca.tuplets()[1:2].leaves().group(),
            ...         ),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.OverrideCommand(
            attribute_name='color',
            attribute_value=color,
            grob_name='script',
            selector=selector,
            )

    @staticmethod
    def script_extra_offset(pair, selector='baca.leaf(0)'):
        r'''Overrides script extra offset.

        ..  container:: example

            Overrides script extra offset on leaf 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accents(),
            ...     baca.rests_around([2], [4]),
            ...     baca.script_extra_offset((-1.5, 0), baca.leaf(1)),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Script.extra-offset = #'(-1.5 . 0)
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accents(),
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.script_extra_offset((-1.5, 0), baca.leaf(0)),
            ...         baca.tuplet(1),
            ...         ),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
                                \once \override Script.extra-offset = #'(-1.5 . 0)
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

        '''
        return baca.OverrideCommand(
            attribute_name='extra_offset',
            attribute_value=pair,
            grob_name='script',
            selector=selector,
            )

    @staticmethod
    def scripts_down(selector='baca.leaves()'):
        r'''Down-overrides script direction on leaves.

        ..  container:: example

            Down-overrides script direction on all leaves:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accents(),
            ...     baca.rests_around([2], [4]),
            ...     baca.scripts_down(
            ...         baca.tuplets()[1:2].leaves().group(),
            ...         ),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
            attribute_value=abjad.Down,
            grob_name='script',
            selector=selector,
            )

    @staticmethod
    def scripts_up(selector='baca.leaves()'):
        r'''Up-overrides script direction.

        ..  container:: example

            Up-overrides script direction on all leaves:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accents(),
            ...     baca.rests_around([2], [4]),
            ...     baca.scripts_up(
            ...         baca.tuplets()[1:2].leaves().group(),
            ...         ),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
            attribute_value=abjad.Up,
            grob_name='script',
            selector=selector,
            )

    @staticmethod
    def short_fermata(selector='baca.leaf(0)'):
        r'''Attaches short fermata to leaf.

        ..  container:: example

            Attaches short fermata to first leaf:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.short_fermata(
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('shortfermata')],
            selector=selector,
            )

    def single_segment_transition(
        start=None,
        stop=None,
        selector='baca.tleaves().group()'
        ):
        r'''Makes single-segment transition spanner.

        ..  container:: example

            Attaches transition spanner to trimmed leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.text_spanner_staff_padding(6),
            ...     baca.text_script_staff_padding(6),
            ...     baca.single_segment_transition(
            ...         baca.markup.pont(),
            ...         baca.markup.ord(),
            ...         baca.tleaves().group(),
            ...         ),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
                                \once \override TextSpanner.arrow-width = 0.25
                                \once \override TextSpanner.bound-details.left-broken.text = ##f
                                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                                \once \override TextSpanner.bound-details.left.text = \markup {
                                    \concat
                                        {
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
                                c'16 [ \startTextSpan
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
                                a'16 \stopTextSpan ^ \markup {
                                    \whiteout
                                        \upright
                                            ord.
                                    }
                                r4
                                \revert TextSpanner.staff-padding
                                \revert TextScript.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches transition spanner to trimmed leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.text_spanner_staff_padding(6),
            ...     baca.text_script_staff_padding(6),
            ...     baca.single_segment_transition(
            ...         baca.markup.pont(),
            ...         baca.markup.ord(),
            ...         baca.tuplet_tleaves()[1:2],
            ...         ),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

        Returns piecewise command.
        '''
        indicators = []
        if start is not None:
            indicators.append((start, baca.dashed_arrow()))
        else:
            indicators.append((None, baca.dashed_arrow()))
        if stop is not None:
            indicators.append(stop)
        return baca.piecewise(
            abjad.TextSpanner(),
            indicators,
            selector,
            bookend=True,
            preamble=selector,
            )

    @staticmethod
    def skips_after(counts):
        r'''Makes skips after music.

        ..  container:: example

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.RestAffixSpecifier(
            skips_instead_of_rests=True,
            suffix=counts,
            )

    @staticmethod
    def skips_around(prefix, suffix):
        r'''Makes skips around music.

        ..  container:: example

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.RestAffixSpecifier(
            prefix=prefix,
            skips_instead_of_rests=True,
            suffix=suffix,
            )

    @staticmethod
    def skips_before(counts):
        r'''Makes skips before music.

        ..  container:: example

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.RestAffixSpecifier(
            prefix=counts,
            skips_instead_of_rests=True,
            )

    @staticmethod
    def slur(selector='baca.tleaves()'):
        r'''Slurs trimmed leaves.

        ..  container:: example

            Slurs trimmed leaves:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            Attaches slur to trimmed leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.slur(), baca.tuplet(1)),
            ...     baca.slurs_down(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
            selector=selector,
            spanner=abjad.Slur(),
            )

    @staticmethod
    def slurs_down(selector='baca.leaves()'):
        r'''Overrides slur direction.

        ..  container:: example

            Overrides slur direction for leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.slur(),
            ...         baca.tuplet_tleaves().nontrivial(),
            ...         ),
            ...     baca.slurs_down(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.slur(),
            ...         baca.tuplet_tleaves().nontrivial(),
            ...         ),
            ...     baca.slurs_down(
            ...         baca.tuplets()[1:2].leaves().group(),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
            attribute_value=abjad.Down,
            grob_name='slur',
            selector=selector,
            )

    @staticmethod
    def slurs_up(selector='baca.leaves()'):
        r'''Overrides slur direction.

        ..  container:: example

            Up-overrides slur direction for leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.slur(),
            ...         baca.tuplet_tleaves().nontrivial(),
            ...         ),
            ...     baca.slurs_up(),
            ...     baca.stems_down(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     baca.tuplet_brackets_down(),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override Slur.direction = #up
                                \override TupletBracket.staff-padding = #5
                                \override TupletBracket.direction = #down
                                r8
                                \override Stem.direction = #down
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
                                \revert Stem.direction
                                r4
                                \revert Slur.direction
                                \revert TupletBracket.staff-padding
                                \revert TupletBracket.direction
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides slur direction for leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.slur(),
            ...         baca.tuplet_tleaves().nontrivial(),
            ...         ),
            ...     baca.slurs_up(
            ...         baca.tuplets()[1:2].leaves().group(),
            ...         ),
            ...     baca.stems_down(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     baca.tuplet_brackets_down(),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                \override TupletBracket.direction = #down
                                r8
                                \override Stem.direction = #down
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
                                \revert Stem.direction
                                r4
                                \revert TupletBracket.staff-padding
                                \revert TupletBracket.direction
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=abjad.Up,
            grob_name='slur',
            selector=selector,
            )

    @staticmethod
    def soprano_to_octave(n, selector='baca.plts()'):
        r"""Octave-transposes music.

        ..  container:: example

            Octave-transposes music such that the highest note in the
            collection of all PLTs appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.color(baca.plts().group()),
            ...     baca.soprano_to_octave(3),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
                                <c,, d,, bf,,>8 ~ [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <c,, d,, bf,,>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f,8 ~ [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f,32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <ef, e, fs>8 ~ [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <ef, e, fs>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <g,, af,>8 ~ [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <g,, af,>32 ]
                                r16.
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a,,8 ~ [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a,,32 ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music that such that the highest note in each
            pitched logical tie appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.map(baca.soprano_to_octave(3), baca.plts()),
            ...     baca.color(baca.plts()),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            Octave-transposes music that such that the highest note in each
            of the last two PLTs appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.map(baca.soprano_to_octave(3), baca.plts()[-2:]),
            ...     baca.color(baca.plts()[-2:]),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
            anchor=abjad.Top,
            octave_number=n,
            selector=selector,
            )

    @staticmethod
    def split_by_durations(durations):
        r'''Splits divisions by `durations`.

        ..  container:: example

            >>> expression = baca.split_by_durations([(3, 8)])

            >>> for item in expression([(2, 8), (2, 8)]):
            ...     item
            ...
            Division((3, 8))
            Division((1, 8))

            >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
            ...     item
            ...
            Division((3, 8))
            Division((3, 8))

            >>> for item in expression([(2, 8), (2, 8), (2, 8), (2, 8)]):
            ...     item
            ...
            Division((3, 8))
            Division((3, 8))
            Division((2, 8))

        '''
        expression = baca.DivisionSequenceExpression()
        expression = expression.division_sequence()
        expression = expression.flatten(depth=-1)
        expression = expression.sum()
        expression = expression.division_sequence()
        expression = expression.split_by_durations(
            cyclic=True,
            durations=durations,
            )
        expression = expression.flatten(depth=-1)
        return expression

    @staticmethod
    def staccati(selector='baca.pheads()'):
        r'''Attaches staccati to pitched heads.

        ..  container:: example

            Attaches staccati to all pitched heads:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.staccati(baca.tuplets()[1:2].pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('staccato')],
            selector=selector,
            )

    @staticmethod
    def staccatissimi(selector='baca.pheads()'):
        r'''Attaches staccatissimi to pitched heads.

        ..  container:: example

            Attaches staccatissimi to all pitched heads:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.staccatissimi(baca.tuplets()[1:2].pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
                                ef''16
                                r16
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
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('staccatissimo')],
            selector=selector,
            )

    @staticmethod
    def staff_lines(n, selector='baca.leaf(0)'):
        r'''Makes staff lines.

        Returns indicator command.
        '''
        return baca.IndicatorCommand(
            indicators=[baca.StaffLines(line_count=n)],
            selector=selector,
            )

    @staticmethod
    def staff_positions(numbers, repeats=None, selector='baca.plts()'):
        r'''Makes staff position command.
        '''
        if repeats is None and len(numbers) == 1:
            repeats = True
        return baca.StaffPositionCommand(
            numbers=numbers,
            repeats=repeats,
            selector=selector,
            ) 

    @staticmethod
    def stem_color(color='red', context_name=None, selector='baca.tleaves()'):
        r'''Overrides stem color.

        ..  container:: example

            Overrides stem color on pitched leaves:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            Overrides stem color on pitched leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.stem_color(
            ...         color='red',
            ...         selector=baca.tuplets()[1:2].pleaves().group(),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.OverrideCommand(
            attribute_name='color',
            attribute_value=color,
            context_name=context_name,
            grob_name='stem',
            selector=selector,
            )

    @staticmethod
    def stem_tremolo(selector='baca.pleaves()', tremolo_flags=32):
        r'''Attaches stem tremolo.

        ..  container:: example

            Attaches stem tremolo to pitched leaves:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.stem_tremolo(), baca.tuplet(1)),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.IndicatorCommand(
            indicators=[abjad.StemTremolo(tremolo_flags=tremolo_flags)],
            selector=selector,
            )

    @staticmethod
    def stems_down(selector='baca.tleaves()'):
        r'''Down-overrides stem direction.

        ..  container:: example

            Down-overrides stem direction pitched leaves:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override Stem.direction = #down
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
                                \revert Stem.direction
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Down-overrides stem direction for leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.stems_down(
            ...         baca.tuplets()[1:2].leaves().group(),
            ...         ),
            ...     baca.stems_up(),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override Stem.direction = #up
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
                                \revert Stem.direction
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        return baca.OverrideCommand(
            attribute_name='direction',
            attribute_value=abjad.Down,
            grob_name='stem',
            selector=selector,
            )

    @staticmethod
    def stems_up(selector='baca.tleaves()'):
        r'''Up-overrides stem direction.

        ..  container:: example

            Up-overrides stem direction on pitched leaves:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override Stem.direction = #up
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
                                \revert Stem.direction
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides stem direction on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [10]],
            ...     baca.rests_around([2], [4]),
            ...     baca.stems_down(),
            ...     baca.stems_up(baca.tuplets()[1:2].leaves().group()),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 2" {
                        \voiceTwo
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \override Stem.direction = #down
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
                                \revert Stem.direction
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
            grob_name='stem',
            selector=selector,
            )

    @staticmethod
    def strict_note_spacing_off(selector='baca.leaves()'):
        r'''Turns strict note spacing off.

        ..  container:: example

            Turns strict note spacing off on leaves:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
            context_name='Score',
            grob_name='spacing_spanner',
            selector=selector,
            )

    @staticmethod
    def strict_quarter_divisions():
        r'''Makes strict quarter divisions.

        ..  container:: example

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
        expression = expression.flatten(depth=-1)
        return expression

    @staticmethod
    def suite(commands, selector=None):
        r'''Makes suite.
        '''
        prototype = (baca.Command, collections.Iterable)
        if not isinstance(commands, prototype):
            raise Exception(f'must be command(s):\n\n{commands}')
        if not isinstance(selector, (abjad.Expression, type(None))):
            raise Exception(f'must be selector or none:\n\n{selector}')
        return baca.SuiteCommand(commands=commands, selector=selector)

    @staticmethod
    def sustain_pedal(selector='baca.leaves()'):
        r'''Pedals leaves.

        ..  container:: example

            Pedals leaves:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.sustain_pedal(), baca.tuplet(1)),
            ...     baca.sustain_pedal_staff_padding(4),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.sustain_pedal(baca.lleaves()),
            ...         baca.tuplet(1),
            ...         ),
            ...     baca.sustain_pedal_staff_padding(4),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.sustain_pedal(baca.rleaves()),
            ...         baca.tuplet(1),
            ...         ),
            ...     baca.sustain_pedal_staff_padding(4),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            Pedals leaves in tuplet 1 (leaked wide):

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.sustain_pedal(baca.wleaves()),
            ...         baca.tuplet(1),
            ...         ),
            ...     baca.sustain_pedal_staff_padding(4),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.sustain_pedal(), baca.tuplets()),
            ...     baca.sustain_pedal_staff_padding(4),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.sustain_pedal(baca.lleaves()),
            ...         baca.tuplets(),
            ...         ),
            ...     baca.sustain_pedal_staff_padding(4),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.sustain_pedal(baca.rleaves()),
            ...         baca.tuplets(),
            ...         ),
            ...     baca.sustain_pedal_staff_padding(4),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
            spanner=abjad.PianoPedalSpanner(style='bracket'),
            )

    @staticmethod
    def sustain_pedal_staff_padding(
        n,
        context='Staff',
        selector='baca.leaves()',
        ):
        r'''Overrides sustain pedal staff padding.

        ..  container:: example

            Overrides sustain pedal staff padding on leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.sustain_pedal(baca.rleaves()),
            ...         baca.tuplets(),
            ...         ),
            ...     baca.sustain_pedal_staff_padding(4),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.sustain_pedal(), baca.tuplets()),
            ...     baca.sustain_pedal_staff_padding(
            ...         n=4,
            ...         selector=baca.tuplets()[1:2].leaves().group(),
            ...         ),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
            selector=selector,
            )
