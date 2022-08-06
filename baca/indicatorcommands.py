"""
Articulations.
"""
import collections
import copy
import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import command as _command
from . import indicatorclasses as _indicatorclasses
from . import overridecommands as _overridecommands
from . import select as _select
from . import tags as _tags
from . import treat as _treat
from . import tweaks as _tweaks
from . import typings as _typings
from .enums import enums as _enums


def _attach_persistent_indicator(
    argument,
    indicators,
    *,
    context=None,
    do_not_test=False,
    deactivate=False,
    direction=None,
    manifests=None,
    predicate=None,
    # TODO: remove tag keyword?
    tag=None,
) -> list[abjad.Wrapper]:
    assert isinstance(manifests, dict), repr(manifests)
    cyclic_indicators = abjad.CyclicTuple(indicators)
    # TODO: eventually uncomment following two lines:
    # for indicator in cyclic_indicators:
    #     assert getattr(indicator, "persistent", False) is True, repr(indicator)
    leaves = abjad.select.leaves(argument)
    tag_ = _tags.function_name(_frame())
    if tag is not None:
        tag_ = tag_.append(tag)
    wrappers = []
    for i, leaf in enumerate(leaves):
        if predicate and not predicate(leaf):
            continue
        indicators = cyclic_indicators[i]
        indicators = _token_to_indicators(indicators)
        for indicator in indicators:
            reapplied = _treat.remove_reapplied_wrappers(leaf, indicator)
            wrapper = abjad.attach(
                indicator,
                leaf,
                context=context,
                deactivate=deactivate,
                direction=direction,
                do_not_test=do_not_test,
                tag=tag_,
                wrapper=True,
            )
            if _treat.compare_persistent_indicators(indicator, reapplied):
                _treat.treat_persistent_wrapper(manifests, wrapper, "redundant")
            wrappers.append(wrapper)
    return wrappers


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


def _token_to_indicators(token):
    result = []
    if not isinstance(token, tuple | list):
        token = [token]
    for item in token:
        if item is None:
            continue
        result.append(item)
    return result


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


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class IndicatorCommand(_command.Command):

    indicators: typing.Sequence = ()
    context: str | None = None
    direction: abjad.Vertical | None = None
    do_not_test: bool = False
    predicate: typing.Callable | None = None
    redundant: bool = False

    def __post_init__(self):
        _command.Command.__post_init__(self)
        if self.context is not None:
            assert isinstance(self.context, str), repr(self.context)
        assert isinstance(self.do_not_test, bool), repr(self.do_not_test)
        assert isinstance(self.redundant, bool), repr(self.redundant)

    def __copy__(self, *arguments):
        result = dataclasses.replace(self)
        result.indicators = copy.deepcopy(self._indicators_coerced())
        return result

    __repr__ = _command.Command.__repr__

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self._indicators_coerced() is None:
            return False
        if self.redundant is True:
            return False
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return False
        _attach_persistent_indicator(
            argument,
            self._indicators_coerced(),
            context=self.context,
            do_not_test=self.do_not_test,
            deactivate=self.deactivate,
            direction=self.direction,
            manifests=runtime.get("manifests", {}),
            predicate=self.predicate,
            tag=self.tag,
        )
        return False

    def _indicators_coerced(self):
        indicators_ = None
        if self.indicators is not None:
            if isinstance(self.indicators, collections.abc.Iterable):
                indicators_ = abjad.CyclicTuple(self.indicators)
            else:
                indicators_ = abjad.CyclicTuple([self.indicators])
        return indicators_


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class InstrumentChangeCommand(IndicatorCommand):
    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.selector is not None:
            argument = self.selector(argument)
        if self._indicators_coerced() is None:
            return False
        return IndicatorCommand._call(self, argument=argument, runtime=runtime)


class SchemeManifest:
    """
    Scheme manifest.

    New functions defined in ``~/baca/lilypond/baca.ily`` must be added here.
    """

    _dynamics = (
        ("baca-appena-udibile", "appena udibile"),
        ("baca-f-but-accents-sffz", "f"),
        ("baca-f-sub-but-accents-continue-sffz", "f"),
        ("baca-ffp", "p"),
        ("baca-fffp", "p"),
        ("niente", "niente"),
        ("baca-p-sub-but-accents-continue-sffz", "p"),
        #
        ("baca-pppf", "f"),
        ("baca-pppff", "ff"),
        ("baca-pppfff", "fff"),
        #
        ("baca-ppf", "f"),
        ("baca-ppff", "ff"),
        ("baca-ppfff", "fff"),
        #
        ("baca-pf", "f"),
        ("baca-pff", "ff"),
        ("baca-pfff", "fff"),
        #
        ("baca-ppp-ppp", "ppp"),
        ("baca-ppp-pp", "pp"),
        ("baca-ppp-p", "p"),
        ("baca-ppp-mp", "mp"),
        ("baca-ppp-mf", "mf"),
        ("baca-ppp-f", "f"),
        ("baca-ppp-ff", "ff"),
        ("baca-ppp-fff", "fff"),
        #
        ("baca-pp-ppp", "ppp"),
        ("baca-pp-pp", "pp"),
        ("baca-pp-p", "p"),
        ("baca-pp-mp", "mp"),
        ("baca-pp-mf", "mf"),
        ("baca-pp-f", "f"),
        ("baca-pp-ff", "ff"),
        ("baca-pp-fff", "fff"),
        #
        ("baca-p-ppp", "ppp"),
        ("baca-p-pp", "pp"),
        ("baca-p-p", "p"),
        ("baca-p-mp", "mp"),
        ("baca-p-mf", "mf"),
        ("baca-p-f", "f"),
        ("baca-p-ff", "ff"),
        ("baca-p-fff", "fff"),
        #
        ("baca-mp-ppp", "ppp"),
        ("baca-mp-pp", "pp"),
        ("baca-mp-p", "p"),
        ("baca-mp-mp", "mp"),
        ("baca-mp-mf", "mf"),
        ("baca-mp-f", "f"),
        ("baca-mp-ff", "ff"),
        ("baca-mp-fff", "fff"),
        #
        ("baca-mf-ppp", "ppp"),
        ("baca-mf-pp", "pp"),
        ("baca-mf-p", "p"),
        ("baca-mf-mp", "mp"),
        ("baca-mf-mf", "mf"),
        ("baca-mf-f", "f"),
        ("baca-mf-ff", "ff"),
        ("baca-mf-fff", "fff"),
        #
        ("baca-f-ppp", "ppp"),
        ("baca-f-pp", "pp"),
        ("baca-f-p", "p"),
        ("baca-f-mp", "mp"),
        ("baca-f-mf", "mf"),
        ("baca-f-f", "f"),
        ("baca-f-ff", "ff"),
        ("baca-f-fff", "fff"),
        #
        ("baca-ff-ppp", "ppp"),
        ("baca-ff-pp", "pp"),
        ("baca-ff-p", "p"),
        ("baca-ff-mp", "mp"),
        ("baca-ff-mf", "mf"),
        ("baca-ff-f", "f"),
        ("baca-ff-ff", "ff"),
        ("baca-ff-fff", "fff"),
        #
        ("baca-fff-ppp", "ppp"),
        ("baca-fff-pp", "pp"),
        ("baca-fff-p", "p"),
        ("baca-fff-mp", "mp"),
        ("baca-fff-mf", "mf"),
        ("baca-fff-f", "f"),
        ("baca-fff-ff", "ff"),
        ("baca-fff-fff", "fff"),
        #
        ("baca-sff", "ff"),
        ("baca-sffp", "p"),
        ("baca-sffpp", "pp"),
        ("baca-sfffz", "fff"),
        ("baca-sffz", "ff"),
        ("baca-sfpp", "pp"),
        ("baca-sfz-f", "f"),
        ("baca-sfz-p", "p"),
    )

    @property
    def dynamics(self) -> list[str]:
        """
        Gets dynamics.

        ..  container:: example

            >>> scheme_manifest = baca.SchemeManifest()
            >>> for dynamic in scheme_manifest.dynamics:
            ...     dynamic
            ...
            'baca-appena-udibile'
            'baca-f-but-accents-sffz'
            'baca-f-sub-but-accents-continue-sffz'
            'baca-ffp'
            'baca-fffp'
            'niente'
            'baca-p-sub-but-accents-continue-sffz'
            'baca-pppf'
            'baca-pppff'
            'baca-pppfff'
            'baca-ppf'
            'baca-ppff'
            'baca-ppfff'
            'baca-pf'
            'baca-pff'
            'baca-pfff'
            'baca-ppp-ppp'
            'baca-ppp-pp'
            'baca-ppp-p'
            'baca-ppp-mp'
            'baca-ppp-mf'
            'baca-ppp-f'
            'baca-ppp-ff'
            'baca-ppp-fff'
            'baca-pp-ppp'
            'baca-pp-pp'
            'baca-pp-p'
            'baca-pp-mp'
            'baca-pp-mf'
            'baca-pp-f'
            'baca-pp-ff'
            'baca-pp-fff'
            'baca-p-ppp'
            'baca-p-pp'
            'baca-p-p'
            'baca-p-mp'
            'baca-p-mf'
            'baca-p-f'
            'baca-p-ff'
            'baca-p-fff'
            'baca-mp-ppp'
            'baca-mp-pp'
            'baca-mp-p'
            'baca-mp-mp'
            'baca-mp-mf'
            'baca-mp-f'
            'baca-mp-ff'
            'baca-mp-fff'
            'baca-mf-ppp'
            'baca-mf-pp'
            'baca-mf-p'
            'baca-mf-mp'
            'baca-mf-mf'
            'baca-mf-f'
            'baca-mf-ff'
            'baca-mf-fff'
            'baca-f-ppp'
            'baca-f-pp'
            'baca-f-p'
            'baca-f-mp'
            'baca-f-mf'
            'baca-f-f'
            'baca-f-ff'
            'baca-f-fff'
            'baca-ff-ppp'
            'baca-ff-pp'
            'baca-ff-p'
            'baca-ff-mp'
            'baca-ff-mf'
            'baca-ff-f'
            'baca-ff-ff'
            'baca-ff-fff'
            'baca-fff-ppp'
            'baca-fff-pp'
            'baca-fff-p'
            'baca-fff-mp'
            'baca-fff-mf'
            'baca-fff-f'
            'baca-fff-ff'
            'baca-fff-fff'
            'baca-sff'
            'baca-sffp'
            'baca-sffpp'
            'baca-sfffz'
            'baca-sffz'
            'baca-sfpp'
            'baca-sfz-f'
            'baca-sfz-p'

        """
        return [_[0] for _ in self._dynamics]

    def dynamic_to_steady_state(self, dynamic) -> str:
        """
        Changes ``dynamic`` to steady state.

        ..  container:: example

            >>> scheme_manifest = baca.SchemeManifest()
            >>> scheme_manifest.dynamic_to_steady_state("sfz-p")
            'p'

        """
        for dynamic_, steady_state in self._dynamics:
            if dynamic_ == dynamic:
                return steady_state
            if dynamic_ == "baca-" + dynamic:
                return steady_state
        raise KeyError(dynamic)


def accent(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
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


def allow_octaves(
    *, selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
) -> IndicatorCommand:
    return IndicatorCommand(indicators=[_enums.ALLOW_OCTAVE], selector=selector)


def alternate_bow_strokes(
    *tweaks: abjad.Tweak,
    downbow_first: bool = True,
    full: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    indicators = _prepare_alternate_bow_strokes(
        *tweaks, downbow_first=downbow_first, full=full
    )
    return IndicatorCommand(
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
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("arpeggio")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def articulation(
    articulation: str,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    articulation_ = abjad.Articulation(articulation)
    return IndicatorCommand(
        indicators=[articulation_],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def articulations(
    articulations: list,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=articulations,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def bar_line_function(
    argument,
    abbreviation: str = "|",
    *,
    site: str = "after",
):
    assert isinstance(abbreviation, str), repr(abbreviation)
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.BarLine(abbreviation, site=site)
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def breathe(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
) -> IndicatorCommand:
    indicator: abjad.LilyPondLiteral | abjad.Bundle
    indicator = abjad.LilyPondLiteral(r"\breathe", site="after")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
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


def clef(
    clef: str = "treble",
    *,
    redundant: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    indicator = abjad.Clef(clef)
    return IndicatorCommand(
        indicators=[indicator],
        redundant=redundant,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def clef_function(
    argument,
    clef: str,
) -> None:
    assert isinstance(clef, str), repr(clef)
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.Clef(clef)
        _attach_persistent_indicator(
            leaf,
            [indicator],
            manifests={},
            tag=tag,
        )


def close_volta_function(skip, first_measure_number, site: str = "before"):
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    assert isinstance(site, str), repr(site)
    after = site == "after"
    bar_line_function(skip, ":|.", site=site)
    tag = _tags.function_name(_frame())
    measure_number = abjad.get.measure_number(skip)
    measure_number += first_measure_number - 1
    if after is True:
        measure_number += 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    wrappers = _overridecommands.bar_line_x_extent([skip], (0, 1.5), after=after)
    _tags.wrappers(wrappers, tag, measure_number_tag, _tags.ONLY_MOL)


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


def cross_staff(
    *, selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\crossStaff")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def damp(
    *tweaks: abjad.Tweak,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    indicator: abjad.Articulation | abjad.Bundle
    indicator = abjad.Articulation("baca-damp")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_flageolet(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("baca-double-flageolet")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_staccato(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
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


def double_volta_function(skip, first_measure_number):
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    bar_line_function(skip, ":.|.:", site="before")
    tag = _tags.function_name(_frame())
    measure_number = abjad.get.measure_number(skip)
    measure_number += first_measure_number - 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    wrappers = _overridecommands.bar_line_x_extent([skip], (0, 3))
    _tags.wrappers(wrappers, tag, _tags.NOT_MOL, measure_number_tag)
    wrappers = _overridecommands.bar_line_x_extent([skip], (0, 4))
    _tags.wrappers(wrappers, tag, _tags.ONLY_MOL, measure_number_tag)


def down_arpeggio(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.DOWN)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def down_bow(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> IndicatorCommand:
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


def dynamic(
    dynamic: str | abjad.Dynamic,
    *tweaks: abjad.Tweak,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    redundant: bool = False,
) -> IndicatorCommand:
    if isinstance(dynamic, str):
        indicator = make_dynamic(dynamic)
    else:
        indicator = dynamic
    prototype = (abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin)
    assert isinstance(indicator, prototype), repr(indicator)
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        context="Voice",
        indicators=[indicator],
        map=map,
        match=match,
        measures=measures,
        redundant=redundant,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_function(
    argument,
    dynamic: str | abjad.Dynamic,
    *tweaks: abjad.Tweak,
) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        if isinstance(dynamic, str):
            indicator = make_dynamic(dynamic)
        else:
            indicator = dynamic
        prototype = (abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin)
        assert isinstance(indicator, prototype), repr(indicator)
        indicator = _tweaks.bundle_tweaks(indicator, tweaks)
        _attach_persistent_indicator(
            leaf,
            [indicator],
            manifests={},
            tag=tag,
        )


def dynamic_down(
    *, selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicDown")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_up(
    *, selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicUp")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def edition(
    not_parts: str | abjad.Markup | IndicatorCommand,
    only_parts: str | abjad.Markup | IndicatorCommand,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _command.Suite:
    """
    Makes not-parts / only-parts markup suite.
    """
    if isinstance(not_parts, str):
        not_parts = markup(rf"\markup {{ {not_parts} }}", selector=selector)
    elif isinstance(not_parts, abjad.Markup):
        not_parts = markup(not_parts, selector=selector)
    assert isinstance(not_parts, IndicatorCommand)
    not_parts_ = _command.not_parts(not_parts)
    if isinstance(only_parts, str):
        only_parts = markup(rf"\markup {{ {only_parts} }}", selector=selector)
    elif isinstance(only_parts, abjad.Markup):
        only_parts = markup(only_parts, selector=selector)
    assert isinstance(only_parts, IndicatorCommand)
    only_parts_ = _command.only_parts(only_parts)
    return _command.suite(not_parts_, only_parts_)


def espressivo(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
) -> IndicatorCommand:
    indicator: abjad.Articulation | abjad.Bundle
    indicator = abjad.Articulation("espressivo")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
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


def extend_beam(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(indicators=[_enums.RIGHT_BROKEN_BEAM], selector=selector)


def fermata(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("fermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def flageolet(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("flageolet")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def flageolet_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("flageolet")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def global_fermata_function(
    argument,
    description: str = "fermata",
) -> None:
    description_to_command = {
        "short": "shortfermata",
        "fermata": "fermata",
        "long": "longfermata",
        "very_long": "verylongfermata",
    }
    fermatas = description_to_command.keys()
    if description not in fermatas:
        message = f"must be in {repr(', '.join(fermatas))}:\n"
        message += f"   {repr(description)}"
        raise Exception(message)
    if isinstance(description, str) and description != "fermata":
        command = description.replace("_", "-")
        command = f"{command}-fermata"
    else:
        command = "fermata"
    if description == "short":
        fermata_duration = 1
    elif description == "fermata":
        fermata_duration = 2
    elif description == "long":
        fermata_duration = 4
    elif description == "very_long":
        fermata_duration = 8
    else:
        raise Exception(description)
    assert isinstance(command, str), repr(command)
    assert isinstance(fermata_duration, int), repr(fermata_duration)
    for leaf in abjad.select.leaves(argument):
        markup = abjad.Markup(rf"\baca-{command}-markup")
        abjad.attach(
            markup,
            leaf,
            direction=abjad.UP,
            tag=abjad.Tag("baca.global_fermata_function(1)"),
        )
        literal = abjad.LilyPondLiteral(r"\baca-fermata-measure")
        abjad.attach(
            literal,
            leaf,
            tag=abjad.Tag("baca.global_fermata_function(2)"),
        )
        abjad.attach(
            _enums.FERMATA_MEASURE,
            leaf,
            # TODO: remove enum tag?
            tag=_tags.FERMATA_MEASURE,
        )
        abjad.annotate(leaf, _enums.FERMATA_DURATION, fermata_duration)


def instrument(
    instrument: abjad.Instrument,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> InstrumentChangeCommand:
    assert isinstance(instrument, abjad.Instrument), repr(instrument)
    return InstrumentChangeCommand(
        indicators=[instrument],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def instrument_function(
    argument,
    instrument: abjad.Instrument,
    manifests: dict = None,
) -> None:
    assert isinstance(instrument, abjad.Instrument), repr(instrument)
    manifests = manifests or {}
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        _attach_persistent_indicator(
            leaf,
            [instrument],
            manifests=manifests,
            tag=tag,
        )


def instrument_name(
    string: str,
    *,
    context: str = "Staff",
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    assert isinstance(string, str), repr(string)
    assert string.startswith("\\"), repr(string)
    indicator = abjad.InstrumentName(string, context=context)
    command = IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame()), _tags.NOT_PARTS],
    )
    return command


def instrument_name_function(
    argument,
    string: str,
    *,
    context: str = "Staff",
) -> None:
    assert isinstance(string, str), repr(string)
    assert string.startswith("\\"), repr(string)
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.NOT_PARTS)
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.InstrumentName(string, context=context)
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def invisible_music(
    *,
    map=None,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _command.Suite:
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


def laissez_vibrer(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
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


def literal(
    string: str | list[str],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    site: str = "before",
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(string, site=site)
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def literal_function(
    argument,
    string: str | list[str],
    *,
    site: str = "before",
) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.LilyPondLiteral(string, site=site)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def long_fermata(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("longfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def make_dynamic(
    string: str, *, forbid_al_niente_to_bar_line: bool = False
) -> abjad.Dynamic | abjad.StartHairpin | abjad.StopHairpin | abjad.Bundle:
    r"""
    Makes dynamic.

    ..  container:: example

        >>> baca.make_dynamic("p")
        Dynamic(name='p', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("sffz")
        Dynamic(name='ff', command='\\baca-sffz', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=3)

        >>> baca.make_dynamic("niente")
        Dynamic(name='niente', command='\\!', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=NegativeInfinity())

        >>> baca.make_dynamic("<")
        StartHairpin(shape='<')

        >>> baca.make_dynamic("o<|")
        StartHairpin(shape='o<|')

        >>> baca.make_dynamic("appena-udibile")
        Dynamic(name='appena udibile', command='\\baca-appena-udibile', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=None)

    ..  container:: example

        Stop hairpin:

        >>> baca.make_dynamic("!")
        StopHairpin(leak=False)

    ..  container:: example

        Ancora dynamics:

        >>> baca.make_dynamic("p-ancora")
        Dynamic(name='p', command='\\baca-p-ancora', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-ancora")
        Dynamic(name='f', command='\\baca-f-ancora', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Composite dynamics:

        >>> baca.make_dynamic("pf")
        Dynamic(name='f', command='\\baca-pf', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=2)

        >>> baca.make_dynamic("pff")
        Dynamic(name='ff', command='\\baca-pff', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=3)

    ..  container:: example

        Effort dynamics:

        >>> baca.make_dynamic('"p"')
        Dynamic(name='"p"', command='\\baca-effort-p', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic('"f"')
        Dynamic(name='"f"', command='\\baca-effort-f', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Effort dynamics (parenthesized):

        >>> baca.make_dynamic('("p")')
        Dynamic(name='p', command='\\baca-effort-p-parenthesized', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic('("f")')
        Dynamic(name='f', command='\\baca-effort-f-parenthesized', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Effort dynamics (ancora):

        >>> baca.make_dynamic('"p"-ancora')
        Dynamic(name='p', command='\\baca-effort-ancora-p', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic('"f"-ancora')
        Dynamic(name='f', command='\\baca-effort-ancora-f', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Effort dynamics (sempre):

        >>> baca.make_dynamic('"p"-sempre')
        Dynamic(name='p', command='\\baca-effort-p-sempre', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic('"f"-sempre')
        Dynamic(name='f', command='\\baca-effort-f-sempre', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Sub. effort dynamics:

        >>> baca.make_dynamic("p-effort-sub")
        Dynamic(name='p', command='\\baca-p-effort-sub', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-effort-sub")
        Dynamic(name='f', command='\\baca-f-effort-sub', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Mezzo:

        >>> baca.make_dynamic("m")
        Dynamic(name='m', command='\\baca-m', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=None)

    ..  container:: example

        Parenthesized dynamics:

        >>> baca.make_dynamic("(p)")
        Dynamic(name='p', command='\\baca-p-parenthesized', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("(f)")
        Dynamic(name='f', command='\\baca-f-parenthesized', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Poco scratch dynamics:

        >>> baca.make_dynamic("p-poco-scratch")
        Dynamic(name='p', command='\\baca-p-poco-scratch', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-poco-scratch")
        Dynamic(name='f', command='\\baca-f-poco-scratch', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Possibile dynamics:

        >>> baca.make_dynamic("p-poss")
        Dynamic(name='p', command='\\baca-p-poss', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-poss")
        Dynamic(name='f', command='\\baca-f-poss', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Scratch dynamics:

        >>> baca.make_dynamic("p-scratch")
        Dynamic(name='p', command='\\baca-p-scratch', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-scratch")
        Dynamic(name='f', command='\\baca-f-scratch', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Sempre dynamics:

        >>> baca.make_dynamic("p-sempre")
        Dynamic(name='p', command='\\baca-p-sempre', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-sempre")
        Dynamic(name='f', command='\\baca-f-sempre', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Subito dynamics:

        >>> baca.make_dynamic("p-sub")
        Dynamic(name='p', command='\\baca-p-sub', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-sub")
        Dynamic(name='f', command='\\baca-f-sub', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Whiteout dynamics:

        >>> baca.make_dynamic("p-whiteout")
        Dynamic(name='p', command='\\baca-p-whiteout', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-whiteout")
        Dynamic(name='f', command='\\baca-f-whiteout', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Al niente hairpins are special-cased to carry to-barline tweaks:

        >>> baca.make_dynamic(">o")
        Bundle(indicator=StartHairpin(shape='>o'), tweaks=(Tweak(string='- \\tweak to-barline ##t', tag=None),))

        >>> baca.make_dynamic("|>o")
        Bundle(indicator=StartHairpin(shape='|>o'), tweaks=(Tweak(string='- \\tweak to-barline ##t', tag=None),))

    ..  container:: example exception

        Errors on nondynamic input:

        >>> baca.make_dynamic("text")
        Traceback (most recent call last):
            ...
        Exception: the string 'text' initializes no known dynamic.

    """
    assert isinstance(string, str), repr(string)
    scheme_manifest = SchemeManifest()
    known_shapes = abjad.StartHairpin("<").known_shapes
    indicator: abjad.Dynamic | abjad.StartHairpin | abjad.StopHairpin | abjad.Bundle
    if "_" in string:
        raise Exception(f"use hyphens instead of underscores ({string!r}).")
    if string == "niente":
        indicator = abjad.Dynamic("niente", command=r"\!")
    elif string.endswith("-ancora") and '"' not in string:
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-ancora"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-ancora") and '"' in string:
        dynamic = string.split("-")[0]
        dynamic = dynamic.strip('"')
        command = rf"\baca-effort-ancora-{dynamic}"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-effort-sub"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-effort-sub"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.startswith('("') and string.endswith('")'):
        dynamic = string.strip('(")')
        command = rf"\baca-effort-{dynamic}-parenthesized"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.startswith("(") and string.endswith(")"):
        dynamic = string.strip("()")
        command = rf"\baca-{dynamic}-parenthesized"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-poco-scratch"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-poco-scratch"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-poss"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-poss"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-scratch"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-scratch"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-sempre") and not string.startswith('"'):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-sempre"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-sempre") and string.startswith('"'):
        dynamic = string.split("-")[0].strip('"')
        command = rf"\baca-effort-{dynamic}-sempre"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-sub"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-sub"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-whiteout"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-whiteout"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif "baca-" + string in scheme_manifest.dynamics:
        name = scheme_manifest.dynamic_to_steady_state(string)
        command = "\\baca-" + string
        pieces = string.split("-")
        if pieces[0] in ("sfz", "sffz", "sfffz"):
            sforzando = True
        else:
            sforzando = False
        name_is_textual = not (sforzando)
        indicator = abjad.Dynamic(
            name,
            command=command,
            name_is_textual=name_is_textual,
        )
    elif string.startswith('"'):
        assert string.endswith('"')
        stripped_string = string.strip('"')
        command = rf"\baca-effort-{stripped_string}"
        indicator = abjad.Dynamic(f"{string}", command=command)
    elif string in known_shapes:
        indicator = abjad.StartHairpin(string)
        if string.endswith(">o") and not forbid_al_niente_to_bar_line:
            indicator = abjad.bundle(indicator, r"- \tweak to-barline ##t")
    elif string == "!":
        indicator = abjad.StopHairpin()
    elif string == "m":
        indicator = abjad.Dynamic("m", command=r"\baca-m")
    else:
        failed = False
        try:
            indicator = abjad.Dynamic(string)
        except Exception:
            failed = True
        if failed:
            raise Exception(f"the string {string!r} initializes no known dynamic.")
    prototype = (abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin, abjad.Bundle)
    assert isinstance(indicator, prototype), repr(indicator)
    return indicator


def marcato(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
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


def mark(
    argument: str,
    *tweaks: abjad.Tweak,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    assert isinstance(argument, abjad.Markup | str), repr(argument)
    rehearsal_mark = abjad.RehearsalMark(markup=argument)
    rehearsal_mark = _tweaks.bundle_tweaks(rehearsal_mark, tweaks)
    return IndicatorCommand(
        indicators=[rehearsal_mark],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def mark_function(
    argument,
    string: str,
    *tweaks: abjad.Tweak,
) -> None:
    assert isinstance(string, abjad.Markup | str), repr(string)
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        rehearsal_mark = abjad.RehearsalMark(markup=string)
        rehearsal_mark = _tweaks.bundle_tweaks(rehearsal_mark, tweaks)
        abjad.attach(
            rehearsal_mark,
            leaf,
            tag=tag,
        )


def markup(
    argument: str | abjad.Markup,
    *tweaks: abjad.Tweak,
    direction=abjad.UP,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
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
    return IndicatorCommand(
        direction=direction,
        indicators=[indicator],
        map=map,
        match=match,
        measures=measures,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def markup_function(
    argument,
    markup: str | abjad.Markup,
    *tweaks: abjad.Tweak,
    direction: abjad.Vertical = abjad.UP,
) -> list[abjad.Wrapper]:
    assert direction in (abjad.DOWN, abjad.UP), repr(direction)
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator: abjad.Markup | abjad.Bundle
        if isinstance(markup, str):
            indicator = abjad.Markup(markup)
        else:
            assert isinstance(markup, abjad.Markup), repr(markup)
            indicator = dataclasses.replace(markup)
        if tweaks:
            indicator = abjad.bundle(indicator, *tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            direction=direction,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def metronome_mark_function(
    argument,
    indicator,
    manifests,
) -> list[abjad.Wrapper]:
    prototype = (
        abjad.MetricModulation,
        abjad.MetronomeMark,
        _indicatorclasses.Accelerando,
        _indicatorclasses.Ritardando,
    )
    assert isinstance(indicator, prototype), repr(indicator)
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        wrappers_ = _attach_persistent_indicator(
            leaf,
            [indicator],
            manifests=manifests,
            tag=tag,
        )
        wrappers.extend(wrappers_)
    return wrappers


def one_voice(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\oneVoice")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def open_volta_function(skip, first_measure_number):
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    bar_line_function(skip, ".|:", site="before")
    tag = _tags.function_name(_frame())
    measure_number = abjad.get.measure_number(skip)
    measure_number += first_measure_number - 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    wrappers = _overridecommands.bar_line_x_extent([skip], (0, 2))
    _tags.wrappers(wrappers, tag, _tags.NOT_MOL, measure_number_tag)
    wrappers = _overridecommands.bar_line_x_extent([skip], (0, 3))
    _tags.wrappers(wrappers, tag, _tags.ONLY_MOL, measure_number_tag)


def parenthesize_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\parenthesize")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def quadruple_staccato(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #4")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def quadruple_staccato_function(argument) -> list[abjad.Wrapper]:
    wrappers = []
    tag = _tags.function_name(_frame())
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("baca-staccati #4")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def rehearsal_mark_function(
    argument,
    string: str,
    *tweaks: abjad.Tweak,
    font_size: int = 10,
) -> list[abjad.Wrapper]:
    assert isinstance(string, str), repr(string)
    assert isinstance(font_size, int | float), repr(font_size)
    string = rf'\baca-rehearsal-mark-markup "{string}" #{font_size}'
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator: abjad.Markup | abjad.Bundle
        indicator = abjad.Markup(string)
        indicator = _tweaks.bundle_tweaks(indicator, tweaks)
        tag = _tags.function_name(_frame())
        wrapper = abjad.attach(
            indicator,
            leaf,
            direction=abjad.CENTER,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def repeat_tie(selector, *, allow_rest: bool = False) -> IndicatorCommand:
    if allow_rest is not None:
        allow_rest = bool(allow_rest)
    return IndicatorCommand(
        do_not_test=allow_rest,
        indicators=[abjad.RepeatTie()],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def repeat_tie_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.RepeatTie()
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def short_fermata(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("shortfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def short_instrument_name(
    argument: str,
    *,
    alert: IndicatorCommand = None,
    context: str = "Staff",
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand | _command.Suite:
    if isinstance(argument, str):
        markup = abjad.Markup(argument)
        short_instrument_name = abjad.ShortInstrumentName(markup, context=context)
    elif isinstance(argument, abjad.Markup):
        markup = abjad.Markup(argument)
        short_instrument_name = abjad.ShortInstrumentName(markup, context=context)
    elif isinstance(argument, abjad.ShortInstrumentName):
        short_instrument_name = dataclasses.replace(argument, context=context)
    else:
        raise TypeError(argument)
    assert isinstance(short_instrument_name, abjad.ShortInstrumentName)
    command = IndicatorCommand(
        indicators=[short_instrument_name],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )
    if bool(alert):
        assert isinstance(alert, IndicatorCommand), repr(alert)
        return _command.suite(command, alert)
    else:
        return command


def short_instrument_name_function(
    argument,
    short_instrument_name: abjad.ShortInstrumentName,
    manifests: dict = None,
    *,
    context: str = "Staff",
) -> None:
    assert isinstance(short_instrument_name, abjad.ShortInstrumentName), repr(
        short_instrument_name
    )
    manifests = manifests or {}
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.NOT_PARTS)
    for leaf in abjad.select.leaves(argument):
        _attach_persistent_indicator(
            leaf,
            [short_instrument_name],
            manifests=manifests,
            tag=tag,
        )


def snap_pizzicato(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("snappizzicato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccatissimo(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
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
) -> IndicatorCommand:
    return IndicatorCommand(
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


def staff_lines(
    n: int,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _command.Suite:
    command_1 = IndicatorCommand(
        indicators=[_indicatorclasses.BarExtent(n)],
        selector=selector,
        tags=[_tags.function_name(_frame(), n=1), _tags.NOT_PARTS],
    )
    command_2 = IndicatorCommand(
        indicators=[_indicatorclasses.StaffLines(n)],
        selector=selector,
        tags=[_tags.function_name(_frame(), n=2)],
    )
    return _command.suite(command_1, command_2)


def staff_lines_function(argument, n: int) -> None:
    assert isinstance(n, int), repr(n)
    for leaf in abjad.select.leaves(argument):
        bar_extent = _indicatorclasses.BarExtent(n)
        _attach_persistent_indicator(
            leaf,
            [bar_extent],
            manifests={},
            tag=abjad.Tag("baca.staff_lines_function(1)").append(_tags.NOT_PARTS),
        )
        staff_lines = _indicatorclasses.StaffLines(n)
        _attach_persistent_indicator(
            leaf,
            [staff_lines],
            manifests={},
            tag=abjad.Tag("baca.staff_lines_function(2)"),
        )


def stem_tremolo(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    *,
    tremolo_flags: int = 32,
) -> IndicatorCommand:
    return IndicatorCommand(
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
) -> IndicatorCommand:
    articulation = abjad.Articulation("baca-stop-on-string")
    return IndicatorCommand(
        indicators=[articulation],
        map=map,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stop_trill(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches stop trill to closing-slot.

    The closing format slot is important because LilyPond fails to compile when
    ``\stopTrillSpan`` appears after ``\set instrumentName`` accumulator (and
    probably other ``\set`` accumulator). Setting format slot to closing here
    positions ``\stopTrillSpan`` after the leaf in question (which is required)
    and also draws ``\stopTrillSpan`` closer to the leaf in question, prior to
    ``\set instrumentName`` and other accumulator positioned in the after slot.

    Eventually it will probably be necessary to model ``\stopTrillSpan`` with a
    dedicated format slot.
    """
    return literal(r"\stopTrillSpan", site="closing", selector=selector)


def stopped(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("stopped")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def tenuto(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
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


def tie(
    *, selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Tie()],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def tie_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.Tie()
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def triple_staccato(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #3")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def up_arpeggio(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.UP)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def up_bow(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> IndicatorCommand:
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
    )


def very_long_fermata(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("verylongfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_four(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\voiceFour")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_one(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\voiceOne")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_three(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\voiceThree")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_two(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\voiceTwo")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )
