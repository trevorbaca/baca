import abjad
import baca
import collections
from abjad import rhythmmakertools as rhythmos


class LibraryTZ(abjad.AbjadObject):
    r'''Library T - Z.

    >>> from abjad import rhythmmakertools as rhythmos

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(1) Library'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def tenuti(selector='baca.pheads()'):
        r'''Attaches tenuti to pitched heads.

        ..  container:: example

            Attaches tenuti to all pitched heads:

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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.tenuti(baca.tuplets()[1:2].pheads()),
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
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('tenuto')],
            selector=selector,
            )

    @staticmethod
    def text_script_color(color='red', selector='baca.leaves()'):
        r'''Overrides text script color.

        ..  container:: example

            Overrides text script color on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.markup('più mosso'),
            ...     baca.markup(
            ...         'lo stesso tempo',
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.text_script_color('red'),
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
                                \override TextScript.color = #red
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "più mosso"
                                        }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "lo stesso tempo"
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
                                \revert TextScript.color
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides text script color on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.markup('più mosso'),
            ...     baca.markup(
            ...         'lo stesso tempo',
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.text_script_color('red'), baca.tuplet(1)),
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
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "più mosso"
                                        }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.color = #red
                                fs''16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "lo stesso tempo"
                                        }
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
            attribute='color',
            value=color,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_script_padding(n, selector='baca.leaves()'):
        r'''Overrides text script padding.

        ..  container:: example

            Overrides text script padding on leaves:


                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup('più mosso'),
                ...     baca.markup(
                ...         'lo stesso tempo',
                ...         baca.tuplets()[1:2].phead(0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.text_script_padding(4),
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
                                \override TextScript.padding = #4
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "più mosso"
                                        }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "lo stesso tempo"
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
                                \revert TextScript.padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides text script padding on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.markup('più mosso'),
            ...     baca.markup(
            ...         'lo stesso tempo',
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.text_script_padding(4), baca.tuplet(1)),
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
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "più mosso"
                                        }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.padding = #4
                                fs''16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "lo stesso tempo"
                                        }
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
            attribute='padding',
            value=n,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_script_staff_padding(n, selector='baca.leaves()'):
        r'''Overrides text script staff padding.

        ..  container:: example

            Overrides text script staff padding on leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.markup('più mosso'),
            ...     baca.markup(
            ...         'lo stesso tempo',
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.text_script_staff_padding(n=4),
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
                                \override TextScript.staff-padding = #4
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "più mosso"
                                        }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "lo stesso tempo"
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
                                \revert TextScript.staff-padding
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides text script staff padding on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.markup('più mosso'),
            ...     baca.markup(
            ...         'lo stesso tempo',
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.text_script_staff_padding(4),
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
                                c'16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "più mosso"
                                        }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.staff-padding = #4
                                fs''16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "lo stesso tempo"
                                        }
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
            attribute='staff_padding',
            value=n,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_scripts_down(selector='baca.leaves()'):
        r'''Down-overrides text script.

        ..  container:: example

            Down-overrides text script direction on leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.markup('più mosso'),
            ...     baca.markup(
            ...         'lo stesso tempo',
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.text_scripts_down(),
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
                                \override TextScript.direction = #down
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "più mosso"
                                        }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "lo stesso tempo"
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
                                \revert TextScript.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Down-overrides text script direction on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.markup('più mosso'),
            ...     baca.markup(
            ...         'lo stesso tempo',
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.text_scripts_down(), baca.tuplet(1)),
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
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "più mosso"
                                        }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.direction = #down
                                fs''16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "lo stesso tempo"
                                        }
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
            attribute='direction',
            value=abjad.Down,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_scripts_up(selector='baca.leaves()'):
        r'''Up-overrides text script direction.

        ..  container:: example

            Up-overrides text script direction on leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.markup('più mosso'),
            ...     baca.markup(
            ...         'lo stesso tempo',
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.text_scripts_up(),
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
                                \override TextScript.direction = #up
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "più mosso"
                                        }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "lo stesso tempo"
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
                                \revert TextScript.direction
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides text script direction on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.markup('più mosso'),
            ...     baca.markup(
            ...         'lo stesso tempo',
            ...         baca.tuplets()[1:2].phead(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.text_scripts_up(), baca.tuplet(1)),
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
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "più mosso"
                                        }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.direction = #up
                                fs''16 [
                                    ^ \markup {
                                        \whiteout
                                            \upright
                                                "lo stesso tempo"
                                        }
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
            attribute='direction',
            value=abjad.Up,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_spanner(selector='baca.leaves()'):
        r'''Makes text spanner.

        Returns spanner command.
        '''
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.TextSpanner(),
            )

    @staticmethod
    def text_spanner_staff_padding(n, selector='baca.leaves()'):
        r'''Overrides text spanner staff padding.

        ..  container:: example

            Overrides text spanner staff padding on all trimmed leaves:

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

            Overrides text spanner staff padding on trimmed leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.text_spanner_staff_padding(6),
            ...         baca.tuplet(1),
            ...         ),
            ...     baca.text_script_staff_padding(6),
            ...     baca.single_segment_transition(
            ...         baca.markup.pont(),
            ...         baca.markup.ord(),
            ...         baca.map(baca.tleaves(), baca.tuplet(1)),
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
                                \override TextSpanner.staff-padding = #6
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
            attribute='staff_padding',
            value=n,
            grob='text_spanner',
            selector=selector,
            )

    @staticmethod
    def tie(repeat=False, selector='baca.qrun(0)'):
        r'''Attaches tie to equipitch run 0.

        ..  container:: example

            Attaches ties to equipitch runs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.map(baca.tie(), baca.qruns()),
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

            Attaches tie to equipitch run 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.tie(),
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

        ..  container:: example

            Attaches repeat tie to each equipitch run:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.map(baca.tie(repeat=True), baca.qruns()),
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

        '''
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.Tie(repeat_ties=repeat),
            )

    @staticmethod
    def ties_down(selector='baca.tleaves()'):
        r'''Overrides tie direction.

        ..  container:: example

            Overrides tie direction on pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.rests_around([2], [4]),
            ...     baca.stems_up(),
            ...     baca.map(baca.tie(), baca.qruns()),
            ...     baca.ties_down(),
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
                                \revert Stem.direction
                                \revert Tie.direction
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides tie direction on pitched leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.rests_around([2], [4]),
            ...     baca.stems_up(),
            ...     baca.map(baca.tie(), baca.qruns()),
            ...     baca.map(baca.ties_down(), baca.tuplet(1)),
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
                                \revert Tie.direction
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
            attribute='direction',
            value=abjad.Down,
            grob='tie',
            selector=selector,
            )

    @staticmethod
    def ties_up(selector='baca.tleaves()'):
        r'''Overrides tie direction.

        ..  container:: example

            Overrides tie direction on pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.rests_around([2], [4]),
            ...     baca.stems_down(),
            ...     baca.map(baca.tie(), baca.qruns()),
            ...     baca.ties_up(),
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
                                \revert Stem.direction
                                \revert Tie.direction
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides tie direction on pitched leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.rests_around([2], [4]),
            ...     baca.stems_down(),
            ...     baca.map(baca.tie(), baca.qruns()),
            ...     baca.map(baca.ties_up(), baca.tuplet(1)),
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
                                \revert Tie.direction
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
            attribute='direction',
            value=abjad.Up,
            grob='tie',
            selector=selector,
            )

    @staticmethod
    def time_signature_extra_offset(pair, selector='baca.leaf(0)'):
        r'''Overrides time signature extra offset.

        ..  container:: example

            Overrides time signature extra offset on leaf 0:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Score.TimeSignature.extra-offset = #'(-6 . 0)
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
        assert isinstance(pair, tuple), repr(pair)
        return baca.OverrideCommand(
            attribute='extra_offset',
            value=pair,
            context='Score',
            grob='time_signature',
            selector=selector,
            )

    @staticmethod
    def timeline(scopes):
        r'''Makes timeline scope.

        Returns timeline scope.
        '''
        scopes = [baca.scope(*_) for _ in scopes]
        return baca.TimelineScope(scopes)

    @staticmethod
    def transparent_bar_lines(selector='baca.leaves()'):
        r'''Makes bar lines transparent.

        ..  container:: example

            Makes all bar lines transparent:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=rhythmos.TaleaRhythmMaker(
            ...             talea=rhythmos.Talea(
            ...                 counts=[1, 1, 1, -1],
            ...                 denominator=8,
            ...                 ),
            ...             ),
            ...         ),
            ...     baca.transparent_bar_lines(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \override Score.BarLine.transparent = ##t
                                \clef "treble"
                                e'8 [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8 ]
                <BLANKLINE>
                                r8
                <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                e''8 [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                f''8 ]
                <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                r8
                <BLANKLINE>
                                e'8 [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8 ]
                <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                r8
                <BLANKLINE>
                                e''8 [
                <BLANKLINE>
                                g'8 ]
                                \bar "|"
                                \revert Score.BarLine.transparent
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Makes bar line before measure 1 transparent:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=rhythmos.TaleaRhythmMaker(
            ...             talea=rhythmos.Talea(
            ...                 counts=[1, 1, 1, -1],
            ...                 denominator=8,
            ...                 ),
            ...             ),
            ...         ),
            ...     baca.transparent_bar_lines(baca.group_by_measure()[1]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble"
                                e'8 [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8 ]
                <BLANKLINE>
                                r8
                <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                \override Score.BarLine.transparent = ##t
                                e''8 [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                f''8 ]
                                \revert Score.BarLine.transparent
                <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                r8
                <BLANKLINE>
                                e'8 [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8 ]
                <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                r8
                <BLANKLINE>
                                e''8 [
                <BLANKLINE>
                                g'8 ]
                                \bar "|"
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        return baca.OverrideCommand(
            attribute='transparent',
            value=True,
            context='Score',
            grob='bar_line',
            selector=selector,
            )

    @staticmethod
    def transparent_rests(selector='baca.rests()'):
        r'''Makes rests transparent.

        ..  container:: example

            Makes rests transparent:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.transparent_rests(), baca.tuplet(1)),
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
                                \once \override Rest.transparent = ##t
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
            attribute='transparent',
            value=True,
            grob='rest',
            selector=selector,
            )

    @staticmethod
    def transparent_span_bars(selector='baca.leaf(0)'):
        r'''Makes span bars transparent.

        ..  container:: example

            Makes span bar before leaf 0 transparent:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.OverrideCommand(
            attribute='transparent',
            value=True,
            context='Score',
            grob='span_bar',
            selector=selector,
            )

    @staticmethod
    def transparent_time_signatures(selector='baca.leaves()'):
        r'''Makes time signatures transparent.

        ..  container:: example

            Makes all time signatures transparent:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        return baca.OverrideCommand(
            attribute='transparent',
            value=True,
            context='GlobalContext',
            grob='time_signature',
            selector=selector,
            )

    @staticmethod
    def tremolo_down(n, selector='baca.tleaves()'):
        r'''Overrides stem tremolo extra offset on trimmed leaves.
        '''
        pair = (0, -n)
        return baca.OverrideCommand(
            attribute='extra_offset',
            value=str(pair),
            grob='stem_tremolo',
            selector=selector,
            )

    @staticmethod
    def trill(
        pitch=None,
        harmonic=None,
        selector='baca.tleaves().with_next_leaf()',
        ):
        r'''Attaches trill to trimmed leaves (leaked to the right).

        ..  container:: example

            Attaches trill to trimmed leaves (leaked to the right):

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.trill(),
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
                                c'16 [ \startTrillSpan
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
                                r4 \stopTrillSpan
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches trill to trimmed leaves (leaked to the right) in every
            equipitch run:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.trill(), baca.qruns()),
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

            Attaches trill to trimmed leaves (leaked to the right) in every
            run:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.trill(), baca.runs()),
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
                                c'16 [ \startTrillSpan
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16 \stopTrillSpan
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ \startTrillSpan
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16 \stopTrillSpan
                                af''16 [ \startTrillSpan
                                g''16 ]
                            }
                            \times 4/5 {
                                a'16
                                r4 \stopTrillSpan
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches pitched trill to trimmed leaves (leaked to the right) in
            equipitch run 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.trill('Eb4'), baca.qrun(0)),
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
                                \pitchedTrill
                                c'16 [ \startTrillSpan ef'
                                d'16 ] \stopTrillSpan
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

            Attaches pitched trill to trimmed leaves (leaked to the right) in
            every equipitch run:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.trill('Eb4'), baca.qruns()),
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
                                \pitchedTrill
                                c'16 [ \startTrillSpan ef'
                                \pitchedTrill
                                d'16 ] \stopTrillSpan \startTrillSpan ef'
                                \pitchedTrill
                                bf'4 ~ \stopTrillSpan \startTrillSpan ef'
                                bf'16
                                r16 \stopTrillSpan
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \pitchedTrill
                                fs''16 [ \startTrillSpan ef'
                                \pitchedTrill
                                e''16 ] \stopTrillSpan \startTrillSpan ef'
                                \pitchedTrill
                                ef''4 ~ \stopTrillSpan \startTrillSpan ef'
                                ef''16
                                r16 \stopTrillSpan
                                \pitchedTrill
                                af''16 [ \startTrillSpan ef'
                                \pitchedTrill
                                g''16 ] \stopTrillSpan \startTrillSpan ef'
                            }
                            \times 4/5 {
                                \pitchedTrill
                                a'16 \stopTrillSpan \startTrillSpan ef'
                                r4 \stopTrillSpan
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches pitched trill (specified by interval) to trimmed leaves
            (leaked to the right) in every equipitch run:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.trill('M2'), baca.qruns()),
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

        '''
        if pitch is None:
            interval = None
        else:
            try:
                interval = None
                pitch = abjad.NamedPitch(pitch)
            except ValueError:
                interval = abjad.NamedInterval(pitch)
                pitch = None
        return baca.SpannerCommand(
            spanner=abjad.TrillSpanner(
                interval=interval,
                is_harmonic=harmonic,
                pitch=pitch,
                ),
            selector=selector,
            )

    @staticmethod
    def tuplet_bracket_extra_offset(pair, selector='baca.leaf(0)'):
        r'''Overrides tuplet bracket extra offset.

        ..  container:: example

            Overrides tuplet bracket extra offset on leaf 0:

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override TupletBracket.extra-offset = #'(-1 . 0)
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

            Overrides tuplet bracket extra offset on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.tuplet_bracket_extra_offset((-1, 0)),
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
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override TupletBracket.extra-offset = #'(-1 . 0)
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
        return baca.OverrideCommand(
            attribute='extra_offset',
            value=pair,
            grob='tuplet_bracket',
            selector=selector,
            )

    @staticmethod
    def tuplet_bracket_staff_padding(n, selector='baca.leaves()'):
        r'''Overrides tuplet bracket staff padding.

        ..  container:: example

            Overrides tuplet bracket staff padding on leaves:

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
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides tuplet bracket staff padding on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.tuplet_bracket_staff_padding(5),
            ...         baca.tuplet(1),
            ...         ),
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
            attribute='staff_padding',
            value=n,
            grob='tuplet_bracket',
            selector=selector,
            )

    @staticmethod
    def tuplet_brackets_down(selector='baca.leaves()'):
        r'''Overrides tuplet bracket direction.

        ..  container:: example

            Overrides tuplet bracket direction on leaves:

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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     baca.map(baca.tuplet_brackets_down(), baca.tuplet(1)),
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
            attribute='direction',
            value=abjad.Down,
            grob='tuplet_bracket',
            selector=selector,
            )

    @staticmethod
    def tuplet_brackets_up(selector='baca.leaves()'):
        r'''Overrides tuplet bracket direction.

        ..  container:: example

            Override tuplet bracket direction on leaves:

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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     baca.map(baca.tuplet_brackets_up(), baca.tuplet(1)),
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
            attribute='direction',
            value=abjad.Up,
            grob='tuplet_bracket',
            selector=selector,
            )

    @staticmethod
    def tuplet_number_extra_offset(pair, selector='baca.leaf(0)'):
        r'''Overrides tuplet number extra offset.

        ..  container:: example

            Overrides tuplet number extra offset on leaf 0:

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
                                \once \override TupletNumber.extra-offset = #'(-1 . 0)
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

            Overrides tuplet number extra offset on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     baca.map(
            ...         baca.tuplet_number_extra_offset((-1, 0)),
            ...         baca.tuplet(1),
            ...         ),
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
                                \once \override TupletNumber.extra-offset = #'(-1 . 0)
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
        return baca.OverrideCommand(
            attribute='extra_offset',
            value=pair,
            grob='tuplet_number',
            selector=selector,
            )

    @staticmethod
    def up_arpeggios(selector='baca.cheads()'):
        r"""Attaches up-arpeggios to chord heads.

        ..  container:: example

            Attaches up-arpeggios to all chord heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.up_arpeggios(),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.up_arpeggios(baca.cheads()[-2:]),
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
        return baca.IndicatorCommand(
            indicators=[abjad.Arpeggio(direction=abjad.Up)],
            selector=selector,
            )

    @staticmethod
    def up_bows(selector='baca.pheads()'):
        r'''Attaches up-bows to pitched heads.

        ..  container:: example

            Attaches up-bows to all pitched heads:

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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     baca.up_bows(
            ...         baca.tuplets()[1:2].pheads(),
            ...         ),
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
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('upbow')],
            selector=selector,
            )

    @staticmethod
    def very_long_fermata(selector='baca.leaf(0)'):
        r'''Attaches very long fermata to leaf.

        ..  container:: example

            Attaches very long fermata to first leaf:

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

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.very_long_fermata(
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
        return baca.IndicatorCommand(
            indicators=[abjad.Articulation('verylongfermata')],
            selector=selector,
            )

    @staticmethod
    def volta(selector='baca.leaves()'):
        r'''Wraps leaves in volta container.

        ..  container:: example

            Wraps stage 1 (global skips 1 and 2) in volta container:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=rhythmos.TaleaRhythmMaker(
            ...             talea=rhythmos.Talea(
            ...                 counts=[1, 1, 1, -1],
            ...                 denominator=8,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> maker(
            ...     baca.scope('GlobalSkips', 1),
            ...     baca.volta(baca.skips()[1:3]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            s1 * 1/2
                            \repeat volta 2
                            {
                <BLANKLINE>
                                %%% GlobalSkips [measure 2] %%%
                                \time 3/8
                                s1 * 3/8
                <BLANKLINE>
                                %%% GlobalSkips [measure 3] %%%
                                \time 4/8
                                s1 * 1/2
                            }
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble"
                                e'8 [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8 ]
                <BLANKLINE>
                                r8
                <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                e''8 [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                f''8 ]
                <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                r8
                <BLANKLINE>
                                e'8 [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8 ]
                <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                r8
                <BLANKLINE>
                                e''8 [
                <BLANKLINE>
                                g'8 ]
                                \bar "|"
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Wraps stage 2 global skips in volta container:

            >>> maker = baca.SegmentMaker(
            ...     label_stages=True,
            ...     measures_per_stage=[1, 2, 1],
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1, 3),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=rhythmos.TaleaRhythmMaker(
            ...             talea=rhythmos.Talea(
            ...                 counts=[1, 1, 1, -1],
            ...                 denominator=8,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> maker(
            ...     baca.scope('GlobalSkips', 2),
            ...     baca.volta(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            s1 * 1/2
                                - \markup {
                                    \fontsize
                                        #-3
                                        \with-color
                                            #blue
                                            [1]
                                    }
                            \repeat volta 2
                            {
                <BLANKLINE>
                                %%% GlobalSkips [measure 2] %%%
                                \time 3/8
                                s1 * 3/8
                                    - \markup {
                                        \fontsize
                                            #-3
                                            \with-color
                                                #blue
                                                [2]
                                        }
                <BLANKLINE>
                                %%% GlobalSkips [measure 3] %%%
                                \time 4/8
                                s1 * 1/2
                            }
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                                - \markup {
                                    \fontsize
                                        #-3
                                        \with-color
                                            #blue
                                            [3]
                                    }
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble"
                                e'8 [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8 ]
                <BLANKLINE>
                                r8
                <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                e''8 [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                f''8 ]
                <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                r8
                <BLANKLINE>
                                e'8 [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8 ]
                <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                r8
                <BLANKLINE>
                                e''8 [
                <BLANKLINE>
                                g'8 ]
                                \bar "|"
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        return baca.VoltaCommand(selector=selector)
