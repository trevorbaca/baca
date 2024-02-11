"""
Piecewise.
"""

import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import dynamics as _dynamics
from . import helpers as _helpers
from . import indicators as _indicators
from . import scope as _scope
from . import select as _select
from . import tags as _tags
from . import tweaks as _tweaks
from . import typings as _typings


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class _Specifier:
    bookended_spanner_start: abjad.StartTextSpan | abjad.Bundle | None = None
    # TODO: should only be abjad.Dynamic:
    indicator: abjad.Dynamic | abjad.StartHairpin | abjad.StopHairpin | None = None
    spanner_start: abjad.StartHairpin | abjad.StartTextSpan | abjad.Bundle | None = None
    spanner_stop: abjad.StopHairpin | abjad.StopTextSpan | None = None

    def __iter__(self) -> typing.Iterator:
        return iter(self.indicators)

    def __len__(self) -> int:
        return len(self.indicators)

    def __post_init__(self):
        if self.bookended_spanner_start is not None:
            unbundled = _indicators._unbundle_indicator(self.bookended_spanner_start)
            assert isinstance(unbundled, abjad.StartTextSpan), repr(self.spanner_start)
        if self.indicator is not None:
            unbundled = _indicators._unbundle_indicator(self.indicator)
            # TODO: this should be abjad.Dynamic only:
            prototype = (abjad.StartHairpin, abjad.StopHairpin, abjad.Dynamic)
            assert isinstance(unbundled, prototype), repr(self.indicator)
        if self.spanner_start is not None:
            unbundled = _indicators._unbundle_indicator(self.spanner_start)
            prototype = (abjad.StartHairpin, abjad.StartTextSpan)
            assert isinstance(unbundled, prototype), repr(self.spanner_start)
        if self.spanner_stop is not None:
            unbundled = _indicators._unbundle_indicator(self.spanner_stop)
            prototype = (abjad.StopHairpin, abjad.StopTextSpan)
            assert isinstance(unbundled, prototype), repr(self.spanner_stop)

    # TODO: why ordered this way?
    @property
    def indicators(self) -> list:
        result: list = []
        if self.spanner_stop:
            result.append(self.spanner_stop)
        if self.indicator:
            result.append(self.indicator)
        if self.spanner_start:
            result.append(self.spanner_start)
        return result

    def compound(self) -> bool:
        return bool(self.indicator) and bool(self.spanner_start)

    def indicator_only(self) -> bool:
        if self.indicator and not self.spanner_start:
            return True
        return False

    def simple(self) -> bool:
        return len(self) == 1

    def spanner_start_only(self) -> bool:
        if not self.indicator and self.spanner_start:
            return True
        return False


def _attach_specifier(
    leaf,
    specifier,
    i,
    tag,
    tweaks,
    total_pieces,
    *,
    just_bookended_leaf=None,
) -> list[abjad.Wrapper]:
    assert isinstance(leaf, abjad.Leaf), repr(leaf)
    assert isinstance(specifier, _Specifier), repr(specifier)
    assert isinstance(i, int), repr(i)
    assert isinstance(tag, abjad.Tag), repr(tag)
    for tweak in tweaks:
        assert isinstance(tweak, abjad.Tweak | tuple), repr(tweak)
    assert isinstance(total_pieces, int), repr(total_pieces)
    if just_bookended_leaf is not None:
        assert isinstance(just_bookended_leaf, abjad.Leaf), repr(just_bookended_leaf)
    wrappers = []
    prototype = (
        abjad.Bundle,
        abjad.Dynamic,
        abjad.StartHairpin,
        abjad.StopHairpin,
        abjad.StartTextSpan,
        abjad.StopTextSpan,
    )
    for indicator in specifier:
        assert isinstance(indicator, prototype), repr(indicator)
        if (
            not getattr(_indicators._unbundle_indicator(indicator), "trend", False)
            and leaf is just_bookended_leaf
        ):
            continue
        if not isinstance(indicator, abjad.Bundle):
            indicator = dataclasses.replace(indicator)
        if (
            _indicators._is_maybe_bundled(
                indicator, abjad.StartTextSpan | abjad.StartHairpin
            )
            and tweaks
        ):
            for item in tweaks:
                if isinstance(item, abjad.Tweak):
                    new_tweak = item
                else:
                    assert isinstance(item, tuple), repr(item)
                    new_tweak = item[0]
                assert isinstance(new_tweak, abjad.Tweak), repr(item)
            indicator = _tweaks.bundle_tweaks(
                indicator, tweaks, i=i, total=total_pieces, overwrite=True
            )
        tag_ = tag
        wrapper = _indicators._attach_persistent_indicator(
            leaf,
            indicator,
            tag=tag_,
        )
        wrappers.append(wrapper)
    return wrappers


def _iterate_pieces(
    pieces,
    *tweaks: _typings.IndexedTweak,
    attach_stop_hairpin_on_right_broken_final_piece: bool = False,
    bookend: bool = False,
    bound_details_right_padding: int | float | None = None,
    do_not_start_spanner_on_final_piece: bool = False,
    leak_spanner_stop: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    specifiers: typing.Sequence = (),
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    assert isinstance(tweaks, tuple), repr(tweaks)
    for tweak in tweaks:
        assert isinstance(tweak, abjad.Tweak | tuple), repr(tweak)
    assert pieces is not None
    assert isinstance(bookend, bool), repr(bookend)
    assert isinstance(do_not_start_spanner_on_final_piece, bool)
    assert isinstance(leak_spanner_stop, bool), repr(leak_spanner_stop)
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
    assert all(isinstance(_, _Specifier) for _ in specifiers), repr(specifiers)
    assert isinstance(staff_padding, int | float | type(None)), repr(staff_padding)
    cyclic_specifiers = abjad.CyclicTuple(specifiers)
    if bound_details_right_padding is not None:
        string = rf"- \tweak bound-details.right.padding {bound_details_right_padding}"
        tweaks = tweaks + (abjad.Tweak(string),)
    if staff_padding is not None:
        tweaks = tweaks + (abjad.Tweak(rf"- \tweak staff-padding {staff_padding}"),)
    total_pieces = len(pieces)
    assert 0 < total_pieces, repr(total_pieces)
    just_backstole_right_text = None
    just_bookended_leaf = None
    previous_had_bookend = None
    wrappers = []
    for i, piece in enumerate(pieces):
        start_leaf = abjad.select.leaf(piece, 0)
        stop_leaf = abjad.select.leaf(piece, -1)
        is_first_piece = i == 0
        is_penultimate_piece = i == total_pieces - 2
        is_final_piece = i == total_pieces - 1
        if (
            is_final_piece
            and right_broken is True
            and attach_stop_hairpin_on_right_broken_final_piece is True
        ):
            specifier = _Specifier(spanner_stop=abjad.StopHairpin())
            tag_ = _helpers.function_name(_frame(), n=1)
            tag_ = tag_.append(_tags.RIGHT_BROKEN)
            wrappers_ = _attach_specifier(
                stop_leaf,
                specifier,
                i,
                tag_,
                tweaks,
                total_pieces,
            )
            wrappers.extend(wrappers_)
        if (
            bookend is True
            and i == total_pieces - 1
            and not isinstance(piece, abjad.Leaf)
            and 1 < len(piece)
        ):
            should_bookend = True
        else:
            should_bookend = False
        if is_final_piece and do_not_start_spanner_on_final_piece is True:
            should_bookend = False
        specifier = cyclic_specifiers[i]
        if (
            is_final_piece
            and right_broken
            and not _indicators._is_maybe_bundled(
                specifier.spanner_start, abjad.StartTextSpan
            )
        ):
            should_bookend = False
        if is_final_piece and just_backstole_right_text:
            specifier = dataclasses.replace(specifier, spanner_start=None)
        next_bundle = cyclic_specifiers[i + 1]
        if should_bookend and specifier.bookended_spanner_start:
            specifier = dataclasses.replace(
                specifier, spanner_start=specifier.bookended_spanner_start
            )
        if (
            is_penultimate_piece
            and (
                (isinstance(pieces[-1], abjad.Leaf) or len(pieces[-1]) == 1)
                or do_not_start_spanner_on_final_piece is True
            )
            and _indicators._is_maybe_bundled(
                next_bundle.spanner_start, abjad.StartTextSpan
            )
        ):
            specifier = dataclasses.replace(
                specifier, spanner_start=specifier.bookended_spanner_start
            )
            just_backstole_right_text = True
        if is_final_piece and specifier.spanner_start:
            if _indicators._is_maybe_bundled(
                specifier.spanner_start, abjad.StartHairpin
            ):
                if do_not_start_spanner_on_final_piece is True:
                    specifier = dataclasses.replace(specifier, spanner_start=None)
            elif _indicators._is_maybe_bundled(
                specifier.spanner_start, abjad.StartTextSpan
            ):
                if do_not_start_spanner_on_final_piece is True:
                    specifier = dataclasses.replace(specifier, spanner_start=None)
        tag_ = _helpers.function_name(_frame(), n=2)
        if is_first_piece or previous_had_bookend:
            specifier = dataclasses.replace(specifier, spanner_stop=None)
            if left_broken:
                tag_ = tag_.append(_tags.LEFT_BROKEN)
        if is_final_piece and right_broken:
            tag_ = tag_.append(_tags.RIGHT_BROKEN)
        wrappers_ = _attach_specifier(
            start_leaf,
            specifier,
            i,
            tag_,
            tweaks,
            total_pieces,
            just_bookended_leaf=just_bookended_leaf,
        )
        wrappers.extend(wrappers_)
        if should_bookend:
            tag_ = _helpers.function_name(_frame(), n=3)
            if is_final_piece and right_broken:
                tag_ = tag_.append(_tags.RIGHT_BROKEN)
            if specifier.bookended_spanner_start is not None:
                next_bundle = dataclasses.replace(next_bundle, spanner_start=None)
            if next_bundle.compound():
                next_bundle = dataclasses.replace(next_bundle, spanner_start=None)
            wrappers_ = _attach_specifier(
                stop_leaf,
                next_bundle,
                i,
                tag_,
                tweaks,
                total_pieces,
            )
            wrappers.extend(wrappers_)
            just_bookended_leaf = stop_leaf
        elif (
            is_final_piece
            and not just_backstole_right_text
            and next_bundle.spanner_stop
            and ((start_leaf is not stop_leaf) or leak_spanner_stop)
        ):
            spanner_stop = dataclasses.replace(next_bundle.spanner_stop)
            if leak_spanner_stop:
                spanner_stop = dataclasses.replace(spanner_stop, leak=True)
            specifier = _Specifier(spanner_stop=spanner_stop)
            tag_ = _helpers.function_name(_frame(), n=4)
            if right_broken:
                tag_ = tag_.append(_tags.RIGHT_BROKEN)
            wrappers_ = _attach_specifier(
                stop_leaf,
                specifier,
                i,
                tag_,
                tweaks,
                total_pieces,
            )
            wrappers.extend(wrappers_)
        previous_had_bookend = should_bookend
    return wrappers


def hairpin(
    argument,
    descriptor: str,
    *tweaks: _typings.IndexedTweak,
    bookend: bool = True,
    do_not_start_spanner_on_final_piece: bool = False,
    forbid_al_niente_to_bar_line: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    with_next_leaf: bool = False,
) -> list[abjad.Wrapper]:
    assert isinstance(descriptor, str), repr(descriptor)
    assert isinstance(bookend, bool), repr(bookend)
    assert isinstance(do_not_start_spanner_on_final_piece, bool)
    assert isinstance(left_broken, bool), repr(left_broken)
    assert isinstance(right_broken, bool), repr(right_broken)
    if left_broken is True:
        assert descriptor[0] in ("o", "<", ">"), repr(descriptor)
    if right_broken is True:
        assert descriptor[-1] == "!", repr(descriptor)
    specifiers = parse_hairpin_descriptor(
        descriptor,
        forbid_al_niente_to_bar_line=forbid_al_niente_to_bar_line,
    )
    if with_next_leaf is True:
        next_leaf = _select.rleaf(argument, -1)
        argument[-1].append(next_leaf)
    wrappers = _iterate_pieces(
        argument,
        *tweaks,
        attach_stop_hairpin_on_right_broken_final_piece=True,
        bookend=bookend,
        do_not_start_spanner_on_final_piece=do_not_start_spanner_on_final_piece,
        left_broken=left_broken,
        right_broken=right_broken,
        specifiers=specifiers,
    )
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def parse_hairpin_descriptor(
    descriptor: str,
    forbid_al_niente_to_bar_line: bool = False,
) -> list[_Specifier]:
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
        if _indicators._is_maybe_bundled(indicator, abjad.StartHairpin):
            assert isinstance(indicator, abjad.StartHairpin | abjad.Bundle)
            specifier = _Specifier(spanner_start=indicator)
        elif _indicators._is_maybe_bundled(indicator, abjad.StopHairpin):
            assert isinstance(indicator, abjad.StopHairpin), repr(indicator)
            specifier = _Specifier(spanner_stop=indicator)
        else:
            assert _indicators._is_maybe_bundled(indicator, abjad.Dynamic)
            assert isinstance(indicator, abjad.Dynamic), repr(indicator)
            specifier = _Specifier(indicator=indicator)
        specifiers.append(specifier)
        return specifiers
    if _indicators._is_maybe_bundled(indicators[0], abjad.StartHairpin):
        result = indicators.pop(0)
        assert _indicators._is_maybe_bundled(result, abjad.StartHairpin)
        assert isinstance(result, abjad.StartHairpin | abjad.Bundle)
        specifier = _Specifier(spanner_start=result)
        specifiers.append(specifier)
    # TODO: does this duplicate len(indicators) == 1 branch above?
    if len(indicators) == 1:
        indicator = indicators[0]
        if _indicators._is_maybe_bundled(indicator, abjad.StartHairpin):
            assert isinstance(indicator, abjad.StartHairpin)
            specifier = _Specifier(spanner_start=indicator)
        else:
            # TODO: stop-hairpin should be spanner_stop=stop_hairpin
            assert isinstance(indicator, abjad.Dynamic | abjad.StopHairpin), repr(
                indicator
            )
            specifier = _Specifier(indicator=indicator)
        specifiers.append(specifier)
        return specifiers
    for left, right in abjad.sequence.nwise(indicators):
        if _indicators._is_maybe_bundled(
            left, abjad.StartHairpin
        ) and _indicators._is_maybe_bundled(right, abjad.StartHairpin):
            raise Exception("consecutive start hairpin commands.")
        elif _indicators._is_maybe_bundled(
            left, abjad.Dynamic
        ) and _indicators._is_maybe_bundled(right, abjad.Dynamic):
            specifier = _Specifier(indicator=left)
            specifiers.append(specifier)
        elif _indicators._is_maybe_bundled(left, abjad.Dynamic) and right == "-":
            specifier = _Specifier(indicator=left)
            specifiers.append(specifier)
        elif left == "-" and _indicators._is_maybe_bundled(
            right, abjad.StartHairpin | abjad.StopHairpin
        ):
            specifier = _Specifier(indicator=right)
            specifiers.append(specifier)
        elif _indicators._is_maybe_bundled(
            left, abjad.Dynamic | abjad.StopHairpin
        ) and _indicators._is_maybe_bundled(right, abjad.StartHairpin):
            specifier = _Specifier(indicator=left, spanner_start=right)
            specifiers.append(specifier)
    if indicators and _indicators._is_maybe_bundled(
        indicators[-1], abjad.Dynamic | abjad.StopHairpin
    ):
        indicator = indicators[-1]
        # TODO: stop-hairpin should be spanner_stop=stop_hairpin
        assert isinstance(indicator, abjad.Dynamic | abjad.StopHairpin), repr(indicator)
        specifier = _Specifier(indicator=indicator)
        specifiers.append(specifier)
    return specifiers


def parse_text_spanner_descriptor(
    descriptor: str,
    direction: int | None = None,
    *,
    left_broken_text: str | None = None,
    lilypond_id: str | int | None = None,
) -> list[_Specifier]:
    if left_broken_text is not None:
        assert isinstance(left_broken_text, str), repr(left_broken_text)
    if lilypond_id is not None:
        assert isinstance(lilypond_id, str | int), repr(lilypond_id)
    original_descriptor = descriptor
    if direction == abjad.DOWN:
        shape_to_style = {
            "=>": r"\baca-dashed-line-with-arrow",
            "=|": r"\baca-dashed-line-with-up-hook",
            "||": r"\baca-invisible-line",
            "->": r"\baca-solid-line-with-arrow",
            "-|": r"\baca-solid-line-with-up-hook",
        }
    else:
        shape_to_style = {
            "=>": r"\baca-dashed-line-with-arrow",
            "=|": r"\baca-dashed-line-with-hook",
            "||": r"\baca-invisible-line",
            "->": r"\baca-solid-line-with-arrow",
            "-|": r"\baca-solid-line-with-hook",
        }
    items_ = []
    current_item: list = []
    for word in descriptor.split():
        if word in shape_to_style:
            if current_item:
                item_ = " ".join(current_item)
                items_.append(item_)
                current_item.clear()
            items_.append(word)
        else:
            current_item.append(word)
    if current_item:
        item_ = " ".join(current_item)
        items_.append(item_)
    items = items_
    assert all(isinstance(_, str) for _ in items), repr(items)
    if len(items) == 1:
        message = f"lone item not yet implemented ({original_descriptor!r})."
        raise NotImplementedError(message)
    if lilypond_id is None:
        command = r"\stopTextSpan"
    elif lilypond_id == 1:
        command = r"\stopTextSpanOne"
    elif lilypond_id == 2:
        command = r"\stopTextSpanTwo"
    elif lilypond_id == 3:
        command = r"\stopTextSpanThree"
    elif isinstance(lilypond_id, str):
        command = rf"\bacaStopTextSpan{lilypond_id}"
    else:
        message = "lilypond_id must be 1, 2, 3, str or none"
        message += f" (not {lilypond_id})."
        raise ValueError(message)
    stop_text_span = abjad.StopTextSpan(command=command)
    cyclic_items = abjad.CyclicTuple(items)
    specifiers = []
    for i, item in enumerate(cyclic_items):
        assert isinstance(item, str), repr(item)
        if item in shape_to_style:
            continue
        if item.startswith("\\"):
            item_markup = rf"- \baca-text-spanner-left-markup {item}"
        else:
            item_markup = rf'- \baca-text-spanner-left-text "{item}"'
        assert isinstance(item_markup, str)
        style = r"\baca-invisible-line"
        if cyclic_items[i + 1] in shape_to_style:
            style = shape_to_style[cyclic_items[i + 1]]
            right_text = cyclic_items[i + 2]
        else:
            right_text = cyclic_items[i + 1]
        right_markup: str | abjad.Markup
        if "hook" not in style:
            if right_text.startswith("\\"):
                right_markup = r"- \baca-text-spanner-right-markup"
                right_markup += rf" {right_text}"
            else:
                right_markup = r"- \baca-text-spanner-right-text"
                right_markup += rf' "{right_text}"'
        else:
            right_markup = abjad.Markup(rf"\upright {right_text}")
        if lilypond_id is None:
            command = r"\startTextSpan"
        elif lilypond_id == 1:
            command = r"\startTextSpanOne"
        elif lilypond_id == 2:
            command = r"\startTextSpanTwo"
        elif lilypond_id == 3:
            command = r"\startTextSpanThree"
        elif isinstance(lilypond_id, str):
            command = rf"\bacaStartTextSpan{lilypond_id}"
        else:
            raise ValueError(lilypond_id)
        left_broken_markup = None
        if isinstance(left_broken_text, str):
            left_broken_markup = abjad.Markup(left_broken_text)
        elif isinstance(left_broken_text, abjad.Markup):
            left_broken_markup = left_broken_text
        start_text_span = abjad.StartTextSpan(
            command=command,
            left_broken_text=left_broken_markup,
            left_text=item_markup,
            style=style,
        )
        # kerns bookended hook
        if "hook" in style:
            assert isinstance(right_markup, abjad.Markup)
            content_string = right_markup.string
            string = r"\markup \concat { \raise #-1 \draw-line #'(0 . -1) \hspace #0.75"
            string += rf" \general-align #Y #1 {content_string} }}"
            right_markup = abjad.Markup(string)
        bookended_spanner_start: abjad.StartTextSpan | abjad.Bundle
        bookended_spanner_start = dataclasses.replace(
            start_text_span, right_text=right_markup
        )
        # TODO: find some way to make these tweaks explicit to composer
        bookended_spanner_start = abjad.bundle(
            bookended_spanner_start,
            r"- \tweak bound-details.right.stencil-align-dir-y #center",
        )
        if "hook" in style:
            bookended_spanner_start = abjad.bundle(
                bookended_spanner_start,
                r"- \tweak bound-details.right.padding 1.25",
            )
        else:
            bookended_spanner_start = abjad.bundle(
                bookended_spanner_start,
                r"- \tweak bound-details.right.padding 0.5",
            )
        specifier = _Specifier(
            bookended_spanner_start=bookended_spanner_start,
            spanner_start=start_text_span,
            spanner_stop=stop_text_span,
        )
        specifiers.append(specifier)
    for specifier in specifiers:
        assert specifier.indicator is None, repr(specifier)
    return specifiers
