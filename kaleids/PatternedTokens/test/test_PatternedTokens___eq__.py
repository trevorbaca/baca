import kaleids


def test_PatternedTokens___eq___01():

    kaleid_1 = kaleids.PatternedTokens([-1, 2, -3, 4], 16,
        prolation_addenda=[2, 3],
        secondary_divisions=[6],
        )

    kaleid_2 = kaleids.PatternedTokens([-1, 2, -3, 4], 16,
        prolation_addenda=[2, 3],
        secondary_divisions=[6],
        )

    assert kaleid_1 == kaleid_1
    assert kaleid_1 == kaleid_2
    assert not kaleid_1 == 'foo'
    assert kaleid_2 == kaleid_1
    assert kaleid_2 == kaleid_2
    assert not kaleid_2 == 'foo'
    assert not 'foo' == kaleid_1
    assert not 'foo' == kaleid_2
    assert 'foo' == 'foo'
