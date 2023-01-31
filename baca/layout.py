r"""
Layout.

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

"""
import collections
import dataclasses
from inspect import currentframe as _frame

import abjad

from . import indicatorclasses as _indicatorclasses
from . import select as _select
from . import tags as _tags

# TODO: apply magic_lilypond_eol_adjustment to last measure in all doc examples
magic_lilypond_eol_adjustment = abjad.Fraction(35, 24)

fermata_measure_duration = abjad.Duration(1, 4)


class SpacingSpecifier:
    """
    Spacing specifier.
    """

    def __init__(
        self,
        fallback_duration=None,
        *,
        breaks=None,
        overrides=None,
    ):
        if breaks is not None:
            assert isinstance(breaks, BreakMeasureMap), repr(breaks)
        self.breaks = breaks
        if fallback_duration is not None:
            fallback_duration = abjad.Duration(fallback_duration)
        self.fallback_duration = fallback_duration
        self.overrides = overrides

    def __call__(self, score, page_layout_profile=None, *, has_anchor_skip=False):
        if self.fallback_duration is None:
            return
        page_layout_profile = page_layout_profile or {}
        skips = _select.skips(score["Skips"])
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
                duration = self.fallback_duration
                assert isinstance(duration, abjad.Duration), repr(duration)
                pair = duration.pair
            assert pair is not None
            eol_adjusted = False
            if measure_number in eol_measure_numbers:
                pair_ = pair
                numerator = pair[0] * magic_lilypond_eol_adjustment.numerator
                denominator = pair[1] * magic_lilypond_eol_adjustment.denominator
                pair = numerator, denominator
                eol_adjusted = True
            spacing_section = _indicatorclasses.SpacingSection(pair=pair)
            tag = _tags.SPACING_COMMAND
            abjad.attach(
                spacing_section,
                skip,
                tag=tag.append(_tags.function_name(_frame(), self, n=1)),
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
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag.append(_tags.function_name(_frame(), self, n=2)),
                )
            if 0 < measure_index:
                tag = _tags.SPACING
                stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanSPM")
                abjad.attach(
                    stop_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag.append(_tags.function_name(_frame(), self, n=3)),
                )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class LBSD:
    """
    Line-break system details.
    """

    y_offset: int
    alignment_distances: tuple

    def _get_contributions(self, component=None):
        contributions = abjad.ContributionsBySite()
        alignment_distances = " ".join(str(_) for _ in self.alignment_distances)
        string = rf"\baca-lbsd #{self.y_offset} #'({alignment_distances})"
        contributions.before.commands.append(string)
        return contributions


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class PageSpecifier:
    """
    Page specifier.
    """

    number: int
    systems: list


def make_skip_selector(n):
    def selector(argument):
        return _select.skip(argument, n)

    return selector


def breaks(*page_specifiers):
    """
    Makes break measure map.
    """
    page_count = len(page_specifiers)
    assert 0 < page_count, repr(page_count)
    first_system = page_specifiers[0].systems[0]
    assert first_system.measure == 1, repr(first_system)
    bol_measure_numbers = []
    skip_index_to_indicators = {}
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
            if j == 0:
                literal = abjad.LilyPondLiteral(r"\pageBreak")
            else:
                literal = abjad.LilyPondLiteral(r"\break")
            alignment_distances = abjad.sequence.flatten(alignment_distances, depth=-1)
            lbsd = LBSD(alignment_distances=alignment_distances, y_offset=y_offset)
            skip_index_to_indicators[skip_index] = (literal, lbsd)
    breaks = BreakMeasureMap(
        bol_measure_numbers=bol_measure_numbers,
        page_count=page_count,
        skip_index_to_indicators=skip_index_to_indicators,
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
    ["bol_measure_numbers", "page_count", "skip_index_to_indicators"],
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
