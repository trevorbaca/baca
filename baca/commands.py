"""
Commands.
"""
import pathlib
import typing
from inspect import currentframe as _frame

import abjad

from . import commandclasses as _commandclasses
from . import const as _const
from . import indicatorcommands as _indicatorcommands
from . import indicators as _indicators
from . import overrides as _overrides
from . import parts as _parts
from . import path as _path
from . import pitchcommands as _pitchcommands
from . import scoping as _scoping
from . import selection as _selection
from . import tags as _tags
from . import typings

### FACTORY FUNCTIONS ###


def allow_octaves(
    *, selector=lambda _: _selection.Selection(_).leaves()
) -> _commandclasses.IndicatorCommand:
    """
    Attaches ALLOW_OCTAVE constant.
    """
    return _commandclasses.IndicatorCommand(
        indicators=[_const.ALLOW_OCTAVE], selector=selector
    )


def assign_parts(
    part_assignment: _parts.PartAssignment,
    *,
    selector=lambda _: _selection.Selection(_).leaves(),
) -> _commandclasses.PartAssignmentCommand:
    r"""
    Inserts ``selector`` output in container and sets part assignment.

    ..  container:: example

        >>> def closure():
        ...     return baca.make_empty_score(1)

        >>> maker = baca.CommandAccumulator(
        ...     score_template=closure,
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.assign_parts(baca.parts.PartAssignment("Music_Voice")),
        ...     baca.pitch("E4"),
        ... )

        >>> lilypond_file = baca.interpret_commands(
        ...     maker.commands,
        ...     maker.score_template,
        ...     maker.time_signatures,
        ...     maker.voice_metadata,
        ...     environment="docs",
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Music_Staff"
            <<
                \context Voice = "Global_Skips"
                {
                    \time 4/8
                    s1 * 1/2
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 1/2
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music_Voice"
                {
                    {   %*% PartAssignment('Music_Voice')
                        e'2
                        e'4.
                        e'2
                        e'4.
                    }   %*% PartAssignment('Music_Voice')
                }
            >>
        }

    ..  container:: example exception

        Raises exception when voice does not allow part assignment:

        >>> maker = baca.CommandAccumulator(
        ...     score_template=closure,
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> part_assignment = baca.parts.PartAssignment('Flute')

        >>> maker(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.assign_parts(baca.parts.PartAssignment("Flute_Voice")),
        ...     baca.pitches("E4 F4"),
        ... )

        >>> lilypond_file = baca.interpret_commands(
        ...     maker.commands,
        ...     maker.score_template,
        ...     maker.time_signatures,
        ...     maker.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: Music_Voice does not allow Flute_Voice part assignment:
          PartAssignment('Flute_Voice')

    """
    if not isinstance(part_assignment, _parts.PartAssignment):
        message = "part_assignment must be part assignment"
        message += f" (not {part_assignment!r})."
        raise Exception(message)
    return _commandclasses.PartAssignmentCommand(
        part_assignment=part_assignment, selector=selector
    )


def bcps(
    bcps,
    *tweaks: abjad.IndexedTweakManager,
    bow_change_tweaks: abjad.IndexedTweakManagers = None,
    final_spanner: bool = None,
    helper: typing.Callable = None,
    selector=lambda _: _selection.Selection(_).leaves(),
) -> _commandclasses.BCPCommand:
    r"""
    Makes bow contact point command.

        ..  container:: example

            >>> maker = baca.CommandAccumulator(
            ...     score_template=baca.make_empty_score_maker(1),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     "Music_Voice",
            ...     baca.make_even_divisions(),
            ...     baca.bcps(
            ...         [(1, 5), (3, 5), (2, 5), (4, 5), (5, 5)],
            ...         ),
            ...     baca.pitches('E4 F4'),
            ...     baca.script_staff_padding(5.5),
            ...     baca.text_spanner_staff_padding(2.5),
            ...     )

            >>> lilypond_file = baca.interpret_commands(
            ...     maker.commands,
            ...     maker.score_template,
            ...     maker.time_signatures,
            ...     maker.voice_metadata,
            ...     environment="docs",
            ...     includes=["baca.ily"],
            ...     remove_tags=baca.tags.documentation_removal_tags(),
            ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 16)),
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                {
                    \context Staff = "Music_Staff"
                    <<
                        \context Voice = "Global_Skips"
                        {
                            \baca-new-spacing-section #1 #16
                            \time 4/8
                            s1 * 1/2
                            \baca-new-spacing-section #1 #16
                            \time 3/8
                            s1 * 3/8
                            \baca-new-spacing-section #1 #16
                            \time 4/8
                            s1 * 1/2
                            \baca-new-spacing-section #1 #4
                            \time 3/8
                            s1 * 3/8
                        }
                        \context Voice = "Music_Voice"
                        {
                            \override Script.staff-padding = 5.5
                            \override TextSpanner.staff-padding = 2.5
                            e'8
                            - \downbow
                            [
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #1 #5
                            \bacaStartTextSpanBCP
                            f'8
                            - \upbow
                            \bacaStopTextSpanBCP
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #3 #5
                            \bacaStartTextSpanBCP
                            e'8
                            - \downbow
                            \bacaStopTextSpanBCP
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #2 #5
                            \bacaStartTextSpanBCP
                            f'8
                            \bacaStopTextSpanBCP
                            ]
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #4 #5
                            \bacaStartTextSpanBCP
                            e'8
                            - \upbow
                            \bacaStopTextSpanBCP
                            [
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #5 #5
                            \bacaStartTextSpanBCP
                            f'8
                            - \downbow
                            \bacaStopTextSpanBCP
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #1 #5
                            \bacaStartTextSpanBCP
                            e'8
                            - \upbow
                            \bacaStopTextSpanBCP
                            ]
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #3 #5
                            \bacaStartTextSpanBCP
                            f'8
                            - \downbow
                            \bacaStopTextSpanBCP
                            [
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #2 #5
                            \bacaStartTextSpanBCP
                            e'8
                            \bacaStopTextSpanBCP
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #4 #5
                            \bacaStartTextSpanBCP
                            f'8
                            - \upbow
                            \bacaStopTextSpanBCP
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #5 #5
                            \bacaStartTextSpanBCP
                            e'8
                            - \downbow
                            \bacaStopTextSpanBCP
                            ]
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #1 #5
                            \bacaStartTextSpanBCP
                            f'8
                            - \upbow
                            \bacaStopTextSpanBCP
                            [
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #3 #5
                            \bacaStartTextSpanBCP
                            e'8
                            - \downbow
                            \bacaStopTextSpanBCP
                            - \abjad-solid-line-with-arrow
                            - \baca-bcp-spanner-left-text #2 #5
                            - \baca-bcp-spanner-right-text #4 #5
                            \bacaStartTextSpanBCP
                            f'8
                            \bacaStopTextSpanBCP
                            ]
                            \revert Script.staff-padding
                            \revert TextSpanner.staff-padding
                        }
                    >>
                }

    """
    if final_spanner is not None:
        final_spanner = bool(final_spanner)
    return _commandclasses.BCPCommand(
        bcps=bcps,
        bow_change_tweaks=bow_change_tweaks,
        final_spanner=final_spanner,
        helper=helper,
        selector=selector,
        tags=[_scoping.site(_frame())],
        tweaks=tweaks,
    )


def close_volta(
    selector=lambda _: _selection.Selection(_).leaf(0),
    *,
    format_slot: str = "before",
) -> _scoping.Suite:
    """
    Attaches bar line and overrides bar line X-extent.
    """
    assert format_slot in ("after", "before"), repr(format_slot)
    after = format_slot == "after"
    # does not require not_mol() tagging, just only_mol() tagging:
    return _scoping.suite(
        _indicatorcommands.bar_line(":|.", selector, format_slot=format_slot),
        _scoping.only_mol(
            _overrides.bar_line_x_extent((0, 1.5), selector, after=after)
        ),
    )


def color(
    selector=lambda _: _selection.Selection(_).leaves(),
    lone=False,
) -> _commandclasses.ColorCommand:
    r"""
    Makes color command.

    ..  container:: example

        Colors leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(),
        ...     rmakers.unbeam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["abjad.ily"]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        \abjad-color-music #'red
                        r8
                        \abjad-color-music #'blue
                        c'16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        bf'4
                        ~
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \abjad-color-music #'red
                        fs''16
                        \abjad-color-music #'blue
                        e''16
                        \abjad-color-music #'red
                        ef''4
                        ~
                        \abjad-color-music #'blue
                        ef''16
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        af''16
                        \abjad-color-music #'red
                        g''16
                    }
                    \times 4/5
                    {
                        \abjad-color-music #'blue
                        a'16
                        \abjad-color-music #'red
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Colors leaves in tuplet 1:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(lambda _: baca.Selection(_).tuplets()[1:2].leaves()),
        ...     rmakers.unbeam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["abjad.ily"]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        d'16
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \abjad-color-music #'red
                        fs''16
                        \abjad-color-music #'blue
                        e''16
                        \abjad-color-music #'red
                        ef''4
                        ~
                        \abjad-color-music #'blue
                        ef''16
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        af''16
                        \abjad-color-music #'red
                        g''16
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commandclasses.ColorCommand(selector=selector, lone=lone)


def container(
    identifier: str = None,
    *,
    selector=lambda _: _selection.Selection(_).leaves(),
) -> _commandclasses.ContainerCommand:
    r"""
    Makes container with ``identifier`` and extends container with
    ``selector`` output.

    ..  container:: example

        >>> maker = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     "Music_Voice",
        ...     baca.container('ViolinI', selector=baca.selectors.leaves((None, 2))),
        ...     baca.container('ViolinII', selector=baca.selectors.leaves((2, None))),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     maker.commands,
        ...     maker.score_template,
        ...     maker.time_signatures,
        ...     maker.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Music_Staff"
            <<
                \context Voice = "Global_Skips"
                {
                    \time 4/8
                    s1 * 1/2
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 1/2
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music_Voice"
                {
                    {   %*% ViolinI
                        e'2
                        f'4.
                    }   %*% ViolinI
                    {   %*% ViolinII
                        e'2
                        f'4.
                    }   %*% ViolinII
                }
            >>
        }

    """
    if identifier is not None:
        if not isinstance(identifier, str):
            message = f"identifier must be string (not {identifier!r})."
            raise Exception(message)
    return _commandclasses.ContainerCommand(identifier=identifier, selector=selector)


def cross_staff(
    *, selector=lambda _: _selection.Selection(_).phead(0)
) -> _commandclasses.IndicatorCommand:
    r"""
    Attaches cross-staff command.

    ..  container:: example

        Attaches cross-staff command to last two pitched leaves:

        >>> def closure():
        ...     return baca.make_empty_score(1, 1)

        >>> maker = baca.CommandAccumulator(
        ...     score_template=closure,
        ...     time_signatures=[(4, 4)],
        ... )

        >>> maker(
        ...     ("Music_Voice_1", 1),
        ...     baca.music(abjad.Container("e'4 f' g' a'")[:]),
        ... )

        >>> maker(
        ...     ("Music_Voice_2", 1),
        ...     baca.music(abjad.Container("c'4 d' e' f'")[:]),
        ...     baca.cross_staff(
        ...         selector=baca.selectors.pleaves((-2, None)),
        ...     ),
        ... )

        >>> lilypond_file = baca.interpret_commands(
        ...     maker.commands,
        ...     maker.score_template,
        ...     maker.time_signatures,
        ...     maker.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context StaffGroup = "Music_Staff_Group"
                <<
                    \context Staff = "Music_Staff_1"
                    <<
                        \context Voice = "Global_Skips"
                        {
                            \time 4/4
                            s1 * 1
                        }
                        \context Voice = "Music_Voice_1"
                        {
                            e'4
                            f'4
                            g'4
                            a'4
                        }
                    >>
                    \context Staff = "Music_Staff_2"
                    {
                        \context Voice = "Music_Voice_2"
                        {
                            c'4
                            d'4
                            \crossStaff
                            e'4
                            \crossStaff
                            f'4
                        }
                    }
                >>
            }

    """
    return _commandclasses.IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\crossStaff")],
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def double_volta(
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> _scoping.Suite:
    """
    Attaches bar line and overrides bar line X-extent.
    """
    return _scoping.suite(
        _indicatorcommands.bar_line(":.|.:", selector, format_slot="before"),
        _scoping.not_mol(_overrides.bar_line_x_extent((0, 3), selector)),
        _scoping.only_mol(_overrides.bar_line_x_extent((0, 4), selector)),
    )


def dynamic_down(
    *, selector=lambda _: _selection.Selection(_).leaf(0)
) -> _commandclasses.IndicatorCommand:
    r"""
    Attaches dynamic-down command.

    ..  container:: example

        Attaches dynamic-down command to leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=lambda _: baca.Selection(_).tuplets()[1:2].phead(0)),
        ...     baca.dynamic_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
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
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commandclasses.IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicDown")],
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def dynamic_up(
    *, selector=lambda _: _selection.Selection(_).leaf(0)
) -> _commandclasses.IndicatorCommand:
    r"""
    Attaches dynamic-up command.

    ..  container:: example

        Attaches dynamic-up command to leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=lambda _: baca.Selection(_).tuplets()[1:2].phead(0)),
        ...     baca.dynamic_up(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
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
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commandclasses.IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicUp")],
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def edition(
    not_parts: typing.Union[str, abjad.Markup, _commandclasses.IndicatorCommand],
    only_parts: typing.Union[str, abjad.Markup, _commandclasses.IndicatorCommand],
) -> _scoping.Suite:
    """
    Makes not-parts / only-parts markup suite.
    """
    if isinstance(not_parts, (str, abjad.Markup)):
        not_parts = markup(not_parts)
    assert isinstance(not_parts, _commandclasses.IndicatorCommand)
    not_parts_ = _scoping.not_parts(not_parts)
    if isinstance(only_parts, (str, abjad.Markup)):
        only_parts = markup(only_parts)
    assert isinstance(only_parts, _commandclasses.IndicatorCommand)
    only_parts_ = _scoping.only_parts(only_parts)
    return _scoping.suite(not_parts_, only_parts_)


def finger_pressure_transition(
    *,
    selector=lambda _: _selection.Selection(_).tleaves(),
    right_broken: bool = None,
) -> _commandclasses.GlissandoCommand:
    r"""
    Makes finger pressure transition glissando.

    ..  container:: example

        >>> maker = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     "Music_Voice",
        ...     baca.finger_pressure_transition(selector=baca.selectors.notes((None, 2))),
        ...     baca.finger_pressure_transition(selector=baca.selectors.notes((2, None))),
        ...     baca.make_notes(),
        ...     baca.note_head_style_harmonic(selector=baca.selectors.note(0)),
        ...     baca.note_head_style_harmonic(selector=baca.selectors.note(2)),
        ...     baca.pitch('C5'),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     maker.commands,
        ...     maker.score_template,
        ...     maker.time_signatures,
        ...     maker.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \once \override NoteHead.style = #'harmonic
                        c''2
                        - \tweak arrow-length 2
                        - \tweak arrow-width 0.5
                        - \tweak bound-details.right.arrow ##t
                        - \tweak thickness 3
                        \glissando
                        c''4.
                        \once \override NoteHead.style = #'harmonic
                        c''2
                        - \tweak arrow-length 2
                        - \tweak arrow-width 0.5
                        - \tweak bound-details.right.arrow ##t
                        - \tweak thickness 3
                        \glissando
                        c''4.
                    }
                >>
            }

    """
    return _commandclasses.GlissandoCommand(
        allow_repeats=True,
        right_broken=right_broken,
        selector=selector,
        tags=[_scoping.site(_frame())],
        tweaks=(
            abjad.tweak(2).arrow_length,
            abjad.tweak(0.5).arrow_width,
            abjad.tweak(True).bound_details__right__arrow,
            abjad.tweak(3).thickness,
        ),
    )


def flat_glissando(
    pitch: typing.Union[
        str,
        abjad.NamedPitch,
        abjad.StaffPosition,
        typing.List[abjad.StaffPosition],
    ] = None,
    *tweaks,
    allow_repitch: bool = None,
    do_not_hide_middle_note_heads: bool = None,
    mock: bool = None,
    hide_middle_stems: bool = None,
    hide_stem_selector: typing.Callable = None,
    left_broken: bool = None,
    right_broken: bool = None,
    right_broken_show_next: bool = None,
    rleak: bool = None,
    selector=lambda _: _selection.Selection(_).pleaves(),
    stop_pitch: typing.Union[str, abjad.NamedPitch, abjad.StaffPosition] = None,
) -> _scoping.Suite:
    """
    Makes flat glissando.
    """
    prototype = (list, str, abjad.NamedPitch, abjad.StaffPosition)
    if pitch is not None:
        assert isinstance(pitch, prototype), repr(pitch)
    if stop_pitch is not None:
        assert type(pitch) is type(stop_pitch), repr((pitch, stop_pitch))
    if rleak is True:

        def _selector_rleak(argument):
            return selector(argument).rleak()

        new_selector = _selector_rleak
    else:
        new_selector = selector
    commands: typing.List[_scoping.Command] = []
    command = glissando(
        *tweaks,
        allow_repeats=True,
        allow_ties=True,
        hide_middle_note_heads=not do_not_hide_middle_note_heads,
        hide_middle_stems=hide_middle_stems,
        hide_stem_selector=hide_stem_selector,
        left_broken=left_broken,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
        selector=new_selector,
    )
    commands.append(command)

    def _leaves_of_selector(argument):
        return new_selector(argument).leaves()

    untie_command = untie(_leaves_of_selector)
    commands.append(untie_command)
    if pitch is not None and stop_pitch is None:
        if isinstance(pitch, abjad.StaffPosition) or (
            isinstance(pitch, list) and isinstance(pitch[0], abjad.StaffPosition)
        ):
            staff_position_command = _pitchcommands.staff_position(
                pitch,
                allow_repitch=allow_repitch,
                mock=mock,
                selector=new_selector,
            )
            commands.append(staff_position_command)
        else:
            pitch_command = _pitchcommands.pitch(
                pitch,
                allow_repitch=allow_repitch,
                mock=mock,
                selector=new_selector,
            )
            commands.append(pitch_command)
    elif pitch is not None and stop_pitch is not None:
        if isinstance(pitch, abjad.StaffPosition):
            assert isinstance(stop_pitch, abjad.StaffPosition)
            interpolation_command = _pitchcommands.interpolate_staff_positions(
                pitch, stop_pitch, mock=mock, selector=new_selector
            )
        else:
            assert isinstance(pitch, (str, abjad.NamedPitch))
            assert isinstance(stop_pitch, (str, abjad.NamedPitch))
            interpolation_command = _pitchcommands.interpolate_pitches(
                pitch, stop_pitch, mock=mock, selector=new_selector
            )
        commands.append(interpolation_command)
    return _scoping.suite(*commands)


def fractions(items):
    """
    Makes fractions.
    """
    result = []
    for item in items:
        item_ = abjad.NonreducedFraction(item)
        result.append(item_)
    return result


def glissando(
    *tweaks: abjad.IndexedTweakManager,
    allow_repeats: bool = None,
    allow_ties: bool = None,
    hide_middle_note_heads: bool = None,
    hide_middle_stems: bool = None,
    hide_stem_selector: typing.Callable = None,
    left_broken: bool = None,
    map: abjad.Expression = None,
    right_broken: bool = None,
    right_broken_show_next: bool = None,
    selector=lambda _: _selection.Selection(_).tleaves(),
    style: str = None,
    zero_padding: bool = None,
) -> _commandclasses.GlissandoCommand:
    r"""
    Attaches glissando.

    ..  container:: example

        With segment-maker:

        >>> maker = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.glissando()
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     maker.commands,
        ...     maker.score_template,
        ...     maker.time_signatures,
        ...     maker.voice_metadata,
        ...     environment="docs",
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        e'8
                        [
                        \glissando
                        d''8
                        \glissando
                        f'8
                        \glissando
                        e''8
                        ]
                        \glissando
                        g'8
                        [
                        \glissando
                        f''8
                        \glissando
                        e'8
                        ]
                        \glissando
                        d''8
                        [
                        \glissando
                        f'8
                        \glissando
                        e''8
                        \glissando
                        g'8
                        ]
                        \glissando
                        f''8
                        [
                        \glissando
                        e'8
                        \glissando
                        d''8
                        ]
                    }
                >>
            }

    ..  container:: example

        First and last PLTs:

        >>> maker = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     "Music_Voice",
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.make_even_divisions(),
        ...     baca.glissando(selector=baca.selectors.plts((None, 2))),
        ...     baca.glissando(selector=baca.selectors.plts((-2, None))),
        ... )

        >>> lilypond_file = baca.interpret_commands(
        ...     maker.commands,
        ...     maker.score_template,
        ...     maker.time_signatures,
        ...     maker.voice_metadata,
        ...     environment="docs",
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        e'8
                        [
                        \glissando
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        \glissando
                        d''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Works with tweaks:

        >>> maker = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.glissando(
        ...         abjad.tweak("#red").color,
        ...         ),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     maker.commands,
        ...     maker.score_template,
        ...     maker.time_signatures,
        ...     maker.voice_metadata,
        ...     environment="docs",
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        e'8
                        [
                        - \tweak color #red
                        \glissando
                        d''8
                        - \tweak color #red
                        \glissando
                        f'8
                        - \tweak color #red
                        \glissando
                        e''8
                        ]
                        - \tweak color #red
                        \glissando
                        g'8
                        [
                        - \tweak color #red
                        \glissando
                        f''8
                        - \tweak color #red
                        \glissando
                        e'8
                        ]
                        - \tweak color #red
                        \glissando
                        d''8
                        [
                        - \tweak color #red
                        \glissando
                        f'8
                        - \tweak color #red
                        \glissando
                        e''8
                        - \tweak color #red
                        \glissando
                        g'8
                        ]
                        - \tweak color #red
                        \glissando
                        f''8
                        [
                        - \tweak color #red
                        \glissando
                        e'8
                        - \tweak color #red
                        \glissando
                        d''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Works with indexed tweaks:

        >>> maker = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.glissando(
        ...         (abjad.tweak("#red").color, 0),
        ...         (abjad.tweak("#red").color, -1),
        ...         ),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     maker.commands,
        ...     maker.score_template,
        ...     maker.time_signatures,
        ...     maker.voice_metadata,
        ...     environment="docs",
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        e'8
                        [
                        - \tweak color #red
                        \glissando
                        d''8
                        \glissando
                        f'8
                        \glissando
                        e''8
                        ]
                        \glissando
                        g'8
                        [
                        \glissando
                        f''8
                        \glissando
                        e'8
                        ]
                        \glissando
                        d''8
                        [
                        \glissando
                        f'8
                        \glissando
                        e''8
                        \glissando
                        g'8
                        ]
                        \glissando
                        f''8
                        [
                        \glissando
                        e'8
                        - \tweak color #red
                        \glissando
                        d''8
                        ]
                    }
                >>
            }

    """
    return _commandclasses.GlissandoCommand(
        allow_repeats=allow_repeats,
        allow_ties=allow_ties,
        hide_middle_note_heads=hide_middle_note_heads,
        hide_middle_stems=hide_middle_stems,
        hide_stem_selector=hide_stem_selector,
        left_broken=left_broken,
        map=map,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
        selector=selector,
        tags=[_scoping.site(_frame())],
        tweaks=tweaks,
        zero_padding=zero_padding,
    )


def global_fermata(
    description: str = "fermata",
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> _commandclasses.GlobalFermataCommand:
    """
    Attaches global fermata.
    """
    fermatas = _commandclasses.GlobalFermataCommand.description_to_command.keys()
    if description not in fermatas:
        message = f"must be in {repr(', '.join(fermatas))}:\n"
        message += f"   {repr(description)}"
        raise Exception(message)
    return _commandclasses.GlobalFermataCommand(
        description=description,
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def instrument(
    instrument: abjad.Instrument,
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> _commandclasses.InstrumentChangeCommand:
    """
    Makes instrument change command.
    """
    if not isinstance(instrument, abjad.Instrument):
        message = f"instrument must be instrument (not {instrument!r})."
        raise Exception(message)
    return _commandclasses.InstrumentChangeCommand(
        indicators=[instrument],
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def invisible_music(
    selector=lambda _: _selection.Selection(_).leaf(0),
    *,
    map: abjad.Expression = None,
) -> _scoping.Suite:
    r"""
    Attaches ``\baca-invisible-music`` literal.

    ..  container:: example

        Attaches ``\baca-invisible-music`` literal to middle leaves:

        >>> maker = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     "Music_Voice",
        ...     baca.invisible_music(
        ...         selector=baca.selectors.leaves((1, -1)),
        ...         ),
        ...     baca.make_notes(),
        ...     baca.pitch('C5'),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     maker.commands,
        ...     maker.score_template,
        ...     maker.time_signatures,
        ...     maker.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        c''2
                        %@% \abjad-invisible-music
                        \abjad-invisible-music-coloring
                        c''4.
                        %@% \abjad-invisible-music
                        \abjad-invisible-music-coloring
                        c''2
                        c''4.
                    }
                >>
            }

    """
    tag = _scoping.site(_frame(), n=1)
    tag = tag.append(_tags.INVISIBLE_MUSIC_COMMAND)
    command_1 = _commandclasses.IndicatorCommand(
        [abjad.LilyPondLiteral(r"\abjad-invisible-music")],
        deactivate=True,
        map=map,
        selector=selector,
        tags=[tag],
    )
    tag = _scoping.site(_frame(), n=2)
    tag = tag.append(_tags.INVISIBLE_MUSIC_COLORING)
    command_2 = _commandclasses.IndicatorCommand(
        [abjad.LilyPondLiteral(r"\abjad-invisible-music-coloring")],
        map=map,
        selector=selector,
        tags=[tag],
    )
    return _scoping.suite(command_1, command_2)


def label(
    callable_,
    selector=lambda _: _selection.Selection(_).leaves(),
) -> _commandclasses.LabelCommand:
    r"""
    Applies label ``callable_`` to ``selector`` output.

    ..  container:: example

        Labels pitch names:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.label(lambda _: abjad.label.with_pitches(_, locale="us")),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        ^ \markup { C4 }
                        [
                        d'16
                        ^ \markup { D4 }
                        ]
                        bf'4
                        ^ \markup { Bb4 }
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        ^ \markup { "F#5" }
                        [
                        e''16
                        ^ \markup { E5 }
                        ]
                        ef''4
                        ^ \markup { Eb5 }
                        ~
                        ef''16
                        r16
                        af''16
                        ^ \markup { Ab5 }
                        [
                        g''16
                        ^ \markup { G5 }
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        ^ \markup { A4 }
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commandclasses.LabelCommand(callable_=callable_, selector=selector)


def markup(
    argument: typing.Union[str, abjad.Markup],
    *tweaks: abjad.TweakInterface,
    # typehinting is weird for some reason
    direction=abjad.Up,
    literal: bool = False,
    map: abjad.Expression = None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    selector=lambda _: _selection.Selection(_).pleaf(0),
) -> _commandclasses.IndicatorCommand:
    r"""
    Makes markup and inserts into indicator command.

    ..  container:: example

        Attaches markup to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup('più mosso'),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.outside-staff-priority = 1000
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        ^ \markup { più mosso }
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.outside-staff-priority
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Set ``literal=True`` to pass predefined markup commands:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup(
        ...         r'\markup { \baca-triple-diamond-markup }',
        ...         literal=True,
        ...         ),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.outside-staff-priority = 1000
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        ^ \markup { \baca-triple-diamond-markup }
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.outside-staff-priority
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raises exception on nonstring, nonmarkup ``argument``:

        >>> baca.markup(['Allegro', 'ma non troppo'])
        Traceback (most recent call last):
            ...
        Exception: MarkupLibary.__call__():
            Value of 'argument' must be str or markup.
            Not ['Allegro', 'ma non troppo'].

    """
    if direction not in (abjad.Down, abjad.Up):
        message = f"direction must be up or down (not {direction!r})."
        raise Exception(message)
    if isinstance(argument, str):
        if literal:
            markup = abjad.Markup(argument, direction=direction, literal=True)
        else:
            markup = abjad.Markup(argument, direction=direction)
    elif isinstance(argument, abjad.Markup):
        markup = abjad.new(argument, direction=direction)
    else:
        message = "MarkupLibary.__call__():\n"
        message += "  Value of 'argument' must be str or markup.\n"
        message += f"  Not {argument!r}."
        raise Exception(message)
    if (
        selector is not None
        and not isinstance(selector, str)
        and not callable(selector)
    ):
        message = "selector must be string or callable"
        message += f" (not {selector!r})."
        raise Exception(message)

    def select_phead_0(argument):
        return _selection.Selection(argument).phead(0)

    selector = selector or select_phead_0
    return _commandclasses.IndicatorCommand(
        indicators=[markup],
        map=map,
        match=match,
        measures=measures,
        selector=selector,
        tags=[_scoping.site(_frame())],
        tweaks=tweaks,
    )


def metronome_mark(
    key: typing.Union[str, _indicators.Accelerando, _indicators.Ritardando],
    selector=lambda _: _selection.Selection(_).leaf(0),
    *,
    redundant: bool = None,
) -> typing.Optional[_commandclasses.MetronomeMarkCommand]:
    """
    Attaches metronome mark matching ``key`` metronome mark manifest.
    """
    if redundant is True:
        return None
    return _commandclasses.MetronomeMarkCommand(
        key=key, redundant=redundant, selector=selector
    )


def one_voice(
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> _commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\oneVoice`` command.
    """
    literal = abjad.LilyPondLiteral(r"\oneVoice")
    return _commandclasses.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def open_volta(
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> _scoping.Suite:
    """
    Attaches bar line and overrides bar line X-extent.
    """
    return _scoping.suite(
        _indicatorcommands.bar_line(".|:", selector, format_slot="before"),
        _scoping.not_mol(_overrides.bar_line_x_extent((0, 2), selector)),
        _scoping.only_mol(_overrides.bar_line_x_extent((0, 3), selector)),
    )


def previous_metadata(path: str):
    """
    Gets previous segment metadata before ``path``.
    """
    # reproduces baca.path.Path.get_previous_path()
    # because Travis isn't configured for scores-directory calculations
    music_py = pathlib.Path(path)
    segment = pathlib.Path(music_py).parent
    assert segment.parent.name == "segments", repr(segment)
    segments = segment.parent
    assert segments.name == "segments", repr(segments)
    paths = list(sorted(segments.glob("*")))
    paths = [_ for _ in paths if not _.name.startswith(".")]
    assert all(_.is_dir() for _ in paths), repr(paths)
    index = paths.index(segment)
    if index == 0:
        return {}
    previous_index = index - 1
    previous_segment = paths[previous_index]
    previous_metadata = _path.get_metadata(previous_segment)
    return previous_metadata


def untie(selector: abjad.Expression) -> _commandclasses.DetachCommand:
    """
    Makes (repeat-)tie detach command.
    """
    return _commandclasses.DetachCommand(
        [abjad.Tie, abjad.RepeatTie], selector=selector
    )


def voice_four(
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> _commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceFour`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceFour")
    return _commandclasses.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def voice_one(
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> _commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceOne`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceOne")
    return _commandclasses.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def voice_three(
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> _commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceThree`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceThree")
    return _commandclasses.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def voice_two(
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> _commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceTwo`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceTwo")
    return _commandclasses.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_scoping.site(_frame())],
    )
