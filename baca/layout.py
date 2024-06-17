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


class Breaks:

    __slots__ = ("bol_measure_numbers", "page_count", "skip_index_to_indicators")

    def __init__(self, *pages: "Page"):
        triple = self._initialize(pages)
        bol_measure_numbers, page_count, skip_index_to_indicators = triple
        self.bol_measure_numbers = bol_measure_numbers
        self.page_count = page_count
        self.skip_index_to_indicators = skip_index_to_indicators

    def __call__(self, score):
        assert isinstance(score, abjad.Score), repr(score)
        context = score["Skips"]
        skips = _select.skips(context)
        measure_count = len(skips)
        literal = abjad.LilyPondLiteral(r"\autoPageBreaksOff", site="before")
        abjad.attach(
            literal,
            skips[0],
            tag=_tags.BREAK.append(_helpers.function_name(_frame(), n=1)),
        )
        for skip_index in range(measure_count):
            skip = skips[skip_index]
            indicators = self.skip_index_to_indicators.get(
                skip_index,
                [abjad.LilyPondLiteral(r"\noBreak", site="before")],
            )
            for indicator in indicators:
                abjad.attach(
                    indicator,
                    skip,
                    tag=_tags.BREAK.append(_helpers.function_name(_frame(), n=2)),
                )

    @staticmethod
    def _initialize(pages):
        page_count = len(pages)
        assert 0 < page_count, repr(page_count)
        first_system = pages[0].systems[0]
        assert first_system.measure == 1, repr(first_system)
        bol_measure_numbers = []
        skip_index_to_indicators = {}
        for i, page in enumerate(pages):
            page_number = i + 1
            if page.number is not None:
                if page.number != page_number:
                    message = f"page number ({page.number}) is not {page_number}."
                    raise Exception(message)
            for j, system in enumerate(page.systems):
                measure_number = system.measure
                bol_measure_numbers.append(measure_number)
                skip_index = measure_number - 1
                assert 0 <= skip_index
                if j == 0:
                    literal = abjad.LilyPondLiteral(r"\pageBreak", site="before")
                else:
                    literal = abjad.LilyPondLiteral(r"\break", site="before")
                alignment_distances = abjad.sequence.flatten(system.distances, depth=-1)
                lbsd = LBSD(
                    alignment_distances=alignment_distances,
                    y_offset=system.y_offset,
                    x_offset=system.x_offset,
                )
                skip_index_to_indicators[skip_index] = (literal, lbsd)
        return bol_measure_numbers, page_count, skip_index_to_indicators


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


class Page:

    __slots__ = ("number", "systems")

    def __init__(self, number: int, *systems):
        assert isinstance(number, int), repr(number)
        self.number = number
        assert all(isinstance(_, System) for _ in systems), repr(systems)
        self.systems = list(systems)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class PageLayoutProfile:

    eol_measure_numbers: list[int]
    fermata_measure_numbers: list[int]
    measure_count: int

    def __post_init__(self):
        assert isinstance(self.eol_measure_numbers, list)
        assert isinstance(self.fermata_measure_numbers, list)
        assert isinstance(self.measure_count, int)


class Spacing:

    __slots__ = (
        "default",
        "forbid_new_spacing_section",
        "lax_spacing_section",
        "overrides",
    )

    def __init__(
        self,
        default: tuple[int, int],
        forbid_new_spacing_section: list[int] | None = None,
        lax_spacing_section: list[int] | None = None,
        overrides: list["Override"] | None = None,
    ):
        assert isinstance(default, tuple), repr(default)
        self.default = default
        self.forbid_new_spacing_section = forbid_new_spacing_section or []
        self.lax_spacing_section = lax_spacing_section or []
        self.overrides = overrides

    def __call__(self, score, page_layout_profile, *, has_anchor_skip=False):
        skips_context = score["Skips"]
        skips = _select.skips(skips_context)
        measure_count = page_layout_profile.measure_count or len(skips)
        fermata_measure_numbers = page_layout_profile.fermata_measure_numbers or []
        eol_measure_numbers = page_layout_profile.eol_measure_numbers or []
        measures = {}
        for n in range(1, measure_count + 1):
            if n in fermata_measure_numbers:
                measures[n] = fermata_measure_duration
            else:
                measures[n] = self.default
            measures[n + 1] = fermata_measure_duration
        for override in self.overrides or []:
            token = override.measures
            duration = override.duration
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
            pair = None
            if has_anchor_skip and measure_number == measure_count:
                pair = (1, 4)
            elif measures:
                item = measures[measure_number]
                if isinstance(item, tuple):
                    pair = item
                else:
                    assert isinstance(item, abjad.Duration), repr(item)
                    pair = item.pair
            else:
                pair = self.default
            assert isinstance(pair, tuple), repr(pair)
            eol_adjusted = False
            if (measure_number in eol_measure_numbers) or (
                measure_number == measure_count and not has_anchor_skip
            ):
                pair_ = pair
                numerator = pair[0] * magic_lilypond_eol_adjustment.numerator
                denominator = pair[1] * magic_lilypond_eol_adjustment.denominator
                pair = numerator, denominator
                eol_adjusted = True
            forbid_new_spacing_section = False
            if measure_number in self.forbid_new_spacing_section:
                forbid_new_spacing_section = True
            spacing_section = SpacingSection(
                pair=pair,
                forbid_new_spacing_section=forbid_new_spacing_section,
                lax_spacing_section=measure_number in self.lax_spacing_section,
            )
            tag = _tags.SPACING_COMMAND
            abjad.attach(
                spacing_section,
                skip,
                tag=tag.append(_helpers.function_name(_frame(), n=1)),
            )
            if forbid_new_spacing_section is True:
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
                    skip,
                    context=skips_context.name,
                    deactivate=True,
                    tag=tag.append(_helpers.function_name(_frame(), n=2)),
                )
            if 0 < measure_index:
                tag = _tags.SPACING
                stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanSPM")
                abjad.attach(
                    stop_text_span,
                    skip,
                    context=skips_context.name,
                    deactivate=True,
                    tag=tag.append(_helpers.function_name(_frame(), n=3)),
                )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class SpacingSection:

    pair: tuple[int, int]
    forbid_new_spacing_section: bool = False
    lax_spacing_section: bool = False

    context: typing.ClassVar[str] = "Score"
    persistent: typing.ClassVar[bool] = True

    def __post_init__(self):
        assert isinstance(self.pair, tuple), repr(self.pair)

    def _get_contributions(self, leaf=None):
        contributions = abjad.ContributionsBySite()
        if self.forbid_new_spacing_section is True:
            pass
        elif self.lax_spacing_section is True:
            numerator, denominator = self.pair
            string = rf"\baca-new-lax-spacing-section #{numerator} #{denominator}"
            contributions.before.commands.append(string)
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
