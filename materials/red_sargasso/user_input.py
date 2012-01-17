from abjad.tools.durationtools import Duration
from baca.scf import UserInputWrapper


user_input = UserInputWrapper([
	('measure_denominator', 8),
	('measure_numerator_talea', [2, 2, 3, 4]),
	('measure_division_denominator', None),
	('measure_division_talea', None),
	('total_duration', Duration(3, 1)),
	('measures_are_scaled', None),
	('measures_are_split', True),
	('measures_are_shuffled', False)])