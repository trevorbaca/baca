import abjad


def bound_details_right_end_on_accidental_false(*, index=None):
    tweak = abjad.Tweak(r"- \tweak bound-details.right.end-on-accidental ##f")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = (tweak, index)
    return tweak


def bound_details_right_padding(n, *, grob=None):
    if grob is None:
        tweak = abjad.Tweak(rf"- \tweak bound-details.right.padding {n}")
    else:
        tweak = abjad.Tweak(rf"- \tweak {grob}.bound-details.right.padding {n}")
    return tweak


def color(string):
    tweak = abjad.Tweak(rf"- \tweak color {string}")
    return tweak


def direction_down():
    tweak = abjad.Tweak(r"- \tweak direction #down")
    return tweak


def extra_offset(pair):
    x, y = pair
    tweak = abjad.Tweak(rf"- \tweak extra-offset #'({x} . {y})")
    return tweak


def padding(n, *, grob=None, not_postevent=False):
    if not_postevent is True:
        if grob is None:
            tweak = abjad.Tweak(rf"\tweak padding {n}")
        else:
            tweak = abjad.Tweak(rf"\tweak {grob}.padding {n}")
    else:
        if grob is None:
            tweak = abjad.Tweak(rf"- \tweak padding {n}")
        else:
            tweak = abjad.Tweak(rf"- \tweak {grob}.padding {n}")
    return tweak


def parent_alignment_x(n):
    tweak = abjad.Tweak(rf"- \tweak parent-alignment-X {n}")
    return tweak


def self_alignment_x(n):
    tweak = abjad.Tweak(rf"- \tweak self-alignment-X {n}")
    return tweak


def staff_padding(n, *, grob=None):
    if grob is None:
        tweak = abjad.Tweak(rf"- \tweak staff-padding {n}")
    else:
        tweak = abjad.Tweak(rf"- \tweak {grob}.staff-padding {n}")
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
