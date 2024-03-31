import baca
import pytest


def test_layout_01():
    """
    Raises exception on out-of-sequence page numbers.
    """

    with pytest.raises(Exception) as foo:
        baca.layout.layout(
            baca.layout.page(
                1,
                baca.layout.System(1, y_offset=20, distances=(15, 20, 20)),
                baca.layout.System(13, y_offset=140, distances=(15, 20, 20)),
            ),
            baca.layout.page(
                9,
                baca.layout.System(23, y_offset=20, distances=(15, 20, 20)),
            ),
        )

    assert "page number (9) is not 2" in str(foo), repr(foo)
