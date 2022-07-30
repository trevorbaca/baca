"""
Piecewise.
"""
import copy
import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import command as _command
from . import commands as _commands
from . import select as _select
from . import tags as _tags
from . import treat as _treat
from . import tweaks as _tweaks
from . import typings as _typings
from .enums import enums as _enums


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class _Specifier:

    bookended_spanner_start: typing.Any = None
    indicator: typing.Any = None
    spanner_start: typing.Any = None
    spanner_stop: typing.Any = None

    def __iter__(self) -> typing.Iterator:
        return iter(self.indicators)

    def __len__(self) -> int:
        return len(self.indicators)

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


def _attach_indicators(
    specifier,
    leaf,
    i,
    manifests,
    self_tag,
    self_tweaks,
    total_pieces,
    *,
    autodetected_right_padding=None,
    just_bookended_leaf=None,
    tag=None,
):
    assert isinstance(manifests, dict), repr(manifests)
    assert isinstance(tag, abjad.Tag), repr(tag)
    for indicator in specifier:
        if (
            not getattr(_unbundle_indicator(indicator), "trend", False)
            and leaf is just_bookended_leaf
        ):
            continue
        if not isinstance(indicator, bool | abjad.Bundle):
            indicator = dataclasses.replace(indicator)
        if (
            _is_maybe_bundled(indicator, abjad.StartTextSpan)
            and autodetected_right_padding is not None
        ):
            number = autodetected_right_padding
            tweak = abjad.Tweak(
                rf"- \tweak bound-details.right.padding {number}",
                tag=self_tag.append(tag)
                .append(_tags.AUTODETECT)
                .append(_tags.SPANNER_START),
            )
            indicator = abjad.bundle(indicator, tweak, overwrite=True)
        if _is_maybe_bundled(indicator, abjad.StartTextSpan) and self_tweaks:
            for item in self_tweaks:
                if isinstance(item, abjad.Tweak):
                    new_tweak = item
                else:
                    assert isinstance(item, tuple), repr(item)
                    new_tweak = item[0]
                assert isinstance(new_tweak, abjad.Tweak), repr(item)
            indicator = _tweaks.bundle_tweaks(
                indicator, self_tweaks, i=i, total=total_pieces, overwrite=True
            )
        reapplied = _treat.remove_reapplied_wrappers(leaf, indicator)
        tag_ = self_tag.append(tag)
        if getattr(indicator, "spanner_start", None) is True:
            tag_ = tag_.append(_tags.SPANNER_START)
        elif (
            isinstance(indicator, abjad.Bundle)
            and getattr(indicator.indicator, "spanner_start", None) is True
        ):
            tag_ = tag_.append(_tags.SPANNER_START)
        if getattr(indicator, "spanner_stop", None) is True:
            tag_ = tag_.append(_tags.SPANNER_STOP)
        elif (
            isinstance(indicator, abjad.Bundle)
            and getattr(indicator.indicator, "spanner_stop", None) is True
        ):
            tag_ = tag_.append(_tags.SPANNER_STOP)
        wrapper = abjad.attach(indicator, leaf, tag=tag_, wrapper=True)
        if _treat.compare_persistent_indicators(indicator, reapplied):
            _treat.treat_persistent_wrapper(manifests, wrapper, "redundant")


def _do_piecewise_command(
    argument,
    *,
    manifests=None,
    self_autodetect_right_padding: bool = False,
    self_bookend: bool | int = False,
    self_final_piece_spanner=None,
    self_leak_spanner_stop: bool = False,
    self_left_broken: bool = False,
    self_pieces: typing.Callable = lambda _: _select.leaves(_),
    self_remove_length_1_spanner_start: bool = False,
    self_right_broken: typing.Any = None,
    self_specifiers: typing.Sequence = (),
    self_tag,
    self_tweaks: typing.Sequence[_typings.IndexedTweak] = (),
):
    cyclic_specifiers = abjad.CyclicTuple(self_specifiers)
    manifests = manifests or {}
    if self_pieces is not None:
        assert not isinstance(self_pieces, str)
        pieces = self_pieces(argument)
    else:
        pieces = argument
    assert pieces is not None
    piece_count = len(pieces)
    assert 0 < piece_count, repr(piece_count)
    if self_bookend in (False, None):
        bookend_pattern = abjad.Pattern()
    elif self_bookend is True:
        bookend_pattern = abjad.index([0], 1)
    else:
        assert isinstance(self_bookend, int), repr(self_bookend)
        bookend_pattern = abjad.index([self_bookend], period=piece_count)
    just_backstole_right_text = None
    just_bookended_leaf = None
    previous_had_bookend = None
    total_pieces = len(pieces)
    for i, piece in enumerate(pieces):
        start_leaf = abjad.select.leaf(piece, 0)
        stop_leaf = abjad.select.leaf(piece, -1)
        is_first_piece = i == 0
        is_penultimate_piece = i == piece_count - 2
        is_final_piece = i == piece_count - 1
        if is_final_piece and self_right_broken:
            specifier = _Specifier(spanner_start=self_right_broken)
            tag = abjad.Tag("baca.PiecewiseCommand._call(1)")
            tag = tag.append(_tags.RIGHT_BROKEN)
            _attach_indicators(
                specifier,
                stop_leaf,
                i,
                manifests,
                self_tag,
                self_tweaks,
                total_pieces,
                tag=tag,
            )
        if bookend_pattern.matches_index(i, piece_count) and 1 < len(piece):
            should_bookend = True
        else:
            should_bookend = False
        if is_final_piece and self_final_piece_spanner is False:
            should_bookend = False
        specifier = cyclic_specifiers[i]
        if (
            is_final_piece
            and self_right_broken
            and not _is_maybe_bundled(specifier.spanner_start, abjad.StartTextSpan)
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
            and (len(pieces[-1]) == 1 or self_final_piece_spanner is False)
            and _is_maybe_bundled(next_bundle.spanner_start, abjad.StartTextSpan)
        ):
            specifier = dataclasses.replace(
                specifier, spanner_start=specifier.bookended_spanner_start
            )
            just_backstole_right_text = True
        if (
            len(piece) == 1
            and specifier.compound()
            and self_remove_length_1_spanner_start
        ):
            specifier = dataclasses.replace(specifier, spanner_start=None)
        if is_final_piece and specifier.spanner_start:
            if _is_maybe_bundled(specifier.spanner_start, abjad.StartHairpin):
                if self_final_piece_spanner:
                    specifier = dataclasses.replace(
                        specifier, spanner_start=self_final_piece_spanner
                    )
                elif self_final_piece_spanner is False:
                    specifier = dataclasses.replace(specifier, spanner_start=None)
            elif _is_maybe_bundled(specifier.spanner_start, abjad.StartTextSpan):
                if self_final_piece_spanner is False:
                    specifier = dataclasses.replace(specifier, spanner_start=None)
        tag = abjad.Tag("baca.PiecewiseCommand._call(2)")
        if is_first_piece or previous_had_bookend:
            specifier = dataclasses.replace(specifier, spanner_stop=None)
            if self_left_broken:
                tag = tag.append(_tags.LEFT_BROKEN)
        if is_final_piece and self_right_broken:
            tag = tag.append(_tags.RIGHT_BROKEN)
        autodetected_right_padding = None
        # solution is merely heuristic;
        # TextSpanner.bound-details.right.to-extent = ##t implementation
        # only 100% workable solution
        if is_final_piece and self_autodetect_right_padding:
            if (
                abjad.get.annotation(stop_leaf, _enums.ANCHOR_NOTE) is True
                or abjad.get.annotation(stop_leaf, _enums.ANCHOR_SKIP) is True
            ):
                autodetected_right_padding = 2.5
            # stop leaf multiplied whole note on fermata measure downbeat
            elif (
                isinstance(stop_leaf, abjad.Note)
                and stop_leaf.written_duration == 1
                and stop_leaf.multiplier == abjad.Multiplier(1, 4)
            ):
                autodetected_right_padding = 3.25
            # stop leaf on normal measure downbeat
            else:
                autodetected_right_padding = 2.75
            # there's probably a third case for normal midmeasure leaf
            # else:
            #    autodetected_right_padding = 1.25
        _attach_indicators(
            specifier,
            start_leaf,
            i,
            manifests,
            self_tag,
            self_tweaks,
            total_pieces,
            autodetected_right_padding=autodetected_right_padding,
            just_bookended_leaf=just_bookended_leaf,
            tag=tag,
        )
        if should_bookend:
            tag = abjad.Tag("baca.PiecewiseCommand._call(3)")
            if is_final_piece and self_right_broken:
                tag = tag.append(_tags.RIGHT_BROKEN)
            if specifier.bookended_spanner_start is not None:
                next_bundle = dataclasses.replace(next_bundle, spanner_start=None)
            if next_bundle.compound():
                next_bundle = dataclasses.replace(next_bundle, spanner_start=None)
            _attach_indicators(
                next_bundle,
                stop_leaf,
                i,
                manifests,
                self_tag,
                self_tweaks,
                total_pieces,
                tag=tag,
            )
            just_bookended_leaf = stop_leaf
        elif (
            is_final_piece
            and not just_backstole_right_text
            and next_bundle.spanner_stop
            and ((start_leaf is not stop_leaf) or self_leak_spanner_stop)
        ):
            spanner_stop = dataclasses.replace(next_bundle.spanner_stop)
            if self_leak_spanner_stop:
                spanner_stop = dataclasses.replace(spanner_stop, leak=True)
            specifier = _Specifier(spanner_stop=spanner_stop)
            tag = abjad.Tag("baca.PiecewiseCommand._call(4)")
            if self_right_broken:
                tag = tag.append(_tags.RIGHT_BROKEN)
            _attach_indicators(
                specifier,
                stop_leaf,
                i,
                manifests,
                self_tag,
                self_tweaks,
                total_pieces,
                tag=tag,
            )
        previous_had_bookend = should_bookend


def _is_maybe_bundled(argument, prototype):
    if isinstance(argument, prototype):
        return True
    if isinstance(argument, abjad.Bundle):
        if isinstance(argument.indicator, prototype):
            return True
    return False


def _prepare_hairpin_arguments(
    *,
    dynamics,
    final_hairpin,
    forbid_al_niente_to_bar_line,
    tweaks,
):
    if isinstance(dynamics, str):
        specifiers = parse_hairpin_descriptor(
            dynamics,
            *tweaks,
            forbid_al_niente_to_bar_line=forbid_al_niente_to_bar_line,
        )
    else:
        specifiers = dynamics
    for item in specifiers:
        assert isinstance(item, _Specifier), repr(dynamics)
    final_hairpin_: bool | abjad.StartHairpin | None = None
    if isinstance(final_hairpin, bool):
        final_hairpin_ = final_hairpin
    elif isinstance(final_hairpin, str):
        final_hairpin_ = abjad.StartHairpin(final_hairpin)
    return final_hairpin_, specifiers


def _prepare_text_spanner_arguments(
    items,
    *tweaks,
    autodetect_right_padding,
    bookend,
    boxed,
    direction,
    final_piece_spanner,
    leak_spanner_stop,
    left_broken,
    left_broken_text,
    lilypond_id,
    right_broken,
):
    original_items = items
    if autodetect_right_padding is not None:
        autodetect_right_padding = bool(autodetect_right_padding)
    if direction == abjad.DOWN:
        shape_to_style = {
            "=>": "dashed-line-with-arrow",
            "=|": "dashed-line-with-up-hook",
            "||": "invisible-line",
            "->": "solid-line-with-arrow",
            "-|": "solid-line-with-up-hook",
        }
    else:
        shape_to_style = {
            "=>": "dashed-line-with-arrow",
            "=|": "dashed-line-with-hook",
            "||": "invisible-line",
            "->": "solid-line-with-arrow",
            "-|": "solid-line-with-hook",
        }
    if isinstance(items, str):
        items_: list[str | abjad.Markup] = []
        current_item: list[str] = []
        for word in items.split():
            if word in shape_to_style:
                if current_item:
                    item_ = " ".join(current_item)
                    if boxed:
                        string = rf'\baca-boxed-markup "{item_}"'
                        markup = abjad.Markup(string)
                        items_.append(markup)
                    else:
                        items_.append(item_)
                    current_item = []
                items_.append(word)
            else:
                current_item.append(word)
        if current_item:
            item_ = " ".join(current_item)
            if boxed:
                string = rf'\baca-boxed-markup "{item_}"'
                markup = abjad.Markup(string)
                items_.append(markup)
            else:
                items_.append(item_)
        items = items_
    specifiers = []
    if len(items) == 1:
        message = f"lone item not yet implemented ({original_items!r})."
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
    for i, item in enumerate(cyclic_items):
        item_markup: str | abjad.Markup
        if item in shape_to_style:
            continue
        if isinstance(item, str) and item.startswith("\\"):
            item_markup = rf"- \baca-text-spanner-left-markup {item}"
        elif isinstance(item, str):
            item_markup = rf'- \baca-text-spanner-left-text "{item}"'
        else:
            item_markup = item
            assert isinstance(item_markup, abjad.Markup)
            string = item_markup.string
            item_markup = abjad.Markup(r"\upright {string}")
            assert isinstance(item_markup, abjad.Markup)
        prototype = (str, abjad.Markup)
        assert isinstance(item_markup, prototype)
        style = "invisible-line"
        if cyclic_items[i + 1] in shape_to_style:
            style = shape_to_style[cyclic_items[i + 1]]
            right_text = cyclic_items[i + 2]
        else:
            right_text = cyclic_items[i + 1]
        right_markup: str | abjad.Markup
        if isinstance(right_text, str):
            if "hook" not in style:
                if right_text.startswith("\\"):
                    right_markup = r"- \baca-text-spanner-right-markup"
                    right_markup += rf" {right_text}"
                else:
                    right_markup = r"- \baca-text-spanner-right-text"
                    right_markup += rf' "{right_text}"'
            else:
                right_markup = abjad.Markup(rf"\upright {right_text}")
        else:
            assert isinstance(right_text, abjad.Markup)
            string = right_text.string
            right_markup = abjad.Markup(r"\upright {string}")
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
    return specifiers


def _unbundle_indicator(argument):
    if isinstance(argument, abjad.Bundle):
        return argument.indicator
    return argument


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class PiecewiseCommand(_command.Command):
    """
    Piecewise indicator command.

    Command attaches indicator to first leaf in each group of selector output when
    ``bookend`` is false.

    Command attaches indicator to both first leaf and last leaf in each group of selector
    output when ``bookend`` is true.

    When ``bookend`` equals integer ``n``, command attaches indicator to first leaf and
    last leaf in group ``n`` of selector output and attaches indicator to only first leaf
    in other groups of selector output.
    """

    autodetect_right_padding: bool = False
    bookend: bool | int = False
    specifiers: typing.Sequence[_Specifier] = ()
    final_piece_spanner: typing.Any = None
    leak_spanner_stop: bool = False
    left_broken: bool = False
    pieces: typing.Any = lambda _: _select.leaves(_)
    remove_length_1_spanner_start: bool = False
    right_broken: typing.Any = None
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
    tweaks: typing.Sequence[_typings.IndexedTweak] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.autodetect_right_padding, bool)
        assert isinstance(self.bookend, bool | int), repr(self.bookend)
        assert self.specifiers is not None
        if self.final_piece_spanner not in (None, False):
            assert getattr(self.final_piece_spanner, "spanner_start", False)
        assert isinstance(self.leak_spanner_stop, bool), repr(self.leak_spanner_stop)
        assert isinstance(self.left_broken, bool), repr(self.left_broken)
        if self.pieces is not None:
            assert callable(self.pieces), repr(self.pieces)
        assert isinstance(self.remove_length_1_spanner_start, bool)
        _tweaks.validate_indexed_tweaks(self.tweaks)

    def __copy__(self, *arguments):
        result = dataclasses.replace(self)
        result.specifiers = copy.deepcopy(self.specifiers)
        return result

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.specifiers:
            return False
        if self.selector is not None:
            assert not isinstance(self.selector, str)
            argument = self.selector(argument)
        _do_piecewise_command(
            argument,
            manifests=runtime.get("manifests", {}),
            self_autodetect_right_padding=self.autodetect_right_padding,
            self_bookend=self.bookend,
            self_final_piece_spanner=self.final_piece_spanner,
            self_leak_spanner_stop=self.leak_spanner_stop,
            self_left_broken=self.left_broken,
            self_pieces=self.pieces,
            self_remove_length_1_spanner_start=self.remove_length_1_spanner_start,
            self_right_broken=self.right_broken,
            self_specifiers=self.specifiers,
            self_tag=self.tag,
            self_tweaks=self.tweaks,
        )
        return False


def bow_speed_spanner(
    items: str | list,
    *tweaks: _typings.IndexedTweak,
    autodetect_right_padding: bool = True,
    bookend: bool | int = False,
    final_piece_spanner: bool | None = None,
    left_broken: bool = False,
    left_broken_text: str = None,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.BOW_SPEED_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        final_piece_spanner=final_piece_spanner,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="BowSpeed",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def circle_bow_spanner(
    *tweaks: _typings.IndexedTweak,
    left_broken: bool = False,
    left_broken_text: str | None = r"\baca-left-broken-circle-bowing-markup",
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    qualifier: str = None,
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.CIRCLE_BOW_SPANNER)
    if qualifier is None:
        string = r"\baca-circle-markup =|"
    else:
        assert isinstance(qualifier, str), repr(qualifier)
        string = rf"\baca-circle-{qualifier}-markup =|"
    command = text_spanner(
        string,
        *tweaks,
        autodetect_right_padding=True,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="CircleBow",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def clb_spanner(
    string_number: int,
    *tweaks: _typings.IndexedTweak,
    # NOTE: autodetect default differs from text_spanner():
    autodetect_right_padding: bool = True,
    left_broken: bool = False,
    left_broken_text: str | None = r"\baca-left-broken-clb-markup",
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.CLB_SPANNER)
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
    command = text_spanner(
        f"{markup} =|",
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="CLB",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def covered_spanner(
    *tweaks: _typings.IndexedTweak,
    # NOTE: autodetect default differs from text_spanner():
    autodetect_right_padding: bool = True,
    argument: str = r"\baca-covered-markup =|",
    left_broken: bool = False,
    left_broken_text: str | None = r"\baca-left-broken-covered-markup",
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.COVERED_SPANNER)
    command = text_spanner(
        argument,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="Covered",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def damp_spanner(
    *tweaks: _typings.IndexedTweak,
    # NOTE: autodetect default differs from text_spanner():
    autodetect_right_padding: bool = True,
    left_broken: bool = False,
    left_broken_text: str | None = r"\baca-left-broken-damp-markup",
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.DAMP_SPANNER)
    command = text_spanner(
        r"\baca-damp-markup =|",
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="Damp",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def hairpin(
    dynamics: str | list,
    *tweaks: abjad.Tweak,
    bookend: bool | int = -1,
    final_hairpin: bool | str | abjad.StartHairpin | None = None,
    forbid_al_niente_to_bar_line: bool = False,
    left_broken: bool = False,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    remove_length_1_spanner_start: bool = False,
    right_broken: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> PiecewiseCommand:
    final_hairpin_, specifiers = _prepare_hairpin_arguments(
        dynamics=dynamics,
        final_hairpin=final_hairpin,
        forbid_al_niente_to_bar_line=forbid_al_niente_to_bar_line,
        tweaks=tweaks,
    )
    assert isinstance(bookend, bool | int), repr(bookend)
    assert isinstance(left_broken, bool), repr(left_broken)
    assert isinstance(remove_length_1_spanner_start, bool), repr(
        remove_length_1_spanner_start
    )
    right_broken_: typing.Any = False
    if bool(right_broken) is True:
        right_broken_ = abjad.LilyPondLiteral(r"\!", site="after")
    return PiecewiseCommand(
        bookend=bookend,
        specifiers=specifiers,
        final_piece_spanner=final_hairpin_,
        left_broken=left_broken,
        match=match,
        map=map,
        measures=measures,
        pieces=pieces,
        remove_length_1_spanner_start=remove_length_1_spanner_start,
        right_broken=right_broken_,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def hairpin_function(
    argument,
    dynamics: str | list,
    *tweaks: abjad.Tweak,
    bookend: bool | int = -1,
    final_hairpin: bool | str | abjad.StartHairpin | None = None,
    forbid_al_niente_to_bar_line: bool = False,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    remove_length_1_spanner_start: bool = False,
    right_broken: bool = False,
    tags: list[abjad.Tag] = None,
) -> None:
    final_hairpin_, specifiers = _prepare_hairpin_arguments(
        dynamics=dynamics,
        final_hairpin=final_hairpin,
        forbid_al_niente_to_bar_line=forbid_al_niente_to_bar_line,
        tweaks=tweaks,
    )
    assert isinstance(bookend, bool | int), repr(bookend)
    assert isinstance(remove_length_1_spanner_start, bool), repr(
        remove_length_1_spanner_start
    )
    right_broken_: typing.Any = False
    if bool(right_broken) is True:
        right_broken_ = abjad.LilyPondLiteral(r"\!", site="after")
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    _do_piecewise_command(
        argument,
        manifests={},
        # self_autodetect_right_padding,
        self_bookend=bookend,
        self_final_piece_spanner=final_hairpin_,
        # self_leak_spanner_stop,
        # self_left_broken,
        self_pieces=pieces,
        self_remove_length_1_spanner_start=remove_length_1_spanner_start,
        self_right_broken=right_broken_,
        self_specifiers=specifiers,
        self_tag=tag,
        # self_tweaks,
    )


def half_clt_spanner(
    *tweaks: _typings.IndexedTweak,
    left_broken: bool = False,
    left_broken_text: str | None = r"\baca-left-broken-half-clt-markup",
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.HALF_CLT_SPANNER)
    command = text_spanner(
        "½ clt =|",
        *tweaks,
        autodetect_right_padding=True,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="HalfCLT",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def material_annotation_spanner(
    items: str | list,
    *tweaks: _typings.IndexedTweak,
    left_broken: bool = False,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner()
    selector: typing.Callable = lambda _: _select.rleaves(_),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.MATERIAL_ANNOTATION_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=True,
        bookend=False,
        left_broken=left_broken,
        lilypond_id="MaterialAnnotation",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def metric_modulation_spanner(
    *tweaks: _typings.IndexedTweak,
    argument: str = r"MM =|",
    autodetect_right_padding: bool = True,
    left_broken: bool = False,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner()
    selector: typing.Callable = lambda _: _select.rleaves(_),
) -> PiecewiseCommand:
    # TODO: tag red tweak with METRIC_MODULATION_SPANNER_COLOR
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.METRIC_MODULATION_SPANNER)
    command = text_spanner(
        argument,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=False,
        left_broken=left_broken,
        lilypond_id="MetricModulation",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def parse_hairpin_descriptor(
    descriptor: str,
    *tweaks: abjad.Tweak,
    forbid_al_niente_to_bar_line: bool = False,
) -> list[_Specifier]:
    r"""
    Parses hairpin descriptor.

    ..  container:: example

        >>> for item in baca.parse_hairpin_descriptor("f"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2), spanner_start=None, spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor('"f"'):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='"f"', command='\\baca-effort-f', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2), spanner_start=None, spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("niente"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='niente', command='\\!', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=NegativeInfinity()), spanner_start=None, spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("<"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=None, spanner_start=StartHairpin(shape='<'), spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("< !"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=None, spanner_start=StartHairpin(shape='<'), spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=StopHairpin(leak=False), spanner_start=None, spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("o<|"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=None, spanner_start=StartHairpin(shape='o<|'), spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("--"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=None, spanner_start=StartHairpin(shape='--'), spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("p < f"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='p', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2), spanner_start=StartHairpin(shape='<'), spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2), spanner_start=None, spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("p <"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='p', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2), spanner_start=StartHairpin(shape='<'), spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("p < !"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='p', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2), spanner_start=StartHairpin(shape='<'), spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=StopHairpin(leak=False), spanner_start=None, spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("< f"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=None, spanner_start=StartHairpin(shape='<'), spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2), spanner_start=None, spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("o< f"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=None, spanner_start=StartHairpin(shape='o<'), spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2), spanner_start=None, spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("niente o<| f"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='niente', command='\\!', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=NegativeInfinity()), spanner_start=StartHairpin(shape='o<|'), spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2), spanner_start=None, spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("f >"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2), spanner_start=StartHairpin(shape='>'), spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("f >o"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2), spanner_start=Bundle(indicator=StartHairpin(shape='>o'), tweaks=(Tweak(string='- \\tweak to-barline ##t', tag=None),)), spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("p mp mf f"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='p', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2), spanner_start=None, spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='mp', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-1), spanner_start=None, spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='mf', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=1), spanner_start=None, spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2), spanner_start=None, spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("p < f f > p"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='p', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2), spanner_start=StartHairpin(shape='<'), spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2), spanner_start=None, spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2), spanner_start=StartHairpin(shape='>'), spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='p', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2), spanner_start=None, spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("f -- ! > p"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='f', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2), spanner_start=StartHairpin(shape='--'), spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=StopHairpin(leak=False), spanner_start=StartHairpin(shape='>'), spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='p', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2), spanner_start=None, spanner_stop=None)

        >>> for item in baca.parse_hairpin_descriptor("mf niente o< p"):
        ...     item
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='mf', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=1), spanner_start=None, spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='niente', command='\\!', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=NegativeInfinity()), spanner_start=StartHairpin(shape='o<'), spanner_stop=None)
        _Specifier(bookended_spanner_start=None, indicator=Dynamic(name='p', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2), spanner_start=None, spanner_stop=None)

    """
    assert isinstance(descriptor, str), repr(descriptor)
    indicators: list[
        abjad.Dynamic | abjad.StartHairpin | abjad.StopHairpin | abjad.Bundle
    ] = []
    specifiers: list[_Specifier] = []
    for string in descriptor.split():
        indicator = _commands.make_dynamic(
            string, forbid_al_niente_to_bar_line=forbid_al_niente_to_bar_line
        )
        if _is_maybe_bundled(indicator, abjad.StartHairpin):
            indicator = _tweaks.bundle_tweaks(indicator, tweaks, overwrite=True)
        indicators.append(indicator)
    if len(indicators) == 1:
        if _is_maybe_bundled(indicators[0], abjad.StartHairpin):
            specifier = _Specifier(spanner_start=indicators[0])
        else:
            assert _is_maybe_bundled(indicators[0], abjad.Dynamic)
            specifier = _Specifier(indicator=indicators[0])
        specifiers.append(specifier)
        return specifiers
    if _is_maybe_bundled(indicators[0], abjad.StartHairpin):
        result = indicators.pop(0)
        assert _is_maybe_bundled(result, abjad.StartHairpin)
        specifier = _Specifier(spanner_start=result)
        specifiers.append(specifier)
    if len(indicators) == 1:
        if _is_maybe_bundled(indicators[0], abjad.StartHairpin):
            specifier = _Specifier(spanner_start=indicators[0])
        else:
            specifier = _Specifier(indicator=indicators[0])
        specifiers.append(specifier)
        return specifiers
    for left, right in abjad.sequence.nwise(indicators):
        if _is_maybe_bundled(left, abjad.StartHairpin) and _is_maybe_bundled(
            right, abjad.StartHairpin
        ):
            raise Exception("consecutive start hairpin accumulator.")
        elif _is_maybe_bundled(left, abjad.Dynamic) and _is_maybe_bundled(
            right, abjad.Dynamic
        ):
            specifier = _Specifier(indicator=left)
            specifiers.append(specifier)
        elif _is_maybe_bundled(
            left, abjad.Dynamic | abjad.StopHairpin
        ) and _is_maybe_bundled(right, abjad.StartHairpin):
            specifier = _Specifier(indicator=left, spanner_start=right)
            specifiers.append(specifier)
    if indicators and _is_maybe_bundled(
        indicators[-1], abjad.Dynamic | abjad.StopHairpin
    ):
        specifier = _Specifier(indicator=indicators[-1])
        specifiers.append(specifier)
    return specifiers


def pitch_annotation_spanner(
    items: str | list,
    *tweaks: _typings.IndexedTweak,
    left_broken: bool = False,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner()
    selector: typing.Callable = lambda _: _select.rleaves(_),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.PITCH_ANNOTATION_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=True,
        bookend=False,
        left_broken=left_broken,
        lilypond_id="PitchAnnotation",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def pizzicato_spanner(
    *tweaks: _typings.IndexedTweak,
    # NOTE: autodetect default differs from text_spanner():
    autodetect_right_padding: bool = True,
    left_broken: bool = False,
    left_broken_text: str | None = r"\baca-pizz-markup",
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.PIZZICATO_SPANNER)
    command = text_spanner(
        r"\baca-pizz-markup =|",
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="Pizzicato",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def rhythm_annotation_spanner(
    items: str | list,
    *tweaks: _typings.IndexedTweak,
    left_broken: bool = False,
    leak_spanner_stop: bool = False,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner()
    selector: typing.Callable = lambda _: _select.rleaves(_),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.RHYTHM_ANNOTATION_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=True,
        bookend=False,
        leak_spanner_stop=leak_spanner_stop,
        left_broken=left_broken,
        lilypond_id="RhythmAnnotation",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def scp_spanner(
    items: str | list,
    *tweaks: _typings.IndexedTweak,
    autodetect_right_padding: bool = True,
    bookend: bool | int = False,
    final_piece_spanner: bool | None = None,
    left_broken: bool = False,
    left_broken_text: str = None,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.SCP_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        final_piece_spanner=final_piece_spanner,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="SCP",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def spazzolato_spanner(
    *tweaks: _typings.IndexedTweak,
    # NOTE: autodetect default differs from text_spanner():
    autodetect_right_padding: bool = True,
    items: str | list = r"\baca-spazzolato-markup =|",
    left_broken: bool = False,
    left_broken_text: str | None = r"\baca-left-broken-spazz-markup",
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.SPAZZOLATO_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="Spazzolato",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(command, PiecewiseCommand)
    return result


def string_number_spanner(
    items: str | list,
    *tweaks: _typings.IndexedTweak,
    autodetect_right_padding: bool = True,
    bookend: bool | int = False,
    final_piece_spanner: bool | None = None,
    left_broken: bool = False,
    left_broken_text: str = None,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.STRING_NUMBER_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        final_piece_spanner=final_piece_spanner,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="StringNumber",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def tasto_spanner(
    *tweaks: _typings.IndexedTweak,
    autodetect_right_padding: bool = True,
    bookend: bool | int = False,
    final_piece_spanner: bool | None = None,
    left_broken: bool = False,
    left_broken_text: str = r"\baca-left-broken-t-markup",
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.TASTO_SPANNER)
    command = text_spanner(
        "T =|",
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        final_piece_spanner=final_piece_spanner,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="SCP",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def text_spanner(
    items: str | list,
    *tweaks: _typings.IndexedTweak,
    autodetect_right_padding: bool = False,
    bookend: bool | int = -1,
    boxed: bool = False,
    direction: int = None,
    final_piece_spanner: bool | None = None,
    leak_spanner_stop: bool = False,
    left_broken: bool = False,
    left_broken_text: str = None,
    lilypond_id: int | str | None = None,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> PiecewiseCommand:
    specifiers = _prepare_text_spanner_arguments(
        items,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        boxed=boxed,
        direction=direction,
        final_piece_spanner=final_piece_spanner,
        leak_spanner_stop=leak_spanner_stop,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id=lilypond_id,
        right_broken=right_broken,
    )
    return PiecewiseCommand(
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        specifiers=specifiers,
        final_piece_spanner=final_piece_spanner,
        leak_spanner_stop=leak_spanner_stop,
        left_broken=left_broken,
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
        tags=[_tags.function_name(_frame())],
        tweaks=tweaks,
    )


def text_spanner_function(
    argument,
    items: str | list,
    *tweaks: _typings.IndexedTweak,
    autodetect_right_padding: bool = False,
    bookend: bool | int = -1,
    boxed: bool = False,
    direction: int = None,
    final_piece_spanner: bool | None = None,
    leak_spanner_stop: bool = False,
    left_broken: bool = False,
    left_broken_text: str = None,
    lilypond_id: int | str | None = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    tags: list[abjad.Tag] = None,
) -> None:
    specifiers = _prepare_text_spanner_arguments(
        items,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        boxed=boxed,
        direction=direction,
        final_piece_spanner=final_piece_spanner,
        leak_spanner_stop=leak_spanner_stop,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id=lilypond_id,
        right_broken=right_broken,
    )
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    _do_piecewise_command(
        argument,
        manifests={},
        # self_autodetect_right_padding,
        self_autodetect_right_padding=autodetect_right_padding,
        self_bookend=bookend,
        self_final_piece_spanner=final_piece_spanner,
        # self_leak_spanner_stop,
        self_leak_spanner_stop=leak_spanner_stop,
        # self_left_broken,
        self_left_broken=left_broken,
        self_pieces=pieces,
        # self_remove_length_1_spanner_start,
        # self_right_broken,
        self_specifiers=specifiers,
        self_tag=tag,
        self_tweaks=tweaks,
    )


def vibrato_spanner(
    items: str | list,
    *tweaks: _typings.IndexedTweak,
    autodetect_right_padding: bool = True,
    bookend: bool | int = False,
    final_piece_spanner: bool | None = None,
    left_broken: bool = False,
    left_broken_text: str = None,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.VIBRATO_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        final_piece_spanner=final_piece_spanner,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="Vibrato",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def xfb_spanner(
    *tweaks: _typings.IndexedTweak,
    autodetect_right_padding: bool = True,
    bookend: bool | int = False,
    final_piece_spanner: bool | None = None,
    left_broken: bool = False,
    left_broken_text: str = r"\baca-left-broken-xfb-markup",
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    pieces: typing.Callable = lambda _: abjad.select.group(_),
    right_broken: bool = False,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector: typing.Callable = lambda _: _select.rleak(_select.ltleaves(_)),
) -> PiecewiseCommand:
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.BOW_SPEED_SPANNER)
    command = text_spanner(
        "XFB =|",
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        final_piece_spanner=final_piece_spanner,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="BowSpeed",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = dataclasses.replace(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result
