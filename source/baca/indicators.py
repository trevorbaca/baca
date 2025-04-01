"""
Indicators.
"""

import dataclasses
from inspect import currentframe as _frame

import abjad

from . import classes as _classes
from . import dynamics as _dynamics
from . import helpers as _helpers
from . import indicatorlib as _indicatorlib
from . import override as _override
from . import tags as _tags
from .enums import enums as _enums


def _assert_no_post_event_tweaks(tweaks, command):
    for tweak in tweaks:
        if tweak.post_event() is True:
            message = f"LilyPond {command} is not a post-event:"
            message += f"\n    {tweak}"
            raise Exception(message)


def _prepare_alternate_bow_strokes(*tweaks, downbow_first, full):
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
    indicators = [_helpers.bundle_tweaks(_, tweaks) for _ in indicators]
    for indicator in indicators:
        assert isinstance(indicator, abjad.Articulation | abjad.Bundle)
    return indicators


def accent(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def alternate_bow_strokes(
    argument,
    *tweaks: abjad.Tweak,
    downbow_first: bool = True,
    full: bool = False,
) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def arpeggio(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def articulation(
    argument,
    string: str,
    *tweaks: abjad.Tweak,
) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation(string)
        indicator = _helpers.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def articulations(argument, articulations: list) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def bar_line(
    argument, abbreviation: str = "|", *, site: str = "after"
) -> list[abjad.Wrapper]:
    assert isinstance(abbreviation, str), repr(abbreviation)
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.BarLine(abbreviation, site=site)
        wrapper = abjad.attach(indicator, leaf, tag=tag, wrapper=True)
        wrappers.append(wrapper)
    return wrappers


def bend_after(
    argument,
    numbers: list,
    *tweaks: abjad.Tweak,
) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    leaves = abjad.iterate.leaves(argument)
    cyclic_numbers = abjad.CyclicTuple(numbers)
    for i, leaf in enumerate(leaves):
        number = cyclic_numbers[i]
        indicator = abjad.BendAfter(number)
        indicator = _helpers.bundle_tweaks(indicator, tweaks)
        if indicator is not None:
            wrapper = abjad.attach(
                indicator,
                leaf,
                tag=tag,
                wrapper=True,
            )
            wrappers.append(wrapper)
    return wrappers


def breathe(argument, *tweaks: abjad.Tweak) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    _assert_no_post_event_tweaks(tweaks, r"\breathe")
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator: abjad.LilyPondLiteral | abjad.Bundle
        indicator = abjad.LilyPondLiteral(r"\breathe", site="after")
        indicator = _helpers.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def clef(argument, clef: str) -> list[abjad.Wrapper]:
    assert isinstance(clef, str), repr(clef)
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.Clef(clef)
        wrapper = _indicatorlib.attach_persistent_indicator(
            leaf,
            indicator,
            tag=tag,
        )
        wrappers.append(wrapper)
    return wrappers


def close_volta(
    skip, first_measure_number, site: str = "before"
) -> list[abjad.Wrapper]:
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    assert isinstance(site, str), repr(site)
    wrappers = []
    after = site == "after"
    wrappers_ = bar_line(skip, ":|.", site=site)
    wrappers.extend(wrappers_)
    tag = _helpers.function_name(_frame())
    measure_number = abjad.get.measure_number(skip)
    measure_number += first_measure_number - 1
    if after is True:
        measure_number += 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    # TODO: make this override visible to the composer:
    wrappers_ = _override.bar_line_x_extent([skip], (0, 1.5), after=after)
    _tags.tag(wrappers_, tag, measure_number_tag, _tags.ONLY_MOL)
    wrappers.extend(wrappers_)
    return wrappers


def color_fingerings(
    argument,
    numbers: list[int],
    *tweaks: abjad.Tweak,
) -> list[abjad.Wrapper]:
    cyclic_numbers = abjad.CyclicTuple(numbers)
    wrappers = []
    leaves = abjad.select.leaves(argument)
    total = len(leaves)
    for i, leaf in enumerate(leaves):
        number = cyclic_numbers[i]
        if number != 0:
            fingering = abjad.ColorFingering(number)
            fingering = _helpers.bundle_tweaks(fingering, tweaks, i=i, total=total)
            wrapper = abjad.attach(fingering, leaf, direction=abjad.UP, wrapper=True)
            wrappers.append(wrapper)
    return wrappers


def cross_staff(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\crossStaff", site="before")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def damp(argument, *tweaks: abjad.Tweak) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator: abjad.Articulation | abjad.Bundle
        indicator = abjad.Articulation("baca-damp")
        indicator = _helpers.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def dimensionless_boxed_markup(
    argument,
    string: str,
    *tweaks: abjad.Tweak,
    font_size: int = 10,
) -> list[abjad.Wrapper]:
    assert isinstance(string, str), repr(string)
    assert isinstance(font_size, int | float), repr(font_size)
    string = rf'\baca-dimensionless-boxed-markup "{string}" #{font_size}'
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator: abjad.Markup | abjad.Bundle
        indicator = abjad.Markup(string)
        indicator = _helpers.bundle_tweaks(indicator, tweaks)
        tag = _helpers.function_name(_frame())
        wrapper = abjad.attach(
            indicator,
            leaf,
            # IMPORTANT:
            # markup attach direction must be neutral or down (- or _);
            # markup attach direction of up (^) negatively impacts global
            # skips context vertical spacing
            direction=abjad.CENTER,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def double_flageolet(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def double_staccato(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def double_volta(skip, first_measure_number) -> list[abjad.Wrapper]:
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    wrappers = []
    wrappers_ = bar_line(skip, ":.|.:", site="before")
    wrappers.extend(wrappers_)
    tag = _helpers.function_name(_frame())
    measure_number = abjad.get.measure_number(skip)
    measure_number += first_measure_number - 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    # TODO: make this override visible to the composer:
    wrappers_ = _override.bar_line_x_extent([skip], (0, 3))
    _tags.tag(wrappers_, tag, _tags.NOT_MOL, measure_number_tag)
    wrappers.extend(wrappers_)
    # TODO: make this override visible to the composer:
    wrappers_ = _override.bar_line_x_extent([skip], (0, 4))
    _tags.tag(wrappers_, tag, _tags.ONLY_MOL, measure_number_tag)
    wrappers.extend(wrappers_)
    return wrappers


def down_arpeggio(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def down_bow(
    argument,
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator: abjad.Articulation | abjad.Bundle
        if full:
            indicator = abjad.Articulation("baca-full-downbow")
        else:
            indicator = abjad.Articulation("downbow")
        indicator = _helpers.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def dynamic(
    argument,
    dynamic: str | abjad.Dynamic,
    *tweaks: abjad.Tweak,
) -> list[abjad.Wrapper]:
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        if dynamic == "-":
            continue
        elif isinstance(dynamic, str):
            indicator = _dynamics.make_dynamic(dynamic)
        else:
            indicator = dynamic
        if isinstance(indicator, abjad.StartHairpin | abjad.StopHairpin):
            raise Exception(f"use baca.hairpin() instead: {indicator!r}")
        assert isinstance(indicator, abjad.Dynamic), repr(indicator)
        indicator = _helpers.bundle_tweaks(indicator, tweaks)
        wrapper = _indicatorlib.attach_persistent_indicator(
            leaf,
            indicator,
        )
        wrappers.append(wrapper)
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def dynamic_down(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\dynamicDown", site="before")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def dynamic_up(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\dynamicUp", site="before")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def edition(argument, *, not_parts: str, only_parts: str) -> list[abjad.Wrapper]:
    assert isinstance(not_parts, str), repr(not_parts)
    assert isinstance(only_parts, str), repr(only_parts)
    wrappers = []
    wrappers_ = markup(argument, not_parts)
    _tags.tag(wrappers_, _tags.NOT_PARTS)
    wrappers.extend(wrappers_)
    wrappers_ = markup(argument, only_parts)
    _tags.tag(wrappers_, _tags.ONLY_PARTS)
    wrappers.extend(wrappers_)
    return wrappers


def espressivo(argument, *tweaks: abjad.Tweak) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator: abjad.Articulation | abjad.Bundle
        indicator = abjad.Articulation("espressivo")
        indicator = _helpers.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def extend_beam(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = _enums.RIGHT_OPEN_BEAM
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def fermata(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def flageolet(argument, *tweaks: abjad.Tweak) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("flageolet")
        indicator = _helpers.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def global_fermata(argument, description: str = "fermata") -> list[abjad.Wrapper]:
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
            tag=_helpers.function_name(_frame(), n=1),
            wrapper=True,
        )
        wrappers.append(wrapper)
        literal = abjad.LilyPondLiteral(r"\baca-fermata-measure", site="before")
        abjad.attach(
            literal,
            leaf,
            tag=_helpers.function_name(_frame(), n=2),
            wrapper=True,
        )
        wrappers.append(wrapper)
        abjad.attach(
            _enums.FERMATA_MEASURE,
            leaf,
            wrapper=True,
        )
        wrappers.append(wrapper)
        abjad.annotate(leaf, _enums.FERMATA_DURATION, fermata_duration)
    return wrappers


def instrument(
    argument,
    key: str,
    manifests: dict,
) -> list[abjad.Wrapper]:
    assert isinstance(key, str), repr(key)
    assert isinstance(manifests, dict), repr(manifests)
    dictionary = manifests["abjad.Instrument"]
    instrument = dictionary[key]
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        wrapper = _indicatorlib.attach_persistent_indicator(
            leaf,
            instrument,
            manifests=manifests,
            tag=tag,
        )
        wrappers.append(wrapper)
    return wrappers


def instrument_name(
    argument,
    string: str,
    *,
    context: str = "Staff",
) -> list[abjad.Wrapper]:
    assert isinstance(string, str), repr(string)
    assert string.startswith("\\"), repr(string)
    tag = _helpers.function_name(_frame())
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


def invisible_music(argument) -> list[abjad.Wrapper]:
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        tag = _helpers.function_name(_frame(), n=1)
        tag = tag.append(_tags.INVISIBLE_MUSIC_COMMAND)
        indicator = abjad.LilyPondLiteral(r"\abjad-invisible-music", site="before")
        wrapper = abjad.attach(
            indicator,
            leaf,
            deactivate=True,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
        tag = _helpers.function_name(_frame(), n=2)
        tag = tag.append(_tags.INVISIBLE_MUSIC_COLORING)
        indicator = abjad.LilyPondLiteral(
            r"\abjad-invisible-music-coloring", site="before"
        )
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def laissez_vibrer(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def literal(
    argument,
    string: str | list[str],
    *,
    site: str = "before",
) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def long_fermata(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def marcato(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def markup(
    argument,
    markup: str,
    *tweaks: abjad.Tweak,
    direction: abjad.Vertical = abjad.UP,
) -> list[abjad.Wrapper]:
    assert isinstance(markup, str), repr(markup)
    assert direction in (abjad.DOWN, abjad.UP), repr(direction)
    tag = _helpers.function_name(_frame())
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


def metronome_mark(
    skip: abjad.Skip,
    indicator,
    *tweaks: abjad.Tweak,
    manifests=None,
) -> list[abjad.Wrapper]:
    assert isinstance(skip, abjad.Skip), repr(skip)
    manifests = manifests or {}
    if isinstance(indicator, str):
        indicator_ = manifests["abjad.MetronomeMark"][indicator]
    else:
        indicator_ = indicator
    prototype = (
        abjad.MetricModulation,
        abjad.MetronomeMark,
        _classes.Accelerando,
        _classes.Ritardando,
    )
    assert isinstance(indicator_, prototype), repr(indicator_)
    indicator_ = _helpers.bundle_tweaks(indicator_, tweaks)
    tag = _helpers.function_name(_frame())
    wrappers = []
    if isinstance(indicator_, abjad.MetricModulation):
        wrapper = abjad.attach(
            indicator_,
            skip,
            tag=tag,
            wrapper=True,
        )
    else:
        wrapper = _indicatorlib.attach_persistent_indicator(
            skip,
            indicator_,
            manifests=manifests,
            tag=tag,
        )
    wrappers.append(wrapper)
    return wrappers


def one_voice(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        command = abjad.VoiceNumber()
        wrapper = abjad.attach(
            command,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def open_volta(skip, first_measure_number) -> list[abjad.Wrapper]:
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    wrappers = []
    wrappers_ = bar_line(skip, ".|:-|", site="before")
    wrappers.extend(wrappers_)
    tag = _helpers.function_name(_frame())
    measure_number = abjad.get.measure_number(skip)
    measure_number += first_measure_number - 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    # TODO: make this override visible to the composer:
    wrappers_ = _override.bar_line_x_extent([skip], (0, 2))
    _tags.tag(wrappers_, tag, _tags.NOT_MOL, measure_number_tag)
    wrappers.extend(wrappers_)
    # TODO: make this override visible to the composer:
    wrappers_ = _override.bar_line_x_extent([skip], (0, 3))
    _tags.tag(wrappers_, tag, _tags.ONLY_MOL, measure_number_tag)
    wrappers.extend(wrappers_)
    return wrappers


def ottava(argument, n: int) -> list[abjad.Wrapper]:
    assert isinstance(n, int), repr(n)
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.Ottava(n=n)
        wrapper = _indicatorlib.attach_persistent_indicator(
            leaf,
            indicator,
            tag=tag,
        )
        wrappers.append(wrapper)
    return wrappers


def parenthesize(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\parenthesize", site="before")
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def quadruple_staccato(argument) -> list[abjad.Wrapper]:
    wrappers = []
    tag = _helpers.function_name(_frame())
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


def rehearsal_mark(
    argument,
    string: str,
    *tweaks: abjad.Tweak,
    site: str = "before",
) -> list[abjad.Wrapper]:
    assert isinstance(string, abjad.Markup | str), repr(string)
    _assert_no_post_event_tweaks(tweaks, r"\mark")
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        rehearsal_mark = abjad.RehearsalMark(markup=string, site=site)
        rehearsal_mark = _helpers.bundle_tweaks(rehearsal_mark, tweaks)
        wrapper = abjad.attach(
            rehearsal_mark,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def repeat_tie(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def short_fermata(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def short_instrument_name(
    argument,
    key: str,
    manifests: dict,
    *,
    context: str = "Staff",
    deactivate: bool = False,
) -> list[abjad.Wrapper]:
    assert isinstance(key, str), repr(key)
    assert isinstance(manifests, dict), repr(manifests)
    dictionary = manifests["abjad.ShortInstrumentName"]
    short_instrument_name = dictionary[key]
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.NOT_PARTS)
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        wrapper = _indicatorlib.attach_persistent_indicator(
            leaf,
            short_instrument_name,
            deactivate=deactivate,
            manifests=manifests,
            tag=tag,
        )
        wrappers.append(wrapper)
    return wrappers


def snap_pizzicato(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def staccatissimo(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def staccato(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def staff_lines(argument, n: int) -> list[abjad.Wrapper]:
    assert isinstance(n, int), repr(n)
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        bar_extent = _classes.BarExtent(n)
        wrapper = _indicatorlib.attach_persistent_indicator(
            leaf,
            bar_extent,
            tag=_helpers.function_name(_frame(), n=1).append(_tags.NOT_PARTS),
        )
        wrappers.append(wrapper)
        staff_lines = _classes.StaffLines(n)
        wrapper = _indicatorlib.attach_persistent_indicator(
            leaf,
            staff_lines,
            tag=_helpers.function_name(_frame(), n=2),
        )
        wrappers.append(wrapper)
    return wrappers


def stem_tremolo(argument, *, tremolo_flags: int = 32) -> list[abjad.Wrapper]:
    wrappers = []
    tag = _helpers.function_name(_frame())
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
    argument,
    *tweaks: abjad.Tweak,
) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("baca-stop-on-string")
        indicator = _helpers.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def stop_trill(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.StopTrillSpan()
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def stopped(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def tenuto(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def text_mark(
    argument,
    string: str,
    *tweaks: abjad.Tweak,
    site: str = "before",
) -> list[abjad.Wrapper]:
    assert isinstance(string, str), repr(string)
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        mark = abjad.TextMark(string=string, site=site)
        result = _helpers.bundle_tweaks(mark, tweaks)
        wrapper = abjad.attach(
            result,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def tie(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def triple_staccato(
    argument,
    *tweaks: abjad.Tweak,
) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("baca-staccati #3")
        indicator = _helpers.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def up_arpeggio(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def up_bow(
    argument,
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        indicator: abjad.Articulation | abjad.Bundle
        if full:
            indicator = abjad.Articulation("baca-full-upbow")
        else:
            indicator = abjad.Articulation("upbow")
        indicator = _helpers.bundle_tweaks(indicator, tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def very_long_fermata(argument) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
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


def voice_number(argument, n: int | None = None) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    if n is not None:
        assert isinstance(n, int), repr(n)
    wrappers = []
    for leaf in abjad.iterate.leaves(argument):
        command = abjad.VoiceNumber(n)
        wrapper = _indicatorlib.attach_persistent_indicator(
            leaf,
            command,
            tag=tag,
        )
        wrappers.append(wrapper)
    return wrappers
