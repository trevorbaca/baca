import abjad
import baca


def test_LMR_01():
    """
    Left counts equal to a single 1.
    """

    lmr = baca.LMR(
        left_counts=[1],
        left_cyclic=False,
        left_length=3,
        right_length=2,
    )

    parts = lmr([1])
    assert parts == [[1]]

    parts = lmr([1, 2])
    assert parts == [[1], [2]]

    parts = lmr([1, 2, 3])
    assert parts == [[1], [2, 3]]

    parts = lmr([1, 2, 3, 4])
    assert parts == [[1], [2, 3], [4]]

    parts = lmr([1, 2, 3, 4, 5])
    assert parts == [[1], [2, 3], [4, 5]]

    parts = lmr([1, 2, 3, 4, 5, 6])
    assert parts == [[1], [2, 3], [4], [5, 6]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7])
    assert parts == [[1], [2, 3], [4, 5], [6, 7]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    assert parts == [[1], [2, 3], [4, 5, 6], [7, 8]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert parts == [[1], [2, 3], [4, 5, 6, 7], [8, 9]]


def test_LMR_02():
    """
    Left counts all equal to 1.
    """

    lmr = baca.LMR(
        left_counts=[1],
        left_cyclic=True,
        left_length=3,
        right_length=2,
    )

    parts = lmr([1])
    assert parts == [[1]]

    parts = lmr([1, 2])
    assert parts == [[1], [2]]

    parts = lmr([1, 2, 3])
    assert parts == [[1], [2], [3]]

    parts = lmr([1, 2, 3, 4])
    assert parts == [[1], [2], [3], [4]]

    parts = lmr([1, 2, 3, 4, 5])
    assert parts == [[1], [2], [3], [4, 5]]

    parts = lmr([1, 2, 3, 4, 5, 6])
    assert parts == [[1], [2], [3], [4], [5, 6]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7])
    assert parts == [[1], [2], [3], [4, 5], [6, 7]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    assert parts == [[1], [2], [3], [4, 5, 6], [7, 8]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert parts == [[1], [2], [3], [4, 5, 6, 7], [8, 9]]


def test_LMR_03():
    """
    Left length equal to 2.
    """

    lmr = baca.LMR(
        left_length=2,
    )

    parts = lmr([1])
    assert parts == [[1]]

    parts = lmr([1, 2])
    assert parts == [[1, 2]]

    parts = lmr([1, 2, 3])
    assert parts == [[1, 2], [3]]

    parts = lmr([1, 2, 3, 4])
    assert parts == [[1, 2], [3, 4]]

    parts = lmr([1, 2, 3, 4, 5])
    assert parts == [[1, 2], [3, 4, 5]]

    parts = lmr([1, 2, 3, 4, 5, 6])
    assert parts == [[1, 2], [3, 4, 5, 6]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7])
    assert parts == [[1, 2], [3, 4, 5, 6, 7]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    assert parts == [[1, 2], [3, 4, 5, 6, 7, 8]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert parts == [[1, 2], [3, 4, 5, 6, 7, 8, 9]]


def test_LMR_04():
    """
    Cyclic middle counts equal to [2].

    Odd parity produces length-1 part at right.
    """

    lmr = baca.LMR(
        middle_counts=[2],
        middle_cyclic=True,
    )

    parts = lmr([1])
    assert parts == [[1]]

    parts = lmr([1, 2])
    assert parts == [[1, 2]]

    parts = lmr([1, 2, 3])
    assert parts == [[1, 2], [3]]

    parts = lmr([1, 2, 3, 4])
    assert parts == [[1, 2], [3, 4]]

    parts = lmr([1, 2, 3, 4, 5])
    assert parts == [[1, 2], [3, 4], [5]]

    parts = lmr([1, 2, 3, 4, 5, 6])
    assert parts == [[1, 2], [3, 4], [5, 6]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7])
    assert parts == [[1, 2], [3, 4], [5, 6], [7]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    assert parts == [[1, 2], [3, 4], [5, 6], [7, 8]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert parts == [[1, 2], [3, 4], [5, 6], [7, 8], [9]]


def test_LMR_05():
    """
    Reversed cyclic middle counts equal to [2].

    Odd parity produces length-1 part at left.
    """

    lmr = baca.LMR(
        middle_counts=[2],
        middle_cyclic=True,
        middle_reversed=True,
    )

    parts = lmr([1])
    assert parts == [[1]]

    parts = lmr([1, 2])
    assert parts == [[1, 2]]

    parts = lmr([1, 2, 3])
    assert parts == [[1], [2, 3]]

    parts = lmr([1, 2, 3, 4])
    assert parts == [[1, 2], [3, 4]]

    parts = lmr([1, 2, 3, 4, 5])
    assert parts == [[1], [2, 3], [4, 5]]

    parts = lmr([1, 2, 3, 4, 5, 6])
    assert parts == [[1, 2], [3, 4], [5, 6]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7])
    assert parts == [[1], [2, 3], [4, 5], [6, 7]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    assert parts == [[1, 2], [3, 4], [5, 6], [7, 8]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert parts == [[1], [2, 3], [4, 5], [6, 7], [8, 9]]


def test_LMR_06():
    """
    Priority to the left.
    """

    lmr = baca.LMR(
        left_length=2,
        right_length=1,
    )

    parts = lmr([1])
    assert parts == [[1]]

    parts = lmr([1, 2])
    assert parts == [[1, 2]]

    parts = lmr([1, 2, 3])
    assert parts == [[1, 2], [3]]

    parts = lmr([1, 2, 3, 4])
    assert parts == [[1, 2], [3], [4]]

    parts = lmr([1, 2, 3, 4, 5])
    assert parts == [[1, 2], [3, 4], [5]]

    parts = lmr([1, 2, 3, 4, 5, 6])
    assert parts == [[1, 2], [3, 4, 5], [6]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7])
    assert parts == [[1, 2], [3, 4, 5, 6], [7]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    assert parts == [[1, 2], [3, 4, 5, 6, 7], [8]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert parts == [[1, 2], [3, 4, 5, 6, 7, 8], [9]]


def test_LMR_07():
    """
    Priority to the right.
    """

    lmr = baca.LMR(
        left_length=2,
        priority=abjad.RIGHT,
        right_length=1,
    )

    parts = lmr([1])
    assert parts == [[1]]

    parts = lmr([1, 2])
    assert parts == [[1], [2]]

    parts = lmr([1, 2, 3])
    assert parts == [[1, 2], [3]]

    parts = lmr([1, 2, 3, 4])
    assert parts == [[1, 2], [3], [4]]

    parts = lmr([1, 2, 3, 4, 5])
    assert parts == [[1, 2], [3, 4], [5]]

    parts = lmr([1, 2, 3, 4, 5, 6])
    assert parts == [[1, 2], [3, 4, 5], [6]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7])
    assert parts == [[1, 2], [3, 4, 5, 6], [7]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    assert parts == [[1, 2], [3, 4, 5, 6, 7], [8]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert parts == [[1, 2], [3, 4, 5, 6, 7, 8], [9]]


def test_LMR_08():
    """
    Right length equal to 2.
    """

    lmr = baca.LMR(
        right_length=2,
    )

    parts = lmr([1])
    assert parts == [[1]]

    parts = lmr([1, 2])
    assert parts == [[1, 2]]

    parts = lmr([1, 2, 3])
    assert parts == [[1], [2, 3]]

    parts = lmr([1, 2, 3, 4])
    assert parts == [[1, 2], [3, 4]]

    parts = lmr([1, 2, 3, 4, 5])
    assert parts == [[1, 2, 3], [4, 5]]

    parts = lmr([1, 2, 3, 4, 5, 6])
    assert parts == [[1, 2, 3, 4], [5, 6]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7])
    assert parts == [[1, 2, 3, 4, 5], [6, 7]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    assert parts == [[1, 2, 3, 4, 5, 6], [7, 8]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert parts == [[1, 2, 3, 4, 5, 6, 7], [8, 9]]


def test_LMR_09():
    """
    Right length equal to 2 and left counts equal to [1].
    """

    lmr = baca.LMR(
        left_counts=[1],
        left_cyclic=False,
        right_length=2,
    )

    parts = lmr([1])
    assert parts == [[1]]

    parts = lmr([1, 2])
    assert parts == [[1, 2]]

    parts = lmr([1, 2, 3])
    assert parts == [[1], [2, 3]]

    parts = lmr([1, 2, 3, 4])
    assert parts == [[1], [2], [3, 4]]

    parts = lmr([1, 2, 3, 4, 5])
    assert parts == [[1], [2, 3], [4, 5]]

    parts = lmr([1, 2, 3, 4, 5, 6])
    assert parts == [[1], [2, 3, 4], [5, 6]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7])
    assert parts == [[1], [2, 3, 4, 5], [6, 7]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    assert parts == [[1], [2, 3, 4, 5, 6], [7, 8]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert parts == [[1], [2, 3, 4, 5, 6, 7], [8, 9]]


def test_LMR_10():
    """
    Default LMR.
    """

    lmr = baca.LMR()

    parts = lmr([1])
    assert parts == [[1]]

    parts = lmr([1, 2])
    assert parts == [[1, 2]]

    parts = lmr([1, 2, 3])
    assert parts == [[1, 2, 3]]

    parts = lmr([1, 2, 3, 4])
    assert parts == [[1, 2, 3, 4]]

    parts = lmr([1, 2, 3, 4, 5])
    assert parts == [[1, 2, 3, 4, 5]]

    parts = lmr([1, 2, 3, 4, 5, 6])
    assert parts == [[1, 2, 3, 4, 5, 6]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7])
    assert parts == [[1, 2, 3, 4, 5, 6, 7]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    assert parts == [[1, 2, 3, 4, 5, 6, 7, 8]]

    parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert parts == [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
