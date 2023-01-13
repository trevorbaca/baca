"""
Commands.
"""
import copy
import typing
from inspect import currentframe as _frame

import abjad

from . import pitchcommands as _pitchcommands
from . import select as _select
from . import tags as _tags
from . import tweaks as _tweaks
from . import typings as _typings


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


def bcps(
    argument,
    bcps,
    *tweaks: _typings.IndexedTweak,
    bow_change_tweaks: typing.Sequence[_typings.IndexedTweak] = (),
    final_spanner: bool = False,
    helper: typing.Callable = lambda x, y: x,
) -> list[abjad.Wrapper]:
    wrappers: list[abjad.Wrapper] = []
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    bcps_ = list(bcps)
    bcps_ = helper(bcps_, argument)
    bcps = abjad.CyclicTuple(bcps_)
    lts = _select.lts(argument)
    add_right_text_to_me = None
    if not final_spanner:
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
    if final_spanner and not _is_rest(lts[-1]) and len(lts[-1]) == 1:
        next_leaf_after_argument = abjad.get.leaf(lts[-1][-1], 1)
        if next_leaf_after_argument is None:
            message = "can not attach final spanner: argument includes end of score."
            raise Exception(message)
    previous_bcp = None
    i = 0
    for lt in lts:
        stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanBCP")
        if not final_spanner and lt is lts[-1] and not _is_rest(lt.head):
            wrapper = abjad.attach(
                stop_text_span,
                lt.head,
                tag=_tags.function_name(_frame(), n=1),
                wrapper=True,
            )
            wrappers.append(wrapper)
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
            if final_spanner:
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
            command=r"\bacaStartTextSpanBCP",
            left_text=left_text,
            right_text=right_text,
            style=style,
        )
        if tweaks:
            start_text_span = _tweaks.bundle_tweaks(start_text_span, tweaks)
        if _is_rest(lt.head) and (_is_rest(next_leaf) or next_leaf is None):
            pass
        else:
            wrapper = abjad.attach(
                start_text_span,
                lt.head,
                tag=_tags.function_name(_frame(), n=2),
                wrapper=True,
            )
            wrappers.append(wrapper)
        if 0 < i - 1:
            wrapper = abjad.attach(
                stop_text_span,
                lt.head,
                tag=_tags.function_name(_frame(), n=3),
                wrapper=True,
            )
            wrappers.append(wrapper)
        if lt is lts[-1] and final_spanner:
            wrapper = abjad.attach(
                stop_text_span,
                next_leaf_after_argument,
                tag=_tags.function_name(_frame(), n=4),
                wrapper=True,
            )
            wrappers.append(wrapper)
        bcp_fraction = abjad.Fraction(*bcp)
        next_bcp_fraction = abjad.Fraction(*bcps[i])
        if _is_rest(lt.head):
            pass
        elif _is_rest(previous_leaf) or previous_bcp is None:
            if bcp_fraction > next_bcp_fraction:
                articulation = abjad.Articulation("upbow")
                if bow_change_tweaks:
                    articulation = _tweaks.bundle_tweaks(
                        articulation,
                        bow_change_tweaks,
                    )
                wrapper = abjad.attach(
                    articulation,
                    lt.head,
                    tag=_tags.function_name(_frame(), n=5),
                    wrapper=True,
                )
                wrappers.append(wrapper)
            elif bcp_fraction < next_bcp_fraction:
                articulation = abjad.Articulation("downbow")
                if bow_change_tweaks:
                    articulation = _tweaks.bundle_tweaks(
                        articulation,
                        bow_change_tweaks,
                    )
                wrapper = abjad.attach(
                    articulation,
                    lt.head,
                    tag=_tags.function_name(_frame(), n=6),
                    wrapper=True,
                )
                wrappers.append(wrapper)
        else:
            previous_bcp_fraction = abjad.Fraction(*previous_bcp)
            if previous_bcp_fraction < bcp_fraction > next_bcp_fraction:
                articulation = abjad.Articulation("upbow")
                if bow_change_tweaks:
                    articulation = _tweaks.bundle_tweaks(
                        articulation,
                        bow_change_tweaks,
                    )
                wrapper = abjad.attach(
                    articulation,
                    lt.head,
                    tag=_tags.function_name(_frame(), n=7),
                    wrapper=True,
                )
                wrappers.append(wrapper)
            elif previous_bcp_fraction > bcp_fraction < next_bcp_fraction:
                articulation = abjad.Articulation("downbow")
                if bow_change_tweaks:
                    articulation = _tweaks.bundle_tweaks(
                        articulation,
                        bow_change_tweaks,
                    )
                wrapper = abjad.attach(
                    articulation,
                    lt.head,
                    tag=_tags.function_name(_frame(), n=8),
                    wrapper=True,
                )
                wrappers.append(wrapper)
        previous_bcp = bcp
    return wrappers


def color(argument, *, lone: bool = False) -> None:
    return abjad.label.by_selector(argument, lone=lone)


def finger_pressure_transition(argument) -> None:
    tag = _tags.function_name(_frame())
    tweaks = (
        abjad.Tweak(r"- \tweak arrow-length 2"),
        abjad.Tweak(r"- \tweak arrow-width 0.5"),
        abjad.Tweak(r"- \tweak bound-details.right.arrow ##t"),
        abjad.Tweak(r"- \tweak thickness 3"),
    )
    abjad.glissando(
        argument,
        *tweaks,
        allow_repeats=True,
        tag=tag,
    )


def flat_glissando(
    argument,
    pitch: str
    | abjad.NamedPitch
    | abjad.StaffPosition
    | list[abjad.StaffPosition]
    | None = None,
    *tweaks,
    allow_hidden: bool = False,
    allow_repitch: bool = False,
    do_not_hide_middle_note_heads: bool = False,
    mock: bool = False,
    hide_middle_stems: bool = False,
    hide_stem_selector: typing.Callable | None = None,
    left_broken: bool = False,
    right_broken: bool = False,
    right_broken_show_next: bool = False,
    stop_pitch: str | abjad.NamedPitch | abjad.StaffPosition | None = None,
) -> None:
    prototype = (list, str, abjad.NamedPitch, abjad.StaffPosition)
    if pitch is not None:
        assert isinstance(pitch, prototype), repr(pitch)
    if stop_pitch is not None:
        assert type(pitch) is type(stop_pitch), repr((pitch, stop_pitch))
    glissando(
        argument,
        *tweaks,
        allow_repeats=True,
        allow_ties=True,
        hide_middle_note_heads=not do_not_hide_middle_note_heads,
        hide_middle_stems=hide_middle_stems,
        hide_stem_selector=hide_stem_selector,
        left_broken=left_broken,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
    )
    untie(argument)
    if pitch is not None and stop_pitch is None:
        # TODO: remove list test from or-clause?
        if isinstance(pitch, abjad.StaffPosition) or (
            isinstance(pitch, list) and isinstance(pitch[0], abjad.StaffPosition)
        ):
            _pitchcommands.staff_position(
                argument,
                pitch,
                allow_hidden=allow_hidden,
                allow_repitch=allow_repitch,
                mock=mock,
            )
        else:
            _pitchcommands.pitch(
                argument,
                pitch,
                allow_hidden=allow_hidden,
                allow_repitch=allow_repitch,
                mock=mock,
            )
    elif pitch is not None and stop_pitch is not None:
        if isinstance(pitch, abjad.StaffPosition):
            assert isinstance(stop_pitch, abjad.StaffPosition)
            raise Exception("port interpolate_staff_positions()")
            _pitchcommands.interpolate_staff_positions(
                argument,
                pitch,
                stop_pitch,
                allow_hidden=allow_hidden,
                mock=mock,
            )
        else:
            assert isinstance(pitch, str | abjad.NamedPitch)
            assert isinstance(stop_pitch, str | abjad.NamedPitch)
            _pitchcommands.interpolate_pitches(
                argument,
                pitch,
                stop_pitch,
                allow_hidden=allow_hidden,
                mock=mock,
            )


def force_accidental(argument, *, tag: abjad.Tag = abjad.Tag()) -> None:
    cautionary = False
    forced = True
    parenthesized = False
    if tag.string:
        if not tag.only_edition() and not tag.not_editions():
            raise Exception(f"tag must have edition: {tag!r}.")
        here_tag = _tags.function_name(_frame())
        alternative_tag = tag.append(here_tag)
        primary_tag = alternative_tag.invert_edition_tags()
    pleaves = _select.pleaves(argument)
    for pleaf in pleaves:
        if isinstance(pleaf, abjad.Note):
            note_heads = [pleaf.note_head]
        else:
            assert isinstance(pleaf, abjad.Chord)
            note_heads = list(pleaf.note_heads)
        for note_head in note_heads:
            assert note_head is not None
            if not tag.string:
                if cautionary:
                    note_head.is_cautionary = True
                if forced:
                    note_head.is_forced = True
                if parenthesized:
                    note_head.is_parenthesized = True
            else:
                alternative = copy.copy(note_head)
                if cautionary:
                    alternative.is_cautionary = True
                if forced:
                    alternative.is_forced = True
                if parenthesized:
                    alternative.is_parenthesized = True
                note_head.alternative = (
                    alternative,
                    alternative_tag,
                    primary_tag,
                )


def fractions(items):
    result = []
    for item in items:
        item_ = abjad.NonreducedFraction(item)
        result.append(item_)
    return result


def glissando(
    argument,
    *tweaks: abjad.Tweak,
    allow_repeats: bool = False,
    allow_ties: bool = False,
    hide_middle_note_heads: bool = False,
    hide_middle_stems: bool = False,
    hide_stem_selector: typing.Callable | None = None,
    left_broken: bool = False,
    parenthesize_repeats: bool = False,
    right_broken: bool = False,
    right_broken_show_next: bool = False,
    style: str | None = None,
    zero_padding: bool = False,
) -> None:
    leaves = abjad.select.leaves(argument)
    tweaks_ = []
    prototype = (abjad.Tweak, tuple)
    for tweak in tweaks or []:
        assert isinstance(tweak, prototype), repr(tweak)
        tweaks_.append(tweak)
    tag = _tags.function_name(_frame())
    abjad.glissando(
        leaves,
        *tweaks_,
        allow_repeats=allow_repeats,
        allow_ties=allow_ties,
        hide_middle_note_heads=hide_middle_note_heads,
        hide_middle_stems=hide_middle_stems,
        hide_stem_selector=hide_stem_selector,
        left_broken=left_broken,
        parenthesize_repeats=parenthesize_repeats,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
        tag=tag,
        zero_padding=zero_padding,
    )


def levine_multiphonic(n: int) -> abjad.Markup:
    assert isinstance(n, int), repr(n)
    return abjad.Markup(rf'\baca-boxed-markup "L.{n}"')


def untie(argument) -> None:
    indicators = [abjad.Tie, abjad.RepeatTie]
    leaves = abjad.select.leaves(argument)
    assert isinstance(leaves, list)
    for leaf in leaves:
        for indicator in indicators:
            abjad.detach(indicator, leaf)
