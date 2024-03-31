"""
Layout.
"""

import dataclasses
from inspect import currentframe as _frame

import abjad

from . import classes as _classes
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
                    message = f"page number ({page.number})"
                    message += f" is not {page_number}."
                    raise Exception(message)
            for j, system in enumerate(page.systems):
                measure_number = system.measure
                bol_measure_numbers.append(measure_number)
                skip_index = measure_number - 1
                y_offset = system.y_offset
                assert isinstance(system.distances, tuple | list), repr(
                    system.distances
                )
                alignment_distances = system.distances
                assert 0 <= skip_index
                if j == 0:
                    literal = abjad.LilyPondLiteral(r"\pageBreak", site="before")
                else:
                    literal = abjad.LilyPondLiteral(r"\break", site="before")
                alignment_distances = abjad.sequence.flatten(
                    alignment_distances, depth=-1
                )
                lbsd = LBSD(alignment_distances=alignment_distances, y_offset=y_offset)
                skip_index_to_indicators[skip_index] = (literal, lbsd)
        return bol_measure_numbers, page_count, skip_index_to_indicators


class Layout:

    __slots__ = ("breaks", "spacing")

    def __init__(
        self,
        *pages: "Page",
        default_spacing: abjad.Duration | tuple[int, int] | None = None,
        spacing_overrides: list["Override"] | None = None,
    ):
        self.breaks = Breaks(*pages)
        self.spacing = Spacing(default_spacing, spacing_overrides)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class LBSD:

    y_offset: int
    alignment_distances: tuple

    def _get_contributions(self, component=None):
        contributions = abjad.ContributionsBySite()
        alignment_distances = " ".join(str(_) for _ in self.alignment_distances)
        string = rf"\baca-lbsd #{self.y_offset} #'({alignment_distances})"
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


class Spacing:

    __slots__ = ("default_spacing", "spacing_overrides")

    def __init__(
        self,
        default_spacing: abjad.Duration | tuple[int, int] | None = None,
        spacing_overrides: list["Override"] | None = None,
    ):
        if default_spacing is not None:
            default_spacing = abjad.Duration(default_spacing)
        self.default_spacing = default_spacing
        self.spacing_overrides = spacing_overrides

    def __call__(self, score, page_layout_profile=None, *, has_anchor_skip=False):
        if self.default_spacing is None:
            return
        page_layout_profile = page_layout_profile or {}
        skips_context = score["Skips"]
        skips = _select.skips(skips_context)
        measure_count = page_layout_profile.get("measure_count") or len(skips)
        fermata_measure_numbers = page_layout_profile.get("fermata_measure_numbers", [])
        eol_measure_numbers = page_layout_profile.get("eol_measure_numbers", [])
        measures = {}
        for n in range(1, measure_count + 1):
            if n in fermata_measure_numbers:
                measures[n] = fermata_measure_duration
            else:
                measures[n] = self.default_spacing
            measures[n + 1] = fermata_measure_duration
        for override in self.spacing_overrides or []:
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
                elif item is False:
                    pair = "ZEBRA"
                else:
                    assert isinstance(item, abjad.Duration), repr(item)
                    pair = item.pair
            else:
                duration = self.default_spacing
                assert isinstance(duration, abjad.Duration), repr(duration)
                pair = duration.pair
            assert pair is not None
            eol_adjusted = False
            if (measure_number in eol_measure_numbers) or (
                measure_number == measure_count and not has_anchor_skip
            ):
                pair_ = pair
                numerator = pair[0] * magic_lilypond_eol_adjustment.numerator
                denominator = pair[1] * magic_lilypond_eol_adjustment.denominator
                pair = numerator, denominator
                eol_adjusted = True
            spacing_section = _classes.SpacingSection(pair=pair)
            tag = _tags.SPACING_COMMAND
            abjad.attach(
                spacing_section,
                skip,
                tag=tag.append(_helpers.function_name(_frame(), n=1)),
            )
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
class System:

    measure: int
    y_offset: int
    distances: tuple[int, ...]
