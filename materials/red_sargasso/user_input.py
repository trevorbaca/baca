from abjad.tools.durationtools import Duration
from baca.scf import UserInputWrapper


user_input = UserInputWrapper([
	('measure_denominator', 8),
	('measure_numerator_talea', [1, 1, 1, 1, 2, 2, 9]),
	('measure_division_denominator', 16),
	('measure_division_talea', [1, 1, 2, 1, 1, 2]),
	('total_duration', Duration(3, 1)),
	('measures_are_scaled', True),
	('measures_are_split', False),
	('measures_are_shuffled', False)])