import baca
import pytest


def test_layout_01():
    """
    baca.breaks() raises exception on out-of-sequence page speicfiers.
    """

    with pytest.raises(Exception) as foo:
        baca.breaks(
            baca.page(
                1,
                baca.system(measure=1, y_offset=20, distances=(15, 20, 20)),
                baca.system(measure=13, y_offset=140, distances=(15, 20, 20)),
            ),
            baca.page(
                9,
                baca.system(measure=23, y_offset=20, distances=(15, 20, 20)),
            ),
        )

    assert "page number (9) is not 2" in str(foo), repr(foo)
