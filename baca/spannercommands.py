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
from . import tweaks as _tweaks
from . import typings as _typings
from .enums import enums as _enums


# TODO: remove deactivate (after migration)
# TODO: remove detach_first
def _do_spanner_indicator_command(
    argument,
    start_indicator,
    stop_indicator,
    *tweaks,
    deactivate: bool = False,
    detach_first: bool = False,
    direction: abjad.Vertical | None = None,
    left_broken: bool = False,
    right_broken: bool = False,
) -> list[abjad.Wrapper]:
    wrappers = []
    if start_indicator is not None:
        start_indicator = _tweaks.bundle_tweaks(start_indicator, tweaks)
        tag = _tags.function_name(_frame(), n=1)
        tag = tag.append(_tags.SPANNER_START)
        if left_broken:
            tag = tag.append(_tags.LEFT_BROKEN)
        if detach_first:
            for leaf in abjad.iterate.leaves(argument, grace=False):
                abjad.detach(type(start_indicator), leaf)
        first_leaf = abjad.select.leaf(argument, 0)
        wrapper = abjad.attach(
            start_indicator,
            first_leaf,
            deactivate=deactivate,
            direction=direction,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    if stop_indicator is not None:
        tag = _tags.function_name(_frame(), n=2)
        tag = tag.append(_tags.SPANNER_STOP)
        if right_broken:
            tag = tag.append(_tags.RIGHT_BROKEN)
        if detach_first:
            for leaf in abjad.iterate.leaves(argument, grace=False):
                abjad.detach(type(stop_indicator), leaf)
        final_leaf = abjad.select.leaf(argument, -1)
        wrapper = abjad.attach(
            stop_indicator,
            final_leaf,
            deactivate=deactivate,
            direction=direction,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def _prepare_start_trill_span(
    *,
    alteration,
    harmonic,
    start_trill_span,
):
    assert isinstance(start_trill_span, abjad.StartTrillSpan), repr(start_trill_span)
    interval = pitch = None
    if alteration is not None:
        prototype = (abjad.NamedPitch, abjad.NamedInterval, str)
        assert isinstance(alteration, prototype), repr(alteration)
        try:
            pitch = abjad.NamedPitch(alteration)
        except Exception:
            pass
        try:
            interval = abjad.NamedInterval(alteration)
        except Exception:
            pass
    start_trill_span_: abjad.StartTrillSpan | abjad.Bundle
    start_trill_span_ = start_trill_span
    if pitch is not None or interval is not None:
        start_trill_span_ = dataclasses.replace(
            start_trill_span_, interval=interval, pitch=pitch
        )
    if harmonic is True:
        string = "#(lambda (grob) (grob-interpret-markup grob"
        string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
        string = rf"- \tweak TrillPitchHead.stencil {string}"
        start_trill_span_ = abjad.bundle(start_trill_span_, string)
    return start_trill_span_


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
        _do_spanner_indicator_command(
            argument,
            self.start_indicator,
            self.stop_indicator,
            *self.tweaks,
            deactivate=self.deactivate,
            detach_first=self.detach_first,
            direction=self.direction,
            left_broken=self.left_broken,
            right_broken=self.right_broken,
        )
        return False


def beam(
    *tweaks: abjad.Tweak,
    direction: abjad.Vertical | None = None,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    start_beam: abjad.StartBeam = abjad.StartBeam(),
    stop_beam: abjad.StopBeam = abjad.StopBeam(),
) -> SpannerIndicatorCommand:
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
    start_beam: abjad.StartBeam = abjad.StartBeam(),
    stop_beam: abjad.StopBeam = abjad.StopBeam(),
) -> list[abjad.Wrapper]:
    assert isinstance(start_beam, abjad.StartBeam), repr(start_beam)
    assert isinstance(stop_beam, abjad.StopBeam), repr(stop_beam)
    wrappers = _do_spanner_indicator_command(
        argument,
        start_beam,
        stop_beam,
        *tweaks,
        detach_first=True,
        direction=direction,
    )
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def ottava(
    start_ottava: abjad.Ottava = abjad.Ottava(n=1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, site="after"),
    *,
    right_broken: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> SpannerIndicatorCommand:
    assert isinstance(start_ottava, abjad.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, abjad.Ottava), repr(stop_ottava)
    return SpannerIndicatorCommand(
        right_broken=right_broken,
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[_tags.function_name(_frame())],
    )


def ottava_function(
    argument,
    *,
    start_ottava: abjad.Ottava = abjad.Ottava(n=1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, site="after"),
    right_broken: bool = False,
) -> list[abjad.Wrapper]:
    assert isinstance(start_ottava, abjad.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, abjad.Ottava), repr(stop_ottava)
    return _do_spanner_indicator_command(
        argument,
        start_ottava,
        stop_ottava,
        right_broken=right_broken,
    )


def ottava_bassa(
    start_ottava: abjad.Ottava = abjad.Ottava(n=-1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, site="after"),
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> SpannerIndicatorCommand:
    assert isinstance(start_ottava, abjad.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, abjad.Ottava), repr(stop_ottava)
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[_tags.function_name(_frame())],
    )


def ottava_bassa_function(
    argument,
    *,
    start_ottava: abjad.Ottava = abjad.Ottava(n=-1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, site="after"),
    right_broken: bool = False,
) -> list[abjad.Wrapper]:
    assert isinstance(start_ottava, abjad.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, abjad.Ottava), repr(stop_ottava)
    wrappers = _do_spanner_indicator_command(
        argument,
        start_ottava,
        stop_ottava,
        right_broken=right_broken,
    )
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def slur(
    *tweaks: abjad.Tweak,
    map: typing.Callable = None,
    phrasing_slur: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
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
    argument,
    *tweaks: abjad.Tweak,
    phrasing_slur: bool = False,
    start_slur: abjad.StartSlur = None,
    stop_slur: abjad.StopSlur = None,
) -> list[abjad.Wrapper]:
    if phrasing_slur is True:
        start_slur_ = start_slur or abjad.StartPhrasingSlur()
        stop_slur_ = stop_slur or abjad.StopPhrasingSlur()
    else:
        start_slur_ = start_slur or abjad.StartSlur()
        stop_slur_ = stop_slur or abjad.StopSlur()
    wrappers = _do_spanner_indicator_command(
        argument,
        start_slur_,
        stop_slur_,
        *tweaks,
    )
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def sustain_pedal(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    start_piano_pedal: abjad.StartPianoPedal = abjad.StartPianoPedal(),
    stop_piano_pedal: abjad.StopPianoPedal = abjad.StopPianoPedal(),
) -> SpannerIndicatorCommand:
    assert isinstance(start_piano_pedal, abjad.StartPianoPedal), repr(start_piano_pedal)
    assert isinstance(stop_piano_pedal, abjad.StopPianoPedal), repr(stop_piano_pedal)
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_piano_pedal,
        stop_indicator=stop_piano_pedal,
        tags=[_tags.function_name(_frame())],
    )


def sustain_pedal_function(
    argument,
    *,
    start_piano_pedal: abjad.StartPianoPedal = abjad.StartPianoPedal(),
    stop_piano_pedal: abjad.StopPianoPedal = abjad.StopPianoPedal(),
) -> list[abjad.Wrapper]:
    assert isinstance(start_piano_pedal, abjad.StartPianoPedal), repr(start_piano_pedal)
    assert isinstance(stop_piano_pedal, abjad.StopPianoPedal), repr(stop_piano_pedal)
    wrappers = _do_spanner_indicator_command(
        argument,
        start_piano_pedal,
        stop_piano_pedal,
    )
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def trill_spanner(
    *tweaks: abjad.Tweak,
    alteration: str = None,
    harmonic: bool = False,
    left_broken: bool = False,
    map: typing.Callable = None,
    right_broken: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    start_trill_span: abjad.StartTrillSpan = abjad.StartTrillSpan(),
    stop_trill_span: abjad.StopTrillSpan = abjad.StopTrillSpan(),
) -> SpannerIndicatorCommand:
    start_trill_span_ = _prepare_start_trill_span(
        alteration=alteration,
        harmonic=harmonic,
        start_trill_span=start_trill_span,
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
    argument,
    *tweaks: abjad.Tweak,
    alteration: str = None,
    harmonic: bool = False,
    start_trill_span: abjad.StartTrillSpan = abjad.StartTrillSpan(),
    stop_trill_span: abjad.StopTrillSpan = abjad.StopTrillSpan(),
) -> list[abjad.Wrapper]:
    start_trill_span_ = _prepare_start_trill_span(
        alteration=alteration,
        harmonic=harmonic,
        start_trill_span=start_trill_span,
    )
    wrappers = _do_spanner_indicator_command(
        argument,
        start_trill_span_,
        stop_trill_span,
        *tweaks,
    )
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers
