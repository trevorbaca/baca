"""
Layout.
"""

import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import select as _select
from . import tags as _tags

magic_lilypond_eol_adjustment = abjad.Fraction(35, 24)

fermata_measure_duration = abjad.Duration(1, 4)


@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class Breaks:

    pages: list["Page"] = dataclasses.field(default_factory=list)

    def __init__(self, *arguments: "Page"):
        for page_number, argument in enumerate(arguments, start=1):
            assert isinstance(argument, Page), repr(argument)
            if argument.number != page_number:
                message = f"page number ({argument.number}) is not {page_number}"
                raise Exception(message)
        self.pages = list(arguments)

    def _iterate_pages(self):
        first_system = self.pages[0].systems[0]
        assert first_system.measure == 1, repr(first_system)
        bol_measure_numbers = []
        skip_index_to_indicators = {}
        for page in self.pages:
            for j, system in enumerate(page.systems):
                measure_number, indicators = system.measure, []
                bol_measure_numbers.append(measure_number)
                skip_index = measure_number - 1
                assert 0 <= skip_index
                if j == 0 and 1 < page.number:
                    literal = abjad.LilyPondLiteral(r"\pageBreak", site="before")
                    indicators.append(literal)
                elif 0 < j:
                    literal = abjad.LilyPondLiteral(r"\break", site="before")
                    indicators.append(literal)
                alignment_distances = abjad.sequence.flatten(system.distances, depth=-1)
                lbsd = LBSD(
                    alignment_distances=alignment_distances,
                    y_offset=system.y_offset,
                    x_offset=system.x_offset,
                )
                indicators.append(lbsd)
                skip_index_to_indicators[skip_index] = indicators
        return bol_measure_numbers, skip_index_to_indicators

    def attach_indicators(self, context):
        assert context.name == "Breaks"
        abjad.attach(
            abjad.LilyPondLiteral(r"\autoLineBreaksOff", site="before"),
            context[0],
            tag=None,
        )
        abjad.attach(
            abjad.LilyPondLiteral(r"\autoPageBreaksOff", site="before"),
            context[0],
            tag=None,
        )
        _, skip_index_to_indicators = self._iterate_pages()
        for i, skip in enumerate(context):
            indicators = skip_index_to_indicators.get(i, [])
            for indicator in indicators:
                abjad.attach(
                    indicator,
                    skip,
                    tag=None,
                )

    def bol_measure_numbers(self):
        bol_measure_numbers, _ = self._iterate_pages()
        return bol_measure_numbers


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class LBSD:

    y_offset: int
    alignment_distances: tuple
    x_offset: int | None = None

    def _get_contributions(self, component=None):
        contributions = abjad.ContributionsBySite()
        alignment_distances = " ".join(str(_) for _ in self.alignment_distances)
        if self.x_offset is None:
            string = rf"\baca-lbsd #{self.y_offset}"
        else:
            string = rf"\baca-lbsd-xy #{self.x_offset} #{self.y_offset}"
        string += f" #'({alignment_distances})"
        contributions.before.commands.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Override:

    measures: int | tuple[int, int] | list
    duration: tuple[int, int]


@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class Page:

    number: int
    systems: list["System"] = dataclasses.field(default_factory=list)

    def __init__(self, number: int, *systems):
        assert isinstance(number, int), repr(number)
        self.number = number
        assert all(isinstance(_, System) for _ in systems), repr(systems)
        self.systems = list(systems)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Spacing:

    default: tuple[int, int]
    annotate_spacing: bool = False
    empty_spacing_sections: list[int] = dataclasses.field(default_factory=list)
    lax_spacing_sections: list[int] = dataclasses.field(default_factory=list)
    overrides: list["Override"] = dataclasses.field(default_factory=list)
    vanilla_spacing_sections: list[int] = dataclasses.field(default_factory=list)

    def attach_indicators(
        self,
        spacing_commands_context,
        spacing_annotations_context=None,
        *,
        eol_measure_numbers=None,
        fermata_measure_numbers=None,
        has_anchor_skip=False,
        measure_count=None,
    ):
        assert spacing_commands_context.name == "SpacingCommands"
        spacing_commands_skips = _select.skips(spacing_commands_context)
        spacing_annotations_skips = _select.skips(spacing_annotations_context)
        measure_count = measure_count or len(spacing_commands_skips)
        fermata_measure_numbers = fermata_measure_numbers or []
        eol_measure_numbers = eol_measure_numbers or []
        measures = {}
        for n in range(1, measure_count + 1):
            if n in fermata_measure_numbers:
                measures[n] = fermata_measure_duration
            else:
                measures[n] = self.default
            measures[n + 1] = fermata_measure_duration
        for override in self.overrides or []:
            duration = override.duration
            measure_numbers = []
            if isinstance(override.measures, int):
                measure_numbers.append(override.measures)
            elif isinstance(override.measures, tuple):
                start, stop = override.measures
                for measure_number in range(start, stop + 1):
                    measure_numbers.append(measure_number)
            elif isinstance(override.measures, list):
                measure_numbers.extend(override.measures)
            else:
                message = f"must be int, pair, list (not {override.measures!r})."
                raise TypeError(message)
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
        measure_count = len(spacing_commands_skips)
        for measure_index in range(measure_count):
            spacing_commands_skip = spacing_commands_skips[measure_index]
            if spacing_annotations_skips:
                spacing_annotations_skip = spacing_annotations_skips[measure_index]
            measure_number = measure_index + 1
            if has_anchor_skip and measure_number == measure_count:
                pair = (1, 4)
            elif measures:
                item = measures[measure_number]
                if isinstance(item, tuple):
                    pair = item
                elif item == "vanilla":
                    pair = "vanilla"
                else:
                    assert isinstance(item, abjad.Duration), repr(item)
                    pair = item.pair
            else:
                pair = self.default
            if not isinstance(pair, tuple):
                assert pair == "vanilla"
            eol_adjusted = False
            if (measure_number in eol_measure_numbers) or (
                measure_number == measure_count and not has_anchor_skip
            ):
                pair_ = pair
                numerator = pair[0] * magic_lilypond_eol_adjustment.numerator
                denominator = pair[1] * magic_lilypond_eol_adjustment.denominator
                pair = numerator, denominator
                eol_adjusted = True
            spacing_section = SpacingSection(
                empty=measure_number in self.empty_spacing_sections,
                lax=measure_number in self.lax_spacing_sections,
                pair=pair,
                vanilla=measure_number in self.vanilla_spacing_sections,
            )
            abjad.attach(
                spacing_section,
                spacing_commands_skip,
                tag=_helpers.function_name(_frame(), n=1),
            )
            if self.annotate_spacing is False:
                continue
            if spacing_annotations_context is None:
                continue
            if measure_number in self.empty_spacing_sections:
                continue
            if measure_number in self.lax_spacing_sections:
                continue
            if measure_number in self.vanilla_spacing_sections:
                continue
            if eol_adjusted:
                multiplier = magic_lilypond_eol_adjustment
                string_ = f"[[{pair_[0]}/{pair_[1]} * {multiplier!s}]]"
            else:
                string_ = f"[{pair[0]}/{pair[1]}]"
            if measure_index < measure_count - 1:
                tag = _tags.SPACING
                string = r"- \baca-start-spm-left-only"
                string += f' "{string_}"'
                start_text_span = abjad.StartTextSpan(
                    command=r"\bacaStartTextSpanSPM", left_text=string
                )
                abjad.attach(
                    start_text_span,
                    spacing_annotations_skip,
                    context=spacing_annotations_context.name,
                    deactivate=True,
                    tag=tag.append(_helpers.function_name(_frame(), n=2)),
                )
            if 0 < measure_index:
                tag = _tags.SPACING
                stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanSPM")
                abjad.attach(
                    stop_text_span,
                    spacing_annotations_skip,
                    context=spacing_annotations_context.name,
                    deactivate=True,
                    tag=tag.append(_helpers.function_name(_frame(), n=3)),
                )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class SpacingSection:

    pair: tuple[int, int] | None = None
    empty: bool = False
    lax: bool = False
    vanilla: bool = False

    context: typing.ClassVar[str] = "Score"
    persistent: typing.ClassVar[bool] = True

    def _get_contributions(self, leaf=None):
        contributions = abjad.ContributionsBySite()
        if self.empty is True:
            pass
        elif self.lax is True:
            numerator, denominator = self.pair
            string = rf"\baca-new-lax-spacing-section #{numerator} #{denominator}"
            contributions.before.commands.append(string)
        elif self.vanilla is True:
            contributions.before.commands.append(r"\baca-new-vanilla-spacing-section")
        else:
            numerator, denominator = self.pair
            string = rf"\baca-new-strict-spacing-section #{numerator} #{denominator}"
            contributions.before.commands.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class System:

    measure: int
    y_offset: int
    distances: tuple[int, ...]
    x_offset: int | None = None


def apply_spacing_dictionary(context, spacing_dictionary):
    assert context.name == "SpacingCommands"
    for n, skip in enumerate(context, start=1):
        value = spacing_dictionary.get(n)
        if value is None:
            continue
        elif value == "vanilla":
            string = r"\baca-new-vanilla-spacing-section"
            literal = abjad.LilyPondLiteral(string, site="before")
            abjad.attach(
                literal,
                skip,
            )
        elif isinstance(value, tuple):
            n, d = value
            string = rf"\baca-new-strict-spacing-section #{n} #{d}"
            literal = abjad.LilyPondLiteral(string, site="before")
            abjad.attach(
                literal,
                skip,
            )
        elif isinstance(value, list):
            assert all(isinstance(_, str) for _ in value), repr(value)
            literal = abjad.LilyPondLiteral(value, site="before")
            abjad.attach(
                literal,
                skip,
            )
            skip._hide_body = True
