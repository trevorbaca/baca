import baca


def test_baca_dynamics__DynamicsSpecifier_is_hairpin_token_01():

    assert baca.dynamics._DynamicsSpecifier._DynamicsSpecifier.is_hairpin_token(('', '<', ''))
    assert baca.dynamics._DynamicsSpecifier._DynamicsSpecifier.is_hairpin_token(('p', '<', ''))
    assert baca.dynamics._DynamicsSpecifier._DynamicsSpecifier.is_hairpin_token(('', '<', 'f'))
    assert baca.dynamics._DynamicsSpecifier._DynamicsSpecifier.is_hairpin_token(('p', '<', 'f'))


def test_baca_dynamics__DynamicsSpecifier_is_hairpin_token_02():

    assert not baca.dynamics._DynamicsSpecifier._DynamicsSpecifier.is_hairpin_token(())
    assert not baca.dynamics._DynamicsSpecifier._DynamicsSpecifier.is_hairpin_token(('p', 'f'))
    assert not baca.dynamics._DynamicsSpecifier._DynamicsSpecifier.is_hairpin_token(('p', '@', 'f'))
    assert not baca.dynamics._DynamicsSpecifier._DynamicsSpecifier.is_hairpin_token(('x', '<', 'y'))


def test_baca_dynamics__DynamicsSpecifier_is_hairpin_token_03():

    assert not baca.dynamics._DynamicsSpecifier._DynamicsSpecifier.is_hairpin_token(('f', '<', 'p'))
    assert not baca.dynamics._DynamicsSpecifier._DynamicsSpecifier.is_hairpin_token(('p', '>', 'f'))
    assert not baca.dynamics._DynamicsSpecifier._DynamicsSpecifier.is_hairpin_token(('p', '<', 'p'))
    assert not baca.dynamics._DynamicsSpecifier._DynamicsSpecifier.is_hairpin_token(('f', '>', 'f'))
