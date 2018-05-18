import abjad
import baca
import collections
import typing
from abjad import rhythmos as rhythmos
from .Command import Command
from .Expression import Expression
from .IndicatorCommand import IndicatorCommand
from .MapCommand import MapCommand
from .OverrideCommand import OverrideCommand
from .PiecewiseCommand import PiecewiseCommand
from .Selection import Selection
from .SpannerCommand import SpannerCommand
from .SuiteCommand import SuiteCommand
from .TextSpannerCommand import TextSpannerCommand
from .TieCorrectionCommand import TieCorrectionCommand
from .TimelineScope import TimelineScope
from .VoltaCommand import VoltaCommand
from .Typing import Number
from .Typing import NumberPair
from .Typing import Selector


class LibraryTZ(abjad.AbjadObject):
    """
    Library T - Z.

    >>> from abjad import rhythmos as rhythmos

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(1) Library'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def tag(
        tags: typing.Union[str, typing.List[str]],
        command: Command,
        *,
        deactivate: bool = None,
        tag_measure_number: bool = None,
        ) -> Command:
        """
        Appends each tag in ``tags`` to ``command``.

        Sorts ``command`` tags.

        Returns ``command`` for in-place definition file application.
        """
        if isinstance(tags, str):
            tags = [tags]
        if not isinstance(tags, list):
            message = f'tags must be string or list of strings'
            message += ' (not {tags!r}).'
            raise Exception(message)
        assert Command._are_valid_tags(tags), repr(tags)
        if isinstance(command, SuiteCommand):
            for command_ in command.commands:
                LibraryTZ.tag(
                    tags,
                    command_,
                    deactivate=deactivate,
                    tag_measure_number=tag_measure_number,
                    )
        else:
            assert command._tags is not None
            tags.sort()
            tags_ = [abjad.Tag(_) for _ in tags]
            command._tags.extend(tags_)
            command._deactivate = deactivate
            command.tag_measure_number = tag_measure_number
        return command

    @staticmethod
    def tenuto(
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches tenuto.

        ..  container:: example

            Attaches tenuto to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.tenuto(),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                c'16
                                -\tenuto                                                                 %! IC
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches tenuto to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.tenuto(selector=baca.pheads()),
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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return IndicatorCommand(
            indicators=[abjad.Articulation('tenuto')],
            selector=selector,
            )

    @staticmethod
    def text_script_color(
        color: str = 'red',
        *,
        selector: Selector = 'baca.leaves()',
        allow_mmrests: bool = False,
        ) -> OverrideCommand:
        r"""
        Overrides text script color.

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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.color = #red                                        %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TextScript.color                                                 %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \override TextScript.color = #red                                        %! OC1
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
                                \revert TextScript.color                                                 %! OC2
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Raises exception when called on multimeasure rests:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.text_script_color('red'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            Traceback (most recent call last):
                ...
            Exception: MultimeasureRest is forbidden.

        """
        if allow_mmrests is True:
            blacklist = None
        else:
            blacklist = (abjad.MultimeasureRest,)
        return OverrideCommand(
            attribute='color',
            blacklist=blacklist,
            value=color,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_script_down(
        selector: Selector = 'baca.leaves()',
        *,
        allow_mmrests: bool = False,
        ) -> OverrideCommand:
        r"""
        Overrides text script direction.

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
            ...     baca.text_script_down(),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.direction = #down                                   %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TextScript.direction                                             %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
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
            ...     baca.map(baca.text_script_down(), baca.tuplet(1)),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \override TextScript.direction = #down                                   %! OC1
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
                                \revert TextScript.direction                                             %! OC2
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Raises exception when called on multimeasure rests:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.text_script_down()
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            Traceback (most recent call last):
                ...
            Exception: MultimeasureRest is forbidden.

        """
        if allow_mmrests is True:
            blacklist = None
        else:
            blacklist = (abjad.MultimeasureRest,)
        return OverrideCommand(
            attribute='direction',
            blacklist=blacklist,
            value=abjad.Down,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_script_extra_offset(
        pair: NumberPair,
        *,
        selector: Selector = 'baca.leaves()',
        allow_mmrests: bool = False,
        ) -> OverrideCommand:
        r"""
        Overrides text script extra offset.

        ..  container:: example

            Raises exception when called on multimeasure rests:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.text_script_extra_offset((0, 2)),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            Traceback (most recent call last):
                ...
            Exception: MultimeasureRest is forbidden.

        """
        if allow_mmrests is True:
            blacklist = None
        else:
            blacklist = (abjad.MultimeasureRest,)
        return OverrideCommand(
            attribute='extra_offset',
            blacklist=blacklist,
            value=pair,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_script_padding(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        allow_mmrests: bool = False,
        ) -> OverrideCommand:
        r"""
        Overrides text script padding.

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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.padding = #4                                        %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TextScript.padding                                               %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \override TextScript.padding = #4                                        %! OC1
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
                                \revert TextScript.padding                                               %! OC2
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Raises exception when called on multimeasure rests:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.text_script_padding(2),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            Traceback (most recent call last):
                ...
            Exception: MultimeasureRest is forbidden.

        """
        if allow_mmrests is True:
            blacklist = None
        else:
            blacklist = (abjad.MultimeasureRest,)
        return OverrideCommand(
            attribute='padding',
            blacklist=blacklist,
            value=n,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_script_parent_center(
        selector: Selector = 'baca.leaves()',
        *,
        allow_mmrests: bool = False,
        ) -> OverrideCommand:
        r"""
        Overrides text script parent alignment X to center.

        ..  container:: example

            Raises exception when called on multimeasure rests:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.text_script_parent_center()
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            Traceback (most recent call last):
                ...
            Exception: MultimeasureRest is forbidden.

        """
        if allow_mmrests is True:
            blacklist = None
        else:
            blacklist = (abjad.MultimeasureRest,)
        return OverrideCommand(
            attribute='parent_alignment_X',
            blacklist=blacklist,
            value=0,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_script_staff_padding(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        allow_mmrests: bool = False,
        ) -> OverrideCommand:
        r"""
        Overrides text script staff padding.

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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.staff-padding = #4                                  %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TextScript.staff-padding                                         %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \override TextScript.staff-padding = #4                                  %! OC1
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
                                \revert TextScript.staff-padding                                         %! OC2
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Raises exception when called on multimeasure rests:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.text_script_staff_padding(2)
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            Traceback (most recent call last):
                ...
            Exception: MultimeasureRest is forbidden.

        """
        if allow_mmrests is True:
            blacklist = None
        else:
            blacklist = (abjad.MultimeasureRest,)
        return OverrideCommand(
            attribute='staff_padding',
            blacklist=blacklist,
            value=n,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_script_up(
        selector: Selector = 'baca.leaves()',
        *,
        allow_mmrests: bool = False,
        ) -> OverrideCommand:
        r"""
        Overrides text script direction.

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
            ...     baca.text_script_up(),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.direction = #up                                     %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TextScript.direction                                             %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
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
            ...     baca.map(baca.text_script_up(), baca.tuplet(1)),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \override TextScript.direction = #up                                     %! OC1
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
                                \revert TextScript.direction                                             %! OC2
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Raises exception when called on multimeasure rests:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.text_script_up()
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            Traceback (most recent call last):
                ...
            Exception: MultimeasureRest is forbidden.

        """
        if allow_mmrests is True:
            blacklist = None
        else:
            blacklist = (abjad.MultimeasureRest,)
        return OverrideCommand(
            attribute='direction',
            blacklist=blacklist,
            value=abjad.Up,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_script_x_offset(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        allow_mmrests: bool = False,
        ) -> OverrideCommand:
        """
        Overrides text script X-offset.
        """
        if allow_mmrests is True:
            blacklist = None
        else:
            blacklist = (abjad.MultimeasureRest,)
        return OverrideCommand(
            attribute='X_offset',
            blacklist=blacklist,
            value=n,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_script_y_offset(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        allow_mmrests: bool = False,
        ) -> OverrideCommand:
        """
        Overrides text script Y-offset.
        """
        if allow_mmrests is True:
            blacklist = None
        else:
            blacklist = (abjad.MultimeasureRest,)
        return OverrideCommand(
            attribute='Y_offset',
            blacklist=blacklist,
            value=n,
            grob='text_script',
            selector=selector,
            )

    @staticmethod
    def text_spanner(
        text: typing.Union[str, abjad.Markup, IndicatorCommand],
        *,
        leak: bool = None,
        line_segment: abjad.LineSegment = None,
        lilypond_id: int = None,
        right_padding: typing.Optional[Number] = 1.25,
        selector: Selector = 'baca.leaves()',
        tweaks: typing.List[typing.Tuple] = None,
        ) -> TextSpannerCommand:
        r"""
        Makes text spanner command.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.text_spanner(
            ...         '1/2 clt',
            ...         selector=baca.leaves()[:7 + 1],
            ...         tweaks=[('staff-padding', 4)],
            ...         ),
            ...     baca.text_spanner(
            ...         'damp',
            ...         lilypond_id=1,
            ...         selector=baca.leaves()[:11 + 1],
            ...         tweaks=[('staff-padding', 6.5)],
            ...         ),
            ...     baca.make_even_runs(),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    e'8
                                    [
                                    - \tweak Y-extent ##f
                                    - \tweak bound-details.left.text \markup {
                                        \concat
                                            {
                                                \whiteout
                                                    \upright
                                                        "1/2 clt"
                                                \hspace
                                                    #0.5
                                            }
                                        }
                                    - \tweak dash-fraction 0.25
                                    - \tweak dash-period 1.5
                                    - \tweak bound-details.left-broken.text ##f
                                    - \tweak bound-details.left.stencil-align-dir-y 0
                                    - \tweak bound-details.right-broken.arrow ##f
                                    - \tweak bound-details.right-broken.padding 0
                                    - \tweak bound-details.right-broken.text ##f
                                    - \tweak bound-details.right.padding 1.25
                                    - \tweak bound-details.right.text \markup {
                                        \draw-line
                                            #'(0 . -1)
                                        }
                                    - \tweak staff-padding #4
                                    \startTextSpan
                                    - \tweak Y-extent ##f
                                    - \tweak bound-details.left.text \markup {
                                        \concat
                                            {
                                                \whiteout
                                                    \upright
                                                        damp
                                                \hspace
                                                    #0.5
                                            }
                                        }
                                    - \tweak dash-fraction 0.25
                                    - \tweak dash-period 1.5
                                    - \tweak bound-details.left-broken.text ##f
                                    - \tweak bound-details.left.stencil-align-dir-y 0
                                    - \tweak bound-details.right-broken.arrow ##f
                                    - \tweak bound-details.right-broken.padding 0
                                    - \tweak bound-details.right-broken.text ##f
                                    - \tweak bound-details.right.padding 1.25
                                    - \tweak bound-details.right.text \markup {
                                        \draw-line
                                            #'(0 . -1)
                                        }
                                    - \tweak staff-padding #6.5
                                    \startTextSpanOne
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
                                    % [MusicVoice measure 2]                                             %! SM4
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
                                    % [MusicVoice measure 3]                                             %! SM4
                                    d''8
                                    \stopTextSpan
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
                                    % [MusicVoice measure 4]                                             %! SM4
                                    f''8
                                    \stopTextSpanOne
                                    [
                <BLANKLINE>
                                    e'8
                <BLANKLINE>
                                    d''8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        """
        from .LibraryAF import LibraryAF
        if lilypond_id is not None:
            assert lilypond_id in (1, 2, 3), repr(lilypond_id)
        if line_segment is None:
            line_segment = LibraryAF.dashed_hook()
        if right_padding is not None:
            line_segment = abjad.new(line_segment, right_padding=right_padding)
        return TextSpannerCommand(
            leak=leak,
            lilypond_id=lilypond_id,
            line_segment=line_segment,
            selector=selector,
            text=text,
            tweaks=tweaks,
            )

    @staticmethod
    def text_spanner_left_padding(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides text spanner left padding.
        """
        return OverrideCommand(
            attribute='bound_details__left__padding',
            value=n,
            grob='text_spanner',
            selector=selector,
            )

    @staticmethod
    def text_spanner_right_padding(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides text spanner right padding.
        """
        return OverrideCommand(
            attribute='bound_details__right__padding',
            value=n,
            grob='text_spanner',
            selector=selector,
            )

    @staticmethod
    def text_spanner_staff_padding(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides text spanner staff padding.

        ..  container:: example

            Overrides text spanner staff padding on all trimmed leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.text_spanner_staff_padding(6),
            ...     baca.text_script_staff_padding(6),
            ...     baca.transition(
            ...         baca.markup.pont(),
            ...         baca.markup.ord(),
            ...         ),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextSpanner.staff-padding = #6                                 %! OC1
                                \override TextScript.staff-padding = #6                                  %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                c'16
                                [
                                - \tweak Y-extent ##f                                                    %! PWC1
                                - \tweak bound-details.left.text \markup {                               %! PWC1
                                    \concat                                                              %! PWC1
                                        {                                                                %! PWC1
                                            \whiteout                                                    %! PWC1
                                                \upright                                                 %! PWC1
                                                    pont.                                                %! PWC1
                                            \hspace                                                      %! PWC1
                                                #0.5                                                     %! PWC1
                                        }                                                                %! PWC1
                                    }                                                                    %! PWC1
                                - \tweak arrow-width 0.25                                                %! PWC1
                                - \tweak dash-fraction 0.25                                              %! PWC1
                                - \tweak dash-period 1.5                                                 %! PWC1
                                - \tweak bound-details.left-broken.text ##f                              %! PWC1
                                - \tweak bound-details.left.stencil-align-dir-y #center                  %! PWC1
                                - \tweak bound-details.right.arrow ##t                                   %! PWC1
                                - \tweak bound-details.right-broken.arrow ##f                            %! PWC1
                                - \tweak bound-details.right-broken.padding 0                            %! PWC1
                                - \tweak bound-details.right-broken.text ##f                             %! PWC1
                                - \tweak bound-details.right.padding 0.5                                 %! PWC1
                                - \tweak bound-details.right.stencil-align-dir-y #center                 %! PWC1
                                - \tweak bound-details.right.text \markup {                              %! PWC1
                                    \concat                                                              %! PWC1
                                        {                                                                %! PWC1
                                            \hspace                                                      %! PWC1
                                                #0.0                                                     %! PWC1
                                            \whiteout                                                    %! PWC1
                                                \upright                                                 %! PWC1
                                                    ord.                                                 %! PWC1
                                        }                                                                %! PWC1
                                    }                                                                    %! PWC1
                                \startTextSpan                                                           %! PWC1
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
                                \stopTextSpan                                                            %! PWC1
                                r4
                                \revert TextSpanner.staff-padding                                        %! OC2
                                \revert TextScript.staff-padding                                         %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
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
            ...     baca.transition(
            ...         baca.markup.pont(),
            ...         baca.markup.ord(),
            ...         spanner_selector=baca.map(baca.tleaves(), baca.tuplet(1)),
            ...         ),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TextScript.staff-padding = #6                                  %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \override TextSpanner.staff-padding = #6                                 %! OC1
                                fs''16
                                [
                                - \tweak Y-extent ##f                                                    %! PWC1
                                - \tweak bound-details.left.text \markup {                               %! PWC1
                                    \concat                                                              %! PWC1
                                        {                                                                %! PWC1
                                            \whiteout                                                    %! PWC1
                                                \upright                                                 %! PWC1
                                                    pont.                                                %! PWC1
                                            \hspace                                                      %! PWC1
                                                #0.5                                                     %! PWC1
                                        }                                                                %! PWC1
                                    }                                                                    %! PWC1
                                - \tweak arrow-width 0.25                                                %! PWC1
                                - \tweak dash-fraction 0.25                                              %! PWC1
                                - \tweak dash-period 1.5                                                 %! PWC1
                                - \tweak bound-details.left-broken.text ##f                              %! PWC1
                                - \tweak bound-details.left.stencil-align-dir-y #center                  %! PWC1
                                - \tweak bound-details.right.arrow ##t                                   %! PWC1
                                - \tweak bound-details.right-broken.arrow ##f                            %! PWC1
                                - \tweak bound-details.right-broken.padding 0                            %! PWC1
                                - \tweak bound-details.right-broken.text ##f                             %! PWC1
                                - \tweak bound-details.right.padding 0.5                                 %! PWC1
                                - \tweak bound-details.right.stencil-align-dir-y #center                 %! PWC1
                                - \tweak bound-details.right.text \markup {                              %! PWC1
                                    \concat                                                              %! PWC1
                                        {                                                                %! PWC1
                                            \hspace                                                      %! PWC1
                                                #0.0                                                     %! PWC1
                                            \whiteout                                                    %! PWC1
                                                \upright                                                 %! PWC1
                                                    ord.                                                 %! PWC1
                                        }                                                                %! PWC1
                                    }                                                                    %! PWC1
                                \startTextSpan                                                           %! PWC1
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
                                \stopTextSpan                                                            %! PWC1
                                \revert TextSpanner.staff-padding                                        %! OC2
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TextScript.staff-padding                                         %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='staff_padding',
            value=n,
            grob='text_spanner',
            selector=selector,
            )

    @staticmethod
    def text_spanner_stencil_false(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides text spanner stencil.
        """
        return OverrideCommand(
            attribute='stencil',
            value=False,
            grob='text_spanner',
            selector=selector,
            )

    @staticmethod
    def text_spanner_transparent(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides text spanner transparent.
        """
        return OverrideCommand(
            attribute='transparent',
            value=True,
            grob='text_spanner',
            selector=selector,
            )

    @staticmethod
    def text_spanner_y_offset(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides text spanner Y-offset.
        """
        return OverrideCommand(
            attribute='Y_offset',
            value=n,
            grob='text_spanner',
            selector=selector,
            )

    @staticmethod
    def tie(
        *,
        selector: Selector = 'baca.qrun(0)',
        ) -> SpannerCommand:
        r"""
        Attaches tie.

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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return SpannerCommand(
            selector=selector,
            spanner=abjad.Tie(),
            )

    @staticmethod
    def tie_down(
        *,
        selector: Selector = 'baca.tleaves()',
        ) -> OverrideCommand:
        r"""
        Overrides tie direction.

        ..  container:: example

            Overrides tie direction on pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.rests_around([2], [4]),
            ...     baca.stem_up(),
            ...     baca.map(baca.tie(), baca.qruns()),
            ...     baca.tie_down(),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                \override Stem.direction = #up                                           %! OC1
                                \override Tie.direction = #down                                          %! OC1
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
                                \revert Stem.direction                                                   %! OC2
                                \revert Tie.direction                                                    %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
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
            ...     baca.stem_up(),
            ...     baca.map(baca.tie(), baca.qruns()),
            ...     baca.map(baca.tie_down(), baca.tuplet(1)),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                \override Stem.direction = #up                                           %! OC1
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
                                \override Tie.direction = #down                                          %! OC1
                                b'16
                                ~                                                                        %! SC
                                [
                                b'16
                                ~                                                                        %! SC
                                ]
                                b'4
                                ~                                                                        %! SC
                                b'16
                                \revert Tie.direction                                                    %! OC2
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert Stem.direction                                                   %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='direction',
            value=abjad.Down,
            grob='tie',
            selector=selector,
            )

    @staticmethod
    def tie_from(
        *,
        selector: Selector = 'baca.pleaf(-1)',
        ) -> TieCorrectionCommand:
        r"""
        Ties from leaf.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     baca.tie_from(selector=baca.leaf(1)),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'2
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                                ~                                                                        %! TCC
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return TieCorrectionCommand(
            repeat=False,
            selector=selector,
            )

    @staticmethod
    def tie_repeat_pitches() -> MapCommand:
        """
        Ties repeat pitches.
        """
        return baca.map(
            LibraryTZ.tie(),
            baca.select().ltqruns().nontrivial(),
            )

    @staticmethod
    def tie_to(
        *,
        selector: Selector = 'baca.pleaf(0)',
        ) -> TieCorrectionCommand:
        r"""
        Ties to leaf.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     baca.tie_to(selector=baca.leaf(1)),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'2
                                ~                                                                        %! TCC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return TieCorrectionCommand(
            direction=abjad.Left,
            repeat=False,
            selector=selector,
            )

    @staticmethod
    def tie_up(
        *,
        selector: Selector = 'baca.tleaves()',
        ) -> OverrideCommand:
        r"""
        Overrides tie direction.

        ..  container:: example

            Overrides tie direction on pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.rests_around([2], [4]),
            ...     baca.stem_down(),
            ...     baca.map(baca.tie(), baca.qruns()),
            ...     baca.tie_up(),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                \override Stem.direction = #down                                         %! OC1
                                \override Tie.direction = #up                                            %! OC1
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
                                \revert Stem.direction                                                   %! OC2
                                \revert Tie.direction                                                    %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
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
            ...     baca.stem_down(),
            ...     baca.map(baca.tie(), baca.qruns()),
            ...     baca.map(baca.tie_up(), baca.tuplet(1)),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                \override Stem.direction = #down                                         %! OC1
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
                                \override Tie.direction = #up                                            %! OC1
                                b'16
                                ~                                                                        %! SC
                                [
                                b'16
                                ~                                                                        %! SC
                                ]
                                b'4
                                ~                                                                        %! SC
                                b'16
                                \revert Tie.direction                                                    %! OC2
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert Stem.direction                                                   %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='direction',
            value=abjad.Up,
            grob='tie',
            selector=selector,
            )

    @staticmethod
    def time_signature_extra_offset(
        pair: NumberPair,
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        r"""
        Overrides time signature extra offset.

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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Score.TimeSignature.extra-offset = #'(-6 . 0)            %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        assert isinstance(pair, tuple), repr(pair)
        return OverrideCommand(
            attribute='extra_offset',
            value=pair,
            context='Score',
            grob='time_signature',
            selector=selector,
            )

    @staticmethod
    def time_signature_transparent(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides time signature transparency.

        ..  container:: example

            Makes all time signatures transparent:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.time_signature_transparent(),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override Score.TimeSignature.transparent = ##t                          %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert Score.TimeSignature.transparent                                  %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='transparent',
            value=True,
            context='Score',
            grob='time_signature',
            selector=selector,
            )

    @staticmethod
    def timeline(scopes) -> TimelineScope:
        """
        Makes timeline scope.
        """
        from .LibraryNS import LibraryNS
        scopes = [LibraryNS.scope(*_) for _ in scopes]
        return TimelineScope(scopes)

    @staticmethod
    def transition(
        *markups: typing.Any,
        do_not_bookend: bool = False,
        selector: Selector = 'baca.leaves().group()',
        spanner_selector: typing.Union[MapCommand, Selector] = 'baca.tleaves()',
        tweaks: typing.List[typing.Tuple] = None
        ) -> PiecewiseCommand:
        r"""
        Makes transition text spanner.

        ..  container:: example

            Without bookend:
            
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.transition(
            ...         baca.markup.pont(),
            ...         baca.markup.ord(),
            ...         baca.markup.pont(),
            ...         baca.markup.ord(),
            ...         do_not_bookend=True,
            ...         selector=baca.leaves().enchain([5, 4, 5, 4]),
            ...     ),
            ...     baca.make_even_runs(),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.text_spanner_staff_padding(4.5),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    \override TextSpanner.staff-padding = #4.5                           %! OC1
                                    e'8
                                    [
                                    - \tweak Y-extent ##f                                                %! PWC1
                                    - \tweak bound-details.left.text \markup {                           %! PWC1
                                        \concat                                                          %! PWC1
                                            {                                                            %! PWC1
                                                \whiteout                                                %! PWC1
                                                    \upright                                             %! PWC1
                                                        pont.                                            %! PWC1
                                                \hspace                                                  %! PWC1
                                                    #0.5                                                 %! PWC1
                                            }                                                            %! PWC1
                                        }                                                                %! PWC1
                                    - \tweak arrow-width 0.25                                            %! PWC1
                                    - \tweak dash-fraction 0.25                                          %! PWC1
                                    - \tweak dash-period 1.5                                             %! PWC1
                                    - \tweak bound-details.left-broken.text ##f                          %! PWC1
                                    - \tweak bound-details.left.stencil-align-dir-y #center              %! PWC1
                                    - \tweak bound-details.right.arrow ##t                               %! PWC1
                                    - \tweak bound-details.right-broken.arrow ##f                        %! PWC1
                                    - \tweak bound-details.right-broken.padding 0                        %! PWC1
                                    - \tweak bound-details.right-broken.text ##f                         %! PWC1
                                    - \tweak bound-details.right.padding 0.5                             %! PWC1
                                    - \tweak bound-details.right.stencil-align-dir-y #center             %! PWC1
                                    \startTextSpan                                                       %! PWC1
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
                                    % [MusicVoice measure 2]                                             %! SM4
                                    g'8
                                    \stopTextSpan                                                        %! PWC1
                                    [
                                    - \tweak Y-extent ##f                                                %! PWC1
                                    - \tweak bound-details.left.text \markup {                           %! PWC1
                                        \concat                                                          %! PWC1
                                            {                                                            %! PWC1
                                                \whiteout                                                %! PWC1
                                                    \upright                                             %! PWC1
                                                        ord.                                             %! PWC1
                                                \hspace                                                  %! PWC1
                                                    #0.5                                                 %! PWC1
                                            }                                                            %! PWC1
                                        }                                                                %! PWC1
                                    - \tweak arrow-width 0.25                                            %! PWC1
                                    - \tweak dash-fraction 0.25                                          %! PWC1
                                    - \tweak dash-period 1.5                                             %! PWC1
                                    - \tweak bound-details.left-broken.text ##f                          %! PWC1
                                    - \tweak bound-details.left.stencil-align-dir-y #center              %! PWC1
                                    - \tweak bound-details.right.arrow ##t                               %! PWC1
                                    - \tweak bound-details.right-broken.arrow ##f                        %! PWC1
                                    - \tweak bound-details.right-broken.padding 0                        %! PWC1
                                    - \tweak bound-details.right-broken.text ##f                         %! PWC1
                                    - \tweak bound-details.right.padding 0.5                             %! PWC1
                                    - \tweak bound-details.right.stencil-align-dir-y #center             %! PWC1
                                    \startTextSpan                                                       %! PWC1
                <BLANKLINE>
                                    f''8
                <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    d''8
                                    \stopTextSpan                                                        %! PWC1
                                    [
                                    - \tweak Y-extent ##f                                                %! PWC1
                                    - \tweak bound-details.left.text \markup {                           %! PWC1
                                        \concat                                                          %! PWC1
                                            {                                                            %! PWC1
                                                \whiteout                                                %! PWC1
                                                    \upright                                             %! PWC1
                                                        pont.                                            %! PWC1
                                                \hspace                                                  %! PWC1
                                                    #0.5                                                 %! PWC1
                                            }                                                            %! PWC1
                                        }                                                                %! PWC1
                                    - \tweak arrow-width 0.25                                            %! PWC1
                                    - \tweak dash-fraction 0.25                                          %! PWC1
                                    - \tweak dash-period 1.5                                             %! PWC1
                                    - \tweak bound-details.left-broken.text ##f                          %! PWC1
                                    - \tweak bound-details.left.stencil-align-dir-y #center              %! PWC1
                                    - \tweak bound-details.right.arrow ##t                               %! PWC1
                                    - \tweak bound-details.right-broken.arrow ##f                        %! PWC1
                                    - \tweak bound-details.right-broken.padding 0                        %! PWC1
                                    - \tweak bound-details.right-broken.text ##f                         %! PWC1
                                    - \tweak bound-details.right.padding 0.5                             %! PWC1
                                    - \tweak bound-details.right.stencil-align-dir-y #center             %! PWC1
                                    \startTextSpan                                                       %! PWC1
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
                                    % [MusicVoice measure 4]                                             %! SM4
                                    f''8
                                    \stopTextSpan                                                        %! PWC1
                                    [
                                    - \tweak Y-extent ##f                                                %! PWC1
                                    - \tweak bound-details.left.text \markup {                           %! PWC1
                                        \concat                                                          %! PWC1
                                            {                                                            %! PWC1
                                                \whiteout                                                %! PWC1
                                                    \upright                                             %! PWC1
                                                        ord.                                             %! PWC1
                                                \hspace                                                  %! PWC1
                                                    #0.25                                                %! PWC1
                                            }                                                            %! PWC1
                                        }                                                                %! PWC1
                                    - \tweak dash-period 0                                               %! PWC1
                                    - \tweak bound-details.left-broken.text ##f                          %! PWC1
                                    - \tweak bound-details.left.stencil-align-dir-y #center              %! PWC1
                                    - \tweak bound-details.right-broken.padding 0                        %! PWC1
                                    - \tweak bound-details.right-broken.text ##f                         %! PWC1
                                    - \tweak bound-details.right.padding 1.5                             %! PWC1
                                    - \tweak bound-details.right.stencil-align-dir-y #center             %! PWC1
                                    \startTextSpan                                                       %! PWC1
                <BLANKLINE>
                                    e'8
                <BLANKLINE>
                                    d''8
                                    ]
                                    \stopTextSpan                                                        %! PWC1
                                    \revert TextSpanner.staff-padding                                    %! OC2
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            With bookend:
            
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.transition(
            ...         baca.markup.pont(),
            ...         baca.markup.ord(),
            ...         selector=baca.leaves().enchain([8]),
            ...     ),
            ...     baca.make_even_runs(),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.text_spanner_staff_padding(4.5),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    \override TextSpanner.staff-padding = #4.5                           %! OC1
                                    e'8
                                    [
                                    - \tweak Y-extent ##f                                                %! PWC1
                                    - \tweak bound-details.left.text \markup {                           %! PWC1
                                        \concat                                                          %! PWC1
                                            {                                                            %! PWC1
                                                \whiteout                                                %! PWC1
                                                    \upright                                             %! PWC1
                                                        pont.                                            %! PWC1
                                                \hspace                                                  %! PWC1
                                                    #0.5                                                 %! PWC1
                                            }                                                            %! PWC1
                                        }                                                                %! PWC1
                                    - \tweak arrow-width 0.25                                            %! PWC1
                                    - \tweak dash-fraction 0.25                                          %! PWC1
                                    - \tweak dash-period 1.5                                             %! PWC1
                                    - \tweak bound-details.left-broken.text ##f                          %! PWC1
                                    - \tweak bound-details.left.stencil-align-dir-y #center              %! PWC1
                                    - \tweak bound-details.right.arrow ##t                               %! PWC1
                                    - \tweak bound-details.right-broken.arrow ##f                        %! PWC1
                                    - \tweak bound-details.right-broken.padding 0                        %! PWC1
                                    - \tweak bound-details.right-broken.text ##f                         %! PWC1
                                    - \tweak bound-details.right.padding 0.5                             %! PWC1
                                    - \tweak bound-details.right.stencil-align-dir-y #center             %! PWC1
                                    \startTextSpan                                                       %! PWC1
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
                                    % [MusicVoice measure 2]                                             %! SM4
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
                                    % [MusicVoice measure 3]                                             %! SM4
                                    d''8
                                    \stopTextSpan                                                        %! PWC1
                                    [
                                    - \tweak Y-extent ##f                                                %! PWC1
                                    - \tweak bound-details.left.text \markup {                           %! PWC1
                                        \concat                                                          %! PWC1
                                            {                                                            %! PWC1
                                                \whiteout                                                %! PWC1
                                                    \upright                                             %! PWC1
                                                        ord.                                             %! PWC1
                                                \hspace                                                  %! PWC1
                                                    #0.5                                                 %! PWC1
                                            }                                                            %! PWC1
                                        }                                                                %! PWC1
                                    - \tweak arrow-width 0.25                                            %! PWC1
                                    - \tweak dash-fraction 0.25                                          %! PWC1
                                    - \tweak dash-period 1.5                                             %! PWC1
                                    - \tweak bound-details.left-broken.text ##f                          %! PWC1
                                    - \tweak bound-details.left.stencil-align-dir-y #center              %! PWC1
                                    - \tweak bound-details.right.arrow ##t                               %! PWC1
                                    - \tweak bound-details.right-broken.arrow ##f                        %! PWC1
                                    - \tweak bound-details.right-broken.padding 0                        %! PWC1
                                    - \tweak bound-details.right-broken.text ##f                         %! PWC1
                                    - \tweak bound-details.right.padding 0.5                             %! PWC1
                                    - \tweak bound-details.right.stencil-align-dir-y #center             %! PWC1
                                    - \tweak bound-details.right.text \markup {                          %! PWC1
                                        \concat                                                          %! PWC1
                                            {                                                            %! PWC1
                                                \hspace                                                  %! PWC1
                                                    #0.0                                                 %! PWC1
                                                \whiteout                                                %! PWC1
                                                    \upright                                             %! PWC1
                                                        pont.                                            %! PWC1
                                            }                                                            %! PWC1
                                        }                                                                %! PWC1
                                    \startTextSpan                                                       %! PWC1
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
                                    % [MusicVoice measure 4]                                             %! SM4
                                    f''8
                                    [
                <BLANKLINE>
                                    e'8
                <BLANKLINE>
                                    d''8
                                    ]
                                    \stopTextSpan                                                        %! PWC1
                                    \revert TextSpanner.staff-padding                                    %! OC2
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        """
        from .LibraryAF import LibraryAF
        from .LibraryNS import LibraryNS
        indicators: typing.List[typing.Union[abjad.Markup, tuple]] = []
        for markup in markups[:-1]:
            pair = (markup, LibraryAF.dashed_arrow())
            indicators.append(pair)
        if do_not_bookend:
            indicators.append(markups[-1])
        else:
            pair = (markups[-1], LibraryAF.dashed_arrow())
            indicators.append(pair)
        text_spanner = abjad.TextSpanner()
        return LibraryNS.piecewise(
            text_spanner,
            indicators,
            selector,
            bookend=not(do_not_bookend),
            spanner_selector=spanner_selector,
            tweaks=tweaks,
            )

    @staticmethod
    def tremolo_down(
        n: Number,
        *,
        selector: Selector = 'baca.tleaves()',
        ) -> OverrideCommand:
        """
        Overrides stem tremolo extra offset.
        """
        pair = (0, -n)
        return OverrideCommand(
            attribute='extra_offset',
            value=str(pair),
            grob='stem_tremolo',
            selector=selector,
            )

    @staticmethod
    def trill_spanner(
        string: str = None,
        *,
        harmonic: bool = None,
        left_broken: bool = None,
        right_broken: bool = None,
        selector: Selector = 'baca.tleaves().with_next_leaf()',
        ) -> SpannerCommand:
        r"""
        Attaches trill spanner.

        ..  container:: example

            Attaches trill spanner to trimmed leaves (leaked to the right):

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.trill_spanner(),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches trill spanner to trimmed leaves (leaked to the right) in
            every equipitch run:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.trill_spanner(), baca.qruns()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
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
            ...     baca.map(baca.trill_spanner(), baca.runs()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
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
            ...     baca.map(baca.trill_spanner(string='Eb4'), baca.qrun(0)),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
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
            ...     baca.map(baca.trill_spanner(string='Eb4'), baca.qruns()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
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
            ...     baca.map(baca.trill_spanner(string='M2'), baca.qruns()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        if string is None:
            interval = None
            pitch = None
        else:
            try:
                interval = None
                pitch = abjad.NamedPitch(string)
            except ValueError:
                interval = abjad.NamedInterval(string)
                pitch = None
        return SpannerCommand(
            left_broken=left_broken,
            right_broken=right_broken,
            spanner=abjad.TrillSpanner(
                interval=interval,
                is_harmonic=harmonic,
                pitch=pitch,
                ),
            selector=selector,
            )

    @staticmethod
    def trill_spanner_staff_padding(
        n: Number,
        *,
        selector: Selector = 'baca.tleaves().with_next_leaf()',
        ) -> OverrideCommand:
        """
        Overrides trill spanner staff padding.
        """
        return OverrideCommand(
            attribute='staff_padding',
            value=n,
            grob='trill_spanner',
            selector=selector,
            )

    @staticmethod
    def tuplet_bracket_down(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides tuplet bracket direction.

        ..  container:: example

            Overrides tuplet bracket direction on leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     baca.tuplet_bracket_down(),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                \override TupletBracket.direction = #down                                %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                                \revert TupletBracket.direction                                          %! OC2
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
            ...     baca.map(baca.tuplet_bracket_down(), baca.tuplet(1)),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \override TupletBracket.direction = #down                                %! OC1
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
                                \revert TupletBracket.direction                                          %! OC2
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='direction',
            value=abjad.Down,
            grob='tuplet_bracket',
            selector=selector,
            )

    @staticmethod
    def tuplet_bracket_extra_offset(
        pair: NumberPair,
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        r"""
        Overrides tuplet bracket extra offset.

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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override TupletBracket.extra-offset = #'(-1 . 0)                  %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \once \override TupletBracket.extra-offset = #'(-1 . 0)                  %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='extra_offset',
            value=pair,
            grob='tuplet_bracket',
            selector=selector,
            )

    @staticmethod
    def tuplet_bracket_padding(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides tuplet bracket padding.
        """
        return OverrideCommand(
            attribute='padding',
            value=n,
            grob='tuplet_bracket',
            selector=selector,
            )

    @staticmethod
    def tuplet_bracket_shorten_pair(
        pair: NumberPair,
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides tuplet bracket shorten pair.
        """
        return OverrideCommand(
            attribute='shorten_pair',
            value=pair,
            grob='tuplet_bracket',
            selector=selector,
            )

    @staticmethod
    def tuplet_bracket_staff_padding(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides tuplet bracket staff padding.

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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
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
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                            \times 4/5 {
                                a'16
                                r4
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='staff_padding',
            value=n,
            grob='tuplet_bracket',
            selector=selector,
            )

    @staticmethod
    def tuplet_bracket_up(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides tuplet bracket direction.

        ..  container:: example

            Override tuplet bracket direction on leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     baca.tuplet_bracket_up(),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                \override TupletBracket.direction = #up                                  %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                                \revert TupletBracket.direction                                          %! OC2
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
            ...     baca.map(baca.tuplet_bracket_up(), baca.tuplet(1)),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \override TupletBracket.direction = #up                                  %! OC1
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
                                \revert TupletBracket.direction                                          %! OC2
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='direction',
            value=abjad.Up,
            grob='tuplet_bracket',
            selector=selector,
            )

    @staticmethod
    def tuplet_number_denominator(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides tuplet number text.
        """
        return OverrideCommand(
            attribute='text',
            value='tuplet-number::calc-denominator-text',
            grob='tuplet_number',
            selector=selector,
            )

    @staticmethod
    def tuplet_number_extra_offset(
        pair: NumberPair,
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        r"""
        Overrides tuplet number extra offset.

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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                \once \override TupletNumber.extra-offset = #'(-1 . 0)                   %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \once \override TupletNumber.extra-offset = #'(-1 . 0)                   %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='extra_offset',
            value=pair,
            grob='tuplet_number',
            selector=selector,
            )

    @staticmethod
    def untie_to(
        *,
        selector: Selector = 'baca.pleaf(0)',
        ) -> TieCorrectionCommand:
        r"""
        Unties to leaf.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_tied_notes(),
            ...     baca.untie_to(selector=baca.leaf(2)),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'2
                                ~
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'2
                                ~
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return TieCorrectionCommand(
            direction=abjad.Left,
            selector=selector,
            untie=True,
            )

    @staticmethod
    def up_arpeggio(
        *,
        selector: Selector = 'baca.chead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches up-arpeggio.

        ..  container:: example

            Attaches up-arpeggios to chord head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.up_arpeggio(),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
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
                                <ef'' e'' fs'''>8
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                <g' af''>8
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
            ...     baca.up_arpeggio(selector=baca.cheads()[-2:]),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
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
        return IndicatorCommand(
            indicators=[abjad.Arpeggio(direction=abjad.Up)],
            selector=selector,
            )

    @staticmethod
    def up_bow(
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches up-bow.

        ..  container:: example

            Attaches up-bow to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     baca.up_bow(),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                c'16
                                -\upbow                                                                  %! IC
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches up-bow to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.up_bow(selector=baca.pheads()),
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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return IndicatorCommand(
            indicators=[abjad.Articulation('upbow')],
            selector=selector,
            )

    @staticmethod
    def very_long_fermata(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches very long fermata.

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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
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
            ...         selector=baca.tuplets()[1:2].phead(0),
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
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return IndicatorCommand(
            indicators=[abjad.Articulation('verylongfermata')],
            selector=selector,
            )

    @staticmethod
    def voice_four(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r"""
        Makes LilyPond ``\voiceFour`` command.
        """
        literal = abjad.LilyPondLiteral(r'\voiceFour')
        return IndicatorCommand(
            indicators=[literal],
            selector=selector,
            )

    @staticmethod
    def voice_one(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r"""
        Makes LilyPond ``\voiceOne`` command.
        """
        literal = abjad.LilyPondLiteral(r'\voiceOne')
        return IndicatorCommand(
            indicators=[literal],
            selector=selector,
            )

    @staticmethod
    def voice_three(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r"""
        Makes LilyPond ``\voiceThree`` command.
        """
        literal = abjad.LilyPondLiteral(r'\voiceThree')
        return IndicatorCommand(
            indicators=[literal],
            selector=selector,
            )

    @staticmethod
    def voice_two(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r"""
        Makes LilyPond ``\voiceTwo`` command.
        """
        literal = abjad.LilyPondLiteral(r'\voiceTwo')
        return IndicatorCommand(
            indicators=[literal],
            selector=selector,
            )

    @staticmethod
    def volta(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> VoltaCommand:
        r"""
        Makes volta container and extends container with ``selector`` output.

        ..  container:: example

            Wraps stage 1 (global skips 1 and 2) in volta container:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
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
            ...     'GlobalSkips',
            ...     baca.volta(selector=baca.skips()[1:3]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                            \repeat volta 2
                            {
                <BLANKLINE>
                                % [GlobalSkips measure 2]                                                %! SM4
                                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                                s1 * 3/8
                <BLANKLINE>
                                % [GlobalSkips measure 3]                                                %! SM4
                                \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                                s1 * 1/2
                            }
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
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
                                % [MusicVoice measure 2]                                                 %! SM4
                                e''8
                                [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                f''8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
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
                                % [MusicVoice measure 4]                                                 %! SM4
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
            ...     ('MusicVoice', (1, 3)),
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
            ...     ('GlobalSkips', 2),
            ...     baca.volta(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                            \repeat volta 2
                            {
                <BLANKLINE>
                                % [GlobalSkips measure 2]                                                %! SM4
                                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                                s1 * 3/8
                <BLANKLINE>
                                % [GlobalSkips measure 3]                                                %! SM4
                                \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                                s1 * 1/2
                            }
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
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
                                % [MusicVoice measure 2]                                                 %! SM4
                                e''8
                                [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                f''8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
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
                                % [MusicVoice measure 4]                                                 %! SM4
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

        """
        return VoltaCommand(selector=selector)
