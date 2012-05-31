from baca.specification.Division import Division


def test_Division___eq___01():

    assert Division((4, 8)) == Division((4, 8))

    assert not Division((4, 8), is_left_closed=False) == Division((4, 8))
    assert Division((4, 8), is_left_closed=False) == Division((4, 8), is_left_closed=False)

    assert not Division((4, 8), is_right_closed=False) == Division((4, 8))
    assert Division((4, 8), is_right_closed=False) == Division((4, 8), is_right_closed=False)
