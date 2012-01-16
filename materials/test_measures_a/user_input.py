from abjad.tools.durationtools import Duration
#from baca.scf.material_proxys import SargassoMeasureMaterialProxy
from baca.scf import UserInputWrapper


user_input = UserInputWrapper([
	('measure_denominator', 8),
	('measure_numerator_talea', [2, 2, 3]),
	('measure_division_denominator', 32),
	('measure_division_talea', [1, 1, 1, 1, 2, 3]),
	('total_duration', Duration(7, 2)),
	('measures_are_scaled', False),
	('measures_are_split', False),
	('measures_are_shuffled', False)])

#material_proxy = SargassoMeasureMaterialProxy()
#test_measures_a = material_proxy.make(**user_input)
