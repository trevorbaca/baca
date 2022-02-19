"""
Command classes.
"""
import collections
import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import const as _const
from . import indicators as _indicators
from . import parts as _parts
from . import scoping as _scoping
from . import select as _select
from . import selectors as _selectors
from . import sequence as _sequence
from . import tags as _tags


def _is_rest(argument):
    prototype = (abjad.Rest, abjad.MultimeasureRest, abjad.Skip)
    if isinstance(argument, prototype):
        return True
    annotation = abjad.get.annotation(argument, "is_sounding")
    if annotation is False:
        return True
    return False


def _validate_bcps(bcps):
    if bcps is None:
        return
    for bcp in bcps:
        assert isinstance(bcp, tuple), repr(bcp)
        assert len(bcp) == 2, repr(bcp)


@dataclasses.dataclass
class BCPCommand(_scoping.Command):
    r"""
    Bow contact point command.

    ..  container:: example

        Tweaks LilyPond ``TextSpanner`` grob:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.bcps(
        ...         [(1, 5), (2, 5)],
        ...         abjad.tweak("#red").color,
        ...         abjad.tweak(2.5).staff_padding,
        ...     ),
        ...     baca.pitches("E4 F4"),
        ...     baca.script_staff_padding(5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 16)),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Style LilyPond ``Script`` grob with overrides (instead of tweaks).

        ..  docs::

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
                        \override Script.staff-padding = 5
                        e'8
                        - \downbow
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        ]
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        ]
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        ]
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        - \baca-bcp-spanner-right-text #2 #5
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        \bacaStartTextSpanBCP
                        f'8
                        \bacaStopTextSpanBCP
                        ]
                        \revert Script.staff-padding
                    }
                >>
            }

    ..  container:: example

        REGRESSION. Tweaks survive copy:

        >>> command = baca.bcps(
        ...     [(1, 2), (1, 4)],
        ...     abjad.tweak("#red").color,
        ... )
        >>> command
        BCPCommand()

        >>> import copy
        >>> new_command = copy.copy(command)
        >>> new_command
        BCPCommand()

    ..  container:: example

        PATTERN. Define chunkwise spanners like this:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.new(
        ...         baca.bcps(bcps=[(1, 5), (2, 5)]),
        ...         measures=(1, 2),
        ...     ),
        ...     baca.new(
        ...         baca.bcps(bcps=[(3, 5), (4, 5)]),
        ...         measures=(3, 4),
        ...     ),
        ...     baca.pitches("E4 F4"),
        ...     baca.script_staff_padding(5.5),
        ...     baca.text_spanner_staff_padding(2.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 16)),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

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
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        ]
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        - \baca-bcp-spanner-right-text #1 #5
                        \bacaStartTextSpanBCP
                        e'8
                        \bacaStopTextSpanBCP
                        ]
                        f'8
                        - \downbow
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #3 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #4 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #3 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        ]
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #4 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #3 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #4 #5
                        - \baca-bcp-spanner-right-text #3 #5
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

    bcps: typing.Sequence[abjad.IntegerPair] = None
    bow_change_tweaks: abjad.IndexedTweakManagers = None
    final_spanner: bool = None
    helper: typing.Callable = None
    tweaks: abjad.IndexedTweakManagers = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        if self.bcps is None:
            _validate_bcps(self.bcps)
        _scoping.validate_indexed_tweaks(self.bow_change_tweaks)
        if self.final_spanner is not None:
            self.final_spanner = bool(self.final_spanner)
        if self.helper is not None:
            assert callable(self.helper), repr(self.helper)
        _scoping.validate_indexed_tweaks(self.tweaks)

    __repr__ = _scoping.Command.__repr__

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.bcps is None:
            return
        if self.selector:
            argument = self.selector(argument)
        bcps_ = _sequence.Sequence(self.bcps)
        if self.helper:
            bcps_ = self.helper(bcps_, argument)
        bcps = abjad.CyclicTuple(bcps_)
        lts = _select.lts(argument)
        assert isinstance(lts, list)
        add_right_text_to_me = None
        if not self.final_spanner:
            rest_count, nonrest_count = 0, 0
            lt: abjad.LogicalTie
            for lt in reversed(lts):
                if _is_rest(lt.head):
                    rest_count += 1
                else:
                    if 0 < rest_count and nonrest_count == 0:
                        add_right_text_to_me = lt.head
                        break
                    if 0 < nonrest_count and rest_count == 0:
                        add_right_text_to_me = lt.head
                        break
                    nonrest_count += 1
        if self.final_spanner and not _is_rest(lts[-1]) and len(lts[-1]) == 1:
            next_leaf_after_argument = abjad.get.leaf(lts[-1][-1], 1)
            if next_leaf_after_argument is None:
                message = "can not attach final spanner:"
                message += " argument includes end of score."
                raise Exception(message)
        previous_bcp = None
        i = 0
        for lt in lts:
            stop_text_span = abjad.StopTextSpan(command=self.stop_command)
            if not self.final_spanner and lt is lts[-1] and not _is_rest(lt.head):
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag.append(_scoping.site(_frame(), self, n=1)),
                )
                break
            previous_leaf = abjad.get.leaf(lt.head, -1)
            next_leaf = abjad.get.leaf(lt.head, 1)
            if _is_rest(lt.head) and (_is_rest(previous_leaf) or previous_leaf is None):
                continue
            if (
                isinstance(lt.head, abjad.Note)
                and _is_rest(previous_leaf)
                and previous_bcp is not None
            ):
                numerator, denominator = previous_bcp
            else:
                bcp = bcps[i]
                numerator, denominator = bcp
                i += 1
                next_bcp = bcps[i]
            left_text = r"- \baca-bcp-spanner-left-text"
            left_text += rf" #{numerator} #{denominator}"
            if lt is lts[-1]:
                if self.final_spanner:
                    style = "solid-line-with-arrow"
                else:
                    style = "invisible-line"
            elif not _is_rest(lt.head):
                style = "solid-line-with-arrow"
            else:
                style = "invisible-line"
            right_text = None
            if lt.head is add_right_text_to_me:
                numerator, denominator = next_bcp
                right_text = r"- \baca-bcp-spanner-right-text"
                right_text += rf" #{numerator} #{denominator}"
            start_text_span = abjad.StartTextSpan(
                command=self.start_command,
                left_text=left_text,
                right_text=right_text,
                style=style,
            )
            if self.tweaks:
                _scoping.apply_tweaks(start_text_span, self.tweaks)
            if _is_rest(lt.head) and (_is_rest(next_leaf) or next_leaf is None):
                pass
            else:
                abjad.attach(
                    start_text_span,
                    lt.head,
                    tag=self.tag.append(_scoping.site(_frame(), self, n=2)),
                )
            if 0 < i - 1:
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag.append(_scoping.site(_frame(), self, n=3)),
                )
            if lt is lts[-1] and self.final_spanner:
                abjad.attach(
                    stop_text_span,
                    next_leaf_after_argument,
                    tag=self.tag.append(_scoping.site(_frame(), self, n=4)),
                )
            bcp_fraction = abjad.Fraction(*bcp)
            next_bcp_fraction = abjad.Fraction(*bcps[i])
            if _is_rest(lt.head):
                pass
            elif _is_rest(previous_leaf) or previous_bcp is None:
                if bcp_fraction > next_bcp_fraction:
                    articulation = abjad.Articulation("upbow")
                    if self.bow_change_tweaks:
                        _scoping.apply_tweaks(articulation, self.bow_change_tweaks)
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(_scoping.site(_frame(), self, n=5)),
                    )
                elif bcp_fraction < next_bcp_fraction:
                    articulation = abjad.Articulation("downbow")
                    if self.bow_change_tweaks:
                        _scoping.apply_tweaks(articulation, self.bow_change_tweaks)
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(_scoping.site(_frame(), self, n=6)),
                    )
            else:
                previous_bcp_fraction = abjad.Fraction(*previous_bcp)
                if previous_bcp_fraction < bcp_fraction > next_bcp_fraction:
                    articulation = abjad.Articulation("upbow")
                    if self.bow_change_tweaks:
                        _scoping.apply_tweaks(articulation, self.bow_change_tweaks)
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(_scoping.site(_frame(), self, n=7)),
                    )
                elif previous_bcp_fraction > bcp_fraction < next_bcp_fraction:
                    articulation = abjad.Articulation("downbow")
                    if self.bow_change_tweaks:
                        _scoping.apply_tweaks(articulation, self.bow_change_tweaks)
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(_scoping.site(_frame(), self, n=8)),
                    )
            previous_bcp = bcp

    @property
    def start_command(self) -> str:
        r"""
        Gets ``"\bacaStartTextSpanBCP"``.
        """
        return r"\bacaStartTextSpanBCP"

    @property
    def stop_command(self) -> str:
        r"""
        Gets ``"\bacaStopTextSpanBCP"``.
        """
        return r"\bacaStopTextSpanBCP"


@dataclasses.dataclass
class ColorCommand(_scoping.Command):
    """
    Color command.
    """

    lone: bool = None

    def __post_init__(self):
        assert self.selector is not None
        _scoping.Command.__post_init__(self)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        assert self.selector is not None
        argument = self.selector(argument)
        abjad.label.by_selector(argument, self.selector, lone=self.lone)


@dataclasses.dataclass
class ContainerCommand(_scoping.Command):
    r"""
    Container command.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.container("ViolinI", selector=baca.selectors.leaves((None, 2))),
        ...     baca.container("ViolinII", selector=baca.selectors.leaves((2, None))),
        ...     baca.pitches("E4 F4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

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

    identifier: str = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        if self.identifier is not None:
            if not isinstance(self.identifier, str):
                raise Exception(f"identifier must be string (not {self.identifier!r}).")

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if not self.identifier:
            identifier = None
        elif self.identifier.startswith("%*%"):
            identifier = self.identifier
        else:
            identifier = f"%*% {self.identifier}"
        container = abjad.Container(identifier=identifier)
        components = abjad.select.leaves(argument)
        components = abjad.select.top(components)
        abjad.mutate.wrap(components, container)

    def _mutates_score(self):
        return True


@dataclasses.dataclass
class DetachCommand(_scoping.Command):
    """
    Detach command.

    ..  container:: example

        >>> arguments = [abjad.RepeatTie, abjad.Tie]
        >>> baca.DetachCommand(arguments, baca.selectors.leaves())
        DetachCommand()

    """

    arguments: typing.Sequence[typing.Any] = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)

    __repr__ = _scoping.Command.__repr__

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        assert self.selector is not None
        argument = self.selector(argument)
        leaves = abjad.select.leaves(argument)
        assert isinstance(leaves, list)
        for leaf in leaves:
            for argument in self.arguments:
                abjad.detach(argument, leaf)


@dataclasses.dataclass
class GlissandoCommand(_scoping.Command):
    """
    Glissando command.
    """

    allow_repeats: bool = None
    allow_ties: bool = None
    hide_middle_note_heads: bool = None
    hide_middle_stems: bool = None
    hide_stem_selector: typing.Callable = None
    left_broken: bool = None
    parenthesize_repeats: bool = None
    right_broken: bool = None
    right_broken_show_next: bool = None
    selector: typing.Any = _selectors.tleaves()
    tweaks: abjad.IndexedTweakManagers = None
    zero_padding: bool = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        _scoping.validate_indexed_tweaks(self.tweaks)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = abjad.select.leaves(argument)
        tweaks_: typing.List[abjad.IndexedTweakManager] = []
        prototype = (abjad.TweakInterface, tuple)
        for tweak in self.tweaks or []:
            assert isinstance(tweak, prototype)
            tweaks_.append(tweak)
        abjad.glissando(
            leaves,
            *tweaks_,
            allow_repeats=self.allow_repeats,
            allow_ties=self.allow_ties,
            hide_middle_note_heads=self.hide_middle_note_heads,
            hide_middle_stems=self.hide_middle_stems,
            hide_stem_selector=self.hide_stem_selector,
            left_broken=self.left_broken,
            parenthesize_repeats=self.parenthesize_repeats,
            right_broken=self.right_broken,
            right_broken_show_next=self.right_broken_show_next,
            tag=self.tag,
            zero_padding=self.zero_padding,
        )


@dataclasses.dataclass
class GlobalFermataCommand(_scoping.Command):
    """
    Global fermata command.
    """

    description: str = None

    description_to_command = {
        "short": "shortfermata",
        "fermata": "fermata",
        "long": "longfermata",
        "very_long": "verylongfermata",
    }

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        if self.description is not None:
            assert self.description in self.description_to_command

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if isinstance(self.description, str) and self.description != "fermata":
            description = self.description.replace("_", "-")
            command = f"{description}-fermata"
        else:
            command = "fermata"
        if self.description == "short":
            fermata_duration = 1
        elif self.description == "fermata":
            fermata_duration = 2
        elif self.description == "long":
            fermata_duration = 4
        elif self.description == "very_long":
            fermata_duration = 8
        else:
            raise Exception(self.description)
        for leaf in abjad.iterate.leaves(argument):
            assert isinstance(leaf, abjad.MultimeasureRest)
            string = rf"\baca-{command}-markup"
            markup = abjad.Markup(string)
            markup = dataclasses.replace(markup, direction=abjad.Up)
            abjad.attach(
                markup,
                leaf,
                tag=self.tag.append(_scoping.site(_frame(), self, n=1)),
            )
            literal = abjad.LilyPondLiteral(r"\baca-fermata-measure")
            abjad.attach(
                literal,
                leaf,
                tag=self.tag.append(_scoping.site(_frame(), self, n=2)),
            )
            tag = abjad.Tag(_const.FERMATA_MEASURE)
            tag = tag.append(self.tag)
            tag = tag.append(_scoping.site(_frame(), self, n=3))
            abjad.attach(
                _const.FERMATA_MEASURE,
                leaf,
                tag=_tags.FERMATA_MEASURE,
            )
            abjad.annotate(leaf, _const.FERMATA_DURATION, fermata_duration)


def _token_to_indicators(token):
    result = []
    if not isinstance(token, (tuple, list)):
        token = [token]
    for item in token:
        if item is None:
            continue
        result.append(item)
    return result


@dataclasses.dataclass
class IndicatorCommand(_scoping.Command):
    """
    Indicator command.
    """

    indicators: typing.List[typing.Any] = None
    context: str = None
    do_not_test: bool = None
    predicate: typing.Callable = None
    redundant: bool = None
    tweaks: abjad.IndexedTweakManagers = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        if self.context is not None:
            assert isinstance(self.context, str), repr(self.context)
        if self.do_not_test is not None:
            self.do_not_test = bool(self.do_not_test)
        indicators_ = None
        if self.indicators is not None:
            if isinstance(self.indicators, collections.abc.Iterable):
                indicators_ = abjad.CyclicTuple(self.indicators)
            else:
                indicators_ = abjad.CyclicTuple([self.indicators])
        self.indicators = indicators_
        if self.redundant is not None:
            self.redundant = bool(self.redundant)
        _scoping.validate_indexed_tweaks(self.tweaks)

    __repr__ = _scoping.Command.__repr__

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.indicators is None:
            return
        if self.redundant is True:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        leaves = abjad.select.leaves(argument)
        for i, leaf in enumerate(leaves):
            if self.predicate and not self.predicate(leaf):
                continue
            indicators = self.indicators[i]
            indicators = _token_to_indicators(indicators)
            for indicator in indicators:
                _scoping.apply_tweaks(indicator, self.tweaks)
                reapplied = _scoping.remove_reapplied_wrappers(leaf, indicator)
                wrapper = abjad.attach(
                    indicator,
                    leaf,
                    context=self.context,
                    deactivate=self.deactivate,
                    do_not_test=self.do_not_test,
                    tag=self.tag.append(_scoping.site(_frame(), self)),
                    wrapper=True,
                )
                if _scoping.compare_persistent_indicators(indicator, reapplied):
                    status = "redundant"
                    _scoping.treat_persistent_wrapper(
                        self.runtime["manifests"], wrapper, status
                    )


@dataclasses.dataclass
class InstrumentChangeCommand(IndicatorCommand):
    """
    Instrument change command.
    """

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if self.indicators is None:
            return
        first_leaf = abjad.get.leaf(argument, 0)
        if first_leaf is not None:
            staff = abjad.get.parentage(first_leaf).get(abjad.Staff)
            assert isinstance(staff, abjad.Staff)
            instrument = self.indicators[0]
            assert isinstance(instrument, abjad.Instrument), repr(instrument)
            if self.runtime["allows_instrument"]:
                if not self.runtime["allows_instrument"](staff.name, instrument):
                    message = f"{staff.name} does not allow instrument:\n"
                    message += f"  {instrument}"
                    raise Exception(message)
        super()._call(argument)


@dataclasses.dataclass
class LabelCommand(_scoping.Command):
    """
    Label command.
    """

    callable_: typing.Any = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)

    def _call(self, argument=None):
        if argument is None:
            return
        if self.callable_ is None:
            return
        if self.selector:
            argument = self.selector(argument)
        self.callable_(argument)


@dataclasses.dataclass
class MetronomeMarkCommand(_scoping.Command):
    """
    Metronome mark command.
    """

    key: str | _indicators.Accelerando | _indicators.Ritardando = None
    redundant: bool = None
    selector: typing.Any = _selectors.leaf(0)

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        prototype = (str, _indicators.Accelerando, _indicators.Ritardando)
        if self.key is not None:
            assert isinstance(self.key, prototype), repr(self.key)
        if self.redundant is not None:
            self.redundant = bool(self.redundant)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.key is None:
            return
        if self.redundant is True:
            return
        if isinstance(self.key, str) and self.runtime["manifests"] is not None:
            metronome_marks = self.runtime["manifests"]["abjad.MetronomeMark"]
            indicator = metronome_marks.get(self.key)
            if indicator is None:
                raise Exception(f"can not find metronome mark {self.key!r}.")
        else:
            indicator = self.key
        if self.selector is not None:
            argument = self.selector(argument)
        if not argument:
            return
        leaf = abjad.select.leaf(argument, 0)
        reapplied = _scoping.remove_reapplied_wrappers(leaf, indicator)
        wrapper = abjad.attach(
            indicator,
            leaf,
            deactivate=self.deactivate,
            tag=self.tag,
            wrapper=True,
        )
        if indicator == reapplied:
            _scoping.treat_persistent_wrapper(
                self.runtime["manifests"], wrapper, "redundant"
            )


@dataclasses.dataclass
class PartAssignmentCommand(_scoping.Command):
    """
    Part assignment command.
    """

    part_assignment: _parts.PartAssignment = None

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        if self.part_assignment is not None:
            if not isinstance(self.part_assignment, _parts.PartAssignment):
                message = "part_assignment must be part assignment"
                message += f" (not {self.part_assignment!r})."
                raise Exception(message)

    __repr__ = _scoping.Command.__repr__

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        first_leaf = abjad.get.leaf(argument, 0)
        if first_leaf is None:
            return
        voice = abjad.get.parentage(first_leaf).get(abjad.Voice, -1)
        if voice is not None and self.part_assignment is not None:
            assert isinstance(voice, abjad.Voice)
            section = self.part_assignment.section or "ZZZ"
            if not voice.name.startswith(section):
                message = f"{voice.name} does not allow"
                message += f" {self.part_assignment.section} part assignment:"
                message += f"\n  {self.part_assignment}"
                raise Exception(message)
        section, token = self.part_assignment.section, self.part_assignment.token
        if token is None:
            identifier = f"%*% PartAssignment({section!r})"
        else:
            identifier = f"%*% PartAssignment({section!r}, {token!r})"
        container = abjad.Container(identifier=identifier)
        components = abjad.select.leaves(argument)
        components = abjad.select.top(argument)
        abjad.mutate.wrap(components, container)

    def _mutates_score(self):
        # return True
        return False
