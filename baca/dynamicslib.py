"""
Dynamics library.
"""
import abjad
import baca
import typing
from . import library
from .HairpinCommand import HairpinCommand
from .IndicatorCommand import IndicatorCommand
from .MapCommand import MapCommand
from .OverrideCommand import OverrideCommand
from .PiecewiseCommand import PiecewiseCommand
from .SchemeManifest import SchemeManifest
from .Suite import Suite
from .Typing import Number
from .Typing import NumberPair
from .Typing import Selector


def dynamic(
    dynamic: typing.Union[str, abjad.Dynamic],
    # TODO: add tweaks
    *,
    selector: Selector = 'baca.phead(0)',
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
        if dynamic in scheme_manifest.dynamics:
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
    selector: Selector = 'baca.leaf(0)',
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
    selector: Selector = 'baca.leaf(0)',
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
# TODO: change selector to baca.leaf(0) for niente dynamics
def dynamic_text_center(
    *,
    selector: Selector = 'baca.pleaf(0)',
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
    pair: NumberPair,
    *,
    selector: Selector = 'baca.pleaf(0)',
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
# TODO: change selector to baca.leaf(0) for niente dynamics
def dynamic_text_left(
    *,
    selector: Selector = 'baca.pleaf(0)',
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

# TODO: change selector to baca.leaf(0) for niente dynamics
def dynamic_text_parent_alignment_x(
    n: Number,
    *,
    selector: Selector = 'baca.pleaf(0)',
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
# TODO: change selector to baca.leaf(0) for niente dynamics
def dynamic_text_right(
    *,
    selector: Selector = 'baca.pleaf(0)',
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

# TODO: change selector to baca.leaf(0) for niente dynamics
def dynamic_text_stencil_false(
    *,
    selector: Selector = 'baca.pleaf(0)',
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

# TODO: change selector to baca.leaf(0) for niente dynamics
def dynamic_text_transparent(
    *,
    selector: Selector = 'baca.pleaf(0)',
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

# TODO: change selector to baca.leaf(0) for niente dynamics
def dynamic_text_x_extent_zero(
    *,
    selector: Selector = 'baca.pleaf(0)',
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

# TODO: change selector to baca.leaf(0) for niente dynamics
def dynamic_text_x_offset(
    n: Number,
    *,
    selector: Selector = 'baca.pleaf(0)',
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

# TODO: change selector to baca.leaf(0) for niente dynamics
def dynamic_text_y_offset(
    n: Number,
    *,
    selector: Selector = 'baca.pleaf(0)',
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
    selector: Selector = 'baca.leaf(0)',
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

def dynamics(string: str) -> typing.List[abjad.Dynamic]:
    r"""
    Makes dynamics from ``string``.

    ..  container::

        >>> baca.dynamics('ff p f pp')
        [Dynamic('ff'), Dynamic('p'), Dynamic('f'), Dynamic('pp')]

    """
    return [abjad.Dynamic(_) for _ in string.split()]

_local_dynamics = dynamics

# TODO: merge into baca.hairpin_chain()
def hairpin(
    string: str = None,
    *tweaks: abjad.LilyPondTweakManager,
    left_broken: str = None,
    right_broken: str = None,
    selector: Selector = 'baca.tleaves()',
    start_ordinal: int = None,
    stop_ordinal: int = None,
    ) -> HairpinCommand:
    r"""
    Attaches hairpin.

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
                            \p                                                                       %! HC1
                            \<                                                                       %! HC1
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
                            \f                                                                       %! HC1
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
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
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.hairpin('p < f'),
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
                            [
                            \p                                                                       %! HC1
                            \<                                                                       %! HC1
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
                            \f                                                                       %! HC1
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

        Attaches hairpin to trimmed leaves in each tuplet:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplets(),
        ...         baca.hairpin('p < f'),
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
                            \p                                                                       %! HC1
                            \<                                                                       %! HC1
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            \f                                                                       %! HC1
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            \p                                                                       %! HC1
                            \<                                                                       %! HC1
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
                            \f                                                                       %! HC1
                        }
                        \times 4/5 {
                            a'16
                            \p                                                                       %! HC1
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    dynamics_dynamic = dynamic
    scheme_manifest = SchemeManifest()
    start, shape, stop = abjad.Hairpin._parse_descriptor(string)
    if start == 'niente' or start in scheme_manifest.dynamics:
        start_dynamic_is_textual = True
    else:
        start_dynamic_is_textual = False
    if stop == 'niente' or stop in scheme_manifest.dynamics:
        stop_dynamic_is_textual = True
    else:
        stop_dynamic_is_textual = False
    hairpin = abjad.Hairpin(
        string,
        start_dynamic_is_textual=start_dynamic_is_textual,
        stop_dynamic_is_textual=stop_dynamic_is_textual,
        )
    if left_broken is not None:
        assert isinstance(left_broken, bool), repr(left_broken)
    if right_broken not in ('niente', None):
        assert isinstance(right_broken, bool), repr(right_broken)
    if left_broken and hairpin.start_dynamic is not None:
        raise Exception(f'no start dynamic with left broken: {string!r}.')
    if right_broken and hairpin.stop_dynamic is not None:
        raise Exception(f'no stop dynamic with right broken: {string!r}.')
    if left_broken is True:
        left_broken = hairpin.shape_string
    if right_broken is True:
        right_broken = hairpin.shape_string
    if start is not None:
        command_ = dynamics_dynamic(start)
        assert command_.indicators is not None
        start = command_.indicators[0]
        if start_ordinal is not None:
            start = abjad.new(start, ordinal=start_ordinal)
    if stop is not None:
        command_ = dynamics_dynamic(stop)
        assert command_.indicators is not None
        stop = command_.indicators[0]
        if stop_ordinal is not None:
            stop = abjad.new(stop, ordinal=stop_ordinal)
    command = HairpinCommand(
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        selector=selector,
        start=start,
        stop=stop,
        )
    return command

# TODO: completely refactor;
#       change selector to baca.leaves() because of niente dynamics;
#       remove bookend keyword altogether;
#       add left_broken, right_broken keywords;
#       maybe add start_ordinal, stop_ordinal keywords;
def hairpin_chain(
    *dynamics: typing.Any,
    bookend: typing.Union[bool, int] = False,
    pieces: typing.Union[MapCommand, Selector] = 'baca.tleaves().group()',
    selector: Selector = 'baca.tleaves()'
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

def hairpin_shorten_pair(
    pair: NumberPair,
    *,
    selector: Selector = 'baca.leaves()',
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

def hairpin_start(
    hairpin_start: str,
    *,
    selector: Selector = 'baca.phead(0)',
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
        ...     baca.hairpin_start(
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
        ...     baca.hairpin_start(
        ...         '>',
        ...         selector=baca.leaves().partition_by_counts(
        ...             [4, 3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             )[abjad.index([1], 2)][:-1].map(baca.leaf(0)),
        ...         ),
        ...     baca.hairpin_start(
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
                            [
                            \<                                                                       %! IC
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
                            [
                            \>                                                                       %! IC
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
                            [
                            \<                                                                       %! IC
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
                            [
                            - \tweak circled-tip ##t                                                 %! IC
                            \>                                                                       %! IC
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
    if isinstance(hairpin_start, str):
        indicator = abjad.HairpinStart(hairpin_start)
    else:
        indicator = hairpin_start
    assert isinstance(indicator, abjad.HairpinStart), repr(indicator)
    return IndicatorCommand(
        context='Voice',
        indicators=[indicator],
        selector=selector,
        )

def hairpin_start_shift(
    dynamic: typing.Union[str, abjad.Dynamic],
    *,
    selector: Selector = 'baca.leaf(0)',
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
    selector: Selector = 'baca.leaves()',
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
    selector: Selector = 'baca.leaves()',
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
    ):
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
                            [
                            \<                                                                       %! IC
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
                            [
                            \>                                                                       %! IC
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
                            [
                            \<                                                                       %! IC
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
                            [
                            \>                                                                       %! IC
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
                            [
                            \<                                                                       %! IC
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
                            [
                            \>                                                                       %! IC
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
                            [
                            \<                                                                       %! IC
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
                            [
                            \>                                                                       %! IC
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
                            [
                            \<                                                                       %! IC
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
                            [
                            \>                                                                       %! IC
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
                            [
                            \<                                                                       %! IC
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
                            [
                            - \tweak circled-tip ##t                                                 %! IC
                            \>                                                                       %! IC
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
    selector = baca.tleaves()
    selector = selector.group_by_measure()
    selector = selector.partition_by_counts(
        counts,
        cyclic=True,
        overhang=True,
        )

    commands = []
    # every through and every crescendo
    selector_ = selector[abjad.index([0], 2)]
    selector_ = selector_.map(baca.leaf(0))
    command = baca.dynamic(
        trough,
        selector=selector_
        )
    commands.append(command)
    command = baca.hairpin_start(
        '<',
        selector=selector_
        )
    commands.append(command)

    # every peak
    selector_ = selector[abjad.index([1], 2)]
    selector_ = selector_.map(baca.leaf(0))
    command = baca.dynamic(
        peak,
        selector=selector_
        )
    commands.append(command)

    # all but last decrescendo
    selector_ = selector[abjad.index([1], 2)]
    selector_ = selector_[:-1]
    selector_ = selector_.map(baca.leaf(0))
    command = baca.hairpin_start(
        '>',
        selector=selector_
        )
    commands.append(command)

    # last decrescendo
    selector_ = selector[abjad.index([1], 2)]
    selector_ = selector_[-1:]
    selector_ = selector_.map(baca.leaf(0))
    if al_niente:
        shape = '>o'
    else:
        shape = '>'
    command = baca.hairpin_start(
        shape,
        selector=selector_
        )
    commands.append(command)

    return commands

def niente():
    """
    Makes niente stop dynamic with LilyPond ``\!`` output..
    """
    return abjad.Dynamic('niente', command=r'\!')
