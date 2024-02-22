"""
Commands.
"""

import copy
import typing
from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import pitchtools as _pitchtools
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


def basic_glissando(
    argument,
    *tweaks: abjad.Tweak,
    do_not_allow_repeats: bool = False,
    hide_middle_note_heads: bool = False,
    right_broken: bool = False,
    zero_padding: bool = False,
) -> None:
    leaves = abjad.select.leaves(argument)
    tag = _helpers.function_name(_frame())
    abjad.glissando(
        leaves,
        *tweaks,
        allow_repeats=not do_not_allow_repeats,
        hide_middle_note_heads=hide_middle_note_heads,
        right_broken=right_broken,
        tag=tag,
        zero_padding=zero_padding,
    )


def bcps(
    argument,
    bcps,
    *tweaks: _typings.IndexedTweak,
    bow_change_tweaks: typing.Sequence[_typings.IndexedTweak] = (),
    final_spanner: bool = False,
    helper: typing.Callable = lambda x, y: x,
) -> list[abjad.Wrapper]:
    wrappers: list[abjad.Wrapper] = []
    tag = _helpers.function_name(_frame())
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
                tag=_helpers.function_name(_frame(), n=1),
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
                style = r"\baca-solid-line-with-arrow"
            else:
                style = r"\baca-invisible-line"
        elif not _is_rest(lt.head):
            style = r"\baca-solid-line-with-arrow"
        else:
            style = r"\baca-invisible-line"
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
                tag=_helpers.function_name(_frame(), n=2),
                wrapper=True,
            )
            wrappers.append(wrapper)
        if 0 < i - 1:
            wrapper = abjad.attach(
                stop_text_span,
                lt.head,
                tag=_helpers.function_name(_frame(), n=3),
                wrapper=True,
            )
            wrappers.append(wrapper)
        if lt is lts[-1] and final_spanner:
            wrapper = abjad.attach(
                stop_text_span,
                next_leaf_after_argument,
                tag=_helpers.function_name(_frame(), n=4),
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
                    tag=_helpers.function_name(_frame(), n=5),
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
                    tag=_helpers.function_name(_frame(), n=6),
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
                    tag=_helpers.function_name(_frame(), n=7),
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
                    tag=_helpers.function_name(_frame(), n=8),
                    wrapper=True,
                )
                wrappers.append(wrapper)
        previous_bcp = bcp
    return wrappers


def color(argument, *, lone: bool = False) -> None:
    return abjad.label.by_selector(argument, lone=lone)


def durations(items):
    return [abjad.Duration(_) for _ in items]


def finger_pressure_transition(argument) -> None:
    tag = _helpers.function_name(_frame())
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
    pitch: str,
    *tweaks: abjad.Tweak,
    allow_hidden: bool = False,
    allow_repitch: bool = False,
    do_not_hide_middle_note_heads: bool = False,
    do_not_transpose: bool = False,
    mock: bool = False,
    hide_middle_stems: bool = False,
    hide_stem_selector: typing.Callable | None = None,
    left_broken: bool = False,
    right_broken: bool = False,
    right_broken_show_next: bool = False,
) -> None:
    assert isinstance(pitch, str), repr(pitch)
    stop_pitch = None
    if pitch is not None:
        if " " in pitch:
            parts: list[str] = []
            for part in pitch.split():
                if part.endswith(">"):
                    parts[-1] += " " + part
                else:
                    parts.append(part)
            assert len(parts) in (1, 2), repr(parts)
            if len(parts) == 1:
                pitch = parts[0]
            elif len(parts) == 2:
                pitch, stop_pitch = parts
            else:
                raise Exception(parts)
    untie(argument)
    abjad.glissando(
        argument,
        *tweaks,
        allow_repeats=True,
        hide_middle_note_heads=not do_not_hide_middle_note_heads,
        hide_middle_stems=hide_middle_stems,
        hide_stem_selector=hide_stem_selector,
        left_broken=left_broken,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
        tag=_helpers.function_name(_frame()),
    )
    if pitch is not None:
        if stop_pitch is None or pitch == stop_pitch:
            _pitchtools.pitch(
                argument,
                pitch,
                allow_hidden=allow_hidden,
                allow_repitch=allow_repitch,
                do_not_transpose=do_not_transpose,
                mock=mock,
            )
        else:
            _pitchtools.interpolate_pitches(
                argument,
                pitch,
                stop_pitch,
                allow_hidden=allow_hidden,
                mock=mock,
            )


def flat_glissando_without_pitch(
    argument,
    *tweaks: _typings.IndexedTweak,
    do_not_hide_middle_note_heads: bool = False,
    hide_middle_stems: bool = False,
    hide_stem_selector: typing.Callable | None = None,
    left_broken: bool = False,
    right_broken: bool = False,
    right_broken_show_next: bool = False,
) -> None:
    untie(argument)
    abjad.glissando(
        argument,
        *tweaks,
        allow_repeats=True,
        hide_middle_note_heads=not do_not_hide_middle_note_heads,
        hide_middle_stems=hide_middle_stems,
        hide_stem_selector=hide_stem_selector,
        left_broken=left_broken,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
        tag=_helpers.function_name(_frame()),
    )


def force_accidental(argument, *, tag: abjad.Tag | None = None) -> None:
    tag = tag or abjad.Tag()
    tag = tag.append(_helpers.function_name(_frame()))
    cautionary = False
    forced = True
    parenthesized = False
    if not tag.only_edition() and not tag.not_editions():
        raise Exception(f"tag must have edition: {tag!r}.")
    alternative_tag = tag
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


def levine_multiphonic(n: int) -> str:
    assert isinstance(n, int), repr(n)
    return rf'\baca-boxed-markup "L.{n}"'


def multistage_glissando(
    leaves,
    descriptor: str,
    *tweaks: _typings.IndexedTweak,
    allow_hidden: bool = False,
    allow_repitch: bool = False,
    debug: bool = False,
    do_not_transpose: bool = False,
    hide_middle_stems: bool = False,
    hide_stem_selector: typing.Callable | None = None,
    left_broken: bool = False,
    mock: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
):
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    if rleak:
        leaves = _select.rleak(leaves)
    untie(leaves)
    strings, total_leaves = descriptor.split(), len(leaves)
    if len(strings) == 1:
        strings *= 2
    start_index, stop_index, cumulative_leaves = 0, 0, 0
    for i, string in enumerate(strings[:-1]):
        if ":" in string:
            start_pitch, leaf_count_string = string.split(":")
        else:
            start_pitch, leaf_count_string = string, "1"
        leaf_count = int(leaf_count_string)
        if i == len(strings) - 2 and leaf_count == 1:
            leaf_count = total_leaves - (cumulative_leaves + 1)
        cumulative_leaves += leaf_count
        if i == len(strings) - 1:
            stop_pitch = strings[-1]
        else:
            stop_pitch = strings[i + 1].split(":")[0]
        stop_index = start_index + leaf_count + 1
        abjad.glissando(
            leaves[start_index:stop_index],
            *tweaks,
            allow_repeats=True,
            hide_middle_note_heads=True,
            hide_middle_stems=hide_middle_stems,
            hide_stem_selector=hide_stem_selector,
            left_broken=left_broken,
            right_broken=right_broken,
            tag=_helpers.function_name(_frame()),
        )
        if start_pitch == stop_pitch:
            _pitchtools.pitch(
                leaves[start_index:stop_index],
                start_pitch,
                allow_hidden=allow_hidden,
                allow_repitch=allow_repitch,
                do_not_transpose=do_not_transpose,
                mock=mock,
            )
        else:
            _pitchtools.interpolate_pitches(
                leaves[start_index:stop_index],
                start_pitch,
                stop_pitch,
            )
        start_index = stop_index - 1


def untie(argument) -> None:
    indicators = [abjad.Tie, abjad.RepeatTie]
    leaves = abjad.select.leaves(argument)
    assert isinstance(leaves, list)
    for leaf in leaves:
        for indicator in indicators:
            abjad.detach(indicator, leaf)
