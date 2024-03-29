"""
textspannerlib.py
"""

import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import indicatorlib as _indicatorlib
from . import scope as _scope
from . import tweaks as _tweaks
from . import typings as _typings


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class TextSpannerSpecifier:
    bookended_spanner_start: abjad.Bundle | None = None
    spanner_start: abjad.Bundle | abjad.StartTextSpan | None = None
    spanner_stop: abjad.StopTextSpan | None = None

    def __iter__(self) -> typing.Iterator:
        result: list = []
        if self.spanner_stop:
            result.append(self.spanner_stop)
        if self.spanner_start:
            result.append(self.spanner_start)
        return iter(result)

    def __post_init__(self):
        if self.bookended_spanner_start is not None:
            assert isinstance(self.bookended_spanner_start, abjad.Bundle)
            indicator = _indicatorlib.unbundle_indicator(self.bookended_spanner_start)
            assert isinstance(indicator, abjad.StartTextSpan)
        if self.spanner_start is not None:
            assert isinstance(self.spanner_start, abjad.Bundle | abjad.StartTextSpan)
            indicator = _indicatorlib.unbundle_indicator(self.spanner_start)
            assert isinstance(indicator, abjad.StartTextSpan), repr(indicator)
        if self.spanner_stop is not None:
            assert isinstance(self.spanner_stop, abjad.StopTextSpan)

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
    ) -> list[abjad.Wrapper]:
        assert isinstance(leaf, abjad.Leaf), repr(leaf)
        assert isinstance(current_piece_index, int), repr(current_piece_index)
        assert isinstance(tag, abjad.Tag), repr(tag)
        assert isinstance(tweaks, tuple), repr(tweaks)
        assert isinstance(total_pieces, int), repr(total_pieces)
        wrappers = []
        prototype = (abjad.Bundle, abjad.StartTextSpan, abjad.StopTextSpan)
        for item in self:
            assert isinstance(item, prototype), repr(item)
            indicator = _indicatorlib.unbundle_indicator(item)
            if isinstance(indicator, abjad.StartTextSpan):
                item = _tweaks.bundle_tweaks(
                    item,
                    tweaks,
                    i=current_piece_index,
                    total=total_pieces,
                    overwrite=True,
                )
            left_broken, right_broken = False, False
            if is_left_broken_first_piece and isinstance(
                indicator, abjad.StartTextSpan
            ):
                left_broken = True
            if is_right_broken_final_piece and isinstance(
                indicator, abjad.StopTextSpan
            ):
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


def iterate_text_spanner_pieces(
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
    assert pieces is not None
    assert isinstance(do_not_bookend, bool), repr(do_not_bookend)
    bookend = not do_not_bookend
    assert isinstance(do_not_start_spanner_on_final_piece, bool)
    assert isinstance(left_broken, bool), repr(left_broken)
    assert isinstance(pieces, list | _scope.DynamicScope), repr(pieces)
    assert isinstance(right_broken, bool), repr(right_broken)
    assert isinstance(specifiers, list), repr(specifiers)
    assert all(isinstance(_, TextSpannerSpecifier) for _ in specifiers), repr(
        specifiers
    )
    assert isinstance(staff_padding, int | float | type(None)), repr(staff_padding)
    tweaks = _tweaks.extend(
        tweaks,
        bound_details_right_padding=bound_details_right_padding,
        staff_padding=staff_padding,
    )
    cyclic_specifiers = abjad.CyclicTuple(specifiers)
    total_pieces = len(pieces)
    assert 0 < total_pieces, repr(total_pieces)
    just_backstole_right_text = False
    wrappers = []
    for current_piece_index, piece in enumerate(pieces):
        is_first_piece = current_piece_index == 0
        is_left_broken_first_piece = False
        is_penultimate_piece = current_piece_index == total_pieces - 2
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
        next_unbundled_specifier = _indicatorlib.unbundle_indicator(next_specifier)
        next_unbundled_spanner_start = next_unbundled_specifier.spanner_start
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
            and isinstance(next_unbundled_spanner_start, abjad.StartTextSpan)
        ):
            specifier = dataclasses.replace(
                specifier, spanner_start=specifier.bookended_spanner_start
            )
            just_backstole_right_text = True
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
        )
        wrappers.extend(wrappers_)
        if should_bookend:
            if specifier.bookended_spanner_start is not None:
                next_specifier = dataclasses.replace(next_specifier, spanner_start=None)
            wrappers_ = next_specifier.attach_items(
                stop_leaf,
                current_piece_index,
                _helpers.function_name(_frame(), n=2),
                tweaks,
                total_pieces,
            )
            wrappers.extend(wrappers_)
        elif (
            is_final_piece
            and not just_backstole_right_text
            and next_specifier.spanner_stop
            and (start_leaf is not stop_leaf)
        ):
            spanner_stop = dataclasses.replace(next_specifier.spanner_stop)
            specifier = TextSpannerSpecifier(spanner_stop=spanner_stop)
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


def parse_text_spanner_descriptor(
    descriptor: str,
    direction: int | None = None,
    *,
    left_broken_text: str | None = None,
    lilypond_id: str | int | None = None,
) -> list[TextSpannerSpecifier]:
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
        specifier = TextSpannerSpecifier(
            bookended_spanner_start=bookended_spanner_start,
            spanner_start=start_text_span,
            spanner_stop=stop_text_span,
        )
        specifiers.append(specifier)
    return specifiers
