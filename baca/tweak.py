"""
Tweaks.
"""

import abjad


def bundle_tweaks(argument, tweaks, *, i=None, total=None, overwrite=False):
    if not tweaks:
        return argument
    all_tweaks = []
    for item in tweaks:
        if isinstance(item, tuple):
            assert len(item) == 2
            item, index = item
            if 0 <= index and index != i:
                continue
            if index < 0 and index != -(total - i):
                continue
        assert isinstance(item, abjad.Tweak), repr(item)
        all_tweaks.append(item)
    bundle = abjad.bundle(argument, *all_tweaks, overwrite=overwrite)
    return bundle


def extend(
    tweaks,
    *,
    bound_details_right_padding: int | float | None = None,
    staff_padding: int | float | None = None,
):
    if bound_details_right_padding is not None:
        string = rf"- \tweak bound-details.right.padding {bound_details_right_padding}"
        tweaks = tweaks + (abjad.Tweak(string),)
    if staff_padding is not None:
        tweaks = tweaks + (abjad.Tweak(rf"- \tweak staff-padding {staff_padding}"),)
    return tweaks


def note_head_style_harmonic(note_head):
    assert isinstance(note_head, abjad.NoteHead), repr(note_head)
    abjad.tweak(note_head, abjad.Tweak(r"\tweak style #'harmonic"))


def validate_indexed_tweaks(tweaks):
    if tweaks is None:
        return
    assert isinstance(tweaks, tuple), repr(tweaks)
    for tweak in tweaks:
        if isinstance(tweak, str | abjad.Tweak):
            continue
        if (
            isinstance(tweak, tuple)
            and len(tweak) == 2
            and isinstance(tweak[0], abjad.Tweak)
        ):
            continue
        raise Exception(tweak)
