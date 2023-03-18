"""
Figures.
"""
import dataclasses
import typing

import abjad

from . import select as _select
from . import tags as _tags


def _get_figure_start_offset(figure_name, voice_name_to_timespans):
    assert isinstance(figure_name, str)
    for voice_name in sorted(voice_name_to_timespans.keys()):
        for timespan in voice_name_to_timespans[voice_name]:
            leaf_start_offset = timespan.start_offset
            leaves = abjad.iterate.leaves(timespan.annotation)
            for leaf in leaves:
                if abjad.get.annotation(leaf, "figure_name") == figure_name:
                    return leaf_start_offset
                leaf_duration = abjad.get.duration(leaf)
                leaf_start_offset += leaf_duration
    raise Exception(f"can not find figure {figure_name!r}.")


def _get_leaf_timespan(leaf, timespans):
    assert all(isinstance(_, abjad.Timespan) for _ in timespans), repr(timespans)
    found_leaf = False
    for timespan in timespans:
        leaf_start_offset = abjad.Offset(0)
        for leaf_ in abjad.iterate.leaves(timespan.annotation):
            leaf_duration = abjad.get.duration(leaf_)
            if leaf_ is leaf:
                found_leaf = True
                break
            leaf_start_offset += leaf_duration
        if found_leaf:
            break
    if not found_leaf:
        raise Exception(f"can not find {leaf!r} in timespans.")
    leaf_start_offset = timespan.start_offset + leaf_start_offset
    leaf_stop_offset = leaf_start_offset + leaf_duration
    return abjad.Timespan(leaf_start_offset, leaf_stop_offset)


def _get_start_offset(
    containers, contribution, voice_name_to_timespans, current_offset, score_stop_offset
):
    assert all(isinstance(_, abjad.Container) for _ in containers), repr(containers)
    if contribution.anchor is not None and contribution.anchor.figure_name is not None:
        figure_name = contribution.anchor.figure_name
        start_offset = _get_figure_start_offset(
            figure_name,
            voice_name_to_timespans,
        )
        return start_offset
    anchored = False
    if contribution.anchor is not None:
        remote_voice_name = contribution.anchor.remote_voice_name
        remote_selector = contribution.anchor.remote_selector
        use_remote_stop_offset = contribution.anchor.use_remote_stop_offset
        anchored = True
    else:
        remote_voice_name = None
        remote_selector = None
        use_remote_stop_offset = None
    if not anchored:
        return current_offset
    if anchored and remote_voice_name is None:
        return score_stop_offset
    timespans = voice_name_to_timespans[remote_voice_name]
    container_lists = [_.annotation for _ in timespans]
    for container_list in container_lists:
        assert all(isinstance(_, abjad.Container) for _ in container_list)
    if remote_selector is None:
        result = abjad.select.leaf(container_lists, 0)
    else:
        result = remote_selector(container_lists)
    selected_leaves = list(abjad.iterate.leaves(result))
    first_selected_leaf = selected_leaves[0]
    timespan = _get_leaf_timespan(first_selected_leaf, timespans)
    if use_remote_stop_offset:
        remote_anchor_offset = timespan.stop_offset
    else:
        remote_anchor_offset = timespan.start_offset
    local_anchor_offset = abjad.Offset(0)
    if contribution.anchor is not None:
        local_selector = contribution.anchor.local_selector
    else:
        local_selector = None
    if local_selector is not None:
        result = local_selector(containers)
        selected_leaves = list(abjad.iterate.leaves(result))
        first_selected_leaf = selected_leaves[0]
        dummy_container = abjad.Container(containers)
        timespan = abjad.get.timespan(first_selected_leaf)
        del dummy_container[:]
        local_anchor_offset = timespan.start_offset
    start_offset = remote_anchor_offset - local_anchor_offset
    return start_offset


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Anchor:
    """
    Anchor.

    ``use_remote_stop_offset`` is true when contribution anchors to remote components'
    stop offset; otherwise anchors to remote components' start offset.
    """

    figure_name: str | None = None
    local_selector: typing.Callable | None = None
    remote_selector: typing.Callable | None = None
    remote_voice_name: str | None = None
    use_remote_stop_offset: bool = False

    def __post_init__(self):
        if self.figure_name is not None:
            assert isinstance(self.figure_name, str), repr(self.figure_name)
        if self.local_selector is not None and not callable(self.local_selector):
            raise TypeError(f"must be callable: {self.local_selector!r}.")
        if self.remote_selector is not None and not callable(self.remote_selector):
            raise TypeError(f"must be callable: {self.remote_selector!r}.")
        if self.remote_voice_name is not None:
            assert isinstance(self.remote_voice_name, str), repr(self.remote_voice_name)
        assert isinstance(self.use_remote_stop_offset, bool), repr(
            self.use_remote_stop_offset
        )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Contribution:
    voice_name_to_containers: dict[str, list]
    anchor: Anchor | None = None
    hide_time_signature: bool | None = None
    time_signature: abjad.TimeSignature | None = None

    def __post_init__(self):
        assert isinstance(self.voice_name_to_containers, dict), repr(
            self.voice_name_to_containers
        )
        for value in self.voice_name_to_containers.values():
            assert isinstance(value, list), repr(value)
            assert len(value) == 1, repr(value)
            assert isinstance(value[0], abjad.Container), repr(value)
        if self.anchor is not None:
            assert isinstance(self.anchor, Anchor), repr(self.anchor)
        if self.hide_time_signature is not None:
            assert isinstance(self.hide_time_signature, bool), repr(
                self.hide_time_signature
            )
        if self.time_signature is not None:
            assert isinstance(self.time_signature, abjad.TimeSignature)


class Accumulator:
    __slots__ = (
        "current_offset",
        "figure_number",
        "music_maker",
        "score_stop_offset",
        "voice_names",
        "score",
        "time_signatures",
        "voice_name_to_timespans",
    )

    def __init__(self, score: abjad.Score) -> None:
        assert isinstance(score, abjad.Score), repr(score)
        self.score = score
        voice_names = []
        for voice in abjad.iterate.components(score, abjad.Voice):
            voice_names.append(voice.name)
        self.voice_names = voice_names
        self.current_offset = abjad.Offset(0)
        self.figure_number = 1
        self.score_stop_offset = abjad.Offset(0)
        self.time_signatures: list[abjad.TimeSignature] = []
        self.voice_name_to_timespans: dict = dict([(_, []) for _ in self.voice_names])

    def assemble(self, voice_name: str) -> list[abjad.Component]:
        timespans = self.voice_name_to_timespans[voice_name]
        total_duration = sum([_.duration for _ in self.time_signatures])
        for timespan in timespans:
            assert isinstance(timespan, abjad.Timespan)
        timespans = list(timespans)
        timespans.sort()
        try:
            first_start_offset = timespans[0].start_offset
        except Exception:
            first_start_offset = abjad.Offset(0)
        timespan_list = abjad.TimespanList(timespans)
        if timespan_list:
            gaps = ~timespan_list
        else:
            sectionwide_gap = abjad.Timespan(0, total_duration)
            gaps = abjad.TimespanList([sectionwide_gap])
        if 0 < first_start_offset:
            first_gap = abjad.Timespan(0, first_start_offset)
            gaps.append(first_gap)
        if timespans:
            final_stop_offset = timespans[-1].stop_offset
        else:
            final_stop_offset = total_duration
        if final_stop_offset < total_duration:
            final_gap = abjad.Timespan(final_stop_offset, total_duration)
            gaps.append(final_gap)
        timespans = timespans + list(gaps)
        timespans.sort()
        components = []
        for timespan in timespans:
            if timespan.annotation is not None:
                components_ = timespan.annotation
            else:
                components_ = [abjad.Skip(1, multiplier=timespan.duration.pair)]
            components.extend(components_)
        return components

    def cache(
        self,
        voice_name: str,
        tuplets: abjad.Container | list[abjad.Tuplet],
        *,
        anchor: Anchor | None = None,
        do_not_increment: bool = False,
        hide_time_signature: bool | None = None,
        imbrications: dict[str, list[abjad.Container]] | None = None,
        tsd: int | None = None,
    ):
        assert isinstance(voice_name, str), repr(voice_name)
        assert all(isinstance(_, abjad.Tuplet) for _ in tuplets), repr(tuplets)
        if isinstance(tuplets, abjad.Container):
            container = tuplets
        else:
            container = abjad.Container(tuplets)
        imbrications = imbrications or {}
        assert isinstance(imbrications, dict), repr(imbrications)
        duration = abjad.get.duration(container)
        if tsd is not None:
            pair = abjad.duration.with_denominator(duration, tsd)
        else:
            pair = duration.pair
        time_signature = abjad.TimeSignature(pair)
        voice_name_to_containers = {voice_name: [container]}
        assert isinstance(imbrications, dict)
        for voice_name, containers in imbrications.items():
            assert all(isinstance(_, abjad.Container) for _ in containers), repr(
                containers
            )
            voice_name_to_containers[voice_name] = containers
        if anchor is not None:
            anchor = dataclasses.replace(
                anchor, remote_voice_name=anchor.remote_voice_name
            )
        contribution = Contribution(
            voice_name_to_containers,
            anchor=anchor,
            hide_time_signature=hide_time_signature,
            time_signature=time_signature,
        )
        for voice_name, containers in contribution.voice_name_to_containers.items():
            start_offset = _get_start_offset(
                containers,
                contribution,
                self.voice_name_to_timespans,
                self.current_offset,
                self.score_stop_offset,
            )
            stop_offset = start_offset + abjad.get.duration(containers)
            timespan = abjad.Timespan(start_offset, stop_offset)
            timespan = abjad.Timespan(
                timespan.start_offset,
                timespan.stop_offset,
                annotation=containers,
            )
            self.voice_name_to_timespans[voice_name].append(timespan)
        self.current_offset = stop_offset
        self.score_stop_offset = max(self.score_stop_offset, stop_offset)
        if not contribution.hide_time_signature:
            if (
                contribution.anchor is None
                or contribution.hide_time_signature is False
                or (
                    contribution.anchor
                    and contribution.anchor.remote_voice_name is None
                )
            ):
                assert isinstance(contribution.time_signature, abjad.TimeSignature)
                self.time_signatures.append(contribution.time_signature)

    def populate(self, score):
        assert isinstance(score, abjad.Score), repr(score)
        for voice_name in sorted(self.voice_name_to_timespans):
            components = self.assemble(voice_name)
            if components:
                voice = score[voice_name]
                voice.extend(components)


def anchor(
    remote_voice_name: str,
    remote_selector=None,
    local_selector=None,
) -> Anchor:
    """
    Anchors music in this figure (filtered by ``local_selector``) to start offset of
    ``remote_voice_name`` (filtered by ``remote_selector``).
    """
    return Anchor(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
    )


def anchor_after(
    remote_voice_name: str,
    remote_selector=None,
    local_selector=None,
) -> Anchor:
    """
    Anchors music in this figure (filtered by ``local_selector``) to stop offset of
    ``remote_voice_name`` (filtered by ``remote_selector``).
    """
    return Anchor(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
    )


def anchor_to_figure(figure_name: str) -> Anchor:
    """
    Anchors music in this figure to start of ``figure_name``.
    """
    return Anchor(figure_name=figure_name)


def label_figure(
    tuplets, figure_name, accumulator, direction=None, do_not_increment=False
):
    figure_number = accumulator.figure_number
    if not do_not_increment:
        accumulator.figure_number += 1
    parts = figure_name.split("_")
    if len(parts) == 1:
        body = parts[0]
        figure_label_string = f'"{body}"'
    elif len(parts) == 2:
        body, subscript = parts
        figure_label_string = rf'\concat {{ "{body}" \sub {subscript} }}'
    else:
        raise Exception(f"unrecognized figure name: {figure_name!r}.")
    string = r"\markup"
    string += rf" \concat {{ [ \raise #0.25 \fontsize #-2 ({figure_number})"
    if figure_name:
        string += rf" \hspace #1 {figure_label_string} ] }}"
    else:
        string += r" ] }"
    figure_label_markup = abjad.Markup(string)
    bundle = abjad.bundle(figure_label_markup, r"- \tweak color #blue")
    leaf = abjad.select.leaf(tuplets, 0)
    abjad.annotate(leaf, "figure_name", figure_name)
    if not do_not_increment:
        pleaves = _select.pleaves(tuplets)
        if pleaves:
            leaf = pleaves[0]
        else:
            leaf = abjad.select.leaf(tuplets, 0)
        abjad.attach(
            bundle,
            leaf,
            deactivate=True,
            direction=direction,
            tag=_tags.FIGURE_LABEL,
        )


def resume() -> Anchor:
    """
    Resumes music at next offset across all voices in score.
    """
    return Anchor()


def resume_after(remote_voice_name) -> Anchor:
    """
    Resumes music after remote components.
    """
    return Anchor(
        remote_selector=lambda _: abjad.select.leaf(_, -1),
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
    )
