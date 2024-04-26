import abjad


def _handle_index(tweak, *, index=None):
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = (tweak, index)
    return tweak


def bound_details_left_broken_text(string, *, grob=None, index=None):
    if grob is None:
        tweak = abjad.Tweak(rf"- \tweak bound-details.left-broken.text {string}")
    else:
        tweak = abjad.Tweak(rf"- \tweak {grob}.bound-details.left-broken.text {string}")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = (tweak, index)
    return tweak


def bound_details_left_padding(n, *, grob=None, index=None):
    if grob is None:
        tweak = abjad.Tweak(rf"- \tweak bound-details.left.padding {n}")
    else:
        tweak = abjad.Tweak(rf"- \tweak {grob}.bound-details.left.padding {n}")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = (tweak, index)
    return tweak


def bound_details_left_text(string, *, grob=None, index=None):
    if grob is None:
        tweak = abjad.Tweak(rf"- \tweak bound-details.left.text {string}")
    else:
        tweak = abjad.Tweak(rf"- \tweak {grob}.bound-details.left.text {string}")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = (tweak, index)
    return tweak


def bound_details_right_end_on_accidental_false(*, index=None):
    tweak = abjad.Tweak(r"- \tweak bound-details.right.end-on-accidental ##f")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = (tweak, index)
    return tweak


def bound_details_right_padding(n, *, grob=None, index=None):
    if grob is None:
        tweak = abjad.Tweak(rf"- \tweak bound-details.right.padding {n}")
    else:
        tweak = abjad.Tweak(rf"- \tweak {grob}.bound-details.right.padding {n}")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = (tweak, index)
    return tweak


def bound_details_right_y(n):
    tweak = abjad.Tweak(rf"- \tweak bound-details.right.Y {n}")
    return tweak


def color(string):
    tweak = abjad.Tweak(rf"- \tweak color {string}")
    return tweak


def direction_down():
    tweak = abjad.Tweak(r"- \tweak direction #down")
    return tweak


def extra_offset(pair, *, tag=None):
    x, y = pair
    tweak = abjad.Tweak(rf"- \tweak extra-offset #'({x} . {y})", tag=tag)
    return tweak


def font_size(n, *, index=None):
    tweak = abjad.Tweak(rf"- \tweak font-size {n}")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = (tweak, index)
    return tweak


def padding(n, *, event=False, grob=None):
    if grob is None:
        string = rf"\tweak padding {n}"
    else:
        string = rf"\tweak {grob}.padding {n}"
    if event is False:
        string = "- " + string
    tweak = abjad.Tweak(string)
    return tweak


def parent_alignment_x(n):
    tweak = abjad.Tweak(rf"- \tweak parent-alignment-X {n}")
    return tweak


def self_alignment_x(n):
    tweak = abjad.Tweak(rf"- \tweak self-alignment-X {n}")
    return tweak


def shorten_pair(pair):
    x, y = pair
    tweak = abjad.Tweak(rf"- \tweak shorten-pair #'({x} . {y})")
    return tweak


def staff_padding(n, *, grob=None):
    if grob is None:
        tweak = abjad.Tweak(rf"- \tweak staff-padding {n}")
    else:
        tweak = abjad.Tweak(rf"- \tweak {grob}.staff-padding {n}")
    return tweak


def style_harmonic(*, index=None, target=None):
    string = r"\tweak style #'harmonic"
    if target is not None:
        abjad.tweak(target, string)
    else:
        string = "- " + string
        tweak = abjad.Tweak(string)
        tweak = _handle_index(tweak, index=index)
        return tweak


def style_trill(*, index=None):
    tweak = abjad.Tweak(r"- \tweak style #'trill")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = (tweak, index)
    return tweak


def to_bar_line_false(*, index=None):
    tweak = abjad.Tweak(r"- \tweak to-barline ##f")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = (tweak, index)
    return tweak


def to_bar_line_true(*, index=None):
    tweak = abjad.Tweak(r"- \tweak to-barline ##t")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = (tweak, index)
    return tweak


def x_extent_zero(*, tag=None):
    tweak = abjad.Tweak(r"- \tweak X-extent #'(0 . 0)", tag=tag)
    return tweak


def x_offset(n):
    tweak = abjad.Tweak(rf"- \tweak X-offset {n}")
    return tweak
