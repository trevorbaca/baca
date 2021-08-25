r"""
Classes and functions for spacing.

..  container:: example exception

    Exception 1. Breaks function raises exception on out-of-sequence page specifiers:

    >>> breaks = baca.breaks(
    ...     baca.page(
    ...         1,
    ...         baca.system(measure=1, y_offset=20, distances=(15, 20, 20)),
    ...         baca.system(measure=13, y_offset=140, distances=(15, 20, 20)),
    ...     ),
    ...     baca.page(
    ...         9,
    ...         baca.system(measure=23, y_offset=20, distances=(15, 20, 20)),
    ...     ),
    ... )
    Traceback (most recent call last):
        ...
    Exception: page number (9) is not 2.

..  container:: example exception

    Exception 2. Page function raises exception when Y-offsets overlap:

    >>> baca.page(
    ...     1,
    ...     baca.system(measure=1, y_offset=60, distances=(20, 20)),
    ...     baca.system(measure=4, y_offset=60, distances=(20, 20)),
    ... )
    Traceback (most recent call last):
        ...
    Exception: systems overlap at Y-offset 60.

"""
import collections

import abjad

from . import classes as _classes
from . import commandclasses as _commandclasses
from . import indicators as _indicators
from . import selectors as _selectors
from . import tags as _tags

magic_lilypond_eol_adjustment = abjad.Multiplier(35, 24)

fermata_measure_duration = abjad.Duration(1, 4)


class SpacingSpecifier:
    """
    Spacing specifier.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        breaks=None,
        fallback_duration=None,
        overrides=None,
    ):
        if breaks is not None:
            assert isinstance(breaks, BreakMeasureMap), repr(breaks)
        self.breaks = breaks
        if fallback_duration is not None:
            fallback_duration = abjad.Duration(fallback_duration)
        self.fallback_duration = fallback_duration
        self.overrides = overrides

    ### SPECIAL METHODS ###

    def __call__(self, segment_maker=None):
        if self.fallback_duration is None:
            return
        page_layout_profile = segment_maker._page_layout_profile or {}
        skips = _classes.Selection(segment_maker.score["Global_Skips"]).skips()
        measure_count = page_layout_profile.get("measure_count") or len(skips)
        fermata_measure_numbers = page_layout_profile.get("fermata_measure_numbers", [])
        eol_measure_numbers = page_layout_profile.get("eol_measure_numbers", [])
        measures = {}
        for n in range(1, measure_count + 1):
            if n in fermata_measure_numbers:
                measures[n] = fermata_measure_duration
            else:
                measures[n] = self.fallback_duration
            measures[n + 1] = fermata_measure_duration
        for token, duration in self.overrides or []:
            duration = abjad.NonreducedFraction(duration)
            measure_numbers = []
            if isinstance(token, int):
                measure_numbers.append(token)
            elif isinstance(token, tuple):
                start, stop = token
                for measure_number in range(start, stop + 1):
                    measure_numbers.append(measure_number)
            elif isinstance(token, list):
                measure_numbers.extend(token)
            else:
                raise TypeError(f"token must be int, pair or list (not {token!r}).")
            for n in measure_numbers:
                if n < 1:
                    message = f"Nonpositive measure number ({n}) not allowed."
                elif measure_count < n:
                    message = f"measure number {n} greater than"
                    message += f" last measure number ({measure_count})."
                else:
                    measures[n] = duration
                    continue
                raise Exception(message)
        measure_count = len(skips)
        for measure_index, skip in enumerate(skips):
            measure_number = measure_index + 1
            if measure_number == measure_count:
                duration = abjad.Duration(1, 4)
            elif measures:
                duration = measures[measure_number]
                duration = abjad.NonreducedFraction(duration)
            else:
                duration = self.fallback_duration
            eol_adjusted, duration_ = False, None
            if measure_number in eol_measure_numbers:
                duration_ = duration
                duration *= magic_lilypond_eol_adjustment
                eol_adjusted = True
            spacing_section = _indicators.SpacingSection(duration=duration)
            tag = _tags.SPACING_COMMAND
            abjad.attach(
                spacing_section,
                skip,
                tag=tag.append(abjad.Tag("baca.SpacingSpecifier.__call__(1)")),
            )
            if eol_adjusted:
                multiplier = magic_lilypond_eol_adjustment
                string_ = f"[[{duration_!s} * {multiplier!s}]]"
            else:
                string_ = f"[{duration!s}]"
            if measure_index < measure_count - 1:
                tag = _tags.SPACING
                string = r"- \baca-start-spm-left-only"
                string += f' "{string_}"'
                start_text_span = abjad.StartTextSpan(
                    command=r"\bacaStartTextSpanSPM", left_text=string
                )
                abjad.attach(
                    start_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag.append(abjad.Tag("baca.SpacingSpecifier.__call__(2)")),
                )
            if 0 < measure_index:
                tag = _tags.SPACING
                stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanSPM")
                abjad.attach(
                    stop_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag.append(abjad.Tag("baca.SpacingSpecifier.__call__(3)")),
                )


class LBSD:
    """
    Line-break system details.
    """

    ### CLASS VARIABLES ###

    _override = r"\overrideProperty"
    _override += " Score.NonMusicalPaperColumn.line-break-system-details"

    ### INITIALIZER ###

    def __init__(self, *, y_offset=None, alignment_distances=None):
        self.y_offset = y_offset
        if alignment_distances is not None:
            alignment_distances = tuple(alignment_distances)
        self.alignment_distances = alignment_distances

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        alignment_distances = " ".join(str(_) for _ in self.alignment_distances)
        string = rf"\baca-lbsd #{self.y_offset} #'({alignment_distances})"
        bundle.before.commands.append(string)
        return bundle


class PageSpecifier:
    """
    Page specifier.
    """

    ### INITIALIZER ###

    def __init__(self, *, number, systems):
        assert isinstance(number, int), repr(number)
        assert 1 <= number, repr(number)
        self.number = number
        y_offsets = []
        for system in systems:
            y_offset = system.y_offset
            if y_offset in y_offsets:
                raise Exception(f"systems overlap at Y-offset {y_offset}.")
            else:
                y_offsets.append(y_offset)
        self.systems = systems


def breaks(*page_specifiers):
    """
    Makes break measure map.
    """
    commands = {}
    page_count = len(page_specifiers)
    assert 0 < page_count, repr(page_count)
    first_system = page_specifiers[0].systems[0]
    assert first_system.measure == 1, repr(first_system)
    bol_measure_numbers = []
    for i, page_specifier in enumerate(page_specifiers):
        page_number = i + 1
        if page_specifier.number is not None:
            if page_specifier.number != page_number:
                message = f"page number ({page_specifier.number})"
                message += f" is not {page_number}."
                raise Exception(message)
        for j, system in enumerate(page_specifier.systems):
            measure_number = system.measure
            bol_measure_numbers.append(measure_number)
            skip_index = measure_number - 1
            y_offset = system.y_offset
            alignment_distances = system.distances
            assert 0 <= skip_index
            selector = _selectors.skip(skip_index)
            if j == 0:
                literal = abjad.LilyPondLiteral(r"\pageBreak")
            else:
                literal = abjad.LilyPondLiteral(r"\break")
            command = _commandclasses.IndicatorCommand(
                indicators=[literal], selector=selector
            )
            alignment_distances = _classes.Sequence(alignment_distances)
            alignment_distances = alignment_distances.flatten(depth=-1)
            lbsd = LBSD(alignment_distances=alignment_distances, y_offset=y_offset)
            lbsd_command = _commandclasses.IndicatorCommand(
                indicators=[lbsd], selector=selector
            )
            commands[measure_number] = [command, lbsd_command]
    commands_ = {}
    for measure_number, list_ in commands.items():
        commands_[measure_number] = []
        for command in list_:
            command_ = abjad.new(command, tags=[_tags.BREAK])
            commands_[measure_number].append(command_)
    commands = commands_
    breaks = BreakMeasureMap(
        bol_measure_numbers=bol_measure_numbers,
        commands=commands,
        page_count=page_count,
    )
    return breaks


def page(number, *systems):
    """
    Makes page specifier.
    """
    systems_ = list(systems)
    return PageSpecifier(number=number, systems=systems_)


space = collections.namedtuple(
    "space",
    ["measures", "duration"],
)


BreakMeasureMap = collections.namedtuple(
    "BreakMeasureMap",
    ["bol_measure_numbers", "commands", "page_count"],
)


system = collections.namedtuple(
    "system",
    ["measure", "y_offset", "distances"],
)


def make_layout(
    *pages,
    spacing=None,
    overrides=None,
):
    """
    Makes layout.
    """
    breaks_ = breaks(*pages)
    return SpacingSpecifier(
        breaks=breaks_,
        fallback_duration=spacing,
        overrides=overrides,
    )
