import abjad


def bound_details_right_end_on_accidental_false(*, index=None):
    tweak = abjad.Tweak(r"- \tweak bound-details.right.end-on-accidental ##f")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = (tweak, index)
    return tweak


def bound_details_right_padding(n):
    tweak = abjad.Tweak(rf"- \tweak bound-details.right.padding {n}")
    return tweak


def color(string):
    tweak = abjad.Tweak(rf"- \tweak color {string}")
    return tweak


def direction_down():
    tweak = abjad.Tweak(r"- \tweak direction #down")
    return tweak


def padding(n):
    tweak = abjad.Tweak(rf"- \tweak padding {n}")
    return tweak


def parent_alignment_x(n):
    tweak = abjad.Tweak(rf"- \tweak parent-alignment-X {n}")
    return tweak


def self_alignment_x(n):
    tweak = abjad.Tweak(rf"- \tweak self-alignment-X {n}")
    return tweak


def staff_padding(n):
    tweak = abjad.Tweak(rf"- \tweak staff-padding {n}")
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
