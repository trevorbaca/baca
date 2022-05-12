"""
Command classes.
"""
import collections
import copy
import dataclasses
import numbers
import pathlib
import typing
from inspect import currentframe as _frame

import abjad

from . import command as _command
from . import indicators as _indicators
from . import overrides as _overrides
from . import parts as _parts
from . import path as _path
from . import pcollections as _pcollections
from . import select as _select
from . import tags as _tags
from . import treat as _treat
from . import tweaks as _tweaks
from . import typings as _typings
from .enums import enums as _enums


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


@dataclasses.dataclass(slots=True)
class BCPCommand(_command.Command):
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
        ...         abjad.Tweak(r"- \tweak color #red"),
        ...         abjad.Tweak(r"- \tweak staff-padding 2.5"),
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
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        ]
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        [
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        ]
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        [
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        ]
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        [
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        - \baca-bcp-spanner-right-text #2 #5
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
        ...     abjad.Tweak(r"- \tweak color #red"),
        ... )

        >>> import copy
        >>> new_command = copy.copy(command)
        >>> new_command.tweaks
        (Tweak(string='- \\tweak color #red', tag=None),)

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

    bcps: typing.Sequence[tuple[int, int]] = ()
    bow_change_tweaks: tuple[_typings.IndexedTweak, ...] = ()
    final_spanner: bool = False
    helper: typing.Callable = lambda x, y: x
    tweaks: tuple[_typings.IndexedTweak, ...] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        _validate_bcps(self.bcps)
        _tweaks.validate_indexed_tweaks(self.bow_change_tweaks)
        self.final_spanner = bool(self.final_spanner)
        assert callable(self.helper), repr(self.helper)
        _tweaks.validate_indexed_tweaks(self.tweaks)

    __repr__ = _command.Command.__repr__

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.bcps is None:
            return
        if self.selector:
            argument = self.selector(argument)
        bcps_ = list(self.bcps)
        bcps_ = self.helper(bcps_, argument)
        bcps = abjad.CyclicTuple(bcps_)
        lts = _select.lts(argument)
        add_right_text_to_me = None
        if not self.final_spanner:
            rest_count, nonrest_count = 0, 0
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
                    tag=self.tag.append(_tags.function_name(_frame(), self, n=1)),
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
                start_text_span = _tweaks.bundle_tweaks(start_text_span, self.tweaks)
            if _is_rest(lt.head) and (_is_rest(next_leaf) or next_leaf is None):
                pass
            else:
                abjad.attach(
                    start_text_span,
                    lt.head,
                    tag=self.tag.append(_tags.function_name(_frame(), self, n=2)),
                )
            if 0 < i - 1:
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag.append(_tags.function_name(_frame(), self, n=3)),
                )
            if lt is lts[-1] and self.final_spanner:
                abjad.attach(
                    stop_text_span,
                    next_leaf_after_argument,
                    tag=self.tag.append(_tags.function_name(_frame(), self, n=4)),
                )
            bcp_fraction = abjad.Fraction(*bcp)
            next_bcp_fraction = abjad.Fraction(*bcps[i])
            if _is_rest(lt.head):
                pass
            elif _is_rest(previous_leaf) or previous_bcp is None:
                if bcp_fraction > next_bcp_fraction:
                    articulation = abjad.Articulation("upbow")
                    if self.bow_change_tweaks:
                        articulation = _tweaks.bundle_tweaks(
                            articulation, self.bow_change_tweaks
                        )
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(_tags.function_name(_frame(), self, n=5)),
                    )
                elif bcp_fraction < next_bcp_fraction:
                    articulation = abjad.Articulation("downbow")
                    if self.bow_change_tweaks:
                        articulation = _tweaks.bundle_tweaks(
                            articulation, self.bow_change_tweaks
                        )
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(_tags.function_name(_frame(), self, n=6)),
                    )
            else:
                previous_bcp_fraction = abjad.Fraction(*previous_bcp)
                if previous_bcp_fraction < bcp_fraction > next_bcp_fraction:
                    articulation = abjad.Articulation("upbow")
                    if self.bow_change_tweaks:
                        articulation = _tweaks.bundle_tweaks(
                            articulation, self.bow_change_tweaks
                        )
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(_tags.function_name(_frame(), self, n=7)),
                    )
                elif previous_bcp_fraction > bcp_fraction < next_bcp_fraction:
                    articulation = abjad.Articulation("downbow")
                    if self.bow_change_tweaks:
                        articulation = _tweaks.bundle_tweaks(
                            articulation, self.bow_change_tweaks
                        )
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(_tags.function_name(_frame(), self, n=8)),
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


@dataclasses.dataclass(slots=True)
class ColorCommand(_command.Command):
    """
    Color command.
    """

    lone: bool = False

    def __post_init__(self):
        assert self.selector is not None
        _command.Command.__post_init__(self)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        assert self.selector is not None
        argument = self.selector(argument)
        abjad.label.by_selector(argument, self.selector, lone=self.lone)


@dataclasses.dataclass(slots=True)
class ContainerCommand(_command.Command):
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
        ...     baca.container(
        ...         "ViolinI",
        ...         selector=lambda _: baca.select.leaves(_)[:2],
        ...     ),
        ...     baca.container(
        ...         "ViolinII",
        ...         selector=lambda _: baca.select.leaves(_)[2:],
        ...         ),
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

    identifier: str | None = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.identifier, str), repr(self.identifier)

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
        leaves = abjad.select.leaves(argument)
        components = abjad.select.top(leaves)
        abjad.mutate.wrap(components, container)

    def _mutates_score(self):
        return True


@dataclasses.dataclass(slots=True)
class DetachCommand(_command.Command):
    """
    Detach command.
    """

    arguments: typing.Sequence[typing.Any] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)

    __repr__ = _command.Command.__repr__

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


@dataclasses.dataclass(slots=True)
class GenericCommand(_command.Command):

    function: typing.Callable = lambda _: _
    name: str = ""

    def __post_init__(self):
        assert callable(self.function), repr(self.function)
        _command.Command.__post_init__(self)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        assert self.selector is not None
        argument = self.selector(argument)
        self.function(argument, runtime=self._runtime)


def _attach_default_indicators(staff_or_staff_group):
    prototype = (abjad.Staff, abjad.StaffGroup)
    assert isinstance(staff_or_staff_group, prototype), repr(staff_or_staff_group)
    wrappers = []
    tag = _enums.REMOVE_ALL_EMPTY_STAVES
    empty_prototype = (abjad.MultimeasureRest, abjad.Skip)
    prototype = (abjad.Staff, abjad.StaffGroup)
    if isinstance(staff_or_staff_group, abjad.Staff):
        staff_or_staff_groups = [staff_or_staff_group]
        staves = [staff_or_staff_group]
    else:
        assert isinstance(staff_or_staff_group, abjad.StaffGroup)
        staff_or_staff_groups = [staff_or_staff_group]
        staves = []
    for staff_or_staff_group in staff_or_staff_groups:
        leaf = None
        voices = abjad.select.components(staff_or_staff_group, abjad.Voice)
        assert isinstance(voices, list), repr(voices)
        # find leaf 0 in first nonempty voice
        for voice in voices:
            leaves = []
            for leaf_ in abjad.iterate.leaves(voice):
                if abjad.get.has_indicator(leaf_, _enums.HIDDEN):
                    leaves.append(leaf_)
            if not all(isinstance(_, empty_prototype) for _ in leaves):
                leaf = abjad.get.leaf(voice, 0)
                break
        # otherwise, find first leaf in voice in non-removable staff
        if leaf is None:
            for voice in voices:
                voice_might_vanish = False
                for component in abjad.get.parentage(voice):
                    if abjad.get.annotation(component, tag) is True:
                        voice_might_vanish = True
                if not voice_might_vanish:
                    leaf = abjad.get.leaf(voice, 0)
                    if leaf is not None:
                        break
        # otherwise, as last resort find first leaf in first voice
        if leaf is None:
            leaf = abjad.get.leaf(voices[0], 0)
        if leaf is None:
            continue
        instrument = abjad.get.indicator(leaf, abjad.Instrument)
        if instrument is None:
            string = "default_instrument"
            instrument = abjad.get.annotation(staff_or_staff_group, string)
            if instrument is not None:
                wrapper = abjad.attach(
                    instrument,
                    leaf,
                    context=staff_or_staff_group.lilypond_type,
                    tag=_tags.function_name(_frame(), n=1),
                    wrapper=True,
                )
                wrappers.append(wrapper)
        margin_markup = abjad.get.indicator(leaf, abjad.MarginMarkup)
        if margin_markup is None:
            string = "default_margin_markup"
            margin_markup = abjad.get.annotation(staff_or_staff_group, string)
            if margin_markup is not None:
                wrapper = abjad.attach(
                    margin_markup,
                    leaf,
                    tag=_tags.NOT_PARTS.append(_tags.function_name(_frame(), n=2)),
                    wrapper=True,
                )
                wrappers.append(wrapper)
    for staff in staves:
        leaf = abjad.get.leaf(staff, 0)
        clef = abjad.get.indicator(leaf, abjad.Clef)
        if clef is not None:
            continue
        clef = abjad.get.annotation(staff, "default_clef")
        if clef is not None:
            wrapper = abjad.attach(
                clef,
                leaf,
                tag=_tags.function_name(_frame(), n=3),
                wrapper=True,
            )
            wrappers.append(wrapper)
    return wrappers


def _attach_first_segment_default_indicators(manifests, staff_or_staff_group):
    for wrapper in _attach_default_indicators(staff_or_staff_group):
        _treat.treat_persistent_wrapper(manifests, wrapper, "default")


def attach_first_appearance_default_indicators(
    *, selector=lambda _: _select.leaves(_)
) -> GenericCommand:
    def function(argument, *, runtime=None):
        manifests = runtime["manifests"]
        previous_persistent_indicators = runtime["previous_persistent_indicators"]
        leaf = abjad.select.leaf(argument, 0)
        parentage = abjad.get.parentage(leaf)
        staff_or_staff_groups = []
        for component in parentage:
            if isinstance(component, abjad.Staff | abjad.StaffGroup):
                if component.name not in previous_persistent_indicators:
                    staff_or_staff_groups.append(component)
        for staff_or_staff_group in staff_or_staff_groups:
            for wrapper in _attach_default_indicators(staff_or_staff_group):
                _treat.treat_persistent_wrapper(manifests, wrapper, "default")

    command = GenericCommand(function=function, selector=selector)
    command.name = "attach_first_apperance_default_indicators"
    return command


def attach_first_segment_default_indicators(
    *, selector=lambda _: _select.leaves(_)
) -> GenericCommand:
    def function(argument, *, runtime=None):
        manifests = runtime["manifests"]
        leaf = abjad.select.leaf(argument, 0)
        parentage = abjad.get.parentage(leaf)
        staff_or_staff_groups = []
        for component in parentage:
            if isinstance(component, abjad.Staff | abjad.StaffGroup):
                staff_or_staff_groups.append(component)
        for staff_or_staff_group in staff_or_staff_groups:
            _attach_first_segment_default_indicators(manifests, staff_or_staff_group)

    command = GenericCommand(function=function, selector=selector)
    command.name = "attach_first_segment_default_indicators"
    return command


def append_phantom_measure(*, selector=lambda _: _select.leaves(_)) -> GenericCommand:
    def function(argument, *, runtime=None):
        from . import interpret as _interpret

        leaf = abjad.get.leaf(argument, 0)
        parentage = abjad.get.parentage(leaf)
        voice = parentage.get(abjad.Voice, n=-1)
        final_leaf = abjad.get.leaf(voice, -1)
        suppress_note = False
        if isinstance(final_leaf, abjad.MultimeasureRest):
            suppress_note = True
        container = _interpret._make_multimeasure_rest_container(
            voice.name,
            (1, 4),
            skips_instead_of_rests=False,
            phantom=True,
            suppress_note=suppress_note,
        )
        voice.append(container)

    command = GenericCommand(function=function, selector=selector)
    command.name = "append_phantom_measure"
    return command


def reapply_persistent_indicators(
    *, selector=lambda _: _select.leaves(_)
) -> GenericCommand:
    from . import interpret as _interpret

    def function(argument, *, runtime=None):
        already_reapplied_contexts = runtime["already_reapplied_contexts"]
        manifests = runtime["manifests"]
        previous_persistent_indicators = runtime["previous_persistent_indicators"]
        leaf = abjad.select.leaf(argument, 0)
        parentage = abjad.get.parentage(leaf)
        contexts = []
        score = None
        for component in parentage:
            if isinstance(component, abjad.Score):
                score = component
            elif isinstance(component, abjad.Context):
                contexts.append(component)
        assert isinstance(score, abjad.Score)
        for context in contexts:
            _interpret._reapply_persistent_indicators(
                already_reapplied_contexts,
                manifests,
                previous_persistent_indicators,
                score,
                do_not_iterate=context,
            )

    command = GenericCommand(function=function, selector=selector)
    command.name = "reapply_persistent_indicators"
    return command


@dataclasses.dataclass(slots=True)
class GlissandoCommand(_command.Command):
    """
    Glissando command.
    """

    allow_repeats: bool = False
    allow_ties: bool = False
    hide_middle_note_heads: bool = False
    hide_middle_stems: bool = False
    hide_stem_selector: typing.Callable | None = None
    left_broken: bool = False
    parenthesize_repeats: bool = False
    right_broken: bool = False
    right_broken_show_next: bool = False
    selector: typing.Callable = lambda _: _select.tleaves(_)
    tweaks: typing.Sequence[abjad.Tweak] = ()
    zero_padding: bool = False

    def __post_init__(self):
        _command.Command.__post_init__(self)
        _tweaks.validate_indexed_tweaks(self.tweaks)

    def _call(self, argument=None):
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = abjad.select.leaves(argument)
        tweaks_ = []
        prototype = (abjad.Tweak, tuple)
        for tweak in self.tweaks or []:
            assert isinstance(tweak, prototype), repr(tweak)
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


@dataclasses.dataclass(slots=True)
class GlobalFermataCommand(_command.Command):
    """
    Global fermata command.
    """

    description: str = ""

    description_to_command = {
        "short": "shortfermata",
        "fermata": "fermata",
        "long": "longfermata",
        "very_long": "verylongfermata",
    }

    def __post_init__(self):
        _command.Command.__post_init__(self)
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
            markup = dataclasses.replace(markup)
            abjad.attach(
                markup,
                leaf,
                direction=abjad.UP,
                tag=self.tag.append(_tags.function_name(_frame(), self, n=1)),
            )
            literal = abjad.LilyPondLiteral(r"\baca-fermata-measure")
            abjad.attach(
                literal,
                leaf,
                tag=self.tag.append(_tags.function_name(_frame(), self, n=2)),
            )
            tag = abjad.Tag(_enums.FERMATA_MEASURE.name)
            tag = tag.append(self.tag)
            tag = tag.append(_tags.function_name(_frame(), self, n=3))
            abjad.attach(
                _enums.FERMATA_MEASURE,
                leaf,
                tag=_tags.FERMATA_MEASURE,
            )
            abjad.annotate(leaf, _enums.FERMATA_DURATION, fermata_duration)


def _token_to_indicators(token):
    result = []
    if not isinstance(token, tuple | list):
        token = [token]
    for item in token:
        if item is None:
            continue
        result.append(item)
    return result


@dataclasses.dataclass(slots=True)
class IndicatorCommand(_command.Command):
    """
    Indicator command.
    """

    indicators: typing.Sequence = ()
    context: str | None = None
    direction: abjad.Vertical | None = None
    do_not_test: bool = False
    predicate: typing.Callable | None = None
    redundant: bool = False
    tweaks: typing.Sequence[_typings.IndexedTweak] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        if self.context is not None:
            assert isinstance(self.context, str), repr(self.context)
        self.do_not_test = bool(self.do_not_test)
        indicators_ = None
        if self.indicators is not None:
            if isinstance(self.indicators, collections.abc.Iterable):
                indicators_ = abjad.CyclicTuple(self.indicators)
            else:
                indicators_ = abjad.CyclicTuple([self.indicators])
        self.indicators = indicators_
        self.redundant = bool(self.redundant)
        _tweaks.validate_indexed_tweaks(self.tweaks)

    def __copy__(self, *arguments):
        result = dataclasses.replace(self)
        result.indicators = copy.deepcopy(self.indicators)
        return result

    __repr__ = _command.Command.__repr__

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
                reapplied = _treat.remove_reapplied_wrappers(leaf, indicator)
                if self.tweaks:
                    indicator = _tweaks.bundle_tweaks(indicator, self.tweaks)
                wrapper = abjad.attach(
                    indicator,
                    leaf,
                    context=self.context,
                    deactivate=self.deactivate,
                    direction=self.direction,
                    do_not_test=self.do_not_test,
                    tag=self.tag.append(_tags.function_name(_frame(), self)),
                    wrapper=True,
                )
                if _treat.compare_persistent_indicators(indicator, reapplied):
                    status = "redundant"
                    _treat.treat_persistent_wrapper(
                        self.runtime["manifests"], wrapper, status
                    )


@dataclasses.dataclass(slots=True)
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
        IndicatorCommand._call(self, argument)


@dataclasses.dataclass(slots=True)
class LabelCommand(_command.Command):
    """
    Label command.
    """

    callable_: typing.Any = None

    def __post_init__(self):
        _command.Command.__post_init__(self)

    def _call(self, argument=None):
        if argument is None:
            return
        if self.callable_ is None:
            return
        if self.selector:
            argument = self.selector(argument)
        self.callable_(argument)


@dataclasses.dataclass(slots=True)
class MetronomeMarkCommand(_command.Command):
    """
    Metronome mark command.
    """

    key: str | _indicators.Accelerando | _indicators.Ritardando | None = None
    redundant: bool = False
    selector: typing.Callable = lambda _: abjad.select.leaf(_, 0)

    def __post_init__(self):
        _command.Command.__post_init__(self)
        prototype = (str, _indicators.Accelerando, _indicators.Ritardando)
        if self.key is not None:
            assert isinstance(self.key, prototype), repr(self.key)
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
        reapplied = _treat.remove_reapplied_wrappers(leaf, indicator)
        wrapper = abjad.attach(
            indicator,
            leaf,
            deactivate=self.deactivate,
            tag=self.tag,
            wrapper=True,
        )
        if indicator == reapplied:
            _treat.treat_persistent_wrapper(
                self.runtime["manifests"], wrapper, "redundant"
            )


@dataclasses.dataclass(slots=True)
class PartAssignmentCommand(_command.Command):
    """
    Part assignment command.
    """

    part_assignment: _parts.PartAssignment | None = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        if not isinstance(self.part_assignment, _parts.PartAssignment):
            message = "part_assignment must be part assignment"
            message += f" (not {self.part_assignment!r})."
            raise Exception(message)

    __repr__ = _command.Command.__repr__

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
            assert voice.name is not None
            if not voice.name.startswith(section):
                message = f"{voice.name} does not allow"
                message += f" {self.part_assignment.section} part assignment:"
                message += f"\n  {self.part_assignment}"
                raise Exception(message)
        assert self.part_assignment is not None
        section, token = self.part_assignment.section, self.part_assignment.token
        if token is None:
            identifier = f"%*% PartAssignment({section!r})"
        else:
            identifier = f"%*% PartAssignment({section!r}, {token!r})"
        container = abjad.Container(identifier=identifier)
        leaves = abjad.select.leaves(argument)
        components = abjad.select.top(leaves)
        abjad.mutate.wrap(components, container)

    def _mutates_score(self):
        # return True
        return False


@dataclasses.dataclass(slots=True)
class AccidentalAdjustmentCommand(_command.Command):
    r"""
    Accidental adjustment command.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches("E4 F4"),
        ...     baca.force_accidental(
        ...         selector=lambda _: baca.select.pleaves(_)[:2],
        ...     ),
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
                        e'!2
                        f'!4.
                        e'2
                        f'4.
                    }
                >>
            }

    """

    cautionary: bool = False
    forced: bool = False
    parenthesized: bool = False

    def __post_init__(self):
        _command.Command.__post_init__(self)
        self.cautionary = bool(self.cautionary)
        self.forced = bool(self.forced)
        self.parenthesized = bool(self.parenthesized)

    __repr__ = _command.Command.__repr__

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if self.tag.string:
            if not self.tag.only_edition() and not self.tag.not_editions():
                raise Exception(f"tag must have edition: {self.tag!r}.")
            tag = _tags.function_name(_frame(), self)
            alternative_tag = self.tag.append(tag)
            primary_tag = alternative_tag.invert_edition_tags()
        pleaves = _select.pleaves(argument)
        assert isinstance(pleaves, list)
        for pleaf in pleaves:
            if isinstance(pleaf, abjad.Note):
                note_heads = [pleaf.note_head]
            else:
                assert isinstance(pleaf, abjad.Chord)
                note_heads = list(pleaf.note_heads)
            for note_head in note_heads:
                assert note_head is not None
                if not self.tag.string:
                    if self.cautionary:
                        note_head.is_cautionary = True
                    if self.forced:
                        note_head.is_forced = True
                    if self.parenthesized:
                        note_head.is_parenthesized = True
                else:
                    alternative = copy.copy(note_head)
                    if self.cautionary:
                        alternative.is_cautionary = True
                    if self.forced:
                        alternative.is_forced = True
                    if self.parenthesized:
                        alternative.is_parenthesized = True
                    note_head.alternative = (
                        alternative,
                        alternative_tag,
                        primary_tag,
                    )


@dataclasses.dataclass(slots=True)
class ClusterCommand(_command.Command):
    r"""
    Cluster command.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.replace_with_clusters([3, 4]),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        \time 9/16
                        <c' e' g'>16
                        ^ \markup \center-align \concat { \natural \flat }
                        [
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <d' f' a' c''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <bf' d'' f''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <fs'' a'' c''' e'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        [
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'' g'' b''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <ef'' g'' b'' d'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <af'' c''' e'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g'' b'' d''' f'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <a' c'' e''>16
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                }
            >>

    ..  container:: example

        Hides flat markup:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitch("E4"),
        ...     baca.natural_clusters(widths=[3]),
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

        ..  docs::

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
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \natural
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \natural
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \natural
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \natural
                    }
                >>
            }

    ..  container:: example

        Takes start pitch from input notes:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches("C4 D4 E4 F4"),
        ...     baca.replace_with_clusters([3]),
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

        ..  docs::

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
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <c' e' g'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <d' f' a'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <f' a' c''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Sets start pitch explicitly:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.replace_with_clusters([3], start_pitch="G4"),
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

        ..  docs::

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
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Increasing widths:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.replace_with_clusters([1, 2, 3, 4], start_pitch="E4"),
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

        ..  docs::

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
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b' d''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Patterned widths:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.replace_with_clusters([1, 3], start_pitch="E4"),
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

        ..  docs::

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
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Leaves notes and chords unchanged:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitch("E4"),
        ...     baca.replace_with_clusters([]),
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
                        e'2
                        e'4.
                        e'2
                        e'4.
                    }
                >>
            }

        Inteprets positive integers as widths in thirds.

        Interprets zero to mean input note or chord is left unchanged.

    """

    direction: abjad.Vertical | None = abjad.UP
    hide_flat_markup: bool = False
    selector: typing.Callable = lambda _: _select.plts(_)
    start_pitch: typing.Any = None
    widths: typing.Any = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        self.hide_flat_markup = bool(self.hide_flat_markup)
        if self.start_pitch is not None:
            self.start_pitch = abjad.NamedPitch(self.start_pitch)
        assert abjad.math.all_are_nonnegative_integers(self.widths)
        self.widths = abjad.CyclicTuple(self.widths)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if not self.widths:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        leaf = abjad.select.leaf(argument, 0)
        root = abjad.get.parentage(leaf).root
        with abjad.ForbidUpdate(component=root):
            for i, plt in enumerate(_select.plts(argument)):
                width = self.widths[i]
                self._make_cluster(plt, width)

    def _make_cluster(self, plt, width):
        assert plt.is_pitched, repr(plt)
        if not width:
            return
        if self.start_pitch is not None:
            start_pitch = self.start_pitch
        else:
            start_pitch = plt.head.written_pitch
        pitches = self._make_pitches(start_pitch, width)
        key_cluster = abjad.KeyCluster(include_flat_markup=not self.hide_flat_markup)
        for pleaf in plt:
            chord = abjad.Chord(pitches, pleaf.written_duration)
            wrappers = abjad.get.wrappers(pleaf)
            abjad.detach(object, pleaf)
            for wrapper in wrappers:
                abjad.attach(wrapper, chord, direction=wrapper.direction)
            abjad.mutate.replace(pleaf, chord)
            abjad.attach(key_cluster, chord, direction=self.direction)
            abjad.attach(_enums.ALLOW_REPEAT_PITCH, chord)
            abjad.detach(_enums.NOT_YET_PITCHED, chord)

    def _make_pitches(self, start_pitch, width):
        pitches = [start_pitch]
        for i in range(width - 1):
            pitch = pitches[-1] + abjad.NamedInterval("M3")
            pitch = abjad.NamedPitch(pitch, accidental="natural")
            assert pitch.accidental == abjad.Accidental("natural")
            pitches.append(pitch)
        return pitches

    def _mutates_score(self):
        return True


@dataclasses.dataclass(slots=True)
class ColorFingeringCommand(_command.Command):
    r"""
    Color fingering command.

    ..  container:: example

        With segment-commands:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitch("E4"),
        ...     baca.ColorFingeringCommand(numbers=[0, 1, 2, 1]),
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
                        e'2
                        e'4.
                        ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }
                        e'2
                        ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 2 }
                        e'4.
                        ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }
                    }
                >>
            }

    """

    direction: abjad.Vertical | None = abjad.UP
    numbers: typing.Any = None
    tweaks: tuple[_typings.IndexedTweak, ...] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        if self.numbers is not None:
            assert abjad.math.all_are_nonnegative_integers(self.numbers)
            self.numbers = abjad.CyclicTuple(self.numbers)
        _tweaks.validate_indexed_tweaks(self.tweaks)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if not self.numbers:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        pheads = _select.pheads(argument)
        total = len(pheads)
        for i, phead in enumerate(pheads):
            number = self.numbers[i]
            if number != 0:
                fingering = abjad.ColorFingering(number)
                fingering = _tweaks.bundle_tweaks(
                    fingering, self.tweaks, i=i, total=total
                )
                abjad.attach(fingering, phead, direction=self.direction)


@dataclasses.dataclass(slots=True)
class DiatonicClusterCommand(_command.Command):
    r"""
    Diatonic cluster command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> command = baca.diatonic_clusters([4, 6])
        >>> command(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' d' e' f'>4
                <d' e' f' g' a' b'>4
                <e' f' g' a'>4
                <f' g' a' b' c'' d''>4
            }

    """

    widths: typing.Any = None
    selector: typing.Callable = lambda _: _select.plts(_)

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert abjad.math.all_are_nonnegative_integers(self.widths)
        self.widths = abjad.CyclicTuple(self.widths)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if not self.widths:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        for i, plt in enumerate(_select.plts(argument)):
            width = self.widths[i]
            start = self._get_lowest_diatonic_pitch_number(plt)
            numbers = range(start, start + width)
            change = abjad.pitch._diatonic_pc_number_to_pitch_class_number
            numbers_ = [(12 * (_ // 7)) + change[_ % 7] for _ in numbers]
            pitches = [abjad.NamedPitch(_) for _ in numbers_]
            for pleaf in plt:
                chord = abjad.Chord(pleaf)
                chord.note_heads[:] = pitches
                abjad.mutate.replace(pleaf, chord)

    def _get_lowest_diatonic_pitch_number(self, plt):
        if isinstance(plt.head, abjad.Note):
            pitch = plt.head.written_pitch
        elif isinstance(plt.head, abjad.Chord):
            pitch = plt.head.written_pitches[0]
        else:
            raise TypeError(plt)
        return pitch._get_diatonic_pitch_number()

    def _mutates_score(self):
        return True


# TODO: frozen=True
@dataclasses.dataclass(slots=True)
class Loop(abjad.CyclicTuple):
    """
    Loop.

    ..  container:: example

        >>> loop = baca.Loop([0, 2, 4], intervals=[1])
        >>> loop
        Loop(items=CyclicTuple(items=(NamedPitch("c'"), NamedPitch("d'"), NamedPitch("e'"))), intervals=CyclicTuple(items=(1,)))

        >>> for i in range(12):
        ...     loop[i]
        NamedPitch("c'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("cs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("fs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("g'")

        >>> isinstance(loop, abjad.CyclicTuple)
        True

    """

    intervals: typing.Any = None

    def __post_init__(self):
        if self.items is not None:
            assert isinstance(self.items, collections.abc.Iterable), repr(self.items)
            self.items = [abjad.NamedPitch(_) for _ in self.items]
            self.items = abjad.CyclicTuple(self.items)
        if self.intervals is not None:
            assert isinstance(self.items, collections.abc.Iterable), repr(self.items)
            self.intervals = abjad.CyclicTuple(self.intervals)

    def __getitem__(self, i) -> abjad.Pitch:
        """
        Gets pitch ``i`` cyclically with intervals.
        """
        if isinstance(i, slice):
            raise NotImplementedError
        iteration = i // len(self)
        if self.intervals is None:
            transposition = 0
        else:
            transposition = sum(self.intervals[:iteration])
        pitch_ = abjad.CyclicTuple(list(self))[i]
        pitch = type(pitch_)(pitch_.number + transposition)
        return pitch


@dataclasses.dataclass(slots=True)
class MicrotoneDeviationCommand(_command.Command):
    r"""
    Microtone deviation command.

    ..  container:: example

        With alternating up- and down-quatertones:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4"),
        ...     baca.deviation([0, 0.5, 0, -0.5]),
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
                        eqs'8
                        e'8
                        eqf'8
                        ]
                        e'8
                        [
                        eqs'8
                        e'8
                        ]
                        eqf'8
                        [
                        e'8
                        eqs'8
                        e'8
                        ]
                        eqf'8
                        [
                        e'8
                        eqs'8
                        ]
                    }
                >>
            }

    """

    deviations: typing.Any = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        if self.deviations is not None:
            assert isinstance(self.deviations, collections.abc.Iterable)
            assert all(isinstance(_, numbers.Number) for _ in self.deviations)
        self.deviations = abjad.CyclicTuple(self.deviations)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if not self.deviations:
            return
        if self.selector:
            argument = self.selector(argument)
        for i, plt in enumerate(_select.plts(argument)):
            deviation = self.deviations[i]
            self._adjust_pitch(plt, deviation)

    def _adjust_pitch(self, plt, deviation):
        assert deviation in (0.5, 0, -0.5)
        if deviation == 0:
            return
        for pleaf in plt:
            pitch = pleaf.written_pitch
            accidental = pitch.accidental.semitones + deviation
            pitch = abjad.NamedPitch(pitch, accidental=accidental)
            pleaf.written_pitch = pitch
            annotation = {"color microtone": True}
            abjad.attach(annotation, pleaf)


@dataclasses.dataclass(slots=True)
class OctaveDisplacementCommand(_command.Command):
    r"""
    Octave displacement command.

    ..  container:: example

        Displaces octaves:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.suite(
        ...         baca.pitch("G4"),
        ...         baca.displacement([0, 0, 1, 1, 0, 0, -1, -1, 2, 2]),
        ...     ),
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
                        g'8
                        [
                        g'8
                        g''8
                        g''8
                        ]
                        g'8
                        [
                        g'8
                        g8
                        ]
                        g8
                        [
                        g'''8
                        g'''8
                        g'8
                        ]
                        g'8
                        [
                        g''8
                        g''8
                        ]
                    }
                >>
            }

    """

    displacements: typing.Any = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        if self.displacements is not None:
            self.displacements = tuple(self.displacements)
            assert self._is_octave_displacement_vector(self.displacements)
            self.displacements = abjad.CyclicTuple(self.displacements)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.displacements is None:
            return
        if self.selector:
            argument = self.selector(argument)
        for i, plt in enumerate(_select.plts(argument)):
            displacement = self.displacements[i]
            interval = abjad.NumberedInterval(12 * displacement)
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    pitch = pleaf.written_pitch
                    assert isinstance(pitch, abjad.NamedPitch)
                    pitch += interval
                    pleaf.written_pitch = pitch
                elif isinstance(pleaf, abjad.Chord):
                    pitches = [_ + interval for _ in pleaf.written_pitches]
                    pleaf.written_pitches = tuple(pitches)
                else:
                    raise TypeError(pleaf)

    def _is_octave_displacement_vector(self, argument):
        if isinstance(argument, tuple | list):
            if all(isinstance(_, int) for _ in argument):
                return True
        return False


def _parse_string(string):
    items, current_chord = [], []
    for part in string.split():
        if "<" in part:
            assert not current_chord
            current_chord.append(part)
        elif ">" in part:
            assert current_chord
            current_chord.append(part)
            item = " ".join(current_chord)
            items.append(item)
            current_chord = []
        elif current_chord:
            current_chord.append(part)
        else:
            items.append(part)
    assert not current_chord, repr(current_chord)
    return items


def _coerce_pitches(pitches):
    if isinstance(pitches, str):
        pitches = _parse_string(pitches)
    items = []
    for item in pitches:
        if isinstance(item, str) and "<" in item and ">" in item:
            item = item.strip("<")
            item = item.strip(">")
            item = set(abjad.NamedPitch(_) for _ in item.split())
        elif isinstance(item, str):
            item = abjad.NamedPitch(item)
        elif isinstance(item, collections.abc.Iterable):
            item = set(abjad.NamedPitch(_) for _ in item)
        else:
            item = abjad.NamedPitch(item)
        items.append(item)
    if isinstance(pitches, Loop):
        pitches = type(pitches)(items=items, intervals=pitches.intervals)
    else:
        pitches = abjad.CyclicTuple(items)
    return pitches


def _set_lt_pitch(
    lt,
    pitch,
    *,
    allow_repitch=False,
    mock=False,
    set_chord_pitches_equal=False,
):
    new_lt = None
    already_pitched = _enums.ALREADY_PITCHED
    for leaf in lt:
        abjad.detach(_enums.NOT_YET_PITCHED, leaf)
        if mock is True:
            abjad.attach(_enums.MOCK, leaf)
        if allow_repitch:
            continue
        if abjad.get.has_indicator(leaf, already_pitched):
            voice = abjad.get.parentage(leaf).get(abjad.Voice)
            if voice is None:
                name = "no voice"
            else:
                name = voice.name
            raise Exception(f"already pitched {repr(leaf)} in {name}.")
        abjad.attach(already_pitched, leaf)
    if pitch is None:
        if not lt.is_pitched:
            pass
        else:
            for leaf in lt:
                rest = abjad.Rest(leaf.written_duration, multiplier=leaf.multiplier)
                abjad.mutate.replace(leaf, rest, wrappers=True)
            new_lt = abjad.get.logical_tie(rest)
    elif isinstance(pitch, collections.abc.Iterable):
        if isinstance(lt.head, abjad.Chord):
            for chord in lt:
                chord.written_pitches = pitch
        else:
            assert isinstance(lt.head, abjad.Note | abjad.Rest)
            for leaf in lt:
                chord = abjad.Chord(
                    pitch,
                    leaf.written_duration,
                    multiplier=leaf.multiplier,
                )
                abjad.mutate.replace(leaf, chord, wrappers=True)
            new_lt = abjad.get.logical_tie(chord)
    else:
        if isinstance(lt.head, abjad.Note):
            for note in lt:
                note.written_pitch = pitch
        elif set_chord_pitches_equal is True and isinstance(lt.head, abjad.Chord):
            for chord in lt:
                for note_head in chord.note_heads:
                    note_head.written_pitch = pitch
        else:
            assert isinstance(lt.head, abjad.Chord | abjad.Rest)
            for leaf in lt:
                note = abjad.Note(
                    pitch,
                    leaf.written_duration,
                    multiplier=leaf.multiplier,
                )
                abjad.mutate.replace(leaf, note, wrappers=True)
            new_lt = abjad.get.logical_tie(note)
    return new_lt


@dataclasses.dataclass(slots=True)
class PitchCommand(_command.Command):
    r"""
    Pitch command.

    ..  container:: example

        With pitch numbers:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches([19, 13, 15, 16, 17, 23]),
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
                        g''8
                        [
                        cs''8
                        ef''8
                        e''8
                        ]
                        f''8
                        [
                        b''8
                        g''8
                        ]
                        cs''8
                        [
                        ef''8
                        e''8
                        f''8
                        ]
                        b''8
                        [
                        g''8
                        cs''8
                        ]
                    }
                >>
            }

    ..  container:: example

        With pitch numbers:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches("C4 F4 F#4 <B4 C#5> D5"),
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
                        c'8
                        [
                        f'8
                        fs'8
                        <b' cs''>8
                        ]
                        d''8
                        [
                        c'8
                        f'8
                        ]
                        fs'8
                        [
                        <b' cs''>8
                        d''8
                        c'8
                        ]
                        f'8
                        [
                        fs'8
                        <b' cs''>8
                        ]
                    }
                >>
            }

    ..  container:: example

        Large chord:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches("<C4 D4 E4 F4 G4 A4 B4 C4>", allow_repeats=True)
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
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                    }
                >>
            }

    ..  container:: example

        Works with Abjad container:

        >>> command = baca.PitchCommand(
        ...     cyclic=True,
        ...     pitches=[19, 13, 15, 16, 17, 23],
        ... )

        >>> staff = abjad.Staff("c'8 c' c' c' c' c' c' c'")
        >>> command(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                g''8
                cs''8
                ef''8
                e''8
                f''8
                b''8
                g''8
                cs''8
            }


    """

    allow_octaves: bool = False
    allow_out_of_range: bool = False
    allow_repeats: bool = False
    allow_repitch: bool = False
    mock: bool = False
    cyclic: bool = False
    do_not_transpose: bool = False
    ignore_incomplete: bool = False
    persist: str | None = None
    pitches: typing.Sequence | Loop = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        self.allow_octaves = bool(self.allow_octaves)
        self.allow_out_of_range = bool(self.allow_out_of_range)
        self.allow_repeats = bool(self.allow_repeats)
        self.allow_repitch = bool(self.allow_repitch)
        self.mock = bool(self.mock)
        self.cyclic = bool(self.cyclic)
        self.do_not_transpose = bool(self.do_not_transpose)
        self.ignore_incomplete = bool(self.ignore_incomplete)
        self._mutated_score = False
        if self.persist is not None:
            assert isinstance(self.persist, str), repr(self.persist)
        self.pitches = _coerce_pitches(self.pitches)
        self._state = {}

    __repr__ = _command.Command.__repr__

    def _call(self, argument=None):
        if argument is None:
            return
        if not self.pitches:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        plts = []
        for pleaf in _select.pleaves(argument):
            plt = abjad.get.logical_tie(pleaf)
            if plt.head is pleaf:
                plts.append(plt)
        self._check_length(plts)
        pitches = self.pitches
        if self.cyclic and not isinstance(pitches, abjad.CyclicTuple):
            pitches = abjad.CyclicTuple(pitches)
        previous_pitches_consumed = self._previous_pitches_consumed()
        if self.cyclic and not isinstance(pitches, abjad.CyclicTuple):
            pitches = abjad.CyclicTuple(pitches)
        pitches_consumed = 0
        for i, plt in enumerate(plts):
            pitch = pitches[i + previous_pitches_consumed]
            new_plt = _set_lt_pitch(
                plt, pitch, allow_repitch=self.allow_repitch, mock=self.mock
            )
            if new_plt is not None:
                self._mutated_score = True
                plt = new_plt
            if self.allow_octaves:
                for pleaf in plt:
                    abjad.attach(_enums.ALLOW_OCTAVE, pleaf)
            if self.allow_out_of_range:
                for pleaf in plt:
                    abjad.attach(_enums.ALLOW_OUT_OF_RANGE, pleaf)
            if self.allow_repeats:
                for pleaf in plt:
                    abjad.attach(_enums.ALLOW_REPEAT_PITCH, pleaf)
            if self.do_not_transpose is True:
                for pleaf in plt:
                    abjad.attach(_enums.DO_NOT_TRANSPOSE, pleaf)
            pitches_consumed += 1
        self._state = {}
        pitches_consumed += previous_pitches_consumed
        self.state["pitches_consumed"] = pitches_consumed

    def _check_length(self, plts):
        if self.cyclic:
            return
        if len(self.pitches) < len(plts):
            message = f"only {len(self.pitches)} pitches"
            message += f" for {len(plts)} logical ties:\n\n"
            message += f"{self!r} and {plts!r}."
            raise Exception(message)

    def _mutates_score(self):
        pitches = self.pitches or []
        if any(isinstance(_, collections.abc.Iterable) for _ in pitches):
            return True
        return self._mutated_score

    def _previous_pitches_consumed(self):
        dictionary = self.runtime.get("previous_segment_voice_metadata", None)
        if not dictionary:
            return 0
        dictionary = dictionary.get(_enums.PITCH.name, None)
        if not dictionary:
            return 0
        if dictionary.get("name") != self.persist:
            return 0
        pitches_consumed = dictionary.get("pitches_consumed", None)
        if not pitches_consumed:
            return 0
        assert 1 <= pitches_consumed
        if self.ignore_incomplete:
            return pitches_consumed
        dictionary = self.runtime["previous_segment_voice_metadata"]
        dictionary = dictionary.get(_enums.RHYTHM.name, None)
        if dictionary:
            if dictionary.get("incomplete_final_note", False):
                pitches_consumed -= 1
        return pitches_consumed

    @property
    def parameter(self) -> str:
        """
        Gets persistence parameter.

        ..  container:: example

            >>> baca.PitchCommand().parameter
            'PITCH'

        """
        return _enums.PITCH.name

    @property
    def state(self):
        """
        Gets state dictionary.
        """
        return self._state


@dataclasses.dataclass(slots=True)
class RegisterCommand(_command.Command):
    r"""
    Register command.

    ..  container:: example

        With music-commands:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [("[A0, C8]", 15)],
        ...         ),
        ...     ),
        ... )
        >>> selection = stack([[10, 12, 14], [10, 12, 14], [10, 12, 14]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 9/16
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        With segment-commands:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches("G4 G+4 G#4 G#+4 A~4 Ab4 Ab~4"),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration([("[A0, C8]", 15)]),
        ...     ),
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

        ..  docs::

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
                        g''8
                        [
                        gqs''8
                        gs''8
                        gtqs''8
                        ]
                        aqf''8
                        [
                        af''8
                        atqf''8
                        ]
                        g''8
                        [
                        gqs''8
                        gs''8
                        gtqs''8
                        ]
                        aqf''8
                        [
                        af''8
                        atqf''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Works with chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration([("[A0, C8]", -6)]),
        ...     ),
        ... )
        >>> selection = stack([{10, 12, 14}])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <bf c' d'>16
                    }
                }
            >>

    """

    registration: typing.Any = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        if self.registration is not None:
            prototype = _pcollections.Registration
            assert isinstance(self.registration, prototype), repr(self.registration)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.registration is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = _select.plts(argument)
        assert isinstance(plts, list)
        for plt in plts:
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    pitch = pleaf.written_pitch
                    pitches = self.registration([pitch])
                    pleaf.written_pitch = pitches[0]
                elif isinstance(pleaf, abjad.Chord):
                    pitches = pleaf.written_pitches
                    pitches = self.registration(pitches)
                    pleaf.written_pitches = pitches
                else:
                    raise TypeError(pleaf)
                abjad.detach(_enums.NOT_YET_REGISTERED, pleaf)


@dataclasses.dataclass(slots=True)
class RegisterInterpolationCommand(_command.Command):
    r"""
    Register interpolation command.

    ..  container:: example

        With music-commands:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.register(0, 24),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c''16
                        b'16
                        af'16
                        g''16
                        cs''16
                        d''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs''16
                        [
                        e''16
                        ef''16
                        f''16
                        a''16
                        bf''16
                        c'''16
                        b''16
                        af''16
                        g'''16
                        cs'''16
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        With chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.register(0, 24),
        ... )

        >>> collections = [
        ...     [6, 4], [3, 5], [9, 10], [0, 11], [8, 7], [1, 2],
        ... ]
        >>> collections = [set(_) for _ in collections]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/8
                        <e' fs'>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <f' ef''>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <a' bf'>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c'' b''>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g'' af''>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <cs''' d'''>16
                    }
                }
            >>

    ..  container:: example

        Holds register constant:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches(pitches),
        ...     baca.register(12, 12),
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

        ..  docs::

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
                        fs''8
                        [
                        e''8
                        ef''8
                        f''8
                        ]
                        a''8
                        [
                        bf''8
                        c''8
                        ]
                        b''8
                        [
                        af''8
                        g''8
                        cs''8
                        ]
                        d''8
                        [
                        fs''8
                        e''8
                        ]
                        ef''8
                        [
                        f''8
                        a''8
                        bf''8
                        ]
                        c''8
                        [
                        b''8
                        af''8
                        ]
                        g''8
                        [
                        cs''8
                        d''8
                        fs''8
                        ]
                        e''8
                        [
                        ef''8
                        f''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to 0:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches(pitches),
        ...     baca.register(12, 0),
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

        ..  docs::

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
                        fs''8
                        [
                        e''8
                        ef''8
                        f''8
                        ]
                        a''8
                        [
                        bf'8
                        c''8
                        ]
                        b'8
                        [
                        af'8
                        g''8
                        cs''8
                        ]
                        d''8
                        [
                        fs'8
                        e''8
                        ]
                        ef''8
                        [
                        f'8
                        a'8
                        bf'8
                        ]
                        c''8
                        [
                        b'8
                        af'8
                        ]
                        g'8
                        [
                        cs''8
                        d'8
                        fs'8
                        ]
                        e'8
                        [
                        ef'8
                        f'8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from 0 up to 12:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches(pitches),
        ...     baca.register(0, 12),
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

        ..  docs::

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
                        fs'8
                        [
                        e'8
                        ef'8
                        f'8
                        ]
                        a'8
                        [
                        bf'8
                        c''8
                        ]
                        b'8
                        [
                        af'8
                        g'8
                        cs''8
                        ]
                        d''8
                        [
                        fs'8
                        e''8
                        ]
                        ef''8
                        [
                        f''8
                        a'8
                        bf'8
                        ]
                        c''8
                        [
                        b'8
                        af'8
                        ]
                        g''8
                        [
                        cs''8
                        d''8
                        fs''8
                        ]
                        e''8
                        [
                        ef''8
                        f''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to -12:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches(pitches),
        ...     baca.register(12, -12),
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

        ..  docs::

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
                        fs''8
                        [
                        e''8
                        ef''8
                        f''8
                        ]
                        a'8
                        [
                        bf'8
                        c''8
                        ]
                        b'8
                        [
                        af'8
                        g'8
                        cs''8
                        ]
                        d'8
                        [
                        fs'8
                        e'8
                        ]
                        ef'8
                        [
                        f'8
                        a'8
                        bf8
                        ]
                        c'8
                        [
                        b8
                        af8
                        ]
                        g8
                        [
                        cs'8
                        d'8
                        fs8
                        ]
                        e8
                        [
                        ef8
                        f8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from -12 up to 12:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches(pitches),
        ...     baca.register(-12, 12),
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

        ..  docs::

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
                        fs8
                        [
                        e8
                        ef8
                        f8
                        ]
                        a8
                        [
                        bf8
                        c'8
                        ]
                        b8
                        [
                        af8
                        g'8
                        cs'8
                        ]
                        d'8
                        [
                        fs'8
                        e'8
                        ]
                        ef'8
                        [
                        f'8
                        a'8
                        bf'8
                        ]
                        c''8
                        [
                        b'8
                        af'8
                        ]
                        g'8
                        [
                        cs''8
                        d''8
                        fs''8
                        ]
                        e''8
                        [
                        ef''8
                        f''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Selects tuplet 0:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lambda _: baca.select.tuplet(_, 0),
        ...         lone=True,
        ...     ),
        ...     baca.register(
        ...         0, 24,
        ...         selector=lambda _: baca.select.tuplet(_, 0),
        ...     ),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        \time 3/2
                        fs'16
                        [
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        ef''16
                        \abjad-color-music #'green
                        f''16
                        \abjad-color-music #'green
                        a'16
                        \abjad-color-music #'green
                        bf'16
                        \abjad-color-music #'green
                        c''16
                        \abjad-color-music #'green
                        b''16
                        \abjad-color-music #'green
                        af''16
                        \abjad-color-music #'green
                        g''16
                        \abjad-color-music #'green
                        cs'''16
                        \abjad-color-music #'green
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c'16
                        b'16
                        af'16
                        g'16
                        cs'16
                        d'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Selects tuplet -1:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lambda _: baca.select.tuplet(_, -1),
        ...         lone=True,
        ...     ),
        ...     baca.register(
        ...         0, 24,
        ...         selector=lambda _: baca.select.tuplet(_, -1),
        ...     ),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c'16
                        b'16
                        af'16
                        g'16
                        cs'16
                        d'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        fs'16
                        [
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        ef''16
                        \abjad-color-music #'green
                        f''16
                        \abjad-color-music #'green
                        a'16
                        \abjad-color-music #'green
                        bf'16
                        \abjad-color-music #'green
                        c''16
                        \abjad-color-music #'green
                        b''16
                        \abjad-color-music #'green
                        af''16
                        \abjad-color-music #'green
                        g''16
                        \abjad-color-music #'green
                        cs'''16
                        \abjad-color-music #'green
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        Maps to tuplets:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lambda _: abjad.select.tuplets(_)
        ...     ),
        ...     baca.new(
        ...         baca.register(0, 24),
        ...         map=lambda _: abjad.select.tuplets(_),
        ...     ),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        \time 3/2
                        fs'16
                        [
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        ef''16
                        \abjad-color-music #'red
                        f''16
                        \abjad-color-music #'red
                        a'16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'red
                        c''16
                        \abjad-color-music #'red
                        b''16
                        \abjad-color-music #'red
                        af''16
                        \abjad-color-music #'red
                        g''16
                        \abjad-color-music #'red
                        cs'''16
                        \abjad-color-music #'red
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        fs'16
                        [
                        \abjad-color-music #'blue
                        e'16
                        \abjad-color-music #'blue
                        ef''16
                        \abjad-color-music #'blue
                        f''16
                        \abjad-color-music #'blue
                        a'16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'blue
                        c''16
                        \abjad-color-music #'blue
                        b''16
                        \abjad-color-music #'blue
                        af''16
                        \abjad-color-music #'blue
                        g''16
                        \abjad-color-music #'blue
                        cs'''16
                        \abjad-color-music #'blue
                        d'''16
                        ]
                    }
                }
            >>

    """

    start_pitch: int | float | abjad.NumberedPitch = 0
    stop_pitch: int | float | abjad.NumberedPitch = 0

    def __post_init__(self):
        _command.Command.__post_init__(self)
        self.start_pitch = abjad.NumberedPitch(self.start_pitch)
        self.stop_pitch = abjad.NumberedPitch(self.stop_pitch)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = _select.plts(argument)
        length = len(plts)
        for i, plt in enumerate(plts):
            registration = self._get_registration(i, length)
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    written_pitches = registration([pleaf.written_pitch])
                    pleaf.written_pitch = written_pitches[0]
                elif isinstance(pleaf, abjad.Chord):
                    written_pitches = registration(pleaf.written_pitches)
                    pleaf.written_pitches = written_pitches
                else:
                    raise TypeError(pleaf)
                abjad.detach(_enums.NOT_YET_REGISTERED, pleaf)

    def _get_registration(self, i, length):
        start_pitch = self.start_pitch.number
        stop_pitch = self.stop_pitch.number
        compass = stop_pitch - start_pitch
        fraction = abjad.Fraction(i, length)
        addendum = fraction * compass
        current_pitch = start_pitch + addendum
        current_pitch = int(current_pitch)
        return _pcollections.Registration([("[A0, C8]", current_pitch)])


@dataclasses.dataclass(slots=True)
class RegisterToOctaveCommand(_command.Command):
    r"""
    Register-to-octave command.

    ..  container:: example

        Chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.DOWN,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([{0, 14, 28}])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <c' d'' e'''>16
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.CENTER,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([{0, 14, 28}])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <c d' e''>16
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.UP,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([{0, 14, 28}])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <c, d e'>16
                    }
                }
            >>

    ..  container:: example

        Disjunct notes:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.DOWN,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[0, 14, 28]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        c'16
                        [
                        d''16
                        e'''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.CENTER,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[0, 14, 28]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        c16
                        [
                        d'16
                        e''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.UP,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[0, 14, 28]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        c,16
                        [
                        d16
                        e'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Conjunct notes:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.DOWN,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[10, 12, 14]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        bf'16
                        [
                        c''16
                        d''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.CENTER,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[10, 12, 14]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        bf16
                        [
                        c'16
                        d'16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.UP,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[10, 12, 14]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        bf16
                        [
                        c'16
                        d'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Bass anchored at octave 5:

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(
        ...     anchor=abjad.DOWN,
        ...     octave_number=5,
        ... )
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c'' d''' e''''>1

    ..  container:: example

        Center anchored at octave 5:

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(
        ...     anchor=abjad.CENTER,
        ...     octave_number=5,
        ... )
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c' d'' e'''>1

    ..  container:: example

        Soprano anchored at octave 5:

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(
        ...     anchor=abjad.UP,
        ...     octave_number=5,
        ... )
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c d' e''>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> staff = abjad.Staff([chord])
        >>> abjad.attach(abjad.Clef("bass"), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            \clef "bass"
            <c, d e'>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=1)
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c,, d, e>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=2)
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c, d e'>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=3)
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c d' e''>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=4)
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c' d'' e'''>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=5)
        >>> command(chord)

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c'' d''' e''''>1

    """

    anchor: typing.Any = None
    octave_number: typing.Any = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        if self.anchor is not None:
            prototype = (abjad.CENTER, abjad.DOWN, abjad.UP)
            assert self.anchor in prototype, repr(self.anchor)
        if self.octave_number is not None:
            assert isinstance(self.octave_number, int), repr(self.octave_number)

    __repr__ = _command.Command.__repr__

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.octave_number is None:
            return
        if self.selector:
            argument = self.selector(argument)
        pitches = abjad.iterate.pitches(argument)
        octave_adjustment = _pcollections.pitches_to_octave_adjustment(
            pitches, anchor=self.anchor, octave_number=self.octave_number
        )
        pleaves = _select.pleaves(argument)
        for pleaf in pleaves:
            self._set_pitch(pleaf, lambda _: _.transpose(n=12 * octave_adjustment))

    def _set_pitch(self, leaf, transposition):
        if isinstance(leaf, abjad.Note):
            pitch = transposition(leaf.written_pitch)
            leaf.written_pitch = pitch
        elif isinstance(leaf, abjad.Chord):
            pitches = [transposition(_) for _ in leaf.written_pitches]
            leaf.written_pitches = pitches
        abjad.detach(_enums.NOT_YET_REGISTERED, leaf)


@dataclasses.dataclass(slots=True)
class StaffPositionCommand(_command.Command):
    r"""
    Staff position command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef("treble"), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "treble"
                b'4
                d''4
                b'4
                d''4
            }

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef("percussion"), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "percussion"
                c'4
                e'4
                c'4
                e'4
            }

    """

    numbers: typing.Any = ()
    allow_out_of_range: bool = False
    allow_repeats: bool = False
    allow_repitch: bool = False
    exact: bool = False
    mock: bool = False
    selector: typing.Callable = lambda _: _select.plts(_)
    set_chord_pitches_equal: bool = False

    def __post_init__(self):
        _command.Command.__post_init__(self)
        prototype = (int, list, abjad.StaffPosition)
        assert all(isinstance(_, prototype) for _ in self.numbers), repr(self.numbers)
        self.numbers = abjad.CyclicTuple(self.numbers)
        self.allow_out_of_range = bool(self.allow_out_of_range)
        self.allow_repeats = bool(self.allow_repeats)
        self.allow_repitch = bool(self.allow_repitch)
        self.mock = bool(self.mock)
        self.exact = bool(self.exact)
        self._mutated_score = False
        self.set_chord_pitches_equal = bool(self.set_chord_pitches_equal)

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if not self.numbers:
            return
        if self.selector:
            argument = self.selector(argument)
        plt_count = 0
        for i, plt in enumerate(_select.plts(argument)):
            clef = abjad.get.effective(
                plt.head,
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            number = self.numbers[i]
            if isinstance(number, list):
                positions = [abjad.StaffPosition(_) for _ in number]
                pitches = [_.to_pitch(clef) for _ in positions]
                new_lt = _set_lt_pitch(
                    plt,
                    pitches,
                    allow_repitch=self.allow_repitch,
                    mock=self.mock,
                    set_chord_pitches_equal=self.set_chord_pitches_equal,
                )
                if new_lt is not None:
                    self._mutated_score = True
                    plt = new_lt
            else:
                position = abjad.StaffPosition(number)
                pitch = clef.to_pitch(position)
                new_lt = _set_lt_pitch(
                    plt,
                    pitch,
                    allow_repitch=self.allow_repitch,
                    mock=self.mock,
                    set_chord_pitches_equal=self.set_chord_pitches_equal,
                )
                if new_lt is not None:
                    self._mutated_score = True
                    plt = new_lt
            plt_count += 1
            for pleaf in plt:
                abjad.attach(_enums.STAFF_POSITION, pleaf)
                if self.allow_out_of_range:
                    abjad.attach(_enums.ALLOW_OUT_OF_RANGE, pleaf)
                if self.allow_repeats:
                    abjad.attach(_enums.ALLOW_REPEAT_PITCH, pleaf)
                    abjad.attach(_enums.DO_NOT_TRANSPOSE, pleaf)
        if self.exact and plt_count != len(self.numbers):
            message = f"PLT count ({plt_count}) does not match"
            message += f" staff position count ({len(self.numbers)})."
            raise Exception(message)

    def _mutates_score(self):
        numbers = self.numbers or []
        if any(isinstance(_, collections.abc.Iterable) for _ in numbers):
            return True
        return self._mutated_score


@dataclasses.dataclass(slots=True)
class StaffPositionInterpolationCommand(_command.Command):
    """
    Staff position interpolation command.
    """

    start: int | str | abjad.NamedPitch | abjad.StaffPosition | None = None
    stop: int | str | abjad.NamedPitch | abjad.StaffPosition | None = None
    mock: bool = False
    pitches_instead_of_staff_positions: bool = False
    selector: typing.Callable = lambda _: _select.plts(_)

    def __post_init__(self):
        _command.Command.__post_init__(self)
        prototype = (abjad.NamedPitch, abjad.StaffPosition)
        if isinstance(self.start, str):
            self.start = abjad.NamedPitch(self.start)
        elif isinstance(self.start, int):
            self.start = abjad.StaffPosition(self.start)
        assert isinstance(self.start, prototype), repr(self.start)
        if isinstance(self.stop, str):
            self.stop = abjad.NamedPitch(self.stop)
        elif isinstance(self.stop, int):
            self.stop = abjad.StaffPosition(self.stop)
        assert isinstance(self.stop, prototype), repr(self.stop)
        self.mock = bool(self.mock)
        if self.pitches_instead_of_staff_positions is not None:
            self.pitches_instead_of_staff_positions = bool(
                self.pitches_instead_of_staff_positions
            )

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = _select.plts(argument)
        if not plts:
            return
        count = len(plts)
        if isinstance(self.start, abjad.StaffPosition):
            start_staff_position = self.start
        else:
            start_phead = plts[0].head
            clef = abjad.get.effective(start_phead, abjad.Clef)
            start_staff_position = clef.to_staff_position(self.start)
        if isinstance(self.stop, abjad.StaffPosition):
            stop_staff_position = self.stop
        else:
            stop_phead = plts[-1].head
            clef = abjad.get.effective(
                stop_phead,
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            stop_staff_position = clef.to_staff_position(self.stop)
        unit_distance = abjad.Fraction(
            stop_staff_position.number - start_staff_position.number, count - 1
        )
        for i, plt in enumerate(plts):
            staff_position = unit_distance * i + start_staff_position.number
            staff_position = round(staff_position)
            staff_position = abjad.StaffPosition(staff_position)
            clef = abjad.get.effective(
                plt.head,
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            pitch = clef.to_pitch(staff_position)
            new_lt = _set_lt_pitch(plt, pitch, allow_repitch=True, mock=self.mock)
            assert new_lt is None, repr(new_lt)
            for leaf in plt:
                abjad.attach(_enums.ALLOW_REPEAT_PITCH, leaf)
                if not self.pitches_instead_of_staff_positions:
                    abjad.attach(_enums.STAFF_POSITION, leaf)
        if isinstance(self.start, abjad.NamedPitch):
            start_pitch = self.start
        else:
            assert isinstance(self.start, abjad.StaffPosition)
            clef = abjad.get.effective(
                plts[0],
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            start_pitch = clef.to_pitch(self.start)
        new_lt = _set_lt_pitch(plts[0], start_pitch, allow_repitch=True, mock=self.mock)
        assert new_lt is None, repr(new_lt)
        if isinstance(self.stop, abjad.NamedPitch):
            stop_pitch = self.stop
        else:
            assert isinstance(self.stop, abjad.StaffPosition)
            clef = abjad.get.effective(
                plts[0],
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            stop_pitch = clef.to_pitch(self.stop)
        new_lt = _set_lt_pitch(plts[-1], stop_pitch, allow_repitch=True, mock=self.mock)
        assert new_lt is None, repr(new_lt)


def bass_to_octave(
    n: int,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the lowest note in the entire selection appears
        in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.bass_to_octave(3),
        ...     baca.color(
        ...         lambda _: baca.select.plts(_),
        ...         lone=True,
        ...     ),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        \time 5/4
                        <c d bf>8
                        [
                        ~
                        \abjad-color-music #'green
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        f'8
                        [
                        ~
                        \abjad-color-music #'green
                        f'32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <ef' e' fs''>8
                        [
                        ~
                        \abjad-color-music #'green
                        <ef' e' fs''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <g af'>8
                        [
                        ~
                        \abjad-color-music #'green
                        <g af'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        a8
                        [
                        ~
                        \abjad-color-music #'green
                        a32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the lowest pitch in each pitched logical tie
        appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.bass_to_octave(3),
        ...         map=lambda _: baca.select.plts(_),
        ...     ),
        ...     baca.color(lambda _: baca.select.plts(_)),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        \time 5/4
                        <c d bf>8
                        [
                        ~
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        f8
                        [
                        ~
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        <ef e fs'>8
                        [
                        ~
                        \abjad-color-music #'red
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        <g af'>8
                        [
                        ~
                        \abjad-color-music #'blue
                        <g af'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        a8
                        [
                        ~
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.DOWN, octave_number=n, selector=selector
    )


def center_to_octave(
    n: int,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the centroid of all PLTs appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.center_to_octave(3),
        ...     baca.color(
        ...         lambda _: baca.select.plts(_),
        ...         lone=True,
        ...     ),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        \time 5/4
                        <c, d, bf,>8
                        [
                        ~
                        \abjad-color-music #'green
                        <c, d, bf,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        f8
                        [
                        ~
                        \abjad-color-music #'green
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <ef e fs'>8
                        [
                        ~
                        \abjad-color-music #'green
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <g, af>8
                        [
                        ~
                        \abjad-color-music #'green
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        a,8
                        [
                        ~
                        \abjad-color-music #'green
                        a,32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the centroid of each pitched logical tie
        appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.center_to_octave(3),
        ...         map=lambda _: baca.select.plts(_),
        ...     ),
        ...     baca.color(lambda _: baca.select.plts(_)),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        \time 5/4
                        <c d bf>8
                        [
                        ~
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        f8
                        [
                        ~
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        <ef e fs'>8
                        [
                        ~
                        \abjad-color-music #'red
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        <g, af>8
                        [
                        ~
                        \abjad-color-music #'blue
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        a8
                        [
                        ~
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.CENTER, octave_number=n, selector=selector
    )


def color_fingerings(
    numbers: list[int | float],
    *tweaks: _typings.IndexedTweak,
    selector=lambda _: _select.pheads(_, exclude=_enums.HIDDEN),
) -> ColorFingeringCommand:
    """
    Adds color fingerings.
    """
    return ColorFingeringCommand(numbers=numbers, selector=selector, tweaks=tweaks)


def deviation(
    deviations: list[int | float],
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> MicrotoneDeviationCommand:
    """
    Sets microtone ``deviations``.
    """
    return MicrotoneDeviationCommand(deviations=deviations, selector=selector)


def diatonic_clusters(
    widths: list[int],
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> DiatonicClusterCommand:
    """
    Makes diatonic clusters with ``widths``.
    """
    return DiatonicClusterCommand(selector=selector, widths=widths)


def displacement(
    displacements: list[int],
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> OctaveDisplacementCommand:
    r"""
    Octave-displaces ``selector`` output.

    ..  container:: example

        Octave-displaces PLTs:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.displacement([0, 0, -1, -1, 1, 1]),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack(3 * [[0, 2, 3]])

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
                        \time 27/16
                        r8
                        c'16
                        [
                        d'16
                        ]
                        ef4
                        ~
                        ef16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8
                    {
                        c16
                        [
                        d''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 11/12
                    {
                        c'16
                        [
                        d'16
                        ]
                        ef4
                        ~
                        ef16
                        r16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Octave-displaces chords:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [4],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...     ),
        ...     rmakers.beam(),
        ...     baca.displacement([0, 0, -1, -1, 1, 1]),
        ... )
        >>> selection = stack(6 * [{0, 2, 3}])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 15/8
                        r8
                        <c' d' ef'>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c' d' ef'>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c d ef>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c d ef>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c'' d'' ef''>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c'' d'' ef''>4
                        r4
                    }
                }
            >>

    """
    return OctaveDisplacementCommand(displacements=displacements, selector=selector)


def force_accidental(
    selector=lambda _: _select.pleaf(_, 0, exclude=_enums.HIDDEN),
) -> AccidentalAdjustmentCommand:
    r"""
    Forces accidental.

    ..  container:: example

        Inverts edition-specific tags:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches("E4 F4"),
        ...     baca.not_parts(
        ...         baca.force_accidental(
        ...             selector=lambda _: baca.select.pleaves(_)[:2],
        ...         ),
        ...     ),
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
                        e'2
                        %@% e'!2
                        f'4.
                        %@% f'!4.
                        e'2
                        f'4.
                    }
                >>
            }

    """
    return AccidentalAdjustmentCommand(forced=True, selector=selector)


def interpolate_pitches(
    start: int | str | abjad.NamedPitch,
    stop: int | str | abjad.NamedPitch,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    mock: bool = False,
) -> StaffPositionInterpolationCommand:
    r"""
    Interpolates from staff position of ``start`` pitch to staff position of ``stop``
    pitch.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.clef("treble"),
        ...     baca.interpolate_pitches("Eb4", "F#5"),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \clef "treble"
                        \time 3/2
                        ef'16
                        [
                        e'16
                        f'16
                        f'16
                        f'16
                        g'16
                        g'16
                        g'16
                        a'16
                        a'16
                        a'16
                        b'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        b'16
                        [
                        c''16
                        c''16
                        c''16
                        d''16
                        d''16
                        d''16
                        e''16
                        e''16
                        e''16
                        f''16
                        fs''16
                        ]
                    }
                }
            >>

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.clef("treble"),
        ...     baca.interpolate_pitches("Eb4", "F#5"),
        ...     baca.glissando(
        ...         allow_repeats=True,
        ...         hide_middle_note_heads=True,
        ...     ),
        ...     baca.glissando_thickness(3),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \override Glissando.thickness = 3
                        \clef "treble"
                        \time 3/2
                        ef'16
                        [
                        \glissando
                        \hide NoteHead
                        \override Accidental.stencil = ##f
                        \override NoteColumn.glissando-skip = ##t
                        \override NoteHead.no-ledgers = ##t
                        e'16
                        f'16
                        f'16
                        f'16
                        g'16
                        g'16
                        g'16
                        a'16
                        a'16
                        a'16
                        b'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        b'16
                        [
                        c''16
                        c''16
                        c''16
                        d''16
                        d''16
                        d''16
                        e''16
                        e''16
                        e''16
                        f''16
                        \revert Accidental.stencil
                        \revert NoteColumn.glissando-skip
                        \revert NoteHead.no-ledgers
                        \undo \hide NoteHead
                        fs''16
                        ]
                        \revert Glissando.thickness
                    }
                }
            >>

    """
    start_ = abjad.NamedPitch(start)
    stop_ = abjad.NamedPitch(stop)
    return StaffPositionInterpolationCommand(
        start=start_,
        stop=stop_,
        mock=mock,
        pitches_instead_of_staff_positions=True,
        selector=selector,
    )


_interpolate_pitches_function = interpolate_pitches


def interpolate_staff_positions(
    start: int | abjad.StaffPosition,
    stop: int | abjad.StaffPosition,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    mock: bool = False,
) -> StaffPositionInterpolationCommand:
    """
    Interpolates from ``start`` staff position to ``stop`` staff position.
    """
    if isinstance(start, abjad.StaffPosition):
        start_ = start
    else:
        start_ = abjad.StaffPosition(start)
    if isinstance(stop, abjad.StaffPosition):
        stop_ = stop
    else:
        stop_ = abjad.StaffPosition(stop)
    return StaffPositionInterpolationCommand(
        start=start_, stop=stop_, mock=mock, selector=selector
    )


_interpolate_staff_positions_function = interpolate_staff_positions


def levine_multiphonic(n: int) -> abjad.Markup:
    """
    Makes Levine multiphonic markup.
    """
    assert isinstance(n, int), repr(n)
    return abjad.Markup(rf'\baca-boxed-markup "L.{n}"')


def loop(
    items: typing.Sequence,
    intervals: typing.Sequence,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> PitchCommand:
    """
    Loops ``items`` at ``intervals``.
    """
    loop = Loop(items=items, intervals=intervals)
    return pitches(loop, selector=selector)


def natural_clusters(
    widths: typing.Sequence[int],
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    start_pitch: int | str | abjad.NamedPitch | None = None,
) -> ClusterCommand:
    """
    Makes natural clusters with ``widths`` and ``start_pitch``.
    """
    return ClusterCommand(
        hide_flat_markup=True,
        selector=selector,
        start_pitch=start_pitch,
        widths=widths,
    )


def pitch(
    pitch,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_out_of_range: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    do_not_transpose: bool = False,
    persist: str = None,
) -> PitchCommand:
    r"""
    Makes pitch command.

    ..  container:: example

        REGRESSION. Preserves duration multipliers when leaves cast from one type to
        another (note to chord in this example):

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.rhythm(
        ...         rmakers.note(),
        ...         rmakers.written_duration(1),
        ...     ),
        ...     baca.pitch("<C4 D4 E4>"),
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
                        <c' d' e'>1 * 1/2
                        %@% ^ \baca-duration-multiplier-markup #"1" #"2"
                        <c' d' e'>1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        <c' d' e'>1 * 1/2
                        %@% ^ \baca-duration-multiplier-markup #"1" #"2"
                        <c' d' e'>1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

    """
    if isinstance(pitch, list | tuple) and len(pitch) == 1:
        raise Exception(f"one-note chord {pitch!r}?")
    if allow_out_of_range not in (None, True, False):
        raise Exception(
            f"allow_out_of_range must be boolean (not {allow_out_of_range!r})."
        )
    if do_not_transpose not in (None, True, False):
        raise Exception(f"do_not_transpose must be boolean (not {do_not_transpose!r}).")
    if persist is not None and not isinstance(persist, str):
        raise Exception(f"persist name must be string (not {persist!r}).")
    return PitchCommand(
        allow_out_of_range=allow_out_of_range,
        allow_repeats=True,
        allow_repitch=allow_repitch,
        cyclic=True,
        do_not_transpose=do_not_transpose,
        mock=mock,
        persist=persist,
        pitches=[pitch],
        selector=selector,
    )


_pitch_function = pitch


def pitches(
    pitches,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_octaves: bool = False,
    allow_repeats: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    do_not_transpose: bool = False,
    exact: bool = False,
    ignore_incomplete: bool = False,
    persist: str = None,
) -> PitchCommand:
    """
    Makes pitch command.
    """
    if do_not_transpose not in (None, True, False):
        raise Exception(f"do_not_transpose must be boolean (not {do_not_transpose!r}).")
    if bool(exact):
        cyclic = False
    else:
        cyclic = True
    if ignore_incomplete not in (None, True, False):
        raise Exception(
            f"ignore_incomplete must be boolean (not {ignore_incomplete!r})."
        )
    if ignore_incomplete is True and not persist:
        raise Exception("ignore_incomplete is ignored when persist is not set.")
    if persist is not None and not isinstance(persist, str):
        raise Exception(f"persist name must be string (not {persist!r}).")
    return PitchCommand(
        allow_octaves=allow_octaves,
        allow_repeats=allow_repeats,
        allow_repitch=allow_repitch,
        cyclic=cyclic,
        do_not_transpose=do_not_transpose,
        ignore_incomplete=ignore_incomplete,
        mock=mock,
        persist=persist,
        pitches=pitches,
        selector=selector,
    )


def register(
    start: int,
    stop: int = None,
    *,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> RegisterCommand | RegisterInterpolationCommand:
    r"""
    Octave-transposes ``selector`` output.

    ..  container:: example

        Octave-transposes all PLTs to the octave rooted at -6:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.register(-6),
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
                        [
                        d'16
                        ]
                        bf4
                        ~
                        bf16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs16
                        [
                        e'16
                        ]
                        ef'4
                        ~
                        ef'16
                        r16
                        af16
                        [
                        g16
                        ]
                    }
                    \times 4/5
                    {
                        a16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

        Octave-transposes PLTs in tuplet 1 to the octave rooted at -6:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lambda _: baca.select.tuplet(_, 1),
        ...         lone=True,
        ...     ),
        ...     baca.register(
        ...         -6,
        ...         selector=lambda _: baca.select.tuplet(_, 1),
        ...     ),
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
                        \abjad-color-music #'green
                        fs16
                        [
                        \abjad-color-music #'green
                        e'16
                        ]
                        \abjad-color-music #'green
                        ef'4
                        ~
                        \abjad-color-music #'green
                        ef'16
                        \abjad-color-music #'green
                        r16
                        \abjad-color-music #'green
                        af16
                        [
                        \abjad-color-music #'green
                        g16
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

    ..  container:: example

        Octave-transposes all PLTs to an octave interpolated from -6 to 18:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.register(-6, 18),
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
                        fs'16
                        [
                        e'16
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
                        a''16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

        Octave-transposes PLTs in tuplet 1 to an octave interpolated from -6 to 18:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lambda _: baca.select.tuplet(_, 1),
        ...         lone=True,
        ...     ),
        ...     baca.register(
        ...         -6, 18,
        ...         selector=lambda _: baca.select.tuplet(_, 1),
        ...     ),
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
                        \abjad-color-music #'green
                        fs16
                        [
                        \abjad-color-music #'green
                        e'16
                        ]
                        \abjad-color-music #'green
                        ef'4
                        ~
                        \abjad-color-music #'green
                        ef'16
                        \abjad-color-music #'green
                        r16
                        \abjad-color-music #'green
                        af'16
                        [
                        \abjad-color-music #'green
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
    if stop is None:
        return RegisterCommand(
            registration=_pcollections.Registration([("[A0, C8]", start)]),
            selector=selector,
        )
    return RegisterInterpolationCommand(
        selector=selector, start_pitch=start, stop_pitch=stop
    )


def soprano_to_octave(
    n: int,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the highest note in the collection of all PLTs
        appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lambda _: baca.select.plts(_),
        ...         lone=True,
        ...     ),
        ...     baca.soprano_to_octave(3),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        \time 5/4
                        <c,, d,, bf,,>8
                        [
                        ~
                        \abjad-color-music #'green
                        <c,, d,, bf,,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        f,8
                        [
                        ~
                        \abjad-color-music #'green
                        f,32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <ef, e, fs>8
                        [
                        ~
                        \abjad-color-music #'green
                        <ef, e, fs>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <g,, af,>8
                        [
                        ~
                        \abjad-color-music #'green
                        <g,, af,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        a,,8
                        [
                        ~
                        \abjad-color-music #'green
                        a,,32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music that such that the highest note in each pitched logical
        tie appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.soprano_to_octave(3),
        ...         map=lambda _: baca.select.plts(_),
        ...     ),
        ...     baca.color(lambda _: baca.select.plts(_)),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        \time 5/4
                        <c d bf>8
                        [
                        ~
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        f8
                        [
                        ~
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        <ef, e, fs>8
                        [
                        ~
                        \abjad-color-music #'red
                        <ef, e, fs>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        <g, af>8
                        [
                        ~
                        \abjad-color-music #'blue
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        a8
                        [
                        ~
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(anchor=abjad.UP, octave_number=n, selector=selector)


def staff_position(
    argument: int | list | abjad.StaffPosition,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_out_of_range: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    set_chord_pitches_equal: bool = False,
) -> StaffPositionCommand:
    """
    Makes staff position command; allows repeats.
    """
    assert isinstance(argument, int | list | abjad.StaffPosition), repr(argument)
    if isinstance(argument, list):
        assert all(isinstance(_, int | abjad.StaffPosition) for _ in argument)
    return StaffPositionCommand(
        numbers=[argument],
        allow_out_of_range=allow_out_of_range,
        allow_repeats=True,
        allow_repitch=allow_repitch,
        mock=mock,
        selector=selector,
        set_chord_pitches_equal=set_chord_pitches_equal,
    )


_staff_position_function = staff_position


def staff_positions(
    numbers,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_out_of_range: bool = False,
    allow_repeats: bool = False,
    mock: bool = False,
    exact: bool = False,
) -> StaffPositionCommand:
    """
    Makes staff position command; does not allow repeats.
    """
    if allow_repeats is None and len(numbers) == 1:
        allow_repeats = True
    return StaffPositionCommand(
        numbers=numbers,
        allow_out_of_range=allow_out_of_range,
        allow_repeats=allow_repeats,
        exact=exact,
        mock=mock,
        selector=selector,
    )


def accent(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
):
    r"""
    Attaches accent.

    ..  container:: example

        Attaches accent to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.accent(),
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
                        - \accent
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation(">")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def alternate_bow_strokes(
    selector=lambda _: _select.pheads(_, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
    downbow_first: bool = True,
    full: bool = False,
) -> IndicatorCommand:
    r"""
    Attaches alternate bow strokes.

    ..  container:: example

        Attaches alternate bow strokes to pitched heads (down-bow first):

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.alternate_bow_strokes(downbow_first=True),
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
                        - \downbow
                        [
                        d'16
                        - \upbow
                        ]
                        bf'4
                        - \downbow
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \upbow
                        [
                        e''16
                        - \downbow
                        ]
                        ef''4
                        - \upbow
                        ~
                        ef''16
                        r16
                        af''16
                        - \downbow
                        [
                        g''16
                        - \upbow
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \downbow
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Attaches alternate bow strokes to pitched heads (up-bow first):

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.alternate_bow_strokes(downbow_first=False),
        ...     baca.tuplet_bracket_staff_padding(6),
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
                        \override TupletBracket.staff-padding = 6
                        \time 11/8
                        r8
                        c'16
                        - \upbow
                        [
                        d'16
                        - \downbow
                        ]
                        bf'4
                        - \upbow
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \downbow
                        [
                        e''16
                        - \upbow
                        ]
                        ef''4
                        - \downbow
                        ~
                        ef''16
                        r16
                        af''16
                        - \upbow
                        [
                        g''16
                        - \downbow
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \upbow
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Attaches alternate full bow strokes to pitched heads:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.alternate_bow_strokes(full=True),
        ...     baca.tuplet_bracket_staff_padding(6),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
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
                        \override TupletBracket.staff-padding = 6
                        \time 11/8
                        r8
                        c'16
                        - \baca-full-downbow
                        [
                        d'16
                        - \baca-full-upbow
                        ]
                        bf'4
                        - \baca-full-downbow
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \baca-full-upbow
                        [
                        e''16
                        - \baca-full-downbow
                        ]
                        ef''4
                        - \baca-full-upbow
                        ~
                        ef''16
                        r16
                        af''16
                        - \baca-full-downbow
                        [
                        g''16
                        - \baca-full-upbow
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \baca-full-downbow
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicators: list[abjad.Articulation | abjad.Bundle]
    if downbow_first:
        if full:
            strings = ["baca-full-downbow", "baca-full-upbow"]
        else:
            strings = ["downbow", "upbow"]
    else:
        if full:
            strings = ["baca-full-upbow", "baca-full-downbow"]
        else:
            strings = ["upbow", "downbow"]
    indicators = [abjad.Articulation(_) for _ in strings]
    indicators = [_tweaks.bundle_tweaks(_, tweaks) for _ in indicators]
    return IndicatorCommand(
        indicators=indicators,
        selector=selector,
        tags=[_tags.function_name(_frame())],
        # tweaks=tweaks,
    )


def arpeggio(
    selector=lambda _: _select.chead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches arpeggio.

    ..  container:: example

        Attaches arpeggio to chord head 0:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.arpeggio(),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 5/4
                        <c' d' bf'>8
                        - \arpeggio
                        [
                        ~
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        f''8
                        [
                        ~
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <ef'' e'' fs'''>8
                        [
                        ~
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g' af''>8
                        [
                        ~
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        [
                        ~
                        a'32
                        ]
                        r16.
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("arpeggio")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def articulation(
    articulation: str,
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    """
    Attaches articulation.
    """
    articulation_ = abjad.Articulation(articulation)
    return IndicatorCommand(
        indicators=[articulation_],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def articulations(
    articulations: list,
    selector=lambda _: _select.pheads(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    """
    Attaches articulations.
    """
    return IndicatorCommand(
        indicators=articulations,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def bar_line(
    abbreviation: str = "|",
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    site: str = "after",
) -> IndicatorCommand:
    """
    Attaches bar line.
    """
    indicator = abjad.BarLine(abbreviation, site=site)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


_bar_line_function = bar_line


def breathe(
    selector=lambda _: _select.pleaf(_, -1, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
) -> IndicatorCommand:
    """
    Attaches breathe command.
    """
    indicator: abjad.LilyPondLiteral | abjad.Bundle
    # TODO: change to abjad.Articulation("breathe", site="after")?
    indicator = abjad.LilyPondLiteral(r"\breathe", site="after")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
        # tweaks=tweaks,
    )


def clef(
    clef: str = "treble",
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    redundant: bool = False,
) -> IndicatorCommand:
    r"""
    Attaches clef.

    ..  container:: example

        Attaches clef to leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.clef("alto"),
        ...     baca.tuplet_bracket_staff_padding(7),
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
                        \override TupletBracket.staff-padding = 7
                        \clef "alto"
                        \time 11/8
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicator = abjad.Clef(clef)
    return IndicatorCommand(
        indicators=[indicator],
        redundant=redundant,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def damp(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
) -> IndicatorCommand:
    """
    Attaches damp.
    """
    indicator: abjad.Articulation | abjad.Bundle
    indicator = abjad.Articulation("baca-damp")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
        # tweaks=tweaks,
    )


def double_flageolet(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    """
    Attaches double flageolet.
    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("baca-double-flageolet")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_staccato(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches double-staccato.

    ..  container:: example

        Attaches double-staccato to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.double_staccato(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
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
                        - \baca-staccati #2
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #2")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def down_arpeggio(
    selector=lambda _: _select.chead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches down-arpeggio.

    ..  container:: example

        Attaches down-arpeggio to chord head 0:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.down_arpeggio(),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \arpeggioArrowDown
                        \time 5/4
                        <c' d' bf'>8
                        \arpeggio
                        [
                        ~
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        f''8
                        [
                        ~
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <ef'' e'' fs'''>8
                        [
                        ~
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g' af''>8
                        [
                        ~
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        [
                        ~
                        a'32
                        ]
                        r16.
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.DOWN)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def down_bow(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> IndicatorCommand:
    r"""
    Attaches down-bow.

    ..  container:: example

        Attaches down-bow to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.down_bow(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
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
                        - \downbow
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Attaches full down-bow to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.down_bow(full=True),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
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
                        - \baca-full-downbow
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicator: abjad.Articulation | abjad.Bundle
    if full:
        indicator = abjad.Articulation("baca-full-downbow")
    else:
        indicator = abjad.Articulation("downbow")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
        # tweaks=tweaks,
    )


def espressivo(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
) -> IndicatorCommand:
    r"""
    Attaches espressivo.

    ..  container:: example

        Attaches espressivo to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.espressivo(),
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
                        - \espressivo
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicator: abjad.Articulation | abjad.Bundle
    indicator = abjad.Articulation("espressivo")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
        # tweaks=tweaks,
    )


def fermata(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Attaches fermata.

    ..  container:: example

        Attaches fermata to first leaf:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.fermata(),
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
                        - \fermata
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("fermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def flageolet(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches flageolet.

    ..  container:: example

        Attaches flageolet to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.flageolet(),
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
                        - \flageolet
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("flageolet")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def hide_black_note_heads(
    selector=lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches note-head stencil false to black note-heads.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.hide_black_note_heads(),
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
                        b'2
                        \once \override NoteHead.transparent = ##t
                        b'4.
                        b'2
                        \once \override NoteHead.transparent = ##t
                        b'4.
                    }
                >>
            }

    """
    string = r"\once \override NoteHead.transparent = ##t"
    literal = abjad.LilyPondLiteral(string)
    return IndicatorCommand(
        indicators=[literal],
        predicate=lambda _: _.written_duration < abjad.Duration(1, 2),
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def laissez_vibrer(
    selector=lambda _: _select.ptail(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches laissez vibrer.

    ..  container:: example

        Attaches laissez vibrer to PLT tail 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.laissez_vibrer(),
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
                        \laissezVibrer
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.LaissezVibrer()],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def literal(
    string: str | list[str],
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    site: str = "before",
) -> IndicatorCommand:
    """
    Attaches LilyPond literal.
    """
    literal = abjad.LilyPondLiteral(string, site=site)
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def long_fermata(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Attaches long fermata.

    ..  container:: example

        Attaches long fermata to first leaf:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.long_fermata(),
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
                        - \longfermata
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("longfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def marcato(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches marcato.

    ..  container:: example

        Attaches marcato to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.marcato(),
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
                        - \marcato
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("marcato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def margin_markup(
    argument: str,
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    alert: IndicatorCommand = None,
    context: str = "Staff",
) -> IndicatorCommand | _command.Suite:
    r"""
    Attaches margin markup.

    ..  container:: example

        >>> margin_markups = {}
        >>> markup = abjad.Markup(r"\markup Fl.")
        >>> margin_markups["Fl."] = abjad.MarginMarkup(markup=markup)
        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     margin_markups=margin_markups,
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.margin_markup(r"\markup Fl."),
        ...     baca.pitches("E4 F4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     first_segment=True,
        ...     margin_markups=commands.margin_markups,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
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
                        \set Staff.shortInstrumentName =
                        \markup Fl.
                        e'2
                        f'4.
                        e'2
                        f'4.
                    }
                >>
            }

    """
    if isinstance(argument, str):
        markup = abjad.Markup(argument)
        margin_markup = abjad.MarginMarkup(context=context, markup=markup)
    elif isinstance(argument, abjad.Markup):
        markup = abjad.Markup(argument)
        margin_markup = abjad.MarginMarkup(context=context, markup=markup)
    elif isinstance(argument, abjad.MarginMarkup):
        margin_markup = dataclasses.replace(argument, context=context)
    else:
        raise TypeError(argument)
    assert isinstance(margin_markup, abjad.MarginMarkup)
    command = IndicatorCommand(
        indicators=[margin_markup],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )
    if bool(alert):
        assert isinstance(alert, IndicatorCommand), repr(alert)
        return _command.suite(command, alert)
    else:
        return command


def mark(
    argument: str,
    selector=lambda _: abjad.select.leaf(_, 0),
    *tweaks: abjad.Tweak,
) -> IndicatorCommand:
    """
    Attaches mark.
    """
    assert isinstance(argument, abjad.Markup | str), repr(argument)
    rehearsal_mark = abjad.RehearsalMark(markup=argument)
    return IndicatorCommand(
        indicators=[rehearsal_mark],
        selector=selector,
        tags=[_tags.function_name(_frame())],
        tweaks=tweaks,
    )


def parenthesize(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches LilyPond ``\parenthesize`` command.

    ..  container:: example

        Attaches parenthesize command to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.parenthesize(),
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
                        \parenthesize
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\parenthesize")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def quadruple_staccato(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    """
    Attaches quadruple-staccato.
    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #4")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rehearsal_mark(
    argument: int | str,
    selector=lambda _: abjad.select.leaf(_, 0),
    *tweaks: abjad.Tweak,
    font_size: int = 10,
) -> IndicatorCommand:
    """
    Attaches rehearsal mark.
    """
    assert isinstance(argument, str), repr(argument)
    assert isinstance(font_size, int | float), repr(font_size)
    string = rf'\baca-rehearsal-mark-markup "{argument}" #{font_size}'
    indicator: abjad.Markup | abjad.Bundle
    indicator = abjad.Markup(string)
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        direction=abjad.CENTER,
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
        # tweaks=tweaks,
    )


def repeat_tie(selector, *, allow_rest: bool = False) -> IndicatorCommand:
    r"""
    Attaches repeat-tie.

    ..  container:: example

        Attaches repeat-tie to pitched head 1:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.chunk(
        ...         baca.pitch(
        ...             0,
        ...             selector=lambda _: baca.select.plt(_, 1),
        ...         ),
        ...         baca.repeat_tie(
        ...             lambda _: baca.select.phead(_, 1),
        ...         ),
        ...     ),
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
                        [
                        c'16
                        ]
                        \repeatTie
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    if allow_rest is not None:
        allow_rest = bool(allow_rest)
    return IndicatorCommand(
        do_not_test=allow_rest,
        indicators=[abjad.RepeatTie()],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def short_fermata(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Attaches short fermata.

    ..  container:: example

        Attaches short fermata to first leaf:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.short_fermata(),
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
                        - \shortfermata
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("shortfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def snap_pizzicato(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    """
    Attaches snap pizzicato.
    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("snappizzicato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccatissimo(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches staccatissimo.

    ..  container:: example

        Attaches staccatissimo to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.staccatissimo(),
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
                        - \staccatissimo
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("staccatissimo")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccato(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches staccato.

    ..  container:: example

        Attaches staccato to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.staccato(),
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
                        - \staccato
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("staccato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staff_lines(n: int, selector=lambda _: abjad.select.leaf(_, 0)) -> _command.Suite:
    r"""
    Makes staff line command.

    ..  container:: example

        Single-line staff with percussion clef:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.clef("percussion"),
        ...     baca.staff_lines(1),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
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
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 1
                        \startStaff
                        \clef "percussion"
                        a4.
                        b4.
                        c'4.
                        d'4.
                        e'4.
                    }
                >>
            }


        Single-line staff with bass clef:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.clef("bass"),
        ...     baca.staff_lines(1),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
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
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 1
                        \startStaff
                        \clef "bass"
                        b,4.
                        c4.
                        d4.
                        e4.
                        f4.
                    }
                >>
            }

    ..  container:: example

        Two-line staff with percussion clef:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.clef("percussion"),
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
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
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 2
                        \startStaff
                        \clef "percussion"
                        a4.
                        b4.
                        c'4.
                        d'4.
                        e'4.
                    }
                >>
            }

        Two-line staff with bass clef; clef set before staff positions:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.clef("bass"),
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
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
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 2
                        \startStaff
                        \clef "bass"
                        b,4.
                        c4.
                        d4.
                        e4.
                        f4.
                    }
                >>
            }

        Two-line staff with bass clef; staff positions set before clef:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     baca.clef("bass"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
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
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 2
                        \startStaff
                        \clef "bass"
                        g'4.
                        a'4.
                        b'4.
                        c''4.
                        d''4.
                    }
                >>
            }

    """
    command_1 = IndicatorCommand(
        indicators=[_indicators.BarExtent(n)],
        selector=selector,
        tags=[_tags.NOT_PARTS],
    )
    command_2 = IndicatorCommand(
        indicators=[_indicators.StaffLines(n)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )
    return _command.suite(command_1, command_2)


def start_markup(
    argument: str | list[str],
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    context: str = "Staff",
    hcenter_in: int | float | None = None,
    literal: bool = False,
) -> IndicatorCommand:
    """
    Attaches start markup.
    """
    if literal is True or (isinstance(argument, str) and argument.startswith("\\")):
        assert isinstance(argument, str), repr(argument)
        assert argument.startswith("\\"), repr(argument)
        start_markup = abjad.StartMarkup(markup=argument)
    elif isinstance(argument, str):
        width = hcenter_in or 16
        string = rf'\markup \hcenter-in #{width} "{argument}"'
        start_markup = abjad.StartMarkup(markup=string)
    elif isinstance(argument, list) and len(argument) == 2:
        width = hcenter_in or 16
        line_1 = rf'\hcenter-in #{width} "{argument[0]}"'
        line_2 = rf'\hcenter-in #{width} "{argument[1]}"'
        string = rf"\markup \column {{ {line_1} {line_2} }}"
        start_markup = abjad.StartMarkup(markup=string)
    elif isinstance(argument, list) and len(argument) == 3:
        width = hcenter_in or 16
        line_1 = rf'\hcenter-in #{width} "{argument[0]}"'
        line_2 = rf'\hcenter-in #{width} "{argument[1]}"'
        line_3 = rf'\hcenter-in #{width} "{argument[2]}"'
        string = rf"\markup \column {{ {line_1} {line_2} {line_3} }}"
        start_markup = abjad.StartMarkup(markup=string)
    elif isinstance(argument, abjad.Markup):
        start_markup = abjad.StartMarkup(markup=argument)
    elif isinstance(argument, abjad.StartMarkup):
        start_markup = argument
    else:
        raise TypeError(argument)
    assert isinstance(start_markup, abjad.StartMarkup)
    start_markup = dataclasses.replace(start_markup, context=context)
    command = IndicatorCommand(
        indicators=[start_markup],
        selector=selector,
        tags=[_tags.function_name(_frame()), _tags.NOT_PARTS],
    )
    return command


def stem_tremolo(
    selector=lambda _: _select.pleaf(_, 0, exclude=_enums.HIDDEN),
    *,
    tremolo_flags: int = 32,
) -> IndicatorCommand:
    r"""
    Attaches stem tremolo.

    ..  container:: example

        Attaches stem tremolo to pitched leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stem_tremolo(),
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
                        :32
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.StemTremolo(tremolo_flags=tremolo_flags)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stop_on_string(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *,
    map=None,
) -> IndicatorCommand:
    r"""
    Attaches stop-on-string.

    ..  container:: example

        Attaches stop-on-string to pitched head -1:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stop_on_string(
        ...         selector=lambda _: baca.select.pleaf(_, -1),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
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
                        - \baca-stop-on-string
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    articulation = abjad.Articulation("baca-stop-on-string")
    return IndicatorCommand(
        indicators=[articulation],
        map=map,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stop_trill(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Attaches stop trill to closing-slot.

    The closing format slot is important because LilyPond fails to compile when
    ``\stopTrillSpan`` appears after ``\set instrumentName`` commands (and probably other
    ``\set`` commands). Setting format slot to closing here positions ``\stopTrillSpan``
    after the leaf in question (which is required) and also draws ``\stopTrillSpan``
    closer to the leaf in question, prior to ``\set instrumetName`` and other commands
    positioned in the after slot.

    Eventually it will probably be necessary to model ``\stopTrillSpan`` with a dedicated
    format slot.
    """
    return literal(r"\stopTrillSpan", site="closing", selector=selector)


def stopped(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches stopped +-sign.

    ..  container:: example

        Attaches stopped +-sign to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stopped(),
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
                        - \stopped
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("stopped")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def tie(selector) -> IndicatorCommand:
    r"""
    Attaches tie.

    ..  container:: example

        Attaches tie to pitched tail 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.chunk(
        ...         baca.pitch(
        ...             2,
        ...             selector=lambda _: baca.select.plt(_, 0),
        ...         ),
        ...         baca.tie(lambda _: baca.select.ptail(_, 0)),
        ...     ),
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
                        d'16
                        [
                        ~
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Tie()],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def tenuto(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches tenuto.

    ..  container:: example

        Attaches tenuto to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tenuto(),
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
                        - \tenuto
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("tenuto")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def triple_staccato(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    """
    Attaches triple-staccato.
    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #3")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def up_arpeggio(
    selector=lambda _: _select.chead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches up-arpeggio.

    ..  container:: example

        Attaches up-arpeggios to chord head 0:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.up_arpeggio(),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \arpeggioArrowUp
                        \time 5/4
                        <c' d' bf'>8
                        \arpeggio
                        [
                        ~
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        f''8
                        [
                        ~
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <ef'' e'' fs'''>8
                        [
                        ~
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g' af''>8
                        [
                        ~
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        [
                        ~
                        a'32
                        ]
                        r16.
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.UP)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def up_bow(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> IndicatorCommand:
    r"""
    Attaches up-bow.

    ..  container:: example

        Attaches up-bow to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ...     baca.up_bow(),
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
                        - \upbow
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicator: abjad.Articulation | abjad.Bundle
    if full:
        indicator = abjad.Articulation("baca-full-upbow")
    else:
        indicator = abjad.Articulation("upbow")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
        # tweaks=tweaks,
    )


def very_long_fermata(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Attaches very long fermata.

    ..  container:: example

        Attaches very long fermata to first leaf:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.very_long_fermata(),
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
                        - \verylongfermata
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("verylongfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def allow_octaves(*, selector=lambda _: _select.leaves(_)) -> IndicatorCommand:
    """
    Attaches ALLOW_OCTAVE constant.
    """
    return IndicatorCommand(indicators=[_enums.ALLOW_OCTAVE], selector=selector)


def assign_parts(
    part_assignment: _parts.PartAssignment,
    *,
    selector=lambda _: _select.leaves(_),
) -> PartAssignmentCommand:
    r"""
    Inserts ``selector`` output in container and sets part assignment.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.assign_parts(baca.parts.PartAssignment("Music_Voice")),
        ...     baca.pitch("E4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(score)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

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

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> part_assignment = baca.parts.PartAssignment("Flute")

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.assign_parts(baca.parts.PartAssignment("Flute_Voice")),
        ...     baca.pitches("E4 F4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: Music_Voice does not allow Flute_Voice part assignment:
          baca.PartAssignment('Flute_Voice')

    """
    if not isinstance(part_assignment, _parts.PartAssignment):
        message = "part_assignment must be part assignment"
        message += f" (not {part_assignment!r})."
        raise Exception(message)
    return PartAssignmentCommand(part_assignment=part_assignment, selector=selector)


def bcps(
    bcps,
    *tweaks: _typings.IndexedTweak,
    bow_change_tweaks: typing.Sequence[_typings.IndexedTweak] = (),
    final_spanner: bool = False,
    helper: typing.Callable = lambda x, y: x,
    selector=lambda _: _select.leaves(_),
) -> BCPCommand:
    r"""
    Makes bow contact point command.

        ..  container:: example

            >>> score = baca.docs.make_empty_score(1)
            >>> commands = baca.CommandAccumulator(
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ... )

            >>> commands(
            ...     "Music_Voice",
            ...     baca.make_even_divisions(),
            ...     baca.bcps(
            ...         [(1, 5), (3, 5), (2, 5), (4, 5), (5, 5)],
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
    return BCPCommand(
        bcps=bcps,
        bow_change_tweaks=tuple(bow_change_tweaks),
        final_spanner=final_spanner,
        helper=helper,
        selector=selector,
        tags=[_tags.function_name(_frame())],
        tweaks=tweaks,
    )


def close_volta(
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    site: str = "before",
) -> _command.Suite:
    """
    Attaches bar line and overrides bar line X-extent.
    """
    assert site in ("after", "before"), repr(site)
    after = site == "after"
    # does not require not_mol() tagging, just only_mol() tagging:
    return _command.suite(
        bar_line(":|.", selector, site=site),
        _command.only_mol(
            _overrides.bar_line_x_extent((0, 1.5), selector, after=after)
        ),
    )


def color(
    selector=lambda _: _select.leaves(_),
    lone=False,
) -> ColorCommand:
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
                        \abjad-color-music #'red
                        \time 11/8
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

        >>> def color_selector(argument):
        ...     result = abjad.select.tuplet(argument, 1)
        ...     result = abjad.select.leaves(result)
        ...     return result
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(color_selector),
        ...     rmakers.unbeam(),
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
    return ColorCommand(selector=selector, lone=lone)


def container(
    identifier: str = None,
    *,
    selector=lambda _: _select.leaves(_),
) -> ContainerCommand:
    r"""
    Makes container with ``identifier`` and extends container with ``selector`` output.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.container(
        ...         "ViolinI",
        ...         selector=lambda _: baca.select.leaves(_)[:2],
        ...     ),
        ...     baca.container(
        ...         "ViolinII",
        ...         selector=lambda _: baca.select.leaves(_)[2:],
        ...     ),
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
    if identifier is not None:
        if not isinstance(identifier, str):
            raise Exception(f"identifier must be string (not {identifier!r}).")
    return ContainerCommand(identifier=identifier, selector=selector)


def cross_staff(*, selector=lambda _: _select.phead(_, 0)) -> IndicatorCommand:
    r"""
    Attaches cross-staff command.

    ..  container:: example

        Attaches cross-staff command to last two pitched leaves:

        >>> score = baca.docs.make_empty_score(1, 1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 4)],
        ... )

        >>> commands(
        ...     ("Music_Voice_1", 1),
        ...     baca.make_music(abjad.Container("e'4 f' g' a'")[:]),
        ... )

        >>> commands(
        ...     ("Music_Voice_2", 1),
        ...     baca.make_music(abjad.Container("c'4 d' e' f'")[:]),
        ...     baca.cross_staff(
        ...         selector=lambda _: baca.select.pleaves(_)[-2:],
        ...     ),
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
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

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
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\crossStaff")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_volta(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> _command.Suite:
    """
    Attaches bar line and overrides bar line X-extent.
    """
    return _command.suite(
        bar_line(":.|.:", selector, site="before"),
        _command.not_mol(_overrides.bar_line_x_extent((0, 3), selector)),
        _command.only_mol(_overrides.bar_line_x_extent((0, 4), selector)),
    )


def dynamic_down(*, selector=lambda _: abjad.select.leaf(_, 0)) -> IndicatorCommand:
    r"""
    Attaches dynamic-down command.

    ..  container:: example

        Attaches dynamic-down command to leaf 0:

        >>> def forte_selector(argument):
        ...     result = abjad.select.tuplet(argument, 1)
        ...     result = baca.select.phead(result, 0)
        ...     return result
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic("p"),
        ...     baca.dynamic("f", selector=forte_selector),
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
                        \dynamicDown
                        \time 11/8
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
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicDown")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_up(*, selector=lambda _: abjad.select.leaf(_, 0)) -> IndicatorCommand:
    r"""
    Attaches dynamic-up command.

    ..  container:: example

        Attaches dynamic-up command to leaf 0:

        >>> def forte_selector(argument):
        ...     result = abjad.select.tuplet(argument, 1)
        ...     result = baca.select.phead(result, 0)
        ...     return result
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic("p"),
        ...     baca.dynamic("f", selector=forte_selector),
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
                        \dynamicUp
                        \time 11/8
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
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicUp")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def edition(
    not_parts: str | abjad.Markup | IndicatorCommand,
    only_parts: str | abjad.Markup | IndicatorCommand,
) -> _command.Suite:
    """
    Makes not-parts / only-parts markup suite.
    """
    if isinstance(not_parts, str):
        not_parts = markup(rf"\markup {{ {not_parts} }}")
    elif isinstance(not_parts, abjad.Markup):
        not_parts = markup(not_parts)
    assert isinstance(not_parts, IndicatorCommand)
    not_parts_ = _command.not_parts(not_parts)
    if isinstance(only_parts, str):
        only_parts = markup(rf"\markup {{ {only_parts} }}")
    elif isinstance(only_parts, abjad.Markup):
        only_parts = markup(only_parts)
    assert isinstance(only_parts, IndicatorCommand)
    only_parts_ = _command.only_parts(only_parts)
    return _command.suite(not_parts_, only_parts_)


def finger_pressure_transition(
    *,
    selector=lambda _: _select.tleaves(_),
    right_broken: bool = False,
) -> GlissandoCommand:
    r"""
    Makes finger pressure transition glissando.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.pitch("C5"),
        ...     baca.note_head_style_harmonic(selector=lambda _: abjad.select.note(_, 0)),
        ...     baca.note_head_style_harmonic(selector=lambda _: abjad.select.note(_, 2)),
        ...     baca.finger_pressure_transition(
        ...         selector=lambda _: abjad.select.notes(_)[:2],
        ...     ),
        ...     baca.finger_pressure_transition(
        ...         selector=lambda _: abjad.select.notes(_)[2:],
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
    return GlissandoCommand(
        allow_repeats=True,
        right_broken=right_broken,
        selector=selector,
        tags=[_tags.function_name(_frame())],
        tweaks=(
            abjad.Tweak(r"- \tweak arrow-length 2"),
            abjad.Tweak(r"- \tweak arrow-width 0.5"),
            abjad.Tweak(r"- \tweak bound-details.right.arrow ##t"),
            abjad.Tweak(r"- \tweak thickness 3"),
        ),
    )


def flat_glissando(
    pitch: str
    | abjad.NamedPitch
    | abjad.StaffPosition
    | list[abjad.StaffPosition]
    | None = None,
    *tweaks,
    allow_repitch: bool = False,
    do_not_hide_middle_note_heads: bool = False,
    mock: bool = False,
    hide_middle_stems: bool = False,
    hide_stem_selector: typing.Callable = None,
    left_broken: bool = False,
    right_broken: bool = False,
    right_broken_show_next: bool = False,
    rleak: bool = False,
    selector=lambda _: _select.pleaves(_),
    stop_pitch: str | abjad.NamedPitch | abjad.StaffPosition | None = None,
) -> _command.Suite:
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
            result = selector(argument)
            result = _select.rleak(result)
            return result

        new_selector = _selector_rleak
    else:
        new_selector = selector
    commands: list[_command.Command] = []
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
        return abjad.select.leaves(new_selector(argument))

    untie_command = untie(_leaves_of_selector)
    commands.append(untie_command)
    if pitch is not None and stop_pitch is None:
        if isinstance(pitch, abjad.StaffPosition) or (
            isinstance(pitch, list) and isinstance(pitch[0], abjad.StaffPosition)
        ):
            staff_position_command = _staff_position_function(
                pitch,
                allow_repitch=allow_repitch,
                mock=mock,
                selector=new_selector,
            )
            commands.append(staff_position_command)
        else:
            pitch_command = _pitch_function(
                pitch,
                allow_repitch=allow_repitch,
                mock=mock,
                selector=new_selector,
            )
            commands.append(pitch_command)
    elif pitch is not None and stop_pitch is not None:
        if isinstance(pitch, abjad.StaffPosition):
            assert isinstance(stop_pitch, abjad.StaffPosition)
            interpolation_command = _interpolate_staff_positions_function(
                pitch, stop_pitch, mock=mock, selector=new_selector
            )
        else:
            assert isinstance(pitch, str | abjad.NamedPitch)
            assert isinstance(stop_pitch, str | abjad.NamedPitch)
            interpolation_command = _interpolate_pitches_function(
                pitch, stop_pitch, mock=mock, selector=new_selector
            )
        commands.append(interpolation_command)
    return _command.suite(*commands)


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
    *tweaks: abjad.Tweak,
    allow_repeats: bool = False,
    allow_ties: bool = False,
    hide_middle_note_heads: bool = False,
    hide_middle_stems: bool = False,
    hide_stem_selector: typing.Callable = None,
    left_broken: bool = False,
    map=None,
    right_broken: bool = False,
    right_broken_show_next: bool = False,
    selector=lambda _: _select.tleaves(_),
    style: str = None,
    zero_padding: bool = False,
) -> GlissandoCommand:
    r"""
    Attaches glissando.

    ..  container:: example

        With segment-commands:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.glissando()
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(score)
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

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.glissando(selector=lambda _: baca.select.plts(_)[:2]),
        ...     baca.glissando(selector=lambda _: baca.select.plts(_)[-2:]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(score)
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

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.glissando(
        ...         abjad.Tweak(r"- \tweak color #red"),
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(score)
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

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.glissando(
        ...         (abjad.Tweak(r"- \tweak color #red"), 0),
        ...         (abjad.Tweak(r"- \tweak color #red"), -1),
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(score)
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
    return GlissandoCommand(
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
        tags=[_tags.function_name(_frame())],
        tweaks=tweaks,
        zero_padding=zero_padding,
    )


def global_fermata(
    description: str = "fermata",
    selector=lambda _: abjad.select.leaf(_, 0),
) -> GlobalFermataCommand:
    """
    Attaches global fermata.
    """
    fermatas = GlobalFermataCommand.description_to_command.keys()
    if description not in fermatas:
        message = f"must be in {repr(', '.join(fermatas))}:\n"
        message += f"   {repr(description)}"
        raise Exception(message)
    return GlobalFermataCommand(
        description=description,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def instrument(
    instrument: abjad.Instrument,
    selector=lambda _: abjad.select.leaf(_, 0),
) -> InstrumentChangeCommand:
    """
    Makes instrument change command.
    """
    if not isinstance(instrument, abjad.Instrument):
        raise Exception(f"instrument must be instrument (not {instrument!r}).")
    return InstrumentChangeCommand(
        indicators=[instrument],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def invisible_music(
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    map=None,
) -> _command.Suite:
    r"""
    Attaches ``\baca-invisible-music`` literal.

    ..  container:: example

        Attaches ``\baca-invisible-music`` literal to middle leaves:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.pitch("C5"),
        ...     baca.invisible_music(
        ...         selector=lambda _: baca.select.leaves(_)[1:-1],
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
    tag = _tags.function_name(_frame(), n=1)
    tag = tag.append(_tags.INVISIBLE_MUSIC_COMMAND)
    command_1 = IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\abjad-invisible-music")],
        deactivate=True,
        map=map,
        selector=selector,
        tags=[tag],
    )
    tag = _tags.function_name(_frame(), n=2)
    tag = tag.append(_tags.INVISIBLE_MUSIC_COLORING)
    command_2 = IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\abjad-invisible-music-coloring")],
        map=map,
        selector=selector,
        tags=[tag],
    )
    return _command.suite(command_1, command_2)


def label(
    callable_,
    selector=lambda _: _select.leaves(_),
) -> LabelCommand:
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
    return LabelCommand(callable_=callable_, selector=selector)


def markup(
    argument: str | abjad.Markup,
    *tweaks: abjad.Tweak,
    direction=abjad.UP,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    selector=lambda _: _select.pleaf(_, 0),
) -> IndicatorCommand:
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
        ...     baca.markup(r'\markup "più mosso"'),
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
                        ^ \markup "più mosso"
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

        Pass predefined markup commands like this:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup(r"\markup { \baca-triple-diamond-markup }"),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
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
    if direction not in (abjad.DOWN, abjad.UP):
        message = f"direction must be up or down (not {direction!r})."
        raise Exception(message)
    indicator: abjad.Markup | abjad.Bundle
    if isinstance(argument, str):
        indicator = abjad.Markup(argument)
    elif isinstance(argument, abjad.Markup):
        indicator = dataclasses.replace(argument)
    else:
        message = "MarkupLibary.__call__():\n"
        message += "  Value of 'argument' must be str or markup.\n"
        message += f"  Not {argument!r}."
        raise Exception(message)
    if tweaks:
        indicator = abjad.bundle(indicator, *tweaks)
    if (
        selector is not None
        and not isinstance(selector, str)
        and not callable(selector)
    ):
        message = "selector must be string or callable"
        message += f" (not {selector!r})."
        raise Exception(message)

    def select_phead_0(argument):
        return _select.phead(argument, 0)

    selector = selector or select_phead_0
    return IndicatorCommand(
        direction=direction,
        indicators=[indicator],
        map=map,
        match=match,
        measures=measures,
        selector=selector,
        tags=[_tags.function_name(_frame())],
        # tweaks=tweaks,
    )


def metronome_mark(
    key: str | _indicators.Accelerando | _indicators.Ritardando,
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    redundant: bool = False,
) -> MetronomeMarkCommand | None:
    """
    Attaches metronome mark matching ``key`` metronome mark manifest.
    """
    if redundant is True:
        return None
    return MetronomeMarkCommand(key=key, redundant=redundant, selector=selector)


def one_voice(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\oneVoice`` command.
    """
    literal = abjad.LilyPondLiteral(r"\oneVoice")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def open_volta(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> _command.Suite:
    """
    Attaches bar line and overrides bar line X-extent.
    """
    return _command.suite(
        _bar_line_function(".|:", selector, site="before"),
        _command.not_mol(_overrides.bar_line_x_extent((0, 2), selector)),
        _command.only_mol(_overrides.bar_line_x_extent((0, 3), selector)),
    )


def previous_metadata(path: str):
    """
    Gets previous segment metadata before ``path``.
    """
    # reproduces baca.path.Path.get_previous_path()
    # because Travis isn't configured for scores-directory calculations
    music_py = pathlib.Path(path)
    segment = pathlib.Path(music_py).parent
    # assert segment.parent.name == "segments", repr(segment)
    assert segment.parent.name == "sections", repr(segment)
    segments = segment.parent
    # assert segments.name == "segments", repr(segments)
    assert segments.name == "sections", repr(segments)
    paths = list(sorted(segments.glob("*")))
    paths = [_ for _ in paths if not _.name.startswith(".")]
    paths = [_ for _ in paths if _.is_dir()]
    index = paths.index(segment)
    if index == 0:
        return {}
    previous_index = index - 1
    previous_segment = paths[previous_index]
    previous_metadata = _path.get_metadata(previous_segment)
    return previous_metadata


def replace_with_clusters(
    widths: list[int],
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    start_pitch: int | str | abjad.NamedPitch | None = None,
) -> ClusterCommand:
    """
    Makes clusters with ``widths`` and ``start_pitch``.
    """
    return ClusterCommand(selector=selector, start_pitch=start_pitch, widths=widths)


def untie(selector) -> DetachCommand:
    """
    Makes (repeat-)tie detach command.
    """
    return DetachCommand(arguments=[abjad.Tie, abjad.RepeatTie], selector=selector)


def voice_four(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceFour`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceFour")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_one(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceOne`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceOne")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_three(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceThree`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceThree")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_two(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceTwo`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceTwo")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )
