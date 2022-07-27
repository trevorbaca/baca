import typing
from inspect import currentframe as _frame

import abjad

from . import commands as _commands
from . import select as _select
from . import tags as _tags
from . import tweaks as _tweaks
from .enums import enums as _enums


def _prepare_alternate_bow_strokes(*tweaks, downbow_first, full):
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
    return indicators


def accent(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation(">")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def accent_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    tag = abjad.Tag("baca.accent()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("accent")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def alternate_bow_strokes(
    *tweaks: abjad.Tweak,
    downbow_first: bool = True,
    full: bool = False,
    selector: typing.Callable = lambda _: _select.pheads(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    indicators = _prepare_alternate_bow_strokes(
        *tweaks, downbow_first=downbow_first, full=full
    )
    return _commands.IndicatorCommand(
        indicators=indicators,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def alternate_bow_strokes_function(
    argument,
    *tweaks: abjad.Tweak,
    downbow_first: bool = True,
    full: bool = False,
    tags: list[abjad.Tag] = None,
) -> None:
    pass
    tag = abjad.Tag("baca.alternate_bow_strokes()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    indicators = _prepare_alternate_bow_strokes(
        *tweaks, downbow_first=downbow_first, full=full
    )
    indicators = abjad.CyclicTuple(indicators)
    leaves = abjad.select.leaves(argument)
    for i, leaf in enumerate(leaves):
        indicator = indicators[i]
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def staccato(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("staccato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccato_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    tag = abjad.Tag("baca.staccato()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("staccato")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )
