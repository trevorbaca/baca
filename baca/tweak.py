import abjad


def bound_details_left_broken_text(string, *, grob=None, i=None):
    if grob is None:
        tweak = abjad.Tweak(rf"- \tweak bound-details.left-broken.text {string}", i=i)
    else:
        tweak = abjad.Tweak(
            rf"- \tweak {grob}.bound-details.left-broken.text {string}", i=i
        )
    return tweak


def bound_details_left_padding(n, *, grob=None, i=None):
    if grob is None:
        tweak = abjad.Tweak(rf"- \tweak bound-details.left.padding {n}", i=i)
    else:
        tweak = abjad.Tweak(rf"- \tweak {grob}.bound-details.left.padding {n}", i=i)
    return tweak


def bound_details_left_text(string, *, grob=None, i=None):
    if grob is None:
        tweak = abjad.Tweak(rf"- \tweak bound-details.left.text {string}", i=i)
    else:
        tweak = abjad.Tweak(rf"- \tweak {grob}.bound-details.left.text {string}", i=i)
    return tweak


def bound_details_right_end_on_accidental_false(*, i=None):
    tweak = abjad.Tweak(r"- \tweak bound-details.right.end-on-accidental ##f", i=i)
    return tweak


def bound_details_right_padding(n, *, grob=None, i=None):
    if grob is None:
        tweak = abjad.Tweak(rf"- \tweak bound-details.right.padding {n}", i=i)
    else:
        tweak = abjad.Tweak(rf"- \tweak {grob}.bound-details.right.padding {n}", i=i)
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


def extra_offset(pair, *, event=False, tag=None):
    x, y = pair
    string = rf"- \tweak extra-offset #'({x} . {y})"
    if event is True:
        string = string.removeprefix("- ")
    tweak = abjad.Tweak(string, tag=tag)
    return tweak


def font_size(n, *, i=None):
    tweak = abjad.Tweak(rf"- \tweak font-size {n}", i=i)
    return tweak


def padding(n, *, event=False, grob=None):
    if grob is None:
        string = rf"- \tweak padding {n}"
    else:
        string = rf"- \tweak {grob}.padding {n}"
    if event is True:
        string = string.removeprefix("- ")
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


def style_harmonic(*, i=None, target=None):
    string = r"\tweak style #'harmonic"
    if target is not None:
        abjad.tweak(target, string)
    else:
        string = "- " + string
        tweak = abjad.Tweak(string, i=i)
        return tweak


def style_trill(*, i=None):
    tweak = abjad.Tweak(r"- \tweak style #'trill", i=i)
    return tweak


def to_bar_line_false(*, i=None):
    tweak = abjad.Tweak(r"- \tweak to-barline ##f", i=i)
    return tweak


def to_bar_line_true(*, i=None):
    tweak = abjad.Tweak(r"- \tweak to-barline ##t", i=i)
    return tweak


def x_extent_false(*, event=False, tag=None):
    string = r"- \tweak X-extent ##f"
    if event is True:
        string = string.removeprefix("- ")
    tweak = abjad.Tweak(string, tag=tag)
    return tweak


def x_extent_zero(*, tag=None):
    tweak = abjad.Tweak(r"- \tweak X-extent #'(0 . 0)", tag=tag)
    return tweak


def x_offset(n):
    tweak = abjad.Tweak(rf"- \tweak X-offset {n}")
    return tweak
