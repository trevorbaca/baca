import handlers


def test_DynamicHandler_is_hairpin_token_01():

    assert handlers.dynamics.DynamicHandler.is_hairpin_token(('', '<', ''))
    assert handlers.dynamics.DynamicHandler.is_hairpin_token(('p', '<', ''))
    assert handlers.dynamics.DynamicHandler.is_hairpin_token(('', '<', 'f'))
    assert handlers.dynamics.DynamicHandler.is_hairpin_token(('p', '<', 'f'))


def test_DynamicHandler_is_hairpin_token_02():

    assert not handlers.dynamics.DynamicHandler.is_hairpin_token(())
    assert not handlers.dynamics.DynamicHandler.is_hairpin_token(('p', 'f'))
    assert not handlers.dynamics.DynamicHandler.is_hairpin_token(('p', '@', 'f'))
    assert not handlers.dynamics.DynamicHandler.is_hairpin_token(('x', '<', 'y'))


def test_DynamicHandler_is_hairpin_token_03():

    assert not handlers.dynamics.DynamicHandler.is_hairpin_token(('f', '<', 'p'))
    assert not handlers.dynamics.DynamicHandler.is_hairpin_token(('p', '>', 'f'))
    assert not handlers.dynamics.DynamicHandler.is_hairpin_token(('p', '<', 'p'))
    assert not handlers.dynamics.DynamicHandler.is_hairpin_token(('f', '>', 'f'))
