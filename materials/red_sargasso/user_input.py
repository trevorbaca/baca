from abjad.tools.durationtools import Duration
from baca.scf import UserInputWrapper


user_input = UserInputWrapper([
	('measure_denominator', None),
	('measure_numerator_talea', None),
	('measure_division_denominator', None),
	('measure_division_talea', None),
	('total_duration', None),
	('measures_are_scaled', None),
	('measures_are_split', None),
	('measures_are_shuffled', None)])