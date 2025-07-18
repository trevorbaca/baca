"""
hairpins.py.
"""

import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import dynamics as _dynamics
from . import helpers as _helpers
from . import indicatorlib as _indicatorlib
from . import indicators as _indicators
from . import scope as _scope
from . import select as _select
from . import tags as _tags


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ExactHairpinSpecifier:
    start_dynamic: abjad.Dynamic | abjad.StopHairpin | None = None
    spanner_start: abjad.StartHairpin | None = None
    stop_indicator: abjad.Dynamic | abjad.StopHairpin | None = None

    def __post_init__(self):
        if self.start_dynamic is not None:
            assert isinstance(self.start_dynamic, abjad.Dynamic | abjad.StopHairpin)
        if self.spanner_start is not None:
            assert isinstance(self.spanner_start, abjad.StartHairpin)
        if self.stop_indicator is not None:
            assert isinstance(self.stop_indicator, abjad.Dynamic | abjad.StopHairpin)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class HairpinSpecifier:
    indicator: abjad.Dynamic | None = None
    spanner_start: abjad.StartHairpin | None = None
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
            assert isinstance(self.indicator, abjad.Dynamic)
        if self.spanner_start is not None:
            assert isinstance(self.spanner_start, abjad.StartHairpin)
        if self.spanner_stop is not None:
            assert isinstance(self.spanner_stop, abjad.StopHairpin)

    def attach_indicators(
        self,
        leaf,
        current_piece_index,
        tweaks,
        total_pieces,
        *,
        is_left_broken_first_piece: bool = False,
        is_right_broken_final_piece: bool = False,
    ) -> list[abjad.wrapper.Wrapper]:
        assert isinstance(leaf, abjad.Leaf), repr(leaf)
        assert isinstance(current_piece_index, int), repr(current_piece_index)
        assert isinstance(tweaks, tuple), repr(tweaks)
        assert isinstance(total_pieces, int), repr(total_pieces)
        wrappers = []
        prototype = (abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin)
        for indicator in self:
            assert isinstance(indicator, prototype), repr(indicator)
            if isinstance(indicator, abjad.StartHairpin):
                indicator = _helpers.bundle_tweaks(
                    indicator,
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
                indicator,
                left_broken=left_broken,
                right_broken=right_broken,
            )
            wrappers.append(wrapper)
        _tags.tag(wrappers, _helpers.function_name(_frame()))
        return wrappers


def _bookend_final_cyclic_piece(
    final_leaf, next_specifier, current_piece_index, tweaks, total_pieces
):
    wrappers_ = next_specifier.attach_indicators(
        final_leaf,
        current_piece_index,
        tweaks,
        total_pieces,
    )
    _tags.tag(wrappers_, _helpers.function_name(_frame()))
    return wrappers_


def _iterate_cyclic_hairpin_pieces(
    pieces: list,
    *tweaks: abjad.Tweak,
    do_not_bookend: bool = False,
    do_not_start_spanner_on_final_piece: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    specifiers: list[HairpinSpecifier] | None = None,
) -> list[abjad.wrapper.Wrapper]:
    assert isinstance(pieces, list), repr(pieces)
    assert isinstance(tweaks, tuple), repr(tweaks)
    assert isinstance(do_not_bookend, bool), repr(do_not_bookend)
    assert isinstance(do_not_start_spanner_on_final_piece, bool)
    assert isinstance(left_broken, bool), repr(left_broken)
    assert isinstance(pieces, list | _scope.DynamicScope), repr(pieces)
    assert isinstance(right_broken, bool), repr(right_broken)
    assert isinstance(specifiers, list), repr(specifiers)
    assert all(isinstance(_, HairpinSpecifier) for _ in specifiers), repr(specifiers)
    cyclic_specifiers = abjad.CyclicTuple(specifiers)
    total_pieces = len(pieces)
    assert 0 < total_pieces, repr(total_pieces)
    wrappers = []
    for current_piece_index, piece in enumerate(pieces):
        is_first_piece = current_piece_index == 0
        is_final_piece = current_piece_index == total_pieces - 1
        is_left_broken_first_piece = False
        is_right_broken_final_piece = False
        specifier = cyclic_specifiers[current_piece_index]
        if (
            is_final_piece
            and specifier.spanner_start
            and do_not_start_spanner_on_final_piece is True
        ):
            specifier = dataclasses.replace(specifier, spanner_start=None)
        if is_first_piece and left_broken:
            is_left_broken_first_piece = True
        if is_final_piece and right_broken:
            is_right_broken_final_piece = True
        start_leaf = abjad.select.leaf(piece, 0)
        wrappers_ = specifier.attach_indicators(
            start_leaf,
            current_piece_index,
            tweaks,
            total_pieces,
            is_left_broken_first_piece=is_left_broken_first_piece,
            is_right_broken_final_piece=is_right_broken_final_piece,
        )
        wrappers.extend(wrappers_)
        if is_final_piece is True and do_not_bookend is False:
            if right_broken is True:
                raise Exception("do not bookend on right-broken hairpin")
            if isinstance(piece, abjad.Leaf):
                raise Exception(piece)
            if len(piece) == 1:
                raise Exception(f"do not booked length-1 piece: {piece}.")
            next_specifier = cyclic_specifiers[current_piece_index + 1]
            next_specifier = dataclasses.replace(next_specifier, spanner_start=None)
            assert next_specifier.spanner_start is None, repr(next_specifier)
            final_leaf = abjad.select.leaf(piece, -1)
            wrappers_ = _bookend_final_cyclic_piece(
                final_leaf,
                next_specifier,
                current_piece_index,
                tweaks,
                total_pieces,
            )
            wrappers.extend(wrappers_)
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def cyclic(
    argument,
    descriptor: str,
    *tweaks: abjad.Tweak,
    do_not_bookend: bool = False,
    do_not_start_spanner_on_final_piece: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
) -> list[abjad.wrapper.Wrapper]:
    assert isinstance(descriptor, str), repr(descriptor)
    assert isinstance(do_not_bookend, bool), repr(do_not_bookend)
    assert isinstance(do_not_start_spanner_on_final_piece, bool)
    assert isinstance(left_broken, bool), repr(left_broken)
    assert isinstance(right_broken, bool), repr(right_broken)
    assert isinstance(rleak, bool), repr(rleak)
    if left_broken is True:
        assert descriptor[0] in ("o", "<", ">"), repr(descriptor)
    if right_broken is True:
        assert descriptor[-1] == "!", repr(descriptor)
    specifiers = parse_hairpin_descriptor(descriptor)
    if rleak is True:
        argument = _select.rleak_final_item_next_nonobgc_leaf(argument)
    wrappers = _iterate_cyclic_hairpin_pieces(
        argument,
        *tweaks,
        do_not_bookend=do_not_bookend,
        do_not_start_spanner_on_final_piece=do_not_start_spanner_on_final_piece,
        left_broken=left_broken,
        right_broken=right_broken,
        specifiers=specifiers,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def hairpin(
    argument,
    descriptor: str,
    *tweaks: abjad.Tweak,
    allow_extra_specifiers: bool = False,
    extra_specifiers: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
) -> list[abjad.wrapper.Wrapper]:
    argument = list(argument)
    assert isinstance(descriptor, str), repr(descriptor)
    assert isinstance(extra_specifiers, bool), repr(extra_specifiers)
    assert isinstance(left_broken, bool), repr(left_broken)
    assert isinstance(right_broken, bool), repr(right_broken)
    if left_broken is True:
        assert descriptor[0] in ("o", "<", ">"), repr(descriptor)
    if right_broken is True:
        assert descriptor[-1] == "!", repr(descriptor)
    if rleak is True:
        argument = _select.rleak_final_item_next_nonobgc_leaf(argument)
    specifiers = parse_exact_hairpin_descriptor(descriptor)
    if len(specifiers) == 1:
        argument = [argument]
    elif extra_specifiers is True:
        assert len(argument) <= len(specifiers)
    elif len(specifiers) != len(argument):
        message = f"\n{len(specifiers)} specifiers ...."
        for specifier in specifiers:
            message += "\n\t" + str(specifier)
        message += f"\n{len(argument)} argument pieces ..."
        for piece in argument:
            message += "\n\t" + str(piece)
        message += "\nlen(specifiers) must equal len(argument)."
        raise Exception(message)
    total_pieces = len(argument)
    wrappers = []
    for current_piece_index, piece in enumerate(argument):
        is_first_piece = current_piece_index == 0
        is_final_piece = current_piece_index == total_pieces - 1
        is_left_broken_first_piece = False
        is_right_broken_final_piece = False
        if is_first_piece and left_broken:
            is_left_broken_first_piece = True
        if is_final_piece and right_broken:
            is_right_broken_final_piece = True
        specifier = specifiers[current_piece_index]
        first_leaf = abjad.select.leaf(piece, 0)
        final_leaf = abjad.select.leaf(piece, -1)
        if isinstance(specifier.start_dynamic, abjad.StopHairpin):
            wrapper = _indicatorlib.attach_persistent_indicator(
                first_leaf,
                specifier.start_dynamic,
            )
            wrappers.append(wrapper)
        elif specifier.start_dynamic is not None:
            wrappers_ = _indicators.dynamic(
                first_leaf,
                specifier.start_dynamic,
            )
            wrappers.extend(wrappers_)
        if specifier.spanner_start is not None:
            indicator = _helpers.bundle_tweaks(
                specifier.spanner_start,
                tweaks,
                i=current_piece_index,
                total=total_pieces,
                overwrite=True,
            )
            wrapper = _indicatorlib.attach_persistent_indicator(
                first_leaf,
                indicator,
                left_broken=is_left_broken_first_piece,
            )
            wrappers.append(wrapper)
        if isinstance(specifier.stop_indicator, abjad.StopHairpin):
            wrapper = _indicatorlib.attach_persistent_indicator(
                final_leaf,
                specifier.stop_indicator,
                right_broken=is_right_broken_final_piece,
            )
            wrappers.append(wrapper)
        elif specifier.stop_indicator is not None:
            wrappers_ = _indicators.dynamic(
                final_leaf,
                specifier.stop_indicator,
            )
            wrappers.extend(wrappers_)
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def parse_hairpin_descriptor(descriptor: str) -> list[HairpinSpecifier]:
    assert isinstance(descriptor, str), repr(descriptor)
    indicators = []
    specifiers = []
    indicator: str | abjad.Dynamic | abjad.StartHairpin | abjad.StopHairpin
    for string in descriptor.split():
        if string == "-":
            indicator = "-"
        else:
            indicator = _dynamics.make_dynamic(string)
        indicators.append(indicator)
    skip_next_start_hairpin = False
    for left, right in abjad.sequence.nwise(indicators):
        specifier = None
        if isinstance(left, abjad.StartHairpin) and skip_next_start_hairpin is False:
            specifier = HairpinSpecifier(spanner_start=left)
        elif isinstance(left, abjad.Dynamic) and isinstance(right, abjad.Dynamic):
            specifier = HairpinSpecifier(indicator=left)
        elif isinstance(left, abjad.Dynamic) and right == "-":
            specifier = HairpinSpecifier(indicator=left)
        elif left == "-" and isinstance(right, abjad.StartHairpin):
            specifier = HairpinSpecifier(spanner_start=right)
            skip_next_start_hairpin = True
        elif left == "-" and isinstance(right, abjad.StopHairpin):
            specifier = HairpinSpecifier(spanner_stop=right)
        elif isinstance(left, abjad.Dynamic) and isinstance(right, abjad.StartHairpin):
            specifier = HairpinSpecifier(indicator=left, spanner_start=right)
            skip_next_start_hairpin = True
        elif isinstance(left, abjad.StopHairpin) and isinstance(
            right, abjad.StartHairpin
        ):
            specifier = HairpinSpecifier(spanner_stop=left, spanner_start=right)
            skip_next_start_hairpin = True
        else:
            skip_next_start_hairpin = False
        if specifier is not None:
            specifiers.append(specifier)
    if indicators:
        final_indicator = indicators[-1]
        specifier = None
        if isinstance(final_indicator, abjad.StopHairpin):
            specifier = HairpinSpecifier(spanner_stop=final_indicator)
        elif isinstance(final_indicator, abjad.Dynamic):
            specifier = HairpinSpecifier(indicator=final_indicator)
        else:
            assert isinstance(final_indicator, abjad.StartHairpin)
            if skip_next_start_hairpin is False:
                specifier = HairpinSpecifier(spanner_start=final_indicator)
        if specifier is not None:
            specifiers.append(specifier)
    return specifiers


known_shapes = ("o<|", "o<", "<|", "<", "|>o", ">o", "|>", ">", "--")


def parse_exact_hairpin_descriptor(descriptor: str) -> list[ExactHairpinSpecifier]:
    assert isinstance(descriptor, str), repr(descriptor)
    specifiers = []
    for string in descriptor.split():
        start_dynamic, spanner_start, stop_indicator = None, None, None
        for shape in known_shapes:
            if shape in string:
                start_dynamic_string, stop_indicator_string = string.split(shape)
                if start_dynamic_string:
                    start_dynamic = _dynamics.make_dynamic(start_dynamic_string)
                spanner_start = _dynamics.make_dynamic(shape)
                if stop_indicator_string:
                    stop_indicator = _dynamics.make_dynamic(stop_indicator_string)
                break
        else:
            if "+" in string:
                start_dynamic_string, stop_indicator_string = string.split("+")
                if start_dynamic_string:
                    start_dynamic = _dynamics.make_dynamic(start_dynamic_string)
                if stop_indicator_string:
                    stop_indicator = _dynamics.make_dynamic(stop_indicator_string)
            elif string == "!":
                stop_indicator = _dynamics.make_dynamic(string)
            else:
                start_dynamic = _dynamics.make_dynamic(string)
        assert isinstance(start_dynamic, abjad.Dynamic | abjad.StopHairpin | type(None))
        assert isinstance(spanner_start, abjad.StartHairpin | type(None))
        assert isinstance(
            stop_indicator, abjad.Dynamic | abjad.StopHairpin | type(None)
        )
        specifier = ExactHairpinSpecifier(
            start_dynamic=start_dynamic,
            spanner_start=spanner_start,
            stop_indicator=stop_indicator,
        )
        specifiers.append(specifier)
    return specifiers
