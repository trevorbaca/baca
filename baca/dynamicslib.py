"""
Dynamics library.
"""
import abjad
import baca
import typing
from . import library
from . import typings
from .Command import Command
from .Command import Map
from .Command import Suite
from .IndicatorCommand import IndicatorCommand
from .OverrideCommand import OverrideCommand
from .PiecewiseCommand import PiecewiseCommand
from .PiecewiseIndicatorCommand import PiecewiseIndicatorCommand
from .SchemeManifest import SchemeManifest


def dynamic(
    dynamic: typing.Union[str, abjad.Dynamic],
    # TODO: add tweaks
    *,
    selector: typings.Selector = 'baca.phead(0)',
    redundant: bool = None,
    ) -> IndicatorCommand:
    r"""
    Attaches dynamic.

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
                            \f                                                                       %! IC
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

        Attaches dynamic to pitched head 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
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
                            \f                                                                       %! IC
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

        Attaches effort dynamic to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('"f"'),
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
                            \effort_f                                                                %! IC
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
    scheme_manifest = SchemeManifest()
    if isinstance(dynamic, str):
        if dynamic == 'niente':
            indicator = _local_niente()
        elif dynamic in scheme_manifest.dynamics:
            name = scheme_manifest.dynamic_to_steady_state(dynamic)
            command = '\\' + dynamic
            first = dynamic.split('_')[0]
            if first in ('sfz', 'sffz', 'sfffz'):
                sforzando = True
            else:
                sforzando = False
            name_is_textual = not(sforzando)
            indicator = abjad.Dynamic(
                name,
                command=command,
                name_is_textual=name_is_textual,
                sforzando=sforzando,
                )
        elif dynamic.startswith('"'):
            assert dynamic.endswith('"')
            dynamic = dynamic.strip('"')
            command = rf'\effort_{dynamic}'
            indicator = abjad.Dynamic(f'{dynamic}', command=command)
        else:
            indicator = abjad.Dynamic(dynamic)
    else:
        assert isinstance(dynamic, abjad.Dynamic), repr(dynamic)
        indicator = dynamic
    return IndicatorCommand(
        context='Voice',
        indicators=[indicator],
        redundant=redundant,
        selector=selector,
        )

def dynamic_down(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches dynamic-down command.

    ..  container:: example

        Attaches dynamic-down command to leaf 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.dynamic_down(),
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
                            \dynamicDown                                                             %! IC
                            r8
                            c'16
                            \p                                                                       %! IC
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
                            \f                                                                       %! IC
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

        Attaches dynamic-down command to leaf 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.dynamic_down(selector=baca.tuplets()[1:2].leaf(0)),
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
                            \p                                                                       %! IC
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
                            \dynamicDown                                                             %! IC
                            fs''16
                            \f                                                                       %! IC
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
        indicators=[abjad.LilyPondLiteral(r'\dynamicDown')],
        selector=selector,
        )

def dynamic_shift(
    dynamic: typing.Union[str, abjad.Dynamic],
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> Suite:
    """
    Shifts dynamic to left by calculated width of dynamic.
    """
    dynamic = abjad.Dynamic(dynamic)
    width = dynamic._to_width[dynamic.name]
    extra_offset_x = -width
    return library.suite(
        dynamic_text_extra_offset(
            (extra_offset_x, 0),
            selector=selector,
            ),
        dynamic_text_x_extent_zero(
            selector=selector,
            ),
        )

# TODO: test and document?
# TODO: appears not to do anything?
def dynamic_text_center(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> Suite:
    """
    Overrides dynamic text self-alignment-X and dynamic text X-extent.
    """
    command_1 = OverrideCommand(
        attribute='self_alignment_X',
        value=abjad.Center,
        grob='dynamic_text',
        selector=selector,
        )
    command_2 = dynamic_text_x_extent_zero(
        selector=selector,
        )
    return library.suite(
        command_1,
        command_2,
        )

def dynamic_text_extra_offset(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    r"""
    Overrides dynamic text extra offset.

    ..  container:: example

        Overrides dynamic text extra offset on pitched leaf 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].pleaf(0)),
        ...     baca.dynamic_text_extra_offset((-3, 0)),
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
                            \once \override DynamicText.extra-offset = #'(-3 . 0)                    %! OC1
                            c'16
                            \p                                                                       %! IC
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
                            \f                                                                       %! IC
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

        Overrides dynamic text extra offset on leaf 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].leaf(0)),
        ...     baca.dynamic_text_extra_offset(
        ...         (-3, 0),
        ...         selector=baca.tuplets()[1:2].leaf(0),
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
                            \p                                                                       %! IC
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
                            \once \override DynamicText.extra-offset = #'(-3 . 0)                    %! OC1
                            fs''16
                            \f                                                                       %! IC
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

        Raise exception on nonpair input:

        >>> baca.dynamic_text_extra_offset(2)
        Traceback (most recent call last):
            ...
        Exception: dynamic text extra offset must be pair (not 2).

    """
    if not isinstance(pair, tuple):
        raise Exception(
            f'dynamic text extra offset must be pair (not {pair}).'
            )
    if len(pair) != 2:
        raise Exception(
            f'dynamic text extra offset must be pair (not {pair}).'
            )
    return OverrideCommand(
        attribute='extra_offset',
        value=pair,
        grob='dynamic_text',
        selector=selector,
        )

# TODO: test and document?
# TODO: appears not to do anything?
def dynamic_text_left(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> Suite:
    """
    Overrides dynamic text self-alignment-X and dynamic text X-extent.
    """
    command_1 = OverrideCommand(
        attribute='self_alignment_X',
        value=abjad.Left,
        grob='dynamic_text',
        selector=selector,
        )
    command_2 = dynamic_text_x_extent_zero(
        selector=selector,
        )
    return library.suite(
        command_1,
        command_2,
        )

def dynamic_text_parent_alignment_x(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    """
    Overrides dynamic text parent alignment X to ``n``.
    """
    return OverrideCommand(
        attribute='parent_alignment_X',
        value=n,
        grob='dynamic_text',
        selector=selector,
        )

# TODO: test and document?
# TODO: appears not to do anything?
def dynamic_text_right(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> Suite:
    """
    Overrides dynamic text self-alignment-X and dynamic text X-extent.
    """
    command_1 = OverrideCommand(
        attribute='self_alignment_X',
        value=abjad.Right,
        grob='dynamic_text',
        selector=selector,
        )
    command_2 = dynamic_text_x_extent_zero(
        selector=selector,
        )
    return library.suite(
        command_1,
        command_2,
        )

def dynamic_text_stencil_false(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    """
    Overrides dynamic text stencil.
    """
    return OverrideCommand(
        attribute='stencil',
        value=False,
        grob='dynamic_text',
        selector=selector,
        )

def dynamic_text_transparent(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    """
    Overrides dynamic text transparency.
    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='dynamic_text',
        selector=selector,
        )

def dynamic_text_x_extent_zero(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    """
    Overrides dynamic text X-extent.
    """
    return OverrideCommand(
        attribute='X_extent',
        value=(0, 0),
        grob='dynamic_text',
        selector=selector,
        )

def dynamic_text_x_offset(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    """
    Overrides dynamic text X-extent.
    """
    return OverrideCommand(
        attribute='X_offset',
        value=n,
        grob='dynamic_text',
        selector=selector,
        )

def dynamic_text_y_offset(
    n: typings.Number,
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> OverrideCommand:
    """
    Overrides dynamic text Y-extent.
    """
    return OverrideCommand(
        attribute='Y_offset',
        value=n,
        grob='dynamic_text',
        selector=selector,
        )

def dynamic_up(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches dynamic-up command.

    ..  container:: example

        Attaches dynamic-up command to leaf 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.dynamic_up(),
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
                            \dynamicUp                                                               %! IC
                            r8
                            c'16
                            \p                                                                       %! IC
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
                            \f                                                                       %! IC
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

        Attaches dynamic-up command to leaf 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.dynamic_up(selector=baca.tuplets()[1:2].leaf(0)),
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
                            \p                                                                       %! IC
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
                            \dynamicUp                                                               %! IC
                            fs''16
                            \f                                                                       %! IC
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
        indicators=[abjad.LilyPondLiteral(r'\dynamicUp')],
        selector=selector,
        )

_local_dynamic = dynamic

def dynamic_trend(
    dynamic_trend: typing.Union[str, abjad.DynamicTrend],
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches hairpin start.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.dynamic(
        ...         'ppp',
        ...         selector=baca.leaves().partition_by_counts(
        ...             [4, 3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             )[abjad.index([0], 2)].map(baca.leaf(0)),
        ...         ),
        ...     baca.dynamic_trend(
        ...         '<',
        ...         selector=baca.leaves().partition_by_counts(
        ...             [4, 3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             )[abjad.index([0], 2)].map(baca.leaf(0)),
        ...         ),
        ...     baca.dynamic(
        ...         'pp',
        ...         selector=baca.leaves().partition_by_counts(
        ...             [4, 3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             )[abjad.index([1], 2)].map(baca.leaf(0)),
        ...         ),
        ...     baca.dynamic_trend(
        ...         '>',
        ...         selector=baca.leaves().partition_by_counts(
        ...             [4, 3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             )[abjad.index([1], 2)][:-1].map(baca.leaf(0)),
        ...         ),
        ...     baca.dynamic_trend(
        ...         '>o',
        ...         selector=baca.leaves().partition_by_counts(
        ...             [4, 3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             )[abjad.index([1], 2)][-1:].map(baca.leaf(0)),
        ...         ),
        ...     baca.dynamic(
        ...         abjad.Dynamic('niente', command=r'\!'),
        ...         selector=baca.leaf(-1),
        ...         ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            e'8
                            \ppp                                                                     %! SM8:EXPLICIT_DYNAMIC:IC
                            \<                                                                       %! IC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            g'8
                            \pp                                                                      %! SM8:EXPLICIT_DYNAMIC:IC
                            \>                                                                       %! IC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            d''8
                            \ppp                                                                     %! SM8:EXPLICIT_DYNAMIC:IC
                            \<                                                                       %! IC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            f''8
                            \pp                                                                      %! SM8:EXPLICIT_DYNAMIC:IC
                            - \tweak circled-tip ##t                                                 %! IC
                            \>                                                                       %! IC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            d''8
                            \!                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    if isinstance(dynamic_trend, str):
        indicator = abjad.DynamicTrend(dynamic_trend)
    else:
        indicator = dynamic_trend
    assert isinstance(indicator, abjad.DynamicTrend), repr(indicator)
    return IndicatorCommand(
        context='Voice',
        indicators=[indicator],
        selector=selector,
        )

_local_dynamic_trend = dynamic_trend


def dynamics(string: str) -> typing.List[abjad.Dynamic]:
    r"""
    Makes dynamics from ``string``.

    ..  container::

        >>> baca.dynamics('ff p f pp')
        [Dynamic('ff'), Dynamic('p'), Dynamic('f'), Dynamic('pp')]

    """
    return [abjad.Dynamic(_) for _ in string.split()]

_local_dynamics = dynamics

# TODO: completely refactor;
#       remove bookend keyword altogether;
#       add left_broken, right_broken keywords;
def hairpin_chain(
    *dynamics: typing.Any,
    bookend: typing.Union[bool, int] = False,
    pieces: typings.Selector = 'baca.tleaves().group()',
    selector: typings.Selector = 'baca.tleaves()'
    ) -> PiecewiseCommand:
    r"""
    Makes enchained hairpin.

    ..  container:: example

        Partitions leaves:
        
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin_chain(
        ...         baca.dynamics('p f'),
        ...         pieces=baca.leaves().partition_by_counts(
        ...             [3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             ),
        ...         ),
        ...     baca.make_even_divisions(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            [
                            \p                                                                       %! PWC1
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e''8
                            ]
                            \f                                                                       %! PWC1
                            \>                                                                       %! PWC1
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            ]
                            \p                                                                       %! PWC1
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e''8
                            \f                                                                       %! PWC1
                            \>                                                                       %! PWC1
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            \p                                                                       %! PWC1
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends piece -1:
        
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin_chain(
        ...         baca.dynamics('p f'),
        ...         bookend=-1,
        ...         pieces=baca.leaves().partition_by_counts(
        ...             [3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             ),
        ...         ),
        ...     baca.make_even_divisions(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            [
                            \p                                                                       %! PWC1
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e''8
                            ]
                            \f                                                                       %! PWC1
                            \>                                                                       %! PWC1
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            ]
                            \p                                                                       %! PWC1
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e''8
                            \f                                                                       %! PWC1
                            \>                                                                       %! PWC1
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            \p                                                                       %! PWC1
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            d''8
                            ]
                            \f                                                                       %! PWC1
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends each piece:
        
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin_chain(
        ...         baca.dynamics('p f'),
        ...         bookend=True,
        ...         pieces=baca.leaves().partition_by_counts(
        ...             [3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             ),
        ...         ),
        ...     baca.make_even_divisions(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            [
                            \p                                                                       %! PWC1
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            f'8
                            \f                                                                       %! PWC1
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e''8
                            ]
                            \f                                                                       %! PWC1
                            \>                                                                       %! PWC1
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            f''8
                            \p                                                                       %! PWC1
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            ]
                            \p                                                                       %! PWC1
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            f'8
                            \f                                                                       %! PWC1
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e''8
                            \f                                                                       %! PWC1
                            \>                                                                       %! PWC1
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            f''8
                            \p                                                                       %! PWC1
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            \p                                                                       %! PWC1
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            d''8
                            ]
                            \f                                                                       %! PWC1
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Groups leaves by measures:
        
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin_chain(
        ...         baca.dynamics('p f'),
        ...         pieces=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            [
                            \p                                                                       %! PWC1
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            g'8
                            \f                                                                       %! PWC1
                            [
                            \>                                                                       %! PWC1
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            d''8
                            \p                                                                       %! PWC1
                            [
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            f''8
                            \f                                                                       %! PWC1
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends piece -1:
        
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin_chain(
        ...         baca.dynamics('p f'),
        ...         bookend=-1,
        ...         pieces=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            [
                            \p                                                                       %! PWC1
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            g'8
                            \f                                                                       %! PWC1
                            [
                            \>                                                                       %! PWC1
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            d''8
                            \p                                                                       %! PWC1
                            [
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            f''8
                            \f                                                                       %! PWC1
                            [
                            \>                                                                       %! PWC1
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            d''8
                            ]
                            \p                                                                       %! PWC1
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends each piece:
        
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin_chain(
        ...         baca.dynamics('p f'),
        ...         bookend=True,
        ...         pieces=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            [
                            \p                                                                       %! PWC1
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e''8
                            ]
                            \f                                                                       %! PWC1
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            g'8
                            \f                                                                       %! PWC1
                            [
                            \>                                                                       %! PWC1
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            e'8
                            ]
                            \p                                                                       %! PWC1
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            d''8
                            \p                                                                       %! PWC1
                            [
                            \<                                                                       %! PWC1
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            g'8
                            ]
                            \f                                                                       %! PWC1
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            f''8
                            \f                                                                       %! PWC1
                            [
                            \>                                                                       %! PWC1
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PWC3
                            d''8
                            ]
                            \p                                                                       %! PWC1
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    dynamics_: typing.List[abjad.Dynamic] = []
    for dynamic in dynamics:
        if isinstance(dynamic, (list, tuple)):
            dynamics_.extend(dynamic)
        else:
            dynamics_.append(dynamic)
    for dynamic in dynamics_:
        assert isinstance(dynamic, abjad.Dynamic), repr(dynamic)
    spanner = abjad.Hairpin()
    return library.piecewise(
        spanner,
        dynamics_,
        pieces,
        bookend=bookend,
        selector=selector,
        )


def hairpin_indicator_chain(
    *dynamics: typing.Any,
    bookend: typing.Union[bool, int] = False,
    pieces: typings.Selector = 'baca.tleaves().group()',
    selector: typings.Selector = 'baca.tleaves()'
    ) -> PiecewiseCommand:
    r"""
    Makes enchained hairpin with indicators.

    ..  container:: example

        Partitions leaves:
        
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin_indicator_chain(
        ...         baca.dynamics('p f'),
        ...         pieces=baca.leaves().partition_by_counts(
        ...             [3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             ),
        ...         ),
        ...     baca.make_even_divisions(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends piece -1:
        
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin_indicator_chain(
        ...         baca.dynamics('p f'),
        ...         bookend=-1,
        ...         pieces=baca.leaves().partition_by_counts(
        ...             [3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             ),
        ...         ),
        ...     baca.make_even_divisions(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends each piece:
        
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin_indicator_chain(
        ...         baca.dynamics('p f'),
        ...         bookend=True,
        ...         pieces=baca.leaves().partition_by_counts(
        ...             [3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             ),
        ...         ),
        ...     baca.make_even_divisions(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Groups leaves by measures:
        
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin_indicator_chain(
        ...         baca.dynamics('p f'),
        ...         pieces=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends piece -1:
        
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin_indicator_chain(
        ...         baca.dynamics('p f'),
        ...         bookend=-1,
        ...         pieces=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends each piece:
        
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin_indicator_chain(
        ...         baca.dynamics('p f'),
        ...         bookend=True,
        ...         pieces=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    dynamics_: typing.List[abjad.Dynamic] = []
    for dynamic in dynamics:
        if isinstance(dynamic, (list, tuple)):
            dynamics_.extend(dynamic)
        else:
            dynamics_.append(dynamic)
    for dynamic in dynamics_:
        assert isinstance(dynamic, abjad.Dynamic), repr(dynamic)
#    return library.piecewise(
#        spanner,
#        dynamics_,
#        pieces,
#        bookend=bookend,
#        selector=selector,
#        )
    return PiecewiseIndicatorCommand(
        bookend=bookend,
        indicators=dynamics,
        pieces=pieces,
        selector=selector,
        )


def hairpin_shorten_pair(
    pair: typings.NumberPair,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides hairpin shorten pair.
    """
    return OverrideCommand(
        attribute='shorten_pair',
        value=pair,
        grob='hairpin',
        selector=selector,
        )

def hairpin_start_shift(
    dynamic: typing.Union[str, abjad.Dynamic],
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> Suite:
    """
    Shifts hairpin start dynamic to left by width of dynamic.
    """
    dynamic = abjad.Dynamic(dynamic)
    width = dynamic._to_width[dynamic.name]
    extra_offset_x = -width
    hairpin_shorten_left = width - 1.25
    return library.suite(
        dynamic_text_extra_offset((extra_offset_x, 0)),
        dynamic_text_x_extent_zero(),
        hairpin_shorten_pair((hairpin_shorten_left, 0)),
        )

def hairpin_stencil_false(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides hairpin stencil.
    """
    return OverrideCommand(
        attribute='stencil',
        value=False,
        grob='hairpin',
        selector=selector,
        )

def hairpin_transparent(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> OverrideCommand:
    """
    Overrides hairpin transparency.
    """
    return OverrideCommand(
        attribute='transparent',
        value=True,
        grob='hairpin',
        selector=selector,
        )

def measure_swells(
    dynamics: typing.Union[str, typing.List[abjad.Dynamic]],
    counts: typing.List[int] = [1],
    *,
    al_niente: bool = None,
    ) -> typing.List[IndicatorCommand]:
    r"""
    Attaches swell dynamics for tleaves grouped by measure ``counts``.

    ..  container:: example

        Swells every measure:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.suite(
        ...         *baca.measure_swells('p f'),
        ...         baca.dynamic('p', selector=baca.pleaf(-1)),
        ...         ),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \<                                                                       %! IC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            g'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \>                                                                       %! IC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            d''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \<                                                                       %! IC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            f''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \>                                                                       %! IC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            d''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Swells measure groups:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=3 * [(4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.suite(
        ...         *baca.measure_swells('p f', [2, 1]),
        ...         baca.dynamic('p', selector=baca.pleaf(-1)),
        ...         ),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 6]                                                    %! SM4
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \<                                                                       %! IC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            d''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \>                                                                       %! IC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            f''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \<                                                                       %! IC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 5]                                                 %! SM4
                            f'8
                            [
            <BLANKLINE>
                            c''8
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 6]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            e'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \>                                                                       %! IC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            f'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Terminates al niente:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
        ...     baca.suite(
        ...         *baca.measure_swells('p f', al_niente=True),
        ...         baca.dynamic(baca.niente(), selector=baca.rleaves()[-1]),
        ...         ),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \<                                                                       %! IC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            g'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \>                                                                       %! IC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            d''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \<                                                                       %! IC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            f''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            - \tweak circled-tip ##t                                                 %! IC
                            \>                                                                       %! IC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            d''8
                            \!                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    assert all(isinstance(_, int) for _ in counts), repr(counts)
    if isinstance(dynamics, str):
        dynamics_ = _local_dynamics(dynamics)
    else:
        dynamics_ = dynamics
    assert all(isinstance(_, abjad.Dynamic) for _ in dynamics_)
    if len(dynamics_) != 2:
        raise Exception(f'only two dynamics (not {dynamics}).')
    trough, peak = dynamics_
    if peak.ordinal <= trough.ordinal:
        raise Exception(f'trough ({trough}) must be less than peak ({peak}).')
    selector = baca.select().tleaves()
    selector = selector.group_by_measure()
    selector = selector.partition_by_counts(
        counts,
        cyclic=True,
        overhang=True,
        )

    commands = []
    # every trough and every crescendo
    selector_ = selector[abjad.index([0], 2)]
    selector_ = selector_.map(baca.select().leaf(0))
    command = _local_dynamic(
        trough,
        selector=selector_
        )
    commands.append(command)
    command = _local_dynamic_trend(
        '<',
        selector=selector_
        )
    commands.append(command)

    # every peak
    selector_ = selector[abjad.index([1], 2)]
    selector_ = selector_.map(baca.select().leaf(0))
    command = _local_dynamic(
        peak,
        selector=selector_
        )
    commands.append(command)

    # all but last decrescendo
    selector_ = selector[abjad.index([1], 2)]
    selector_ = selector_[:-1]
    selector_ = selector_.map(baca.select().leaf(0))
    command = _local_dynamic_trend(
        '>',
        selector=selector_
        )
    commands.append(command)

    # last decrescendo
    selector_ = selector[abjad.index([1], 2)]
    selector_ = selector_[-1:]
    selector_ = selector_.map(baca.select().leaf(0))
    if al_niente:
        shape = '>o'
    else:
        shape = '>'
    command = _local_dynamic_trend(
        shape,
        selector=selector_
        )
    commands.append(command)

    return commands


class NewHairpinCommand(Command):
    """
    New hairpin command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_dynamic_trend',
        '_lone_dynamic',
        '_right_broken',
        '_start_dynamic',
        '_start_selector',
        '_stop_dynamic',
        '_stop_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        dynamic_trend: abjad.DynamicTrend,
        *,
        lone_dynamic: bool = True,
        right_broken: bool = None,
        selector: typings.Selector = 'baca.teaves()',
        start_dynamic: abjad.Dynamic = None,
        start_selector: typings.Selector = 'baca.leaf(0)',
        stop_dynamic: abjad.Dynamic = None,
        stop_selector: typings.Selector = 'baca.leaf(-1)',
        ) -> None:
        Command.__init__(self, selector=selector)
        assert isinstance(dynamic_trend, abjad.DynamicTrend)
        self._dynamic_trend = dynamic_trend
        if lone_dynamic is not None:
            lone_dynamic = bool(lone_dynamic)
        self._lone_dynamic = lone_dynamic
        if right_broken is not None:
            right_broken = bool(right_broken)
        self._right_broken = right_broken
        if start_dynamic is not None:
            assert isinstance(start_dynamic, abjad.Dynamic)
        self._start_dynamic = start_dynamic
        if start_selector is not None:
            assert isinstance(start_selector, abjad.Expression)
        self._start_selector = start_selector
        if stop_dynamic is not None:
            assert isinstance(stop_dynamic, abjad.Dynamic)
        self._stop_dynamic = stop_dynamic
        if stop_selector is not None:
            assert isinstance(stop_selector, abjad.Expression)
        self._stop_selector = stop_selector
        self._tags = [abjad.Tag('BACA_HAIRPIN')]

    ### PUBLIC PROPERTIES ###

    @property
    def dynamic_trend(self) -> abjad.DynamicTrend:
        """
        Gets dynamic trend.
        """
        return self._dynamic_trend

    @property
    def lone_dynamic(self) -> typing.Optional[bool]:
        """
        Is true when command attaches start dynamic to lone leaf.
        """
        return self._lone_dynamic

    @property
    def right_broken(self) -> typing.Optional[bool]:
        """
        Is true when command formats tagged ``\!`` to stop leaf.
        """
        return self._right_broken

    @property
    def start_dynamic(self) -> typing.Optional[abjad.Dynamic]:
        """
        Gets start dynamic.
        """
        return self._start_dynamic

    @property
    def start_selector(self) -> typings.Selector:
        """
        Gets start selector.
        """
        return self._start_selector

    @property
    def stop_dynamic(self) -> typing.Optional[abjad.Dynamic]:
        """
        Gets stop dynamic.
        """
        return self._stop_dynamic

    @property
    def stop_selector(self) -> typing.Optional[typings.Selector]:
        """
        Gets stop selector.
        """
        return self._stop_selector

    ### SPECIAL METHODS ###

    def __call__(self, argument: abjad.Selection = None) -> None:
        """
        Calls command.
        """
        if self.selector:
            argument = self.selector(argument)
        leaves = baca.select(argument).leaves()
        if len(leaves) == 1 and self.lone_dynamic is False:
            return None
        if self.right_broken is True:
            literal = abjad.LilyPondLiteral(r'\!')
            assert isinstance(self.stop_selector, abjad.Expression)
            command = library.literal(
                r'\!',
                format_slot='after',
                selector=self.stop_selector,
                )
            words = self.tag.words
            words.append(str(abjad.tags.HIDE_TO_JOIN_BROKEN_SPANNERS))
            library.tag(words, command, deactivate=False)
            command.runtime = self.runtime
            command(argument)
        if self.start_dynamic is not None:
            command = _local_dynamic(
                self.start_dynamic,
                selector=self.start_selector,
                )
            library.tag(self.tag.words, command)
            command.runtime = self.runtime
            command(argument)
        if len(leaves) == 1:
            return
        command = _local_dynamic_trend(
            self.dynamic_trend,
            selector=self.start_selector,
            )
        library.tag(self.tag.words, command)
        command.runtime = self.runtime
        command(argument)
        if self.stop_dynamic is not None:
            assert isinstance(self.stop_selector, abjad.Expression)
            command = _local_dynamic(
                self.stop_dynamic,
                selector=self.stop_selector,
                )
            library.tag(self.tag.words, command)
            command.runtime = self.runtime
            command(argument)


def new_hairpin(
    descriptor: typing.Union[
        str,
        typing.List[typing.Union[abjad.Dynamic, abjad.DynamicTrend]],
        ],
    *,
    left_broken: bool = None,
    lone_dynamic: bool = True,
    right_broken: bool = None,
    selector: typings.Selector = 'baca.tleaves()',
    start_selector: typings.Selector = 'baca.leaf(0)',
    stop_selector: typings.Selector = 'baca.leaf(-1)',
    ) -> Command:
    r"""
    Attaches hairpin indicators.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.new_hairpin('p < f'),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            \<                                                                       %! IC:BACA_HAIRPIN
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            d''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Effort dynamic al niente:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.new_hairpin('"ff" >o niente'),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            e'8
                            \effort_ff                                                               %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            - \tweak circled-tip ##t                                                 %! IC:BACA_HAIRPIN
                            \>                                                                       %! IC:BACA_HAIRPIN
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            d''8
                            \!                                                                       %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Effort dynamic dal niente:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.new_hairpin('niente o< "ff"'),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            e'8
                            \!                                                                       %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            - \tweak circled-tip ##t                                                 %! IC:BACA_HAIRPIN
                            \<                                                                       %! IC:BACA_HAIRPIN
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            d''8
                            \effort_ff                                                               %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Effort dynamic constante:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.new_hairpin('"p" -- f'),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            e'8
                            \effort_p                                                                %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            - \tweak stencil #constante-hairpin                                      %! IC:BACA_HAIRPIN
                            \<                                                                       %! IC:BACA_HAIRPIN
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            d''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Effort dynamics crescendo subito, decrescendo subito:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.new_hairpin(
        ...         '"mp" <| "f"',
        ...         stop_selector=baca.leaf(6),
        ...         ),
        ...     baca.new_hairpin(
        ...         '"mf" |> "p"',
        ...         start_selector=baca.leaf(7),
        ...         ),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            e'8
                            \effort_mp                                                               %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            - \tweak stencil #abjad-flared-hairpin                                   %! IC:BACA_HAIRPIN
                            \<                                                                       %! IC:BACA_HAIRPIN
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            e'8
                            \effort_f                                                                %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            d''8
                            \effort_mf                                                               %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            - \tweak stencil #abjad-flared-hairpin                                   %! IC:BACA_HAIRPIN
                            \>                                                                       %! IC:BACA_HAIRPIN
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            d''8
                            \effort_p                                                                %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Attaches start dynamic without trend on lone leaf:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(4),
        ...     baca.make_notes(),
        ...     baca.measures(
        ...         1,
        ...         baca.new_hairpin('p < f'),
        ...         baca.pitch('E4'),
        ...         ),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'4                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            e'2
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \baca_unpitched_music_warning                                            %! SM24
                            c'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \baca_unpitched_music_warning                                            %! SM24
                            c'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \baca_unpitched_music_warning                                            %! SM24
                            c'4.
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Implicit start and stop:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.measures(
        ...         1,
        ...         baca.new_hairpin('f >'),
        ...         ),
        ...     baca.measures(
        ...         (3, 4),
        ...         baca.dynamic(baca.niente()),
        ...         baca.new_hairpin('< f'),
        ...         ),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            e'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            \>                                                                       %! IC:BACA_HAIRPIN
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            d''8
                            \!                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \<                                                                       %! IC:BACA_HAIRPIN
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC:BACA_HAIRPIN
                            d''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC:BACA_HAIRPIN
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    if isinstance(descriptor, str):
        pieces = descriptor.split()
        if len(pieces) == 1:
            start, stop = None, None
            trend = pieces[0]
        elif len(pieces) == 2:
            if '>' in pieces[0] or '<' in pieces[0] or '--' in pieces[0]:
                start = None
                trend, stop = pieces
            else:
                stop = None
                start, trend = pieces
        else:
            assert len(pieces) == 3, repr(pieces)
            start, trend, stop = descriptor.split()
        if start is not None:
            command = _local_dynamic(start)
            assert command.indicators
            start_dynamic = command.indicators[0]
        else:
            start_dynamic = None
        command = _local_dynamic_trend(trend)
        assert command.indicators
        dynamic_trend = command.indicators[0]
        if stop is not None:
            command = _local_dynamic(stop)
            assert command.indicators
            stop_dynamic = command.indicators[0]
        else:
            stop_dynamic = None
    else:
        assert isinstance(descriptor, list), repr(descriptor)
        if len(descriptor) == 1:
            start_dynamic, stop_dynamic = None, None
            dynamic_trend = descriptor[0]
        elif len(descriptor) == 2:
            if isinstance(descriptor[0], abjad.DynamicTrend):
                start_dynamic = None
                dynamic_trend, stop_dynamic = descriptor
            else:
                stop_dynamic = None
                start_dynamic, dynamic_trend = descriptor
        else:
            assert len(descriptor) == 3, repr(descriptor)
            start_dynamic, dynamic_trend, stop_dynamic = descriptor
    if isinstance(selector, str):
        selector = eval(selector)
    if isinstance(start_selector, str):
        start_selector = eval(start_selector)
    if isinstance(stop_selector, str):
        stop_selector = eval(stop_selector)
    if left_broken is not None:
        left_broken = bool(left_broken)
    if left_broken is True:
        assert start_dynamic is None, repr(start_dynamic)
        dynamic_trend = abjad.new(dynamic_trend, left_broken=True)
    if right_broken is not None:
        right_broken = bool(right_broken)
    if right_broken is True:
        assert stop_dynamic is None, repr(stop_dynamic)
    return NewHairpinCommand(
        dynamic_trend,
        lone_dynamic=lone_dynamic,
        right_broken=right_broken,
        selector=selector,
        start_dynamic=start_dynamic,
        start_selector=start_selector,
        stop_dynamic=stop_dynamic,
        stop_selector=stop_selector,
        )


def niente() -> abjad.Dynamic:
    """
    Makes niente stop dynamic with LilyPond ``\!`` output..
    """
    return abjad.Dynamic('niente', command=r'\!')

_local_niente = niente
