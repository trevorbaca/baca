"""
Spanners.
"""

import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import indicatorlib as _indicatorlib
from . import indicators as _indicators
from . import scope as _scope
from . import select as _select
from . import tags as _tags
from . import tweak as _tweak
from . import typings as _typings


def _attach_simplex_spanner_indicators(
    argument,
    spanner_start,
    spanner_stop,
    *tweaks: _typings.IndexedTweak,
    bound_details_right_padding: int | float | None = None,
    direction: abjad.Vertical | None = None,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    wrappers = []
    wrapper = _attach_spanner_start(
        argument,
        spanner_start,
        *tweaks,
        bound_details_right_padding=bound_details_right_padding,
        direction=direction,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _attach_spanner_stop(
        argument,
        spanner_stop,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def _attach_spanner_start(
    argument,
    spanner_start,
    *tweaks: _typings.IndexedTweak,
    bound_details_right_padding: int | float | None = None,
    direction: abjad.Vertical | None = None,
    left_broken: bool = False,
    staff_padding: int | float | None = None,
) -> abjad.Wrapper:
    unbundled_indicator = _indicatorlib.unbundle_indicator(spanner_start)
    assert unbundled_indicator.spanner_start is True
    if bound_details_right_padding is not None:
        string = rf"- \tweak bound-details.right.padding {bound_details_right_padding}"
        tweaks = tweaks + (abjad.Tweak(string),)
    if staff_padding is not None:
        tweaks = tweaks + (abjad.Tweak(rf"- \tweak staff-padding {staff_padding}"),)
    spanner_start = _tweak.bundle_tweaks(spanner_start, tweaks)
    first_leaf = abjad.select.leaf(argument, 0)
    wrapper = _indicatorlib.attach_persistent_indicator(
        first_leaf,
        spanner_start,
        direction=direction,
    )
    tag = _helpers.function_name(_frame())
    if left_broken:
        tag = tag.append(_tags.LEFT_BROKEN)
    _tags.tag([wrapper], tag)
    return wrapper


def _attach_spanner_stop(
    argument,
    spanner_stop,
    *,
    right_broken: bool = False,
) -> abjad.Wrapper:
    assert spanner_stop.spanner_stop is True, repr(spanner_stop)
    final_leaf = abjad.select.leaf(argument, -1)
    wrapper = _indicatorlib.attach_persistent_indicator(
        final_leaf,
        spanner_stop,
    )
    tag = _helpers.function_name(_frame())
    if right_broken:
        tag = tag.append(_tags.RIGHT_BROKEN)
    _tags.tag([wrapper], tag)
    return wrapper


def _iterate_text_spanner_pieces(
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
    assert all(isinstance(_, _TextSpannerSpecifier) for _ in specifiers), repr(
        specifiers
    )
    assert isinstance(staff_padding, int | float | type(None)), repr(staff_padding)
    tweaks = _tweak.extend(
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
            specifier = _TextSpannerSpecifier(spanner_stop=spanner_stop)
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


def _parse_text_spanner_descriptor(
    descriptor: str,
    direction: int | None = None,
    *,
    left_broken_text: str | None = None,
    lilypond_id: str | int | None = None,
) -> list["_TextSpannerSpecifier"]:
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
        specifier = _TextSpannerSpecifier(
            bookended_spanner_start=bookended_spanner_start,
            spanner_start=start_text_span,
            spanner_stop=stop_text_span,
        )
        specifiers.append(specifier)
    return specifiers


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class _TextSpannerSpecifier:
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
                item = _tweak.bundle_tweaks(
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


def beam(
    argument,
    *tweaks: abjad.Tweak,
    direction: abjad.Vertical | None = None,
    start_beam: abjad.StartBeam = abjad.StartBeam(),
    stop_beam: abjad.StopBeam = abjad.StopBeam(),
) -> list[abjad.Wrapper]:
    assert isinstance(start_beam, abjad.StartBeam), repr(start_beam)
    assert isinstance(stop_beam, abjad.StopBeam), repr(stop_beam)
    for leaf in abjad.iterate.leaves(argument, grace=False):
        abjad.detach(abjad.StartBeam, leaf)
        abjad.detach(abjad.StopBeam, leaf)
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        start_beam,
        stop_beam,
        *tweaks,
        direction=direction,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def bow_speed(
    argument,
    descriptor: str,
    *tweaks: _typings.IndexedTweak,
    do_not_bookend: bool = False,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    wrappers = text(
        argument,
        descriptor,
        *tweaks,
        do_not_bookend=do_not_bookend,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="BowSpeed",
        right_broken=right_broken,
        rleak=rleak,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def circle_bow(
    argument,
    *tweaks: _typings.IndexedTweak,
    left_broken: bool = False,
    left_broken_text: str | None = r"\baca-left-broken-circle-bowing-markup",
    qualifier: str | None = None,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if qualifier is None:
        descriptor = r"\baca-circle-markup =|"
    else:
        assert isinstance(qualifier, str), repr(qualifier)
        descriptor = rf"\baca-circle-{qualifier}-markup =|"
    wrappers = text(
        argument,
        descriptor,
        *tweaks,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="CircleBow",
        right_broken=right_broken,
        rleak=rleak,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def clb(
    argument,
    string_number: int,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    assert string_number in (1, 2, 3, 4), repr(string_number)
    if string_number == 1:
        markup = r"\baca-damp-clb-one-markup"
    elif string_number == 2:
        markup = r"\baca-damp-clb-two-markup"
    elif string_number == 3:
        markup = r"\baca-damp-clb-three-markup"
    elif string_number == 4:
        markup = r"\baca-damp-clb-four-markup"
    else:
        raise Exception(string_number)
    specifiers = _parse_text_spanner_descriptor(
        f"{markup} =|",
        left_broken_text=r"\baca-left-broken-clb-markup",
        lilypond_id="CLB",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def covered(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = r"\baca-covered-markup =|",
    left_broken: bool = False,
    left_broken_text: str = r"\baca-parenthesized-cov-markup",
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id="Covered",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def damp(
    argument,
    *tweaks: abjad.Tweak,
    bound_details_right_padding: int | float | None = None,
    left_broken: bool = False,
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _parse_text_spanner_descriptor(
        r"\baca-damp-markup =|",
        left_broken_text=r"\baca-left-broken-damp-markup",
        lilypond_id="Damp",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        bound_details_right_padding=bound_details_right_padding,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def half_clt(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = "½ clt =|",
    left_broken: bool = False,
    left_broken_text: str = r"\baca-left-broken-half-clt-markup",
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id="HalfCLT",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def material_annotation(
    argument,
    descriptor: str,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=None,
        lilypond_id="MaterialAnnotation",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.MATERIAL_ANNOTATION_SPANNER)
    _tags.tag(wrappers, tag)
    return wrappers


def metric_modulation(
    argument,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _parse_text_spanner_descriptor(
        "MM =|",
        left_broken_text=None,
        lilypond_id="MetricModulation",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.METRIC_MODULATION_SPANNER)
    _tags.tag(wrappers, tag)
    return wrappers


def ottava(
    argument,
    n: int = 1,
    *,
    rleak: bool = False,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    assert isinstance(n, int), repr(n)
    wrappers = []
    leaf = abjad.select.leaf(argument, 0)
    wrappers_ = _indicators.ottava(leaf, n)
    wrappers.extend(wrappers_)
    leaf = abjad.select.leaf(argument, -1)
    wrappers_ = _indicators.ottava(leaf, 0)
    wrappers.extend(wrappers_)
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def pizzicato(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = r"\baca-pizz-markup =|",
    left_broken: bool = False,
    rleak: bool = False,
    right_broken: bool = False,
    left_broken_text: str = r"\baca-parenthesized-pizz-markup",
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id="Pizzicato",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def scp(
    argument,
    descriptor: str,
    *tweaks: _typings.IndexedTweak,
    do_not_bookend: bool = False,
    bound_details_right_padding: int | float | None = None,
    do_not_start_spanner_on_final_piece: bool = False,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    wrappers = text(
        argument,
        descriptor,
        *tweaks,
        bound_details_right_padding=bound_details_right_padding,
        do_not_bookend=do_not_bookend,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="SCP",
        right_broken=right_broken,
        rleak=rleak,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def slur(
    argument,
    *tweaks: abjad.Tweak,
    phrasing_slur: bool = False,
    start_slur: abjad.StartSlur | None = None,
    stop_slur: abjad.StopSlur | None = None,
) -> list[abjad.Wrapper]:
    if phrasing_slur is True:
        start_slur_ = start_slur or abjad.StartPhrasingSlur()
        stop_slur_ = stop_slur or abjad.StopPhrasingSlur()
    else:
        start_slur_ = start_slur or abjad.StartSlur()
        stop_slur_ = stop_slur or abjad.StopSlur()
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        start_slur_,
        stop_slur_,
        *tweaks,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def spazzolato(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = r"\baca-spazzolato-markup =|",
    left_broken: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=r"\baca-left-broken-spazz-markup",
        lilypond_id="Spazzolato",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def string_number(
    argument,
    string_number: int,
    *tweaks: abjad.Tweak,
    invisible_line: bool = False,
    left_broken: bool = False,
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    assert isinstance(string_number, int), repr(string_number)
    assert string_number in (1, 2, 3, 4), repr(string_number)
    if string_number == 1:
        string_number_markup = r"\baca-string-i-markup"
        left_broken_text = r"\baca-parenthesized-string-i-markup"
    elif string_number == 2:
        string_number_markup = r"\baca-string-ii-markup"
        left_broken_text = r"\baca-parenthesized-string-ii-markup"
    elif string_number == 3:
        string_number_markup = r"\baca-string-iii-markup"
        left_broken_text = r"\baca-parenthesized-string-iii-markup"
    else:
        assert string_number == 4, repr(string_number)
        string_number_markup = r"\baca-string-iv-markup"
        left_broken_text = r"\baca-parenthesized-string-iv-markup"
    if invisible_line is True:
        descriptor = f"{string_number_markup} ||"
    else:
        descriptor = f"{string_number_markup} =|"
    specifiers = _parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id="StringNumber",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def sustain_pedal(
    argument,
    *tweaks: abjad.Tweak,
    start_piano_pedal: abjad.StartPianoPedal = abjad.StartPianoPedal(),
    stop_piano_pedal: abjad.StopPianoPedal = abjad.StopPianoPedal(),
) -> list[abjad.Wrapper]:
    assert isinstance(start_piano_pedal, abjad.StartPianoPedal), repr(start_piano_pedal)
    assert isinstance(stop_piano_pedal, abjad.StopPianoPedal), repr(stop_piano_pedal)
    wrappers = []
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        start_piano_pedal,
        stop_piano_pedal,
        *tweaks,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def tasto(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = "T =|",
    left_broken: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=r"\baca-left-broken-t-markup",
        lilypond_id="SCP",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def text(
    argument,
    descriptor: str,
    *tweaks: _typings.IndexedTweak,
    bound_details_right_padding: int | float | None = None,
    do_not_bookend: bool = False,
    direction: int | None = None,
    do_not_start_spanner_on_final_piece: bool = False,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    lilypond_id: int | str | None = None,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    assert isinstance(descriptor, str), repr(descriptor)
    assert isinstance(do_not_bookend, bool), repr(do_not_bookend)
    specifiers = _parse_text_spanner_descriptor(
        descriptor,
        direction=direction,
        left_broken_text=left_broken_text,
        lilypond_id=lilypond_id,
    )
    if len(specifiers) == 1:
        assert do_not_bookend is False, repr(do_not_bookend)
        if rleak is True:
            argument = _select.rleak_next_nonobgc_leaf(argument)
        specifier = specifiers[0]
        wrappers = []
        wrapper = _attach_spanner_start(
            argument,
            specifier.spanner_start,
            *tweaks,
            bound_details_right_padding=bound_details_right_padding,
            left_broken=left_broken,
            staff_padding=staff_padding,
        )
        wrappers.append(wrapper)
        wrapper = _attach_spanner_stop(
            argument,
            specifier.spanner_stop,
            right_broken=right_broken,
        )
        wrappers.append(wrapper)
    else:
        if rleak is True:
            argument = _select.rleak_final_item_next_nonobgc_leaf(argument)
        wrappers = _iterate_text_spanner_pieces(
            argument,
            *tweaks,
            bound_details_right_padding=bound_details_right_padding,
            do_not_bookend=do_not_bookend,
            do_not_start_spanner_on_final_piece=do_not_start_spanner_on_final_piece,
            left_broken=left_broken,
            right_broken=right_broken,
            specifiers=specifiers,
            staff_padding=staff_padding,
        )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def trill(
    argument,
    *tweaks: abjad.Tweak,
    alteration: str | None = None,
    force_trill_pitch_head_accidental: bool = False,
    harmonic: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
    start_trill_span: abjad.StartTrillSpan = abjad.StartTrillSpan(),
    stop_trill_span: abjad.StopTrillSpan = abjad.StopTrillSpan(),
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    assert isinstance(start_trill_span, abjad.StartTrillSpan), repr(start_trill_span)
    interval = pitch = None
    if alteration is not None:
        prototype = (abjad.NamedPitch, abjad.NamedInterval, str)
        assert isinstance(alteration, prototype), repr(alteration)
        try:
            pitch = abjad.NamedPitch(alteration)
        except Exception:
            pass
        try:
            interval = abjad.NamedInterval(alteration)
        except Exception:
            pass
    if pitch is not None or interval is not None:
        start_trill_span = dataclasses.replace(
            start_trill_span, interval=interval, pitch=pitch
        )
    if force_trill_pitch_head_accidental is True:
        start_trill_span = dataclasses.replace(
            start_trill_span,
            force_trill_pitch_head_accidental=force_trill_pitch_head_accidental,
        )
    start_trill_span_: abjad.StartTrillSpan | abjad.Bundle = start_trill_span
    start_trill_span_ = start_trill_span
    if harmonic is True:
        # TODO: replace this with a (one-word) predefined function
        string = "#(lambda (grob) (grob-interpret-markup grob"
        string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
        string = rf"- \tweak TrillPitchHead.stencil {string}"
        start_trill_span_ = abjad.bundle(start_trill_span_, string)
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        start_trill_span_,
        stop_trill_span,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def vibrato(
    argument,
    descriptor: str,
    *tweaks: _typings.IndexedTweak,
    do_not_bookend: bool = False,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    wrappers = text(
        argument,
        descriptor,
        *tweaks,
        do_not_bookend=do_not_bookend,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="Vibrato",
        right_broken=right_broken,
        rleak=rleak,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def xfb(
    argument,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _parse_text_spanner_descriptor(
        "XFB =|",
        left_broken_text=r"\baca-left-broken-xfb-markup",
        lilypond_id="BowSpeed",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_simplex_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers
