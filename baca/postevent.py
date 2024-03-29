import abjad


def to_bar_line_false(*, index=None):
    tweak = abjad.Tweak(r"- \tweak to-barline ##t")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = tweak(tweak, index)
    return tweak


def to_bar_line_true(*, index=None):
    tweak = abjad.Tweak(r"- \tweak to-barline ##t")
    if index is not None:
        assert isinstance(index, int), repr(index)
        tweak = tweak(tweak, index)
    return tweak
