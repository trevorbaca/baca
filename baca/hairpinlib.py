"""
hairpinlib.py.
"""

import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import dynamics as _dynamics
from . import helpers as _helpers
from . import indicatorlib as _indicatorlib
from . import scope as _scope
from . import tweaks as _tweaks
from . import typings as _typings


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class HairpinSpecifier:
    # TODO: should only be abjad.Dynamic:
    indicator: abjad.Dynamic | abjad.StartHairpin | abjad.StopHairpin | None = None
    spanner_start: abjad.Bundle | abjad.StartHairpin | None = None
    spanner_stop: abjad.StopHairpin | None = None

    def __iter__(self) -> typing.Iterator:
        result: list = []
        if self.spanner_stop:
            result.append(self.spanner_stop)
        if self.indicator:
            result.append(self.indicator)
        if self.spanner_start:
            result.append(self.spanner_start)
        return iter(result)

    def __post_init__(self):
        if self.indicator is not None:
            assert isinstance(self.indicator, abjad.Dynamic), repr(self.indicator)
        if self.spanner_start is not None:
            assert isinstance(self.spanner_start, abjad.Bundle | abjad.StartHairpin)
            indicator = _indicatorlib.unbundle_indicator(self.spanner_start)
            assert isinstance(indicator, abjad.StartHairpin), repr(self.spanner_start)
        if self.spanner_stop is not None:
            assert isinstance(self.spanner_stop, abjad.StopHairpin)

    def attach_items(
        self,
        leaf,
        current_piece_index,
        tag,
        tweaks,
        total_pieces,
        *,
        is_left_broken_first_piece: bool = False,
        is_right_broken_final_piece: bool = False,
        just_bookended_leaf: abjad.Leaf | None = None,
    ) -> list[abjad.Wrapper]:
        assert isinstance(leaf, abjad.Leaf), repr(leaf)
        assert isinstance(current_piece_index, int), repr(current_piece_index)
        assert isinstance(tag, abjad.Tag), repr(tag)
        assert isinstance(tweaks, tuple), repr(tweaks)
        assert isinstance(total_pieces, int), repr(total_pieces)
        assert isinstance(just_bookended_leaf, abjad.Leaf | type(None))
        wrappers = []
        prototype = (abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin)
        for item in self:
            indicator = _indicatorlib.unbundle_indicator(item)
            assert isinstance(indicator, prototype), repr(item)
            if leaf is just_bookended_leaf and not isinstance(
                indicator, abjad.StartHairpin
            ):
                continue
            if isinstance(indicator, abjad.StartHairpin):
                item = _tweaks.bundle_tweaks(
                    item,
                    tweaks,
                    i=current_piece_index,
                    total=total_pieces,
                    overwrite=True,
                )
            left_broken, right_broken = False, False
            if is_left_broken_first_piece and isinstance(indicator, abjad.StartHairpin):
                left_broken = True
            if is_right_broken_final_piece and isinstance(indicator, abjad.StopHairpin):
                right_broken = True
            wrapper = _indicatorlib.attach_persistent_indicator(
                leaf,
                item,
                left_broken=left_broken,
                right_broken=right_broken,
                tag=tag,
            )
            wrappers.append(wrapper)
        return wrappers


def iterate_hairpin_pieces(
    pieces,
    *tweaks: _typings.IndexedTweak,
    debug: bool = False,
    do_not_bookend: bool = False,
    bound_details_right_padding: int | float | None = None,
    do_not_start_spanner_on_final_piece: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    specifiers: typing.Sequence = (),
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    assert isinstance(tweaks, tuple), repr(tweaks)
    for tweak in tweaks:
        assert isinstance(tweak, abjad.Tweak | tuple), repr(tweak)
    assert pieces is not None
    assert isinstance(do_not_bookend, bool), repr(do_not_bookend)
    bookend = not do_not_bookend
    assert isinstance(do_not_start_spanner_on_final_piece, bool)
    assert isinstance(left_broken, bool), repr(left_broken)
    assert isinstance(pieces, list | _scope.DynamicScope), repr(pieces)
    piece_prototype = (
        list,
        abjad.Container,
        abjad.LogicalTie,
        abjad.Note,
        _scope.DynamicScope,
    )
    for piece in pieces:
        assert isinstance(piece, piece_prototype), repr(piece)
    assert isinstance(right_broken, bool), repr(right_broken)
    assert isinstance(specifiers, list), repr(specifiers)
    assert all(isinstance(_, HairpinSpecifier) for _ in specifiers), repr(specifiers)
    assert isinstance(staff_padding, int | float | type(None)), repr(staff_padding)
    cyclic_specifiers = abjad.CyclicTuple(specifiers)
    if bound_details_right_padding is not None:
        string = rf"- \tweak bound-details.right.padding {bound_details_right_padding}"
        tweaks = tweaks + (abjad.Tweak(string),)
    if staff_padding is not None:
        tweaks = tweaks + (abjad.Tweak(rf"- \tweak staff-padding {staff_padding}"),)
    total_pieces = len(pieces)
    assert 0 < total_pieces, repr(total_pieces)
    just_backstole_right_text = False
    just_bookended_leaf = None
    wrappers = []
    for current_piece_index, piece in enumerate(pieces):
        is_first_piece = current_piece_index == 0
        is_left_broken_first_piece = False
        is_final_piece = current_piece_index == total_pieces - 1
        is_right_broken_final_piece = False
        start_leaf = abjad.select.leaf(piece, 0)
        stop_leaf = abjad.select.leaf(piece, -1)
        specifier = cyclic_specifiers[current_piece_index]
        if (
            bookend is True
            and is_final_piece
            and right_broken is False
            and do_not_start_spanner_on_final_piece is False
            and not isinstance(piece, abjad.Leaf)
            and 1 < len(piece)
        ):
            should_bookend = True
        else:
            should_bookend = False
        if is_final_piece and just_backstole_right_text:
            specifier = dataclasses.replace(specifier, spanner_start=None)
        next_specifier = cyclic_specifiers[current_piece_index + 1]
        if (
            is_final_piece
            and specifier.spanner_start
            and do_not_start_spanner_on_final_piece is True
        ):
            specifier = dataclasses.replace(specifier, spanner_start=None)
        tag_ = _helpers.function_name(_frame(), n=1)
        if is_first_piece:
            specifier = dataclasses.replace(specifier, spanner_stop=None)
        if is_first_piece and left_broken:
            is_left_broken_first_piece = True
        if is_final_piece and right_broken:
            is_right_broken_final_piece = True
        wrappers_ = specifier.attach_items(
            start_leaf,
            current_piece_index,
            tag_,
            tweaks,
            total_pieces,
            is_left_broken_first_piece=is_left_broken_first_piece,
            is_right_broken_final_piece=is_right_broken_final_piece,
            just_bookended_leaf=just_bookended_leaf,
        )
        wrappers.extend(wrappers_)
        if should_bookend:
            if next_specifier.indicator and next_specifier.spanner_start:
                next_specifier = dataclasses.replace(next_specifier, spanner_start=None)
            wrappers_ = next_specifier.attach_items(
                stop_leaf,
                current_piece_index,
                _helpers.function_name(_frame(), n=2),
                tweaks,
                total_pieces,
            )
            wrappers.extend(wrappers_)
            just_bookended_leaf = stop_leaf
        elif (
            is_final_piece
            and not just_backstole_right_text
            and next_specifier.spanner_stop
            and (start_leaf is not stop_leaf)
        ):
            spanner_stop = dataclasses.replace(next_specifier.spanner_stop)
            specifier = HairpinSpecifier(spanner_stop=spanner_stop)
            tag_ = _helpers.function_name(_frame(), n=3)
            if right_broken:
                is_right_broken_final_piece = True
            wrappers_ = specifier.attach_items(
                stop_leaf,
                current_piece_index,
                tag_,
                tweaks,
                total_pieces,
                is_right_broken_final_piece=is_right_broken_final_piece,
            )
            wrappers.extend(wrappers_)
    return wrappers


def parse_hairpin_descriptor(
    descriptor: str,
    forbid_al_niente_to_bar_line: bool = False,
) -> list[HairpinSpecifier]:
    assert isinstance(descriptor, str), repr(descriptor)
    indicators = []
    specifiers = []
    indicator: (
        str | abjad.Dynamic | abjad.StartHairpin | abjad.StopHairpin | abjad.Bundle
    )
    for string in descriptor.split():
        if string == "-":
            indicator = "-"
        else:
            indicator = _dynamics.make_dynamic(
                string, forbid_al_niente_to_bar_line=forbid_al_niente_to_bar_line
            )
        indicators.append(indicator)
    # TODO: does this duplicate len(indicators) == 1 branch below?
    if len(indicators) == 1:
        indicator = indicators[0]
        if _indicatorlib.is_maybe_bundled(indicator, abjad.StartHairpin):
            assert isinstance(indicator, abjad.StartHairpin | abjad.Bundle)
            specifier = HairpinSpecifier(spanner_start=indicator)
        elif _indicatorlib.is_maybe_bundled(indicator, abjad.StopHairpin):
            assert isinstance(indicator, abjad.StopHairpin), repr(indicator)
            specifier = HairpinSpecifier(spanner_stop=indicator)
        else:
            assert _indicatorlib.is_maybe_bundled(indicator, abjad.Dynamic)
            assert isinstance(indicator, abjad.Dynamic), repr(indicator)
            specifier = HairpinSpecifier(indicator=indicator)
        specifiers.append(specifier)
        return specifiers
    if _indicatorlib.is_maybe_bundled(indicators[0], abjad.StartHairpin):
        result = indicators.pop(0)
        assert _indicatorlib.is_maybe_bundled(result, abjad.StartHairpin)
        assert isinstance(result, abjad.StartHairpin | abjad.Bundle)
        specifier = HairpinSpecifier(spanner_start=result)
        specifiers.append(specifier)
    # TODO: does this duplicate len(indicators) == 1 branch above?
    if len(indicators) == 1:
        indicator = indicators[0]
        if _indicatorlib.is_maybe_bundled(indicator, abjad.StartHairpin):
            assert isinstance(indicator, abjad.StartHairpin)
            specifier = HairpinSpecifier(spanner_start=indicator)
        elif isinstance(indicator, abjad.Dynamic):
            specifier = HairpinSpecifier(indicator=indicator)
        else:
            assert isinstance(indicator, abjad.StopHairpin)
            specifier = HairpinSpecifier(spanner_stop=indicator)
        specifiers.append(specifier)
        return specifiers
    for left, right in abjad.sequence.nwise(indicators):
        if _indicatorlib.is_maybe_bundled(
            left, abjad.StartHairpin
        ) and _indicatorlib.is_maybe_bundled(right, abjad.StartHairpin):
            raise Exception("consecutive start hairpin commands.")
        elif _indicatorlib.is_maybe_bundled(
            left, abjad.Dynamic
        ) and _indicatorlib.is_maybe_bundled(right, abjad.Dynamic):
            specifier = HairpinSpecifier(indicator=left)
            specifiers.append(specifier)
        elif _indicatorlib.is_maybe_bundled(left, abjad.Dynamic) and right == "-":
            specifier = HairpinSpecifier(indicator=left)
            specifiers.append(specifier)
        elif left == "-" and _indicatorlib.is_maybe_bundled(right, abjad.StartHairpin):
            specifier = HairpinSpecifier(spanner_start=right)
            specifiers.append(specifier)
        elif left == "-" and _indicatorlib.is_maybe_bundled(right, abjad.StopHairpin):
            specifier = HairpinSpecifier(spanner_stop=right)
            specifiers.append(specifier)
        elif _indicatorlib.is_maybe_bundled(
            left, abjad.Dynamic
        ) and _indicatorlib.is_maybe_bundled(right, abjad.StartHairpin):
            specifier = HairpinSpecifier(indicator=left, spanner_start=right)
            specifiers.append(specifier)
        elif _indicatorlib.is_maybe_bundled(
            left, abjad.StopHairpin
        ) and _indicatorlib.is_maybe_bundled(right, abjad.StartHairpin):
            specifier = HairpinSpecifier(spanner_stop=left, spanner_start=right)
            specifiers.append(specifier)
    if indicators:
        final_indicator = indicators[-1]
        if isinstance(final_indicator, abjad.Dynamic):
            specifier = HairpinSpecifier(indicator=final_indicator)
            specifiers.append(specifier)
        elif isinstance(final_indicator, abjad.StopHairpin):
            specifier = HairpinSpecifier(spanner_stop=final_indicator)
            specifiers.append(specifier)
        else:
            pass
    return specifiers
