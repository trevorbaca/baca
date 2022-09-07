"""
Articulations.
"""
import dataclasses
from inspect import currentframe as _frame

import abjad

from . import dynamics as _dynamics
from . import indicatorclasses as _indicatorclasses
from . import overridecommands as _overridecommands
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
    deactivate=False,
    direction=None,
    manifests=None,
    tag=None,
) -> list[abjad.Wrapper]:
    manifests = manifests or {}
    assert isinstance(manifests, dict), repr(manifests)
    cyclic_indicators = abjad.CyclicTuple(indicators)
    tag_ = _tags.function_name(_frame())
    if tag is not None:
        tag_ = tag_.append(tag)
    wrappers = []
    leaves = abjad.select.leaves(argument)
    for i, leaf in enumerate(leaves):
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
                tag=tag_,
                wrapper=True,
            )
            if _treat.compare_persistent_indicators(indicator, reapplied):
                _treat.treat_persistent_wrapper(manifests, wrapper, "redundant")
            wrappers.append(wrapper)
    return wrappers


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


def accent_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("accent")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def alternate_bow_strokes_function(
    argument,
    *tweaks: abjad.Tweak,
    downbow_first: bool = True,
    full: bool = False,
) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    indicators = _prepare_alternate_bow_strokes(
        *tweaks, downbow_first=downbow_first, full=full
    )
    indicators = abjad.CyclicTuple(indicators)
    leaves = abjad.select.leaves(argument)
    wrappers = []
    for i, leaf in enumerate(leaves):
        indicator = indicators[i]
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def arpeggio_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("arpeggio")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def articulation_function(argument, string: str) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation(string)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def articulations_function(argument, articulations: list) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    leaves = abjad.iterate.leaves(argument)
    cyclic_articulations = abjad.CyclicTuple(articulations)
    for i, leaf in enumerate(leaves):
        indicator = cyclic_articulations[i]
        if indicator is not None:
            wrapper = abjad.attach(
                indicator,
                leaf,
                tag=tag,
                wrapper=True,
            )
            wrappers.append(wrapper)
    return wrappers


def bar_line_function(
    argument, abbreviation: str = "|", *, site: str = "after"
) -> list[abjad.Wrapper]:
    assert isinstance(abbreviation, str), repr(abbreviation)
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.BarLine(abbreviation, site=site)
        wrapper = abjad.attach(indicator, leaf, tag=tag, wrapper=True)
        wrappers.append(wrapper)
    return wrappers


def breathe_function(argument, *tweaks: abjad.Tweak) -> list[abjad.Wrapper]:
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


def clef_function(argument, clef: str) -> list[abjad.Wrapper]:
    assert isinstance(clef, str), repr(clef)
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.Clef(clef)
        wrappers_ = _attach_persistent_indicator(
            leaf,
            [indicator],
            tag=tag,
        )
        wrappers.extend(wrappers_)
    return wrappers


def close_volta_function(
    skip, first_measure_number, site: str = "before"
) -> list[abjad.Wrapper]:
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    assert isinstance(site, str), repr(site)
    wrappers = []
    after = site == "after"
    wrappers_ = bar_line_function(skip, ":|.", site=site)
    wrappers.extend(wrappers_)
    tag = _tags.function_name(_frame())
    measure_number = abjad.get.measure_number(skip)
    measure_number += first_measure_number - 1
    if after is True:
        measure_number += 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    wrappers_ = _overridecommands.bar_line_x_extent([skip], (0, 1.5), after=after)
    _tags.wrappers(wrappers_, tag, measure_number_tag, _tags.ONLY_MOL)
    wrappers.extend(wrappers_)
    return wrappers


def color_fingerings_function(
    argument,
    numbers: list[int],
    *tweaks: _typings.IndexedTweak,
) -> list[abjad.Wrapper]:
    cyclic_numbers = abjad.CyclicTuple(numbers)
    wrappers = []
    leaves = abjad.select.leaves(argument)
    total = len(leaves)
    for i, leaf in enumerate(leaves):
        number = cyclic_numbers[i]
        if number != 0:
            fingering = abjad.ColorFingering(number)
            fingering = _tweaks.bundle_tweaks(fingering, tweaks, i=i, total=total)
            wrapper = abjad.attach(fingering, leaf, direction=abjad.UP, wrapper=True)
            wrappers.append(wrapper)
    return wrappers


def cross_staff_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\crossStaff")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def damp_function(argument, *tweaks: abjad.Tweak) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator: abjad.Articulation | abjad.Bundle
        indicator = abjad.Articulation("baca-damp")
        indicator = _tweaks.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def double_flageolet_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("baca-double-flageolet")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def double_staccato_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("baca-staccati #2")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def double_volta_function(skip, first_measure_number) -> list[abjad.Wrapper]:
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    wrappers = []
    wrappers_ = bar_line_function(skip, ":.|.:", site="before")
    wrappers.extend(wrappers_)
    tag = _tags.function_name(_frame())
    measure_number = abjad.get.measure_number(skip)
    measure_number += first_measure_number - 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    wrappers_ = _overridecommands.bar_line_x_extent([skip], (0, 3))
    _tags.wrappers(wrappers_, tag, _tags.NOT_MOL, measure_number_tag)
    wrappers.extend(wrappers_)
    wrappers_ = _overridecommands.bar_line_x_extent([skip], (0, 4))
    _tags.wrappers(wrappers_, tag, _tags.ONLY_MOL, measure_number_tag)
    wrappers.extend(wrappers_)
    return wrappers


def down_arpeggio_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Arpeggio(direction=abjad.DOWN)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def down_bow_function(
    argument,
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator: abjad.Articulation | abjad.Bundle
        if full:
            indicator = abjad.Articulation("baca-full-downbow")
        else:
            indicator = abjad.Articulation("downbow")
        indicator = _tweaks.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def dynamic_function(
    argument,
    dynamic: str | abjad.Dynamic,
    *tweaks: abjad.Tweak,
    redundant: bool = False,
) -> list[abjad.Wrapper]:
    wrappers: list[abjad.Wrapper] = []
    if redundant:
        return wrappers
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        if isinstance(dynamic, str):
            indicator = _dynamics.make_dynamic(dynamic)
        else:
            indicator = dynamic
        prototype = (abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin)
        assert isinstance(indicator, prototype), repr(indicator)
        indicator = _tweaks.bundle_tweaks(indicator, tweaks)
        wrappers_ = _attach_persistent_indicator(
            leaf,
            [indicator],
            tag=tag,
        )
        wrappers.extend(wrappers_)
    return wrappers


def dynamic_down_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\dynamicDown")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def dynamic_up_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\dynamicUp")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def edition_function(
    argument, *, not_parts: str, only_parts: str
) -> list[abjad.Wrapper]:
    assert isinstance(not_parts, str), repr(not_parts)
    assert isinstance(only_parts, str), repr(only_parts)
    wrappers = []
    wrappers_ = markup_function(argument, not_parts)
    _tags.wrappers(wrappers_, _tags.NOT_PARTS)
    wrappers.extend(wrappers_)
    wrappers_ = markup_function(argument, only_parts)
    _tags.wrappers(wrappers_, _tags.ONLY_PARTS)
    wrappers.extend(wrappers_)
    return wrappers


def espressivo_function(argument, *tweaks: abjad.Tweak) -> list[abjad.Wrapper]:
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


def extend_beam_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = _enums.RIGHT_BROKEN_BEAM
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def fermata_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("fermata")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def flageolet_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("flageolet")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def global_fermata_function(
    argument, description: str = "fermata"
) -> list[abjad.Wrapper]:
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
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        markup = abjad.Markup(rf"\baca-{command}-markup")
        wrapper = abjad.attach(
            markup,
            leaf,
            direction=abjad.UP,
            tag=abjad.Tag("baca.global_fermata_function(1)"),
            wrapper=True,
        )
        wrappers.append(wrapper)
        literal = abjad.LilyPondLiteral(r"\baca-fermata-measure")
        abjad.attach(
            literal,
            leaf,
            tag=abjad.Tag("baca.global_fermata_function(2)"),
            wrapper=True,
        )
        wrappers.append(wrapper)
        abjad.attach(
            _enums.FERMATA_MEASURE,
            leaf,
            # TODO: remove enum tag?
            tag=_tags.FERMATA_MEASURE,
            wrapper=True,
        )
        wrappers.append(wrapper)
        abjad.annotate(leaf, _enums.FERMATA_DURATION, fermata_duration)
    return wrappers


def instrument_function(
    argument,
    key: str,
    manifests: dict,
) -> list[abjad.Wrapper]:
    assert isinstance(key, str), repr(key)
    assert isinstance(manifests, dict), repr(manifests)
    dictionary = manifests["abjad.Instrument"]
    instrument = dictionary[key]
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        wrappers_ = _attach_persistent_indicator(
            leaf,
            [instrument],
            manifests=manifests,
            tag=tag,
        )
        wrappers.extend(wrappers_)
    return wrappers


def instrument_name_function(
    argument,
    string: str,
    *,
    context: str = "Staff",
) -> list[abjad.Wrapper]:
    assert isinstance(string, str), repr(string)
    assert string.startswith("\\"), repr(string)
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.NOT_PARTS)
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.InstrumentName(string, context=context)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def invisible_music_function(argument) -> list[abjad.Wrapper]:
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        tag = _tags.function_name(_frame(), n=1)
        tag = tag.append(_tags.INVISIBLE_MUSIC_COMMAND)
        indicator = abjad.LilyPondLiteral(r"\abjad-invisible-music")
        wrapper = abjad.attach(
            indicator,
            leaf,
            deactivate=True,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
        tag = _tags.function_name(_frame(), n=2)
        tag = tag.append(_tags.INVISIBLE_MUSIC_COLORING)
        indicator = abjad.LilyPondLiteral(r"\abjad-invisible-music-coloring")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def laissez_vibrer_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LaissezVibrer()
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


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


def long_fermata_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("longfermata")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def marcato_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("marcato")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


# TODO: remove
def mark_function(
    argument,
    string: str,
    *tweaks: abjad.Tweak,
) -> list[abjad.Wrapper]:
    assert isinstance(string, abjad.Markup | str), repr(string)
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        rehearsal_mark = abjad.RehearsalMark(markup=string)
        rehearsal_mark = _tweaks.bundle_tweaks(rehearsal_mark, tweaks)
        wrapper = abjad.attach(
            rehearsal_mark,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


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
    if isinstance(indicator, str):
        indicator_ = manifests["abjad.MetronomeMark"][indicator]
    else:
        indicator_ = indicator
    prototype = (
        abjad.MetricModulation,
        abjad.MetronomeMark,
        _indicatorclasses.Accelerando,
        _indicatorclasses.Ritardando,
    )
    assert isinstance(indicator_, prototype), repr(indicator_)
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        wrappers_ = _attach_persistent_indicator(
            leaf,
            [indicator_],
            manifests=manifests,
            tag=tag,
        )
        wrappers.extend(wrappers_)
    return wrappers


def one_voice_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\oneVoice")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def open_volta_function(skip, first_measure_number) -> list[abjad.Wrapper]:
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    wrappers = []
    wrappers_ = bar_line_function(skip, ".|:", site="before")
    wrappers.extend(wrappers_)
    tag = _tags.function_name(_frame())
    measure_number = abjad.get.measure_number(skip)
    measure_number += first_measure_number - 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    wrappers_ = _overridecommands.bar_line_x_extent([skip], (0, 2))
    _tags.wrappers(wrappers_, tag, _tags.NOT_MOL, measure_number_tag)
    wrappers.extend(wrappers_)
    wrappers_ = _overridecommands.bar_line_x_extent([skip], (0, 3))
    _tags.wrappers(wrappers_, tag, _tags.ONLY_MOL, measure_number_tag)
    wrappers.extend(wrappers_)
    return wrappers


def parenthesize_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\parenthesize")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


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


def repeat_tie_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.RepeatTie()
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def short_fermata_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("shortfermata")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def short_instrument_name_function(
    argument,
    key: str,
    manifests: dict,
    *,
    context: str = "Staff",
) -> list[abjad.Wrapper]:
    assert isinstance(key, str), repr(key)
    assert isinstance(manifests, dict), repr(manifests)
    dictionary = manifests["abjad.ShortInstrumentName"]
    short_instrument_name = dictionary[key]
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.NOT_PARTS)
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        wrappers_ = _attach_persistent_indicator(
            leaf,
            [short_instrument_name],
            manifests=manifests,
            tag=tag,
        )
        wrappers.extend(wrappers_)
    return wrappers


def snap_pizzicato_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("snappizzicato")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def staccatissimo_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("staccatissimo")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def staccato_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("staccato")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def staff_lines_function(argument, n: int) -> list[abjad.Wrapper]:
    assert isinstance(n, int), repr(n)
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        bar_extent = _indicatorclasses.BarExtent(n)
        wrappers_ = _attach_persistent_indicator(
            leaf,
            [bar_extent],
            tag=abjad.Tag("baca.staff_lines_function(1)").append(_tags.NOT_PARTS),
        )
        wrappers.extend(wrappers_)
        staff_lines = _indicatorclasses.StaffLines(n)
        wrappers_ = _attach_persistent_indicator(
            leaf,
            [staff_lines],
            tag=abjad.Tag("baca.staff_lines_function(2)"),
        )
        wrappers.extend(wrappers_)
    return wrappers


def stem_tremolo_function(argument, *, tremolo_flags: int = 32) -> list[abjad.Wrapper]:
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


def stop_on_string_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("baca-stop-on-string")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def stop_trill_function(argument) -> list[abjad.Wrapper]:
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
    wrappers = literal_function(
        argument,
        r"\stopTrillSpan",
        site="closing",
    )
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def stopped_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("stopped")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def tenuto_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("tenuto")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def tie_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.Tie()
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def triple_staccato_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("baca-staccati #3")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def up_arpeggio_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Arpeggio(direction=abjad.UP)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def up_bow_function(
    argument, *tweaks: abjad.Tweak, full: bool = False
) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator: abjad.Articulation | abjad.Bundle
        if full:
            indicator = abjad.Articulation("baca-full-upbow")
        else:
            indicator = abjad.Articulation("upbow")
        indicator = _tweaks.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def very_long_fermata_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("verylongfermata")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def voice_four_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\voiceFour")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def voice_one_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\voiceOne")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def voice_three_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\voiceThree")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def voice_two_function(argument) -> list[abjad.Wrapper]:
    tag = _tags.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\voiceTwo")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers
