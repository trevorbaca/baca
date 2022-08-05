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
from .enums import enums as _enums


def _attach_indicator(
    indicator, leaf, *, deactivate=None, direction=None, manifests=None, tag=None
):
    assert isinstance(tag, abjad.Tag), repr(tag)
    reapplied = _treat.remove_reapplied_wrappers(leaf, indicator)
    tag_ = tag
    wrapper = abjad.attach(
        indicator,
        leaf,
        deactivate=deactivate,
        direction=direction,
        tag=tag_,
        wrapper=True,
    )
    if _treat.compare_persistent_indicators(indicator, reapplied):
        status = "redundant"
        _treat.treat_persistent_wrapper(manifests, wrapper, status)
    return wrapper


def _do_spanner_indicator_command(
    argument,
    start_indicator,
    stop_indicator,
    *tweaks,
    deactivate=False,
    detach_first=False,
    direction=None,
    left_broken=False,
    manifests=None,
    right_broken=False,
) -> list[abjad.Wrapper]:
    manifests = manifests or {}
    wrappers = []
    if start_indicator is not None:
        if detach_first:
            for leaf in abjad.iterate.leaves(argument, grace=False):
                abjad.detach(type(start_indicator), leaf)
        start_indicator = _tweaks.bundle_tweaks(start_indicator, tweaks)
        first_leaf = abjad.select.leaf(argument, 0)
        if left_broken:
            wrapper = _attach_indicator(
                start_indicator,
                first_leaf,
                deactivate=deactivate,
                direction=direction,
                manifests=manifests,
                tag=_tags.function_name(_frame(), n=1)
                .append(_tags.SPANNER_START)
                .append(_tags.LEFT_BROKEN),
            )
            wrappers.append(wrapper)
        else:
            wrapper = _attach_indicator(
                start_indicator,
                first_leaf,
                deactivate=deactivate,
                direction=direction,
                manifests=manifests,
                tag=_tags.function_name(_frame(), n=2).append(_tags.SPANNER_START),
            )
            wrappers.append(wrapper)
    if stop_indicator is not None:
        if detach_first:
            for leaf in abjad.iterate.leaves(argument, grace=False):
                abjad.detach(type(stop_indicator), leaf)
        final_leaf = abjad.select.leaf(argument, -1)
        if right_broken:
            wrapper = _attach_indicator(
                stop_indicator,
                final_leaf,
                deactivate=deactivate,
                direction=direction,
                manifests=manifests,
                tag=_tags.function_name(_frame(), n=3)
                .append(_tags.SPANNER_STOP)
                .append(_tags.RIGHT_BROKEN),
            )
            wrappers.append(wrapper)
        else:
            wrapper = _attach_indicator(
                stop_indicator,
                final_leaf,
                deactivate=deactivate,
                direction=direction,
                manifests=manifests,
                tag=_tags.function_name(_frame(), n=4).append(_tags.SPANNER_STOP),
            )
            wrappers.append(wrapper)
    return wrappers


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
            manifests=runtime.get("manifests", {}),
            right_broken=self.right_broken,
        )
        return False


def beam(
    *tweaks: abjad.Tweak,
    direction: abjad.Vertical | None = None,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
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
) -> list[abjad.Wrapper]:
    # TODO: remove tleaves
    leaves = _select.tleaves(argument)
    start_beam = start_beam or abjad.StartBeam()
    stop_beam = stop_beam or abjad.StopBeam()
    assert isinstance(start_beam, abjad.StartBeam), repr(start_beam)
    assert isinstance(stop_beam, abjad.StopBeam), repr(stop_beam)
    start_beam = _tweaks.bundle_tweaks(start_beam, tweaks)
    wrappers = _do_spanner_indicator_command(
        leaves,
        start_beam,
        stop_beam,
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
    # TODO: remove allow_rests keyword
    allow_rests: bool = False,
    start_ottava: abjad.Ottava = abjad.Ottava(n=1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, site="after"),
    right_broken: bool = False,
) -> list[abjad.Wrapper]:
    # TODO: remove tleaves
    if not allow_rests:
        leaves = _select.tleaves(leaves)
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    assert isinstance(start_ottava, abjad.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, abjad.Ottava), repr(stop_ottava)
    return _do_spanner_indicator_command(
        leaves,
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
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[_tags.function_name(_frame())],
    )


def ottava_bassa_function(
    leaves: typing.Sequence[abjad.Leaf],
    *,
    # TODO: remove allow_rests
    allow_rests: bool = False,
    start_ottava: abjad.Ottava = abjad.Ottava(n=-1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, site="after"),
    right_broken: bool = False,
) -> list[abjad.Wrapper]:
    # TODO: remove tleaves
    if not allow_rests:
        leaves = _select.pleaves(leaves)
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    assert isinstance(start_ottava, abjad.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, abjad.Ottava), repr(stop_ottava)
    wrappers = _do_spanner_indicator_command(
        leaves,
        start_ottava,
        stop_ottava,
        right_broken=right_broken,
    )
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def slur(
    *tweaks: abjad.Tweak,
    map=None,
    phrasing_slur=False,
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
    leaves: typing.Sequence[abjad.Leaf],
    *tweaks: abjad.Tweak,
    phrasing_slur: bool = False,
    start_slur: abjad.StartSlur = None,
    stop_slur: abjad.StopSlur = None,
) -> list[abjad.Wrapper]:
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    if phrasing_slur is True:
        start_slur_ = start_slur or abjad.StartPhrasingSlur()
        stop_slur_ = stop_slur or abjad.StopPhrasingSlur()
    else:
        start_slur_ = start_slur or abjad.StartSlur()
        stop_slur_ = stop_slur or abjad.StopSlur()
    start_slur_ = _tweaks.bundle_tweaks(start_slur_, tweaks)
    stop_slur_ = _tweaks.bundle_tweaks(stop_slur_, tweaks)
    wrappers = _do_spanner_indicator_command(
        leaves,
        start_slur_,
        stop_slur_,
    )
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def sustain_pedal(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
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


def sustain_pedal_function(
    argument,
    *,
    start_piano_pedal: abjad.StartPianoPedal = None,
    stop_piano_pedal: abjad.StopPianoPedal = None,
) -> list[abjad.Wrapper]:
    start_piano_pedal = start_piano_pedal or abjad.StartPianoPedal()
    stop_piano_pedal = stop_piano_pedal or abjad.StopPianoPedal()
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
    map=None,
    right_broken: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
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


# TODO: change 'leaves' to 'argument'
def trill_spanner_function(
    leaves: typing.Sequence[abjad.Leaf],
    *tweaks: abjad.Tweak,
    alteration: str = None,
    harmonic: bool = False,
    start_trill_span: abjad.StartTrillSpan = None,
    stop_trill_span: abjad.StopTrillSpan = None,
) -> list[abjad.Wrapper]:
    start_trill_span_, stop_trill_span = _prepare_trill_spanner_arguments(
        alteration=alteration,
        harmonic=harmonic,
        start_trill_span=start_trill_span,
        stop_trill_span=stop_trill_span,
    )
    start_trill_span_ = _tweaks.bundle_tweaks(start_trill_span_, tweaks)
    wrappers = _do_spanner_indicator_command(
        leaves,
        start_trill_span_,
        stop_trill_span,
    )
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers
