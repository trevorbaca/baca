"""
LilyPond.
"""

from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers


def _get_global_spanner_extra_offsets(
    clock_time_extra_offset,
    local_measure_number_extra_offset,
    measure_number_extra_offset,
    spacing_extra_offset,
    stage_number_extra_offset,
):
    strings = []
    if clock_time_extra_offset is not None:
        value = clock_time_extra_offset
        assert isinstance(value, tuple)
        string = f"#'({value[0]} . {value[1]})"
        string = f"clock-time-extra-offset = {string}"
        strings.append(string)
    if local_measure_number_extra_offset is not None:
        value = local_measure_number_extra_offset
        assert isinstance(value, tuple)
        string = f"#'({value[0]} . {value[1]})"
        string = f"local-measure-number-extra-offset = {string}"
        strings.append(string)
    if measure_number_extra_offset is not None:
        value = measure_number_extra_offset
        assert isinstance(value, tuple)
        string = f"#'({value[0]} . {value[1]})"
        string = f"measure-number-extra-offset = {string}"
        strings.append(string)
    if spacing_extra_offset is not None:
        value = spacing_extra_offset
        assert isinstance(value, tuple)
        string = f"#'({value[0]} . {value[1]})"
        string = f"spacing-extra-offset = {string}"
        strings.append(string)
    if stage_number_extra_offset is not None:
        value = stage_number_extra_offset
        assert isinstance(value, tuple)
        string = f"#'({value[0]} . {value[1]})"
        string = f"stage-number-extra-offset = {string}"
        strings.append(string)
    return strings


def _make_lilypond_file(
    include_layout_ily,
    includes,
    preamble,
    score,
):
    tag = _helpers.function_name(_frame())
    items = []
    items.extend(includes)
    items.append("")
    if preamble:
        string = "\n".join(preamble)
        items.append(string)
    block = abjad.Block("score")
    block.items.append(score)
    items.append(block)
    lilypond_file = abjad.LilyPondFile(
        items=items,
        lilypond_language_token=False,
        tag=tag,
    )
    if include_layout_ily:
        assert len(lilypond_file["score"].items) == 1
        score = lilypond_file["Score"]
        assert isinstance(score, abjad.Score)
        include = abjad.Container(tag=tag)
        literal = abjad.LilyPondLiteral("", site="absolute_before")
        abjad.attach(literal, include, tag=None)
        string = r'\include "layout.ly"'
        literal = abjad.LilyPondLiteral(string, site="opening")
        abjad.attach(literal, include, tag=tag)
        container = abjad.Container([include, score], simultaneous=True, tag=tag)
        literal = abjad.LilyPondLiteral("", site="absolute_before")
        abjad.attach(literal, container, tag=None)
        literal = abjad.LilyPondLiteral("", site="closing")
        abjad.attach(literal, container, tag=None)
        lilypond_file["score"].items[:] = [container]
        lilypond_file["score"].items.append("")
    return lilypond_file


def file(
    score,
    clock_time_extra_offset=None,
    include_layout_ily=False,
    includes=None,
    local_measure_number_extra_offset=None,
    measure_number_extra_offset=None,
    preamble=None,
    spacing_extra_offset=None,
    stage_number_extra_offset=None,
):
    assert isinstance(score, abjad.Score), repr(score)
    if clock_time_extra_offset not in (False, None):
        assert isinstance(clock_time_extra_offset, tuple)
        assert len(clock_time_extra_offset) == 2
    includes = list(includes or [])
    includes = [rf'\include "{_}"' for _ in includes]
    preamble = list(preamble or [])
    if preamble:
        assert all(isinstance(_, str) for _ in preamble), repr(preamble)
    strings = _get_global_spanner_extra_offsets(
        clock_time_extra_offset,
        local_measure_number_extra_offset,
        measure_number_extra_offset,
        spacing_extra_offset,
        stage_number_extra_offset,
    )
    preamble.extend(strings)
    lilypond_file = _make_lilypond_file(
        include_layout_ily,
        includes,
        preamble,
        score,
    )
    return lilypond_file
