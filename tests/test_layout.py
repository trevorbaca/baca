import abjad
import baca
import pytest


def test_layout_01():
    """
    Raises exception on out-of-sequence page numbers.
    """

    with pytest.raises(Exception) as foo:
        baca.layout.Breaks(
            baca.layout.Page(
                1,
                baca.layout.System(1, y_offset=20, distances=(15, 20, 20)),
                baca.layout.System(13, y_offset=140, distances=(15, 20, 20)),
            ),
            baca.layout.Page(
                9,
                baca.layout.System(23, y_offset=20, distances=(15, 20, 20)),
            ),
        )

    assert "page number (9) is not 2" in str(foo), repr(foo)


def test_SpacingSection():

    voice = abjad.Voice("c'4 d' e' f'")
    spacing = baca.layout.SpacingSection((2, 24))
    abjad.attach(spacing, voice[0])
    string = abjad.lilypond(voice)

    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            \baca-new-spacing-section #2 #24
            c'4
            d'4
            e'4
            f'4
        }
        """
    )
