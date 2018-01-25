import abjad
import baca
import collections
from typing import Union
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
    def tag(tags, command, deactivate=None, tag_measure_number=None):
        r'''Appends each tag in `tags` to `command`.

        Sorts `comand` tags.

        Returns `command` for in-place definition file application.
        '''
        if isinstance(tags, str):
            tags = [tags]
        assert baca.Command._are_valid_tags(tags), repr(tags)
        if isinstance(command, baca.SuiteCommand):
            for command_ in command.commands:
                baca.tag(
                    tags,
                    command_,
                    deactivate=deactivate,
                    tag_measure_number=tag_measure_number,
                    )
        else:
            if (not hasattr(command, '_deactivate') or
                not hasattr(command, '_tag_measure_number') or
                not hasattr(command, '_tags')):
                raise Exception(f'does not implement tag protocol: {command}.')
            command._tags.extend(tags)
            command._tags.sort()
            command._deactivate = deactivate
            command._tag_measure_number = tag_measure_number
        return command

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
                                -\tenuto                                                                 %! IC
                                [
                                d'16
                                -\tenuto                                                                 %! IC
                                ]
                                bf'4
                                -\tenuto                                                                 %! IC
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\tenuto                                                                 %! IC
                                [
                                e''16
                                -\tenuto                                                                 %! IC
                                ]
                                ef''4
                                -\tenuto                                                                 %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\tenuto                                                                 %! IC
                                [
                                g''16
                                -\tenuto                                                                 %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\tenuto                                                                 %! IC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                -\tenuto                                                                 %! IC
                                [
                                e''16
                                -\tenuto                                                                 %! IC
                                ]
                                ef''4
                                -\tenuto                                                                 %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\tenuto                                                                 %! IC
                                [
                                g''16
                                -\tenuto                                                                 %! IC
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.color = #red                                        %! OC
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "più mosso"                                                  %! IC
                                    }                                                                    %! IC
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
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "lo stesso tempo"                                            %! IC
                                    }                                                                    %! IC
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
                                \revert TextScript.color                                                 %! OC
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "più mosso"                                                  %! IC
                                    }                                                                    %! IC
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.color = #red                                        %! OC
                                fs''16
                                [
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "lo stesso tempo"                                            %! IC
                                    }                                                                    %! IC
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
                                \revert TextScript.color                                                 %! OC
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
        return baca.OverrideCommand(
            attribute='color',
            value=color,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_script_extra_offset(pair, selector='baca.leaves()'):
        r'''Overrides text script extra offset.
        '''
        return baca.OverrideCommand(
            attribute='extra_offset',
            value=pair,
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
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.padding = #4                                        %! OC
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "più mosso"                                                  %! IC
                                    }                                                                    %! IC
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
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "lo stesso tempo"                                            %! IC
                                    }                                                                    %! IC
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
                                \revert TextScript.padding                                               %! OC
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "più mosso"                                                  %! IC
                                    }                                                                    %! IC
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.padding = #4                                        %! OC
                                fs''16
                                [
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "lo stesso tempo"                                            %! IC
                                    }                                                                    %! IC
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
                                \revert TextScript.padding                                               %! OC
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
        return baca.OverrideCommand(
            attribute='padding',
            value=n,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_script_parent_center(selector='baca.leaves()'):
        r'''Overrides text script parent alignment X to center.
        '''
        return baca.OverrideCommand(
            attribute='parent_alignment_X',
            value=0,
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.staff-padding = #4                                  %! OC
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "più mosso"                                                  %! IC
                                    }                                                                    %! IC
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
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "lo stesso tempo"                                            %! IC
                                    }                                                                    %! IC
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
                                \revert TextScript.staff-padding                                         %! OC
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "più mosso"                                                  %! IC
                                    }                                                                    %! IC
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.staff-padding = #4                                  %! OC
                                fs''16
                                [
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "lo stesso tempo"                                            %! IC
                                    }                                                                    %! IC
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
                                \revert TextScript.staff-padding                                         %! OC
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.direction = #down                                   %! OC
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "più mosso"                                                  %! IC
                                    }                                                                    %! IC
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
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "lo stesso tempo"                                            %! IC
                                    }                                                                    %! IC
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
                                \revert TextScript.direction                                             %! OC
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "più mosso"                                                  %! IC
                                    }                                                                    %! IC
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.direction = #down                                   %! OC
                                fs''16
                                [
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "lo stesso tempo"                                            %! IC
                                    }                                                                    %! IC
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
                                \revert TextScript.direction                                             %! OC
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.direction = #up                                     %! OC
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                c'16
                                [
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "più mosso"                                                  %! IC
                                    }                                                                    %! IC
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
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "lo stesso tempo"                                            %! IC
                                    }                                                                    %! IC
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
                                \revert TextScript.direction                                             %! OC
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "più mosso"                                                  %! IC
                                    }                                                                    %! IC
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.direction = #up                                     %! OC
                                fs''16
                                [
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            "lo stesso tempo"                                            %! IC
                                    }                                                                    %! IC
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
                                \revert TextScript.direction                                             %! OC
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextSpanner.staff-padding = #6                                 %! OC
                                \override TextScript.staff-padding = #6                                  %! OC
                                \override TupletBracket.staff-padding = #5                               %! OC
                                r8
                                \once \override TextSpanner.Y-extent = ##f
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
                                \once \override TextSpanner.bound-details.right-broken.text = ##f
                                \once \override TextSpanner.bound-details.right.arrow = ##t
                                \once \override TextSpanner.bound-details.right.padding = 0.5
                                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                                \once \override TextSpanner.bound-details.right.text = \markup {
                                    \concat
                                        {
                                            \hspace
                                                #0.0
                                            \whiteout
                                                \upright
                                                    ord.
                                        }
                                    }
                                \once \override TextSpanner.dash-fraction = 0.25
                                \once \override TextSpanner.dash-period = 1.5
                                c'16
                                [
                                \startTextSpan
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
                                \stopTextSpan
                                r4
                                \revert TextSpanner.staff-padding                                        %! OC
                                \revert TextScript.staff-padding                                         %! OC
                                \revert TupletBracket.staff-padding                                      %! OC
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.staff-padding = #6                                  %! OC
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
                                \override TextSpanner.staff-padding = #6                                 %! OC
                                \once \override TextSpanner.Y-extent = ##f
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
                                \once \override TextSpanner.bound-details.right-broken.text = ##f
                                \once \override TextSpanner.bound-details.right.arrow = ##t
                                \once \override TextSpanner.bound-details.right.padding = 0.5
                                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                                \once \override TextSpanner.bound-details.right.text = \markup {
                                    \concat
                                        {
                                            \hspace
                                                #0.0
                                            \whiteout
                                                \upright
                                                    ord.
                                        }
                                    }
                                \once \override TextSpanner.dash-fraction = 0.25
                                \once \override TextSpanner.dash-period = 1.5
                                fs''16
                                [
                                \startTextSpan
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
                                \stopTextSpan
                                \revert TextSpanner.staff-padding                                        %! OC
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TextScript.staff-padding                                         %! OC
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                ~                                                                        %! SC
                                [
                                c'16
                                ]
                                bf'4
                                ~                                                                        %! SC
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                [
                                e''16
                                ~                                                                        %! SC
                                ]
                                e''4
                                ~                                                                        %! SC
                                e''16
                                r16
                                fs''16
                                [
                                af''16
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
                                ~                                                                        %! SC
                                [
                                c'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                [
                                e''16
                                ]
                                e''4
                                ~
                                e''16
                                r16
                                fs''16
                                [
                                af''16
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
                                c'16
                                \repeatTie                                                               %! SC
                                ]
                                bf'4
                                bf'16
                                \repeatTie                                                               %! SC
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                [
                                e''16
                                ]
                                e''4
                                \repeatTie                                                               %! SC
                                e''16
                                \repeatTie                                                               %! SC
                                r16
                                fs''16
                                [
                                af''16
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
        assert isinstance(repeat, bool), repr(repeat)
        return baca.SpannerCommand(
            selector=selector,
            spanner=abjad.Tie(repeat=repeat),
            )

    @staticmethod
    def tie_from(selector='baca.pleaf(-1)', repeat=None):
        r'''Ties from leaf.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     baca.tie(repeat=True, selector=baca.leaves()[:2]),
            ...     baca.tie(repeat=True, selector=baca.leaves()[-2:]),
            ...     baca.tie_from(baca.leaf(1)),
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
                                c'2
                <BLANKLINE>
                                % MusicVoice [measure 2]                                                 %! SM4
                                c'4.
                                \repeatTie                                                               %! TCC
                <BLANKLINE>
                                % MusicVoice [measure 3]                                                 %! SM4
                                c'2
                                \repeatTie                                                               %! TCC
                <BLANKLINE>
                                % MusicVoice [measure 4]                                                 %! SM4
                                c'4.
                                \repeatTie                                                               %! TCC
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        Returns tie correction command.
        '''
        return baca.TieCorrectionCommand(
            repeat=repeat,
            selector=selector,
            )

    @staticmethod
    def tie_repeat_pitches(repeat=None):
        r'''Ties repeat pitches.

        Returns mapped tie correction command.
        '''
        return baca.map(
            baca.tie(repeat=repeat),
            baca.ltqruns().nontrivial(),
            )

    @staticmethod
    def tie_to(selector='baca.pleaf(0)', repeat=None):
        r'''Ties to leaf.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     baca.tie(repeat=True, selector=baca.leaves()[:2]),
            ...     baca.tie(repeat=True, selector=baca.leaves()[-2:]),
            ...     baca.tie_to(baca.leaf(2)),
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
                                c'2
                <BLANKLINE>
                                % MusicVoice [measure 2]                                                 %! SM4
                                c'4.
                                \repeatTie                                                               %! TCC
                <BLANKLINE>
                                % MusicVoice [measure 3]                                                 %! SM4
                                c'2
                                \repeatTie                                                               %! TCC
                <BLANKLINE>
                                % MusicVoice [measure 4]                                                 %! SM4
                                c'4.
                                \repeatTie                                                               %! TCC
                <BLANKLINE>
                            }
                        }
                    >>
                >>


        '''
        return baca.TieCorrectionCommand(
            direction=abjad.Left,
            repeat=repeat,
            selector=selector,
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
                                \override Stem.direction = #up                                           %! OC
                                \override Tie.direction = #down                                          %! OC
                                b'16
                                ~                                                                        %! SC
                                [
                                b'16
                                ]
                                c''4
                                ~                                                                        %! SC
                                c''16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                b'16
                                ~                                                                        %! SC
                                [
                                b'16
                                ~                                                                        %! SC
                                ]
                                b'4
                                ~                                                                        %! SC
                                b'16
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert Stem.direction                                                   %! OC
                                \revert Tie.direction                                                    %! OC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                \override Stem.direction = #up                                           %! OC
                                b'16
                                ~                                                                        %! SC
                                [
                                b'16
                                ]
                                c''4
                                ~                                                                        %! SC
                                c''16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                \override Tie.direction = #down                                          %! OC
                                b'16
                                ~                                                                        %! SC
                                [
                                b'16
                                ~                                                                        %! SC
                                ]
                                b'4
                                ~                                                                        %! SC
                                b'16
                                \revert Tie.direction                                                    %! OC
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert Stem.direction                                                   %! OC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                \override Stem.direction = #down                                         %! OC
                                \override Tie.direction = #up                                            %! OC
                                b'16
                                ~                                                                        %! SC
                                [
                                b'16
                                ]
                                c''4
                                ~                                                                        %! SC
                                c''16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                b'16
                                ~                                                                        %! SC
                                [
                                b'16
                                ~                                                                        %! SC
                                ]
                                b'4
                                ~                                                                        %! SC
                                b'16
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert Stem.direction                                                   %! OC
                                \revert Tie.direction                                                    %! OC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                \override Stem.direction = #down                                         %! OC
                                b'16
                                ~                                                                        %! SC
                                [
                                b'16
                                ]
                                c''4
                                ~                                                                        %! SC
                                c''16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                \override Tie.direction = #up                                            %! OC
                                b'16
                                ~                                                                        %! SC
                                [
                                b'16
                                ~                                                                        %! SC
                                ]
                                b'4
                                ~                                                                        %! SC
                                b'16
                                \revert Tie.direction                                                    %! OC
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert Stem.direction                                                   %! OC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Score.TimeSignature.extra-offset = #'(-6 . 0)            %! OC
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
                                \override Score.BarLine.transparent = ##t                                %! OC
                                e'8
                                [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                r8
                <BLANKLINE>
                                % MusicVoice [measure 2]                                                 %! SM4
                                e''8
                                [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                f''8
                                ]
                <BLANKLINE>
                                % MusicVoice [measure 3]                                                 %! SM4
                                r8
                <BLANKLINE>
                                e'8
                                [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                % MusicVoice [measure 4]                                                 %! SM4
                                r8
                <BLANKLINE>
                                e''8
                                [
                <BLANKLINE>
                                g'8
                                ]
                                \revert Score.BarLine.transparent                                        %! OC
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
                                e'8
                                [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                r8
                <BLANKLINE>
                                % MusicVoice [measure 2]                                                 %! SM4
                                \override Score.BarLine.transparent = ##t                                %! OC
                                e''8
                                [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                f''8
                                ]
                                \revert Score.BarLine.transparent                                        %! OC
                <BLANKLINE>
                                % MusicVoice [measure 3]                                                 %! SM4
                                r8
                <BLANKLINE>
                                e'8
                                [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                % MusicVoice [measure 4]                                                 %! SM4
                                r8
                <BLANKLINE>
                                e''8
                                [
                <BLANKLINE>
                                g'8
                                ]
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override Rest.transparent = ##t                                         %! OC
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
                                \revert Rest.transparent                                                 %! OC
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                \once \override Rest.transparent = ##t                                   %! OC
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Score.SpanBar.transparent = ##t                          %! OC
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override GlobalContext.TimeSignature.transparent = ##t                  %! OC
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
                                \revert GlobalContext.TimeSignature.transparent                          %! OC
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                \startTrillSpan                                                          %! SC
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
                                \stopTrillSpan                                                           %! SC
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                \startTrillSpan                                                          %! SC
                                d'16
                                ]
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan                                                          %! SC
                                bf'4
                                ~
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan                                                          %! SC
                                bf'16
                                r16
                                \stopTrillSpan                                                           %! SC
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                \startTrillSpan                                                          %! SC
                                e''16
                                ]
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan                                                          %! SC
                                ef''4
                                ~
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan                                                          %! SC
                                ef''16
                                r16
                                \stopTrillSpan                                                           %! SC
                                af''16
                                [
                                \startTrillSpan                                                          %! SC
                                g''16
                                ]
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan                                                          %! SC
                            }
                            \times 4/5 {
                                a'16
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan                                                          %! SC
                                r4
                                \stopTrillSpan                                                           %! SC
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                \startTrillSpan                                                          %! SC
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                                \stopTrillSpan                                                           %! SC
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                \startTrillSpan                                                          %! SC
                                e''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                                \stopTrillSpan                                                           %! SC
                                af''16
                                [
                                \startTrillSpan                                                          %! SC
                                g''16
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \stopTrillSpan                                                           %! SC
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                \pitchedTrill                                                            %! SC
                                c'16
                                [
                                \startTrillSpan ef'                                                      %! SC
                                d'16
                                ]
                                \stopTrillSpan                                                           %! SC
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
                                \pitchedTrill                                                            %! SC
                                c'16
                                [
                                \startTrillSpan ef'                                                      %! SC
                                \pitchedTrill                                                            %! SC
                                d'16
                                ]
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan ef'                                                      %! SC
                                \pitchedTrill                                                            %! SC
                                bf'4
                                ~
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan ef'                                                      %! SC
                                bf'16
                                r16
                                \stopTrillSpan                                                           %! SC
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \pitchedTrill                                                            %! SC
                                fs''16
                                [
                                \startTrillSpan ef'                                                      %! SC
                                \pitchedTrill                                                            %! SC
                                e''16
                                ]
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan ef'                                                      %! SC
                                \pitchedTrill                                                            %! SC
                                ef''4
                                ~
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan ef'                                                      %! SC
                                ef''16
                                r16
                                \stopTrillSpan                                                           %! SC
                                \pitchedTrill                                                            %! SC
                                af''16
                                [
                                \startTrillSpan ef'                                                      %! SC
                                \pitchedTrill                                                            %! SC
                                g''16
                                ]
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan ef'                                                      %! SC
                            }
                            \times 4/5 {
                                \pitchedTrill                                                            %! SC
                                a'16
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan ef'                                                      %! SC
                                r4
                                \stopTrillSpan                                                           %! SC
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                \pitchedTrill                                                            %! SC
                                c'16
                                [
                                \startTrillSpan d'                                                       %! SC
                                \pitchedTrill                                                            %! SC
                                d'16
                                ]
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan e'                                                       %! SC
                                \pitchedTrill                                                            %! SC
                                bf'4
                                ~
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan c''                                                      %! SC
                                bf'16
                                r16
                                \stopTrillSpan                                                           %! SC
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \pitchedTrill                                                            %! SC
                                fs''16
                                [
                                \startTrillSpan gs''                                                     %! SC
                                \pitchedTrill                                                            %! SC
                                e''16
                                ]
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan fs''                                                     %! SC
                                \pitchedTrill                                                            %! SC
                                ef''4
                                ~
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan f''                                                      %! SC
                                ef''16
                                r16
                                \stopTrillSpan                                                           %! SC
                                \pitchedTrill                                                            %! SC
                                af''16
                                [
                                \startTrillSpan bf''                                                     %! SC
                                \pitchedTrill                                                            %! SC
                                g''16
                                ]
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan a''                                                      %! SC
                            }
                            \times 4/5 {
                                \pitchedTrill                                                            %! SC
                                a'16
                                \stopTrillSpan                                                           %! SC
                                \startTrillSpan b'                                                       %! SC
                                r4
                                \stopTrillSpan                                                           %! SC
                                \revert TupletBracket.staff-padding                                      %! OC
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override TupletBracket.extra-offset = #'(-1 . 0)                  %! OC
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
                                \once \override TupletBracket.extra-offset = #'(-1 . 0)                  %! OC
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

        '''
        return baca.OverrideCommand(
            attribute='extra_offset',
            value=pair,
            grob='tuplet_bracket',
            selector=selector,
            )

    @staticmethod
    def tuplet_bracket_padding(n, selector='baca.leaves()'):
        r'''Overrides tuplet bracket padding.

        Returns override command.
        '''
        return baca.OverrideCommand(
            attribute='padding',
            value=n,
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
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
                                \override TupletBracket.staff-padding = #5                               %! OC
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
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                \override TupletBracket.direction = #down                                %! OC
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
                                \revert TupletBracket.direction                                          %! OC
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
                                \override TupletBracket.direction = #down                                %! OC
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
                                \revert TupletBracket.direction                                          %! OC
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
                                \override TupletBracket.direction = #up                                  %! OC
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
                                \revert TupletBracket.direction                                          %! OC
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
                                \override TupletBracket.direction = #up                                  %! OC
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
                                \revert TupletBracket.direction                                          %! OC
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
                                \once \override TupletNumber.extra-offset = #'(-1 . 0)                   %! OC
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
                                \once \override TupletNumber.extra-offset = #'(-1 . 0)                   %! OC
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

        '''
        return baca.OverrideCommand(
            attribute='extra_offset',
            value=pair,
            grob='tuplet_number',
            selector=selector,
            )

    @staticmethod
    def untie_to(selector='baca.pleaf(0)'):
        r'''Unties to leaf.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_tied_notes(),
            ...     baca.untie_to(selector=baca.leaf(2)),
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
                                c'2
                                ~
                <BLANKLINE>
                                % MusicVoice [measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                                % MusicVoice [measure 3]                                                 %! SM4
                                c'2
                                ~
                <BLANKLINE>
                                % MusicVoice [measure 4]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        return baca.TieCorrectionCommand(
            direction=abjad.Left,
            selector=selector,
            untie=True,
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                \arpeggioArrowUp                                                         %! IC
                                <c' d' bf'>8
                                \arpeggio                                                                %! IC
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \arpeggioArrowUp                                                         %! IC
                                <ef'' e'' fs'''>8
                                \arpeggio                                                                %! IC
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \arpeggioArrowUp                                                         %! IC
                                <g' af''>8
                                \arpeggio                                                                %! IC
                                ~
                                [
                                <g' af''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                <c' d' bf'>8
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \arpeggioArrowUp                                                         %! IC
                                <ef'' e'' fs'''>8
                                \arpeggio                                                                %! IC
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \arpeggioArrowUp                                                         %! IC
                                <g' af''>8
                                \arpeggio                                                                %! IC
                                ~
                                [
                                <g' af''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
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
                                -\upbow                                                                  %! IC
                                [
                                d'16
                                -\upbow                                                                  %! IC
                                ]
                                bf'4
                                -\upbow                                                                  %! IC
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\upbow                                                                  %! IC
                                [
                                e''16
                                -\upbow                                                                  %! IC
                                ]
                                ef''4
                                -\upbow                                                                  %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\upbow                                                                  %! IC
                                [
                                g''16
                                -\upbow                                                                  %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\upbow                                                                  %! IC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC
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
                                -\upbow                                                                  %! IC
                                [
                                e''16
                                -\upbow                                                                  %! IC
                                ]
                                ef''4
                                -\upbow                                                                  %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\upbow                                                                  %! IC
                                [
                                g''16
                                -\upbow                                                                  %! IC
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
                                -\verylongfermata                                                        %! IC
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
                                -\verylongfermata                                                        %! IC
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
                            \repeat volta 2
                            {
                <BLANKLINE>
                                % GlobalSkips [measure 2]                                                %! SM4
                                \time 3/8                                                                %! EXPLICIT_TIME_SIGNATURE:SM8
                                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                                s1 * 3/8
                <BLANKLINE>
                                % GlobalSkips [measure 3]                                                %! SM4
                                \time 4/8                                                                %! EXPLICIT_TIME_SIGNATURE:SM8
                                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                                s1 * 1/2
                            }
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
                                e'8
                                [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                r8
                <BLANKLINE>
                                % MusicVoice [measure 2]                                                 %! SM4
                                e''8
                                [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                f''8
                                ]
                <BLANKLINE>
                                % MusicVoice [measure 3]                                                 %! SM4
                                r8
                <BLANKLINE>
                                e'8
                                [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                % MusicVoice [measure 4]                                                 %! SM4
                                r8
                <BLANKLINE>
                                e''8
                                [
                <BLANKLINE>
                                g'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Wraps stage 2 global skips in volta container:

            >>> maker = baca.SegmentMaker(
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
                            \repeat volta 2
                            {
                <BLANKLINE>
                                % GlobalSkips [measure 2]                                                %! SM4
                                \time 3/8                                                                %! EXPLICIT_TIME_SIGNATURE:SM8
                                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                                s1 * 3/8
                <BLANKLINE>
                                % GlobalSkips [measure 3]                                                %! SM4
                                \time 4/8                                                                %! EXPLICIT_TIME_SIGNATURE:SM8
                                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                                s1 * 1/2
                            }
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
                                e'8
                                [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                r8
                <BLANKLINE>
                                % MusicVoice [measure 2]                                                 %! SM4
                                e''8
                                [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                f''8
                                ]
                <BLANKLINE>
                                % MusicVoice [measure 3]                                                 %! SM4
                                r8
                <BLANKLINE>
                                e'8
                                [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                % MusicVoice [measure 4]                                                 %! SM4
                                r8
                <BLANKLINE>
                                e''8
                                [
                <BLANKLINE>
                                g'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        return baca.VoltaCommand(selector=selector)
