"""
Articulations.
"""
import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import command as _command
from . import commands as _commands
from . import select as _select
from . import tags as _tags
from . import tweaks as _tweaks
from . import typings as _typings
from .enums import enums as _enums


def _do_color_fingering_command(argument, numbers, *, direction=abjad.UP, tweaks=None):
    pheads = _select.pheads(argument)
    total = len(pheads)
    numbers = abjad.CyclicTuple(numbers)
    for i, phead in enumerate(pheads):
        number = numbers[i]
        if number != 0:
            fingering = abjad.ColorFingering(number)
            fingering = _tweaks.bundle_tweaks(fingering, tweaks, i=i, total=total)
            abjad.attach(fingering, phead, direction=direction)


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


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ColorFingeringCommand(_command.Command):

    direction: abjad.Vertical | None = abjad.UP
    numbers: typing.Sequence[int] = ()
    tweaks: tuple[_typings.IndexedTweak, ...] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert abjad.math.all_are_nonnegative_integers(self.numbers)
        _tweaks.validate_indexed_tweaks(self.tweaks)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.numbers:
            return False
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return False
        _do_color_fingering_command(
            argument, self.numbers, direction=self.direction, tweaks=self.tweaks
        )
        return False


def accent(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation(">")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def accent_function(argument) -> None:
    tag = _tags.function_name(_frame())
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
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
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
) -> None:
    pass
    tag = _tags.function_name(_frame())
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


def arpeggio(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("arpeggio")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def articulation(
    articulation: str,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    articulation_ = abjad.Articulation(articulation)
    return _commands.IndicatorCommand(
        indicators=[articulation_],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def articulations(
    articulations: list,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=articulations,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def breathe(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
) -> _commands.IndicatorCommand:
    indicator: abjad.LilyPondLiteral | abjad.Bundle
    indicator = abjad.LilyPondLiteral(r"\breathe", site="after")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return _commands.IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def breathe_function(
    argument,
    *tweaks: abjad.Tweak,
) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator: abjad.LilyPondLiteral | abjad.Bundle
        indicator = abjad.LilyPondLiteral(r"\breathe", site="after")
        indicator = _tweaks.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def color_fingerings(
    numbers: list[int],
    *tweaks: _typings.IndexedTweak,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> ColorFingeringCommand:
    return ColorFingeringCommand(numbers=numbers, selector=selector, tweaks=tweaks)


def color_fingerings_function(
    argument,
    numbers: list[int],
    *tweaks: _typings.IndexedTweak,
) -> None:
    _do_color_fingering_command(argument, numbers, tweaks=tweaks)


def damp(
    *tweaks: abjad.Tweak,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    indicator: abjad.Articulation | abjad.Bundle
    indicator = abjad.Articulation("baca-damp")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return _commands.IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_flageolet(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("baca-double-flageolet")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_staccato(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #2")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_staccato_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("baca-staccati #2")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def down_arpeggio(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.DOWN)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def down_bow(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> _commands.IndicatorCommand:
    indicator: abjad.Articulation | abjad.Bundle
    if full:
        indicator = abjad.Articulation("baca-full-downbow")
    else:
        indicator = abjad.Articulation("downbow")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return _commands.IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def down_bow_function(
    leaf: abjad.Leaf,
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> None:
    assert isinstance(leaf, abjad.Leaf), repr(leaf)
    indicator: abjad.Articulation | abjad.Bundle
    if full:
        indicator = abjad.Articulation("baca-full-downbow")
    else:
        indicator = abjad.Articulation("downbow")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    tag = _tags.function_name(_frame())
    abjad.attach(
        indicator,
        leaf,
        tag=tag,
    )


def espressivo(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
) -> _commands.IndicatorCommand:
    indicator: abjad.Articulation | abjad.Bundle
    indicator = abjad.Articulation("espressivo")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return _commands.IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def espressivo_function(
    argument,
    *tweaks: abjad.Tweak,
) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator: abjad.Articulation | abjad.Bundle
        indicator = abjad.Articulation("espressivo")
        indicator = _tweaks.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def fermata(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("fermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def flageolet(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("flageolet")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def laissez_vibrer(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.LaissezVibrer()],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def laissez_vibrer_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LaissezVibrer()
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def long_fermata(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("longfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def marcato(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("marcato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def marcato_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("marcato")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def quadruple_staccato(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #4")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def short_fermata(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("shortfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def snap_pizzicato(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("snappizzicato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccatissimo(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("staccatissimo")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccatissimo_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("staccatissimo")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def staccato(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("staccato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccato_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("staccato")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def stem_tremolo(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    *,
    tremolo_flags: int = 32,
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.StemTremolo(tremolo_flags=tremolo_flags)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stem_tremolo_function(
    argument,
    *,
    tremolo_flags: int = 32,
) -> list[abjad.Wrapper]:
    wrappers = []
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.StemTremolo(tremolo_flags=tremolo_flags)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def stop_on_string(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    *,
    map=None,
) -> _commands.IndicatorCommand:
    articulation = abjad.Articulation("baca-stop-on-string")
    return _commands.IndicatorCommand(
        indicators=[articulation],
        map=map,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stopped(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("stopped")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def tenuto(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("tenuto")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def tenuto_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("tenuto")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def triple_staccato(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #3")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def up_arpeggio(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.UP)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def up_bow(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> _commands.IndicatorCommand:
    indicator: abjad.Articulation | abjad.Bundle
    if full:
        indicator = abjad.Articulation("baca-full-upbow")
    else:
        indicator = abjad.Articulation("upbow")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return _commands.IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def very_long_fermata(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("verylongfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )
