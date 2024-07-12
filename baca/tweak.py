import abjad


def _handle_tweak(string, *, event=False, grob=None, i=None, tag=None, target=None):
    if grob is not None:
        string = grob + "." + string
    string = r"- \tweak " + string
    if event is True or target is not None:
        string = string.removeprefix("- ")
    if target is not None:
        assert i is None, repr(i)
        abjad.tweak(target, string, tag=tag)
        return None
    else:
        tweak = abjad.Tweak(string, i=i, tag=tag)
        return tweak


def bound_details_left_broken_text(
    string, *, event=False, grob=None, i=None, tag=None, target=None
):
    string = f"bound-details.left-broken.text {string}"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def bound_details_left_padding(
    n, *, event=False, grob=None, i=None, tag=None, target=None
):
    string = f"bound-details.left.padding {n}"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def bound_details_left_text(
    string, *, event=False, grob=None, i=None, tag=None, target=None
):
    string = f"bound-details.left.text {string}"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def bound_details_right_end_on_accidental_false(
    *, event=False, grob=None, i=None, tag=None, target=None
):
    string = "bound-details.right.end-on-accidental ##f"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def bound_details_right_padding(
    n, *, event=False, grob=None, i=None, tag=None, target=None
):
    string = f"bound-details.right.padding {n}"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def bound_details_right_y(n, *, event=False, grob=None, i=None, tag=None, target=None):
    string = f"bound-details.right.Y {n}"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def color(string, *, event=False, grob=None, i=None, tag=None, target=None):
    string = f"color {string}"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def direction_down(*, event=False, grob=None, i=None, tag=None, target=None):
    string = "direction #down"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def extra_offset(pair, *, event=False, grob=None, i=None, tag=None, target=None):
    x, y = pair
    string = f"extra-offset #'({x} . {y})"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def font_size(n, *, event=False, grob=None, i=None, tag=None, target=None):
    string = f"font-size {n}"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def padding(n, *, event=False, grob=None, i=None, tag=None, target=None):
    string = f"padding {n}"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def parent_alignment_x(n, *, event=False, grob=None, i=None, tag=None, target=None):
    string = f"parent-alignment-X {n}"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def self_alignment_x(n, *, event=False, grob=None, i=None, tag=None, target=None):
    string = f"self-alignment-X {n}"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def shorten_pair(pair, *, event=False, grob=None, i=None, tag=None, target=None):
    x, y = pair
    string = f"shorten-pair #'({x} . {y})"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def staff_padding(n, *, event=False, grob=None, i=None, tag=None, target=None):
    string = f"staff-padding {n}"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def style_harmonic(*, event=False, grob=None, i=None, tag=None, target=None):
    string = "style #'harmonic"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def style_trill(*, event=False, grob=None, i=None, tag=None, target=None):
    string = "style #'trill"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def to_bar_line_false(*, event=False, grob=None, i=None, tag=None, target=None):
    string = "to-barline ##f"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def to_bar_line_true(*, event=False, grob=None, i=None, tag=None, target=None):
    string = "to-barline ##t"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def x_extent_false(*, event=False, grob=None, i=None, tag=None, target=None):
    string = "X-extent ##f"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def x_extent_zero(*, event=False, grob=None, i=None, tag=None, target=None):
    string = "X-extent #'(0 . 0)"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def x_offset(n, *, event=False, grob=None, i=None, tag=None, target=None):
    string = f"X-offset {n}"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def y_extent_false(*, event=False, grob=None, i=None, tag=None, target=None):
    string = "Y-extent ##f"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)


def y_extent_zero(*, event=False, grob=None, i=None, tag=None, target=None):
    string = "Y-extent #'(0 . 0)"
    return _handle_tweak(string, event=event, grob=grob, i=i, tag=tag, target=target)
