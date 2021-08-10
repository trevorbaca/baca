r"""
Classes and functions for spacing.

..  container:: example exception

    Exception 1. Breaks function raises exception on out-of-sequence page specifiers:

    >>> breaks = baca.breaks(
    ...     baca.page(
    ...         baca.system(measure=1, y_offset=20, distances=(15, 20, 20)),
    ...         baca.system(measure=13, y_offset=140, distances=(15, 20, 20)),
    ...         number=1,
    ...     ),
    ...     baca.page(
    ...         baca.system(measure=23, y_offset=20, distances=(15, 20, 20)),
    ...         number=9
    ...     ),
    ... )
    Traceback (most recent call last):
        ...
    Exception: page number (9) is not 2.

..  container:: example exception

    Exception 2. Spacing specifier raises exception when score contains too few measures:

    >>> maker = baca.SegmentMaker(
    ...     score_template=baca.StringTrioScoreTemplate(),
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8), (4, 8)],
    ...     breaks=baca.breaks(
    ...         baca.page(
    ...             baca.system(measure=1, y_offset=0, distances=(10, 20)),
    ...         ),
    ...         baca.page(
    ...             baca.system(measure=11, y_offset=0, distances=(10, 20)),
    ...         ),
    ...     ),
    ... )
    >>> maker(
    ...     "Violin_Music_Voice",
    ...     baca.make_even_divisions(),
    ...     baca.pitch("E4"),
    ... )
    >>> lilypond_file = maker.run(environment="docs")
    Traceback (most recent call last):
        File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/doctest.py", line 1330, in __run
        compileflags, 1), test.globs)
        File "<doctest spacing.py[82]>", line 1, in <module>
        lilypond_file = maker.run(environment="docs")
        File "/Users/trevorbaca/baca/baca/segmentmaker.py", line 7390, in run
        self._apply_breaks()
        File "/Users/trevorbaca/baca/baca/segmentmaker.py", line 999, in _apply_breaks
        self.breaks(self.score['Global_Skips'])
        File "/Users/trevorbaca/baca/baca/spacing.py", line 319, in __call__
        raise Exception(message)
    Exception: score ends at measure 6 (not 11).

..  container:: example exception

    Exception 3. Page specifier factory function raises exception when system specifier
    Y-offsets overlap:

    >>> baca.page(
    ...     baca.system(measure=1, y_offset=60, distances=(20, 20)),
    ...     baca.system(measure=4, y_offset=60, distances=(20, 20)),
    ...     number=1,
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


class SpacingSpecifier:
    """
    Spacing specifier.
    """

    ### CLASS VARIABLES ###

    magic_lilypond_eol_adjustment = abjad.Multiplier(35, 24)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        eol_measure_numbers=None,
        fermata_measure_numbers=None,
        fermata_measure_duration=(1, 4),
        measure_count=None,
        measures=None,
        minimum_duration=None,
    ):
        self.eol_measure_numbers = eol_measure_numbers or []
        if fermata_measure_numbers is not None:
            assert all(isinstance(_, int) for _ in fermata_measure_numbers)
        self.fermata_measure_numbers = fermata_measure_numbers or []
        duration_ = None
        if fermata_measure_duration is not None:
            duration_ = abjad.Duration(fermata_measure_duration)
        self.fermata_measure_duration = duration_
        if measure_count is not None:
            assert isinstance(measure_count, int)
            assert 0 <= measure_count
        self.measure_count = measure_count
        if minimum_duration is not None:
            minimum_duration = abjad.Duration(minimum_duration)
        self.minimum_duration = minimum_duration
        if measures is not None:
            assert isinstance(measures, dict), repr(measures)
        else:
            measures = {}
        self.measures = measures

    ### SPECIAL METHODS ###

    def __call__(self, segment_maker=None):
        """
        Calls spacing specifier on ``segment_maker``.
        """
        score = segment_maker.score
        skips = _classes.Selection(score["Global_Skips"]).skips()
        programmatic = True
        if self.measures and len(self.measures) == len(skips):
            programmatic = False
        if programmatic:
            leaves = abjad.iterate(score).leaves(grace=False)
            method = self._get_minimum_durations_by_measure
            minimum_durations_by_measure = method(skips, leaves)
        else:
            minimum_durations_by_measure = []
        measure_count = len(skips)
        for measure_index, skip in enumerate(skips):
            measure_number = measure_index + 1
            duration, eol_adjusted, duration_ = self._calculate_duration(
                measure_number,
                minimum_durations_by_measure,
                measure_count,
            )
            spacing_section = _indicators.SpacingSection(duration=duration)
            tag = _tags.SPACING_COMMAND
            abjad.attach(
                spacing_section,
                skip,
                tag=tag.append(abjad.Tag("baca.SpacingSpecifier.__call__(1)")),
            )
            if eol_adjusted:
                multiplier = self.magic_lilypond_eol_adjustment
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

    ### PRIVATE METHODS ###

    def _calculate_duration(
        self,
        measure_number,
        minimum_durations_by_measure,
        measure_count,
    ):
        if self.measures:
            duration = self.measures[measure_number]
            duration = abjad.NonreducedFraction(duration)
        else:
            duration = minimum_durations_by_measure[measure_number - 1]
            if self.minimum_duration is not None:
                if self.minimum_duration < duration:
                    duration = self.minimum_duration
            if measure_number == measure_count:
                duration = abjad.Duration(1, 4)
        eol_adjusted, duration_ = False, None
        if measure_number in self.eol_measure_numbers:
            duration_ = duration
            duration *= self.magic_lilypond_eol_adjustment
            eol_adjusted = True
        return duration, eol_adjusted, duration_

    def _check_measure_number(self, number):
        if number < 1:
            raise Exception(f"Nonpositive measure number ({number}) not allowed.")
        if self.measure_count < number:
            raise Exception(
                f"measure number {number} greater than"
                f" last measure number ({self.measure_count})."
            )

    def _get_minimum_durations_by_measure(self, skips, leaves):
        measure_timespans = []
        durations_by_measure = []
        for skip in skips:
            measure_timespan = abjad.get.timespan(skip)
            measure_timespans.append(measure_timespan)
            durations_by_measure.append([])
        leaf_timespans = set()
        leaf_count = 0
        for leaf in leaves:
            leaf_timespan = abjad.get.timespan(leaf)
            leaf_duration = leaf_timespan.duration
            if leaf.multiplier is not None:
                leaf_duration = leaf_duration / leaf.multiplier
            pair = (leaf_timespan, leaf_duration)
            leaf_timespans.add(pair)
            leaf_count += 1
        measure_index = 0
        measure_timespan = measure_timespans[measure_index]
        leaf_timespans = list(leaf_timespans)
        leaf_timespans.sort(key=lambda _: _[0].start_offset)
        start_offset = 0
        for pair in leaf_timespans:
            leaf_timespan, leaf_duration = pair
            assert start_offset <= leaf_timespan.start_offset
            start_offset = leaf_timespan.start_offset
            if leaf_timespan.starts_during_timespan(measure_timespan):
                durations_by_measure[measure_index].append(leaf_duration)
            else:
                measure_index += 1
                if len(measure_timespans) <= measure_index:
                    continue
                measure_timespan = measure_timespans[measure_index]
                assert leaf_timespan.starts_during_timespan(measure_timespan)
                durations_by_measure[measure_index].append(leaf_duration)
        minimum_durations_by_measure = [min(_) for _ in durations_by_measure]
        return minimum_durations_by_measure

    ### PUBLIC METHODS ###

    def add_override(self, measures, pair):
        """
        Overrides ``measures`` with spacing ``pair``.
        """
        measures_ = []
        duration = abjad.NonreducedFraction(pair)
        if isinstance(measures, int):
            self._check_measure_number(measures)
            self.measures[measures] = duration
            measures_.append(measures)
        elif isinstance(measures, tuple):
            assert len(measures) == 2, repr(measures)
            start_measure, stop_measure = measures
            self._check_measure_number(start_measure)
            self._check_measure_number(stop_measure)
            for number in range(start_measure, stop_measure + 1):
                self.measures[number] = duration
                measures_.append(number)
        elif isinstance(measures, list):
            for measure in measures:
                self._check_measure_number(measure)
                self.measures[measure] = duration
                measures_.append(measure)
        else:
            raise TypeError(f"measures must be int, pair or list (not {measures!r}).")


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
            assert isinstance(alignment_distances, collections.abc.Iterable)
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

    def __init__(
        self,
        *,
        number=None,
        systems=None,
    ):
        if number is not None:
            assert isinstance(number, int), repr(number)
            assert 1 <= number, repr(number)
        self.number = number
        if systems is not None:
            y_offsets: list = []
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


def minimum_duration(duration):
    """
    Makes spacing specifier with ``duration`` minimum width.
    """
    return SpacingSpecifier(minimum_duration=duration)


def page(*systems, number=None):
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
