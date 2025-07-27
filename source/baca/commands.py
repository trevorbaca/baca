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


def _is_rest(argument):
    if argument is None:
        return False
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
    *tweaks: abjad.Tweak,
    bow_change_tweaks: typing.Sequence[abjad.Tweak] = (),
    final_spanner: bool = False,
    helper: typing.Callable = lambda x, y: x,
) -> list[abjad.wrapper.Wrapper]:
    wrappers: list[abjad.wrapper.Wrapper] = []
    tag = _helpers.function_name(_frame())
    _tags.tag(wrappers, tag)
    bcps_ = list(bcps)
    bcps_ = helper(bcps_, argument)
    bcps = abjad.CyclicTuple(bcps_)
    lts = _select.lts(argument)
    add_right_text_to_me = None
    if not final_spanner:
        rest_count, nonrest_count = 0, 0
        for lt in reversed(lts):
            if _is_rest(lt.get_head()):
                rest_count += 1
            else:
                if 0 < rest_count and nonrest_count == 0:
                    add_right_text_to_me = lt.get_head()
                    break
                if 0 < nonrest_count and rest_count == 0:
                    add_right_text_to_me = lt.get_head()
                    break
                nonrest_count += 1
    if final_spanner and len(lts[-1]) == 1 and not _is_rest(lts[-1].get_head()):
        next_leaf_after_argument = abjad.get.leaf(lts[-1][-1], 1)
        if next_leaf_after_argument is None:
            message = "can not attach final spanner: argument includes end of score."
            raise Exception(message)
    previous_bcp = None
    i = 0
    for lt in lts:
        stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanBCP")
        if not final_spanner and lt is lts[-1] and not _is_rest(lt.get_head()):
            abjad.attach(
                stop_text_span,
                lt.get_head(),
                tag=_helpers.function_name(_frame(), n=1),
            )
            wrapper = abjad.get.wrappers(lt.get_head(), stop_text_span)[-1]
            wrappers.append(wrapper)
            break
        previous_leaf = abjad.get.leaf(lt.get_head(), -1)
        next_leaf = abjad.get.leaf(lt.get_head(), 1)
        if _is_rest(lt.get_head()) and (
            _is_rest(previous_leaf) or previous_leaf is None
        ):
            continue
        if (
            isinstance(lt.get_head(), abjad.Note)
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
        elif not _is_rest(lt.get_head()):
            style = r"\baca-solid-line-with-arrow"
        else:
            style = r"\baca-invisible-line"
        right_text = None
        if lt.get_head() is add_right_text_to_me:
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
            start_text_span = _helpers.bundle_tweaks(start_text_span, tweaks)
        if _is_rest(lt.get_head()) and (_is_rest(next_leaf) or next_leaf is None):
            pass
        else:
            abjad.attach(
                start_text_span,
                lt.get_head(),
                tag=_helpers.function_name(_frame(), n=2),
            )
            wrapper = abjad.get.wrappers(lt.get_head(), start_text_span)[-1]
            wrappers.append(wrapper)
        if 0 < i - 1:
            abjad.attach(
                stop_text_span,
                lt.get_head(),
                tag=_helpers.function_name(_frame(), n=3),
            )
            wrapper = abjad.get.wrappers(lt.get_head(), stop_text_span)[-1]
            wrappers.append(wrapper)
        if lt is lts[-1] and final_spanner:
            assert next_leaf_after_argument is not None
            abjad.attach(
                stop_text_span,
                next_leaf_after_argument,
                tag=_helpers.function_name(_frame(), n=4),
            )
            assert next_leaf_after_argument is not None
            wrapper = abjad.get.wrappers(next_leaf_after_argument, stop_text_span)[-1]
            wrappers.append(wrapper)
        bcp_fraction = abjad.Fraction(*bcp)
        next_bcp_fraction = abjad.Fraction(*bcps[i])
        if _is_rest(lt.get_head()):
            pass
        elif _is_rest(previous_leaf) or previous_bcp is None:
            if bcp_fraction > next_bcp_fraction:
                articulation = abjad.Articulation("upbow")
                if bow_change_tweaks:
                    articulation = _helpers.bundle_tweaks(
                        articulation,
                        bow_change_tweaks,
                    )
                abjad.attach(
                    articulation,
                    lt.get_head(),
                    tag=_helpers.function_name(_frame(), n=5),
                )
                wrapper = abjad.get.wrappers(lt.get_head(), articulation)[-1]
                wrappers.append(wrapper)
            elif bcp_fraction < next_bcp_fraction:
                articulation = abjad.Articulation("downbow")
                if bow_change_tweaks:
                    articulation = _helpers.bundle_tweaks(
                        articulation,
                        bow_change_tweaks,
                    )
                abjad.attach(
                    articulation,
                    lt.get_head(),
                    tag=_helpers.function_name(_frame(), n=6),
                )
                wrapper = abjad.get.wrappers(lt.get_head(), articulation)[-1]
                wrappers.append(wrapper)
        else:
            previous_bcp_fraction = abjad.Fraction(*previous_bcp)
            if previous_bcp_fraction < bcp_fraction > next_bcp_fraction:
                articulation = abjad.Articulation("upbow")
                if bow_change_tweaks:
                    articulation = _helpers.bundle_tweaks(
                        articulation,
                        bow_change_tweaks,
                    )
                abjad.attach(
                    articulation,
                    lt.get_head(),
                    tag=_helpers.function_name(_frame(), n=7),
                )
                wrapper = abjad.get.wrappers(lt.get_head(), articulation)[-1]
                wrappers.append(wrapper)
            elif previous_bcp_fraction > bcp_fraction < next_bcp_fraction:
                articulation = abjad.Articulation("downbow")
                if bow_change_tweaks:
                    articulation = _helpers.bundle_tweaks(
                        articulation,
                        bow_change_tweaks,
                    )
                abjad.attach(
                    articulation,
                    lt.get_head(),
                    tag=_helpers.function_name(_frame(), n=8),
                )
                wrapper = abjad.get.wrappers(lt.get_head(), articulation)[-1]
                wrappers.append(wrapper)
        previous_bcp = bcp
    return wrappers


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
            note_heads = [pleaf.get_note_head()]
        else:
            assert isinstance(pleaf, abjad.Chord)
            note_heads = list(pleaf.get_note_heads())
        for note_head in note_heads:
            assert note_head is not None
            if not tag.string:
                if cautionary:
                    note_head.set_is_cautionary(True)
                if forced:
                    note_head.set_is_forced(True)
                if parenthesized:
                    note_head.set_is_parenthesized(True)
            else:
                alternative = copy.copy(note_head)
                if cautionary:
                    alternative.set_is_cautionary(True)
                if forced:
                    alternative.set_is_forced(True)
                if parenthesized:
                    alternative.set_is_parenthesized(True)
                triple = (
                    alternative,
                    alternative_tag,
                    primary_tag,
                )
                note_head.set_alternative(triple)


def glissando(
    leaves,
    descriptor: str | None = None,
    *tweaks: abjad.Tweak,
    allow_hidden: bool = False,
    allow_repitch: bool = False,
    do_not_allow_repeats: bool = False,
    do_not_hide_middle_note_heads: bool = False,
    do_not_transpose: bool = False,
    do_not_untie: bool = False,
    hide_middle_stems: bool = False,
    left_broken: bool = False,
    mock: bool = False,
    right_broken: bool = False,
    right_broken_show_next: bool = False,
    rleak: bool = False,
    staff_position: bool = False,
    zero_padding: bool = False,
) -> None:
    leaves = abjad.select.leaves(leaves)
    assert isinstance(descriptor, str | type(None)), repr(descriptor)
    if do_not_untie is False:
        untie(leaves)
        # total = len(leaves)
        # for i, leaf in enumerate(leaves):
        #     if 0 < i:
        #         abjad.detach(abjad.RepeatTie, leaf)
        #     if i < total - 1:
        #        abjad.detach(abjad.Tie, leaf)
    if rleak:
        leaves = _select.rleak(leaves)
    total_leaves = len(leaves)
    strings: list[str] = []
    if isinstance(descriptor, str):
        for string in descriptor.split():
            if string.endswith(">"):
                strings[-1] += " " + string
            else:
                strings.append(string)
    else:
        strings.append("UNPITCHED")
    if len(strings) == 1:
        strings *= 2
    start_index, stop_index, cumulative_leaves = 0, 0, 0
    for i, string in enumerate(strings[:-1]):
        if "/" in string:
            start_pitch, leaf_count_string = string.split("/")
        else:
            start_pitch, leaf_count_string = string, "1"
        leaf_count = int(leaf_count_string)
        if i == len(strings) - 2 and leaf_count == 1:
            leaf_count = total_leaves - (cumulative_leaves + 1)
        cumulative_leaves += leaf_count
        if i == len(strings) - 1:
            stop_pitch = strings[-1]
        else:
            stop_pitch = strings[i + 1].split("/")[0]
        stop_index = start_index + leaf_count + 1
        abjad.glissando(
            leaves[start_index:stop_index],
            *tweaks,
            allow_repeats=not do_not_allow_repeats,
            hide_middle_note_heads=not do_not_hide_middle_note_heads,
            hide_middle_stems=hide_middle_stems,
            left_broken=left_broken,
            right_broken=right_broken,
            right_broken_show_next=right_broken_show_next,
            tag=_helpers.function_name(_frame()),
            zero_padding=zero_padding,
        )
        if start_pitch == "UNPITCHED":
            pass
        elif start_pitch == stop_pitch:
            if staff_position is True:
                _pitchtools.staff_position(
                    leaves[start_index:stop_index],
                    int(start_pitch),
                    allow_hidden=allow_hidden,
                    allow_repitch=allow_repitch,
                    mock=mock,
                )
            else:
                _pitchtools.pitch(
                    leaves[start_index:stop_index],
                    start_pitch,
                    allow_hidden=allow_hidden,
                    allow_repitch=allow_repitch,
                    do_not_transpose=do_not_transpose,
                    mock=mock,
                )
        else:
            if staff_position is True:
                _pitchtools._do_staff_position_interpolation_command(
                    leaves[start_index:stop_index],
                    abjad.StaffPosition(int(start_pitch)),
                    abjad.StaffPosition(int(stop_pitch)),
                    allow_hidden=allow_hidden,
                    mock=mock,
                    pitches_instead_of_staff_positions=False,
                )
            else:
                _pitchtools.interpolate_pitches(
                    leaves[start_index:stop_index],
                    start_pitch,
                    stop_pitch,
                )
        start_index = stop_index - 1


def levine_multiphonic(n: int) -> str:
    assert isinstance(n, int), repr(n)
    return rf'\baca-boxed-markup "L.{n}"'


def untie(argument) -> None:
    indicators = [abjad.Tie, abjad.RepeatTie]
    for leaf in abjad.select.leaves(argument):
        for indicator in indicators:
            abjad.detach(indicator, leaf)
