from baca.specification.Division import Division


def test_Division___repr___01():

    assert repr(Division((4, 8))) == 'Division((4, 8))'
    assert repr(Division((4, 8), is_left_closed=False)) == 'Division((4, 8), is_left_closed=False)'
    assert repr(Division((4, 8), is_right_closed=False)) == 'Division((4, 8), is_right_closed=False)'
