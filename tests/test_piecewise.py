import abjad
import baca
import pytest


def test_piecewise_01():
    """
    baca.text_spanner() errors on unkonwn LilyPond ID.
    """

    voice = abjad.Voice("c'4 d' e' f'")
    with pytest.raises(Exception):
        baca.text_spanner(
            voice,
            "T -> P",
            lilypond_id=4,
        )
