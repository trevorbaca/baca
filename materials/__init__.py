from baca.scf.helpers import safe_import

safe_import(globals(), 'demo_material', 'demo_material')
safe_import(globals(), 'red_sargasso', 'red_sargasso')
safe_import(globals(), 'sargasso_multipliers', 'sargasso_multipliers')
safe_import(globals(), 'test_measures_a', 'test_measures_a')
safe_import(globals(), 'test_measures_b', 'test_measures_b')

del(safe_import)
