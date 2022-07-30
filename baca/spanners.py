"""
Spanners.
"""
import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import command as _command
from . import select as _select
from . import tags as _tags
from . import treat as _treat
from . import tweaks as _tweaks
from . import typings as _typings


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class SpannerIndicatorCommand(_command.Command):

    detach_first: bool = False
    direction: abjad.Vertical | None = None
    left_broken: bool = False
    right_broken: bool = False
    start_indicator: typing.Any = None
    stop_indicator: typing.Any = None
    tweaks: tuple[_typings.IndexedTweak, ...] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.detach_first, bool), repr(self.detach_first)
        assert isinstance(self.left_broken, bool), repr(self.left_broken)
        assert isinstance(self.right_broken, bool), repr(self.right_broken)
        _tweaks.validate_indexed_tweaks(self.tweaks)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.start_indicator is None and self.stop_indicator is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        if self.start_indicator is not None:
            start_indicator = self.start_indicator
            if self.detach_first:
                for leaf in abjad.iterate.leaves(argument, grace=False):
                    abjad.detach(type(start_indicator), leaf)
            start_indicator = _tweaks.bundle_tweaks(start_indicator, self.tweaks)
            first_leaf = abjad.select.leaf(argument, 0)
            if self.left_broken:
                self._attach_indicator(
                    start_indicator,
                    first_leaf,
                    deactivate=self.deactivate,
                    runtime=runtime,
                    tag=_tags.function_name(_frame(), self, n=1)
                    .append(_tags.SPANNER_START)
                    .append(_tags.LEFT_BROKEN),
                )
            else:
                self._attach_indicator(
                    start_indicator,
                    first_leaf,
                    deactivate=self.deactivate,
                    runtime=runtime,
                    tag=_tags.function_name(_frame(), self, n=2).append(
                        _tags.SPANNER_START
                    ),
                )
        if self.stop_indicator is not None:
            stop_indicator = self.stop_indicator
            if self.detach_first:
                for leaf in abjad.iterate.leaves(argument, grace=False):
                    abjad.detach(type(stop_indicator), leaf)
            final_leaf = abjad.select.leaf(argument, -1)
            if self.right_broken:
                self._attach_indicator(
                    stop_indicator,
                    final_leaf,
                    deactivate=self.deactivate,
                    runtime=runtime,
                    tag=_tags.function_name(_frame(), self, n=3)
                    .append(_tags.SPANNER_STOP)
                    .append(_tags.RIGHT_BROKEN),
                )
            else:
                self._attach_indicator(
                    stop_indicator,
                    final_leaf,
                    deactivate=self.deactivate,
                    runtime=runtime,
                    tag=_tags.function_name(_frame(), self, n=4).append(
                        _tags.SPANNER_STOP
                    ),
                )
        return False

    def _attach_indicator(
        self, indicator, leaf, *, deactivate=None, runtime=None, tag=None
    ):
        assert isinstance(tag, abjad.Tag), repr(tag)
        reapplied = _treat.remove_reapplied_wrappers(leaf, indicator)
        tag_ = self.tag.append(tag)
        wrapper = abjad.attach(
            indicator,
            leaf,
            deactivate=deactivate,
            direction=self.direction,
            tag=tag_,
            wrapper=True,
        )
        if _treat.compare_persistent_indicators(indicator, reapplied):
            status = "redundant"
            _treat.treat_persistent_wrapper(runtime["manifests"], wrapper, status)


def _attach_start_stop_indicators(
    leaves, tag, *, detach_first=False, start_indicator=None, stop_indicator=None
):
    assert isinstance(tag, abjad.Tag), repr(tag)
    if detach_first:
        for leaf in abjad.iterate.leaves(leaves, grace=False):
            abjad.detach(type(start_indicator), leaf)
            abjad.detach(type(stop_indicator), leaf)
    if start_indicator is not None:
        first_leaf = leaves[0]
        here = _tags.function_name(_frame(), n=2)
        abjad.attach(
            start_indicator,
            first_leaf,
            tag=tag.append(_tags.SPANNER_START).append(here),
        )
    if stop_indicator is not None:
        final_leaf = leaves[-1]
        here = _tags.function_name(_frame(), n=4)
        abjad.attach(
            stop_indicator,
            final_leaf,
            tag=tag.append(_tags.SPANNER_STOP).append(here),
        )


def _prepare_trill_spanner_arguments(
    *,
    alteration,
    harmonic,
    start_trill_span,
    stop_trill_span,
):
    if alteration is not None:
        prototype = (abjad.NamedPitch, abjad.NamedInterval, str)
        if not isinstance(alteration, prototype):
            message = "trill spanner 'alteration' must be pitch, interval, str:"
            message += f"\n   {alteration}"
            raise Exception(message)
    interval = pitch = None
    if alteration is not None:
        try:
            pitch = abjad.NamedPitch(alteration)
        except Exception:
            try:
                interval = abjad.NamedInterval(alteration)
            except Exception:
                pass
    start_trill_span_: abjad.StartTrillSpan | abjad.Bundle
    start_trill_span_ = start_trill_span or abjad.StartTrillSpan()
    if pitch is not None or interval is not None:
        start_trill_span_ = dataclasses.replace(
            start_trill_span_, interval=interval, pitch=pitch
        )
    if harmonic is True:
        string = "#(lambda (grob) (grob-interpret-markup grob"
        string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
        string = rf"- \tweak TrillPitchHead.stencil {string}"
        start_trill_span_ = abjad.bundle(start_trill_span_, string)
    stop_trill_span = stop_trill_span or abjad.StopTrillSpan()
    return start_trill_span_, stop_trill_span


def beam(
    *tweaks: abjad.Tweak,
    direction: abjad.Vertical | None = None,
    selector: typing.Callable = lambda _: _select.tleaves(_),
    start_beam: abjad.StartBeam = None,
    stop_beam: abjad.StopBeam = None,
) -> SpannerIndicatorCommand:
    start_beam = start_beam or abjad.StartBeam()
    stop_beam = stop_beam or abjad.StopBeam()
    return SpannerIndicatorCommand(
        detach_first=True,
        direction=direction,
        selector=selector,
        start_indicator=start_beam,
        stop_indicator=stop_beam,
        tags=[_tags.function_name(_frame())],
        tweaks=tweaks,
    )


def beam_function(
    argument,
    *tweaks: abjad.Tweak,
    direction: abjad.Vertical | None = None,
    start_beam: abjad.StartBeam = None,
    stop_beam: abjad.StopBeam = None,
    tags: list[abjad.Tag] = None,
) -> None:
    # TODO: eventually remove tleaves and force call in section files
    leaves = _select.tleaves(argument)
    start_beam = start_beam or abjad.StartBeam()
    stop_beam = stop_beam or abjad.StopBeam()
    assert isinstance(start_beam, abjad.StartBeam), repr(start_beam)
    assert isinstance(stop_beam, abjad.StopBeam), repr(stop_beam)
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    _attach_start_stop_indicators(
        leaves,
        tag,
        detach_first=True,
        start_indicator=start_beam,
        stop_indicator=stop_beam,
    )


def ottava(
    start_ottava: abjad.Ottava = abjad.Ottava(n=1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, site="after"),
    *,
    right_broken: bool = False,
    selector: typing.Callable = lambda _: _select.tleaves(_),
) -> SpannerIndicatorCommand:
    return SpannerIndicatorCommand(
        right_broken=right_broken,
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[_tags.function_name(_frame())],
    )


def ottava_function(
    leaves: typing.Sequence[abjad.Leaf],
    *,
    allow_rests: bool = False,
    start_ottava: abjad.Ottava = abjad.Ottava(n=1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, site="after"),
    # right_broken: bool = False,
    tags: list[abjad.Tag] = None,
) -> None:
    if not allow_rests:
        leaves = _select.tleaves(leaves)
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    assert isinstance(start_ottava, abjad.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, abjad.Ottava), repr(stop_ottava)
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    _attach_start_stop_indicators(
        leaves,
        tag,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
    )


def ottava_bassa(
    start_ottava: abjad.Ottava = abjad.Ottava(n=-1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, site="after"),
    *,
    selector: typing.Callable = lambda _: _select.tleaves(_),
) -> SpannerIndicatorCommand:
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[_tags.function_name(_frame())],
    )


def ottava_bassa_function(
    leaves: typing.Sequence[abjad.Leaf],
    *,
    allow_rests: bool = False,
    start_ottava: abjad.Ottava = abjad.Ottava(n=-1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, site="after"),
    tags: list[abjad.Tag] = None,
) -> None:
    if not allow_rests:
        leaves = _select.pleaves(leaves)
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    assert isinstance(start_ottava, abjad.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, abjad.Ottava), repr(stop_ottava)
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    _attach_start_stop_indicators(
        leaves,
        tag,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
    )


def slur(
    *tweaks: abjad.Tweak,
    map=None,
    phrasing_slur=False,
    selector: typing.Callable = lambda _: _select.tleaves(_),
    start_slur: abjad.StartSlur = None,
    stop_slur: abjad.StopSlur = None,
) -> SpannerIndicatorCommand:
    if phrasing_slur is True:
        start_slur_ = start_slur or abjad.StartPhrasingSlur()
        stop_slur_ = stop_slur or abjad.StopPhrasingSlur()
    else:
        start_slur_ = start_slur or abjad.StartSlur()
        stop_slur_ = stop_slur or abjad.StopSlur()
    return SpannerIndicatorCommand(
        map=map,
        selector=selector,
        start_indicator=start_slur_,
        stop_indicator=stop_slur_,
        tags=[_tags.function_name(_frame())],
        tweaks=tweaks,
    )


def slur_function(
    leaves: typing.Sequence[abjad.Leaf],
    *tweaks: abjad.Tweak,
    phrasing_slur: bool = False,
    start_slur: abjad.StartSlur = None,
    stop_slur: abjad.StopSlur = None,
    tags: list[abjad.Tag] = None,
) -> None:
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    if phrasing_slur is True:
        start_slur_ = start_slur or abjad.StartPhrasingSlur()
        stop_slur_ = stop_slur or abjad.StopPhrasingSlur()
    else:
        start_slur_ = start_slur or abjad.StartSlur()
        stop_slur_ = stop_slur or abjad.StopSlur()
    start_slur_ = _tweaks.bundle_tweaks(start_slur_, tweaks)
    stop_slur_ = _tweaks.bundle_tweaks(stop_slur_, tweaks)
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    _attach_start_stop_indicators(
        leaves,
        tag,
        start_indicator=start_slur_,
        stop_indicator=stop_slur_,
    )


def sustain_pedal(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
    start_piano_pedal: abjad.StartPianoPedal = None,
    stop_piano_pedal: abjad.StopPianoPedal = None,
) -> SpannerIndicatorCommand:
    start_piano_pedal = start_piano_pedal or abjad.StartPianoPedal()
    stop_piano_pedal = stop_piano_pedal or abjad.StopPianoPedal()
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_piano_pedal,
        stop_indicator=stop_piano_pedal,
        tags=[_tags.function_name(_frame())],
    )


def trill_spanner(
    *tweaks: abjad.Tweak,
    alteration: str = None,
    harmonic: bool = False,
    left_broken: bool = False,
    map=None,
    right_broken: bool = False,
    selector: typing.Callable = lambda _: _select.tleaves(_, rleak=True),
    start_trill_span: abjad.StartTrillSpan = None,
    stop_trill_span: abjad.StopTrillSpan = None,
) -> SpannerIndicatorCommand:
    start_trill_span_, stop_trill_span = _prepare_trill_spanner_arguments(
        alteration=alteration,
        harmonic=harmonic,
        start_trill_span=start_trill_span,
        stop_trill_span=stop_trill_span,
    )
    return SpannerIndicatorCommand(
        left_broken=left_broken,
        map=map,
        right_broken=right_broken,
        selector=selector,
        start_indicator=start_trill_span_,
        stop_indicator=stop_trill_span,
        tags=[_tags.function_name(_frame())],
        tweaks=tweaks,
    )


def trill_spanner_function(
    leaves: typing.Sequence[abjad.Leaf],
    *tweaks: abjad.Tweak,
    alteration: str = None,
    harmonic: bool = False,
    start_trill_span: abjad.StartTrillSpan = None,
    stop_trill_span: abjad.StopTrillSpan = None,
    tags: list[abjad.Tag] = None,
) -> None:
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    start_trill_span_, stop_trill_span = _prepare_trill_spanner_arguments(
        alteration=alteration,
        harmonic=harmonic,
        start_trill_span=start_trill_span,
        stop_trill_span=stop_trill_span,
    )
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    _attach_start_stop_indicators(
        leaves,
        tag,
        start_indicator=start_trill_span_,
        stop_indicator=stop_trill_span,
    )
