import baca


def test_baca_dynamic_DynamicsManager_is_hairpin_token_01( ):

   assert baca.dynamics.DynamicsManager.is_hairpin_token(('', '<', ''))
   assert baca.dynamics.DynamicsManager.is_hairpin_token(('p', '<', ''))
   assert baca.dynamics.DynamicsManager.is_hairpin_token(('', '<', 'f'))
   assert baca.dynamics.DynamicsManager.is_hairpin_token(('p', '<', 'f'))


def test_baca_dynamic_DynamicsManager_is_hairpin_token_02( ):

   assert not baca.dynamics.DynamicsManager.is_hairpin_token(( ))
   assert not baca.dynamics.DynamicsManager.is_hairpin_token(('p', 'f'))
   assert not baca.dynamics.DynamicsManager.is_hairpin_token(('p', '@', 'f'))
   assert not baca.dynamics.DynamicsManager.is_hairpin_token(('x', '<', 'y'))
