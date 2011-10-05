from abjad.tools.measuretools.Measure import Measure


test_measures_a = [
	Measure((8, 32), "c'32 c'32 c'32 c'32 c'16 c'16"),
	Measure((8, 32), "c'32 c'32 c'32 c'32 c'32 c'16 c'32"),
	Measure((12, 32), "c'16 c'32 c'32 c'32 c'32 c'16 c'16. c'32"),
	Measure((8, 32), "c'32 c'32 c'32 c'16 c'16."),
	Measure((8, 32), "c'32 c'32 c'32 c'32 c'16 c'16"),
	Measure((12, 32), "c'32 c'32 c'32 c'32 c'32 c'16 c'16. c'32 c'32"),
	Measure((8, 32), "c'32 c'32 c'16 c'16. c'32"),
	Measure((8, 32), "c'32 c'32 c'32 c'16 c'16."),
	Measure((12, 32), "c'32 c'32 c'32 c'32 c'16 c'16. c'32 c'32 c'32"),
	Measure((8, 32), "c'32 c'16 c'16. c'32 c'32"),
	Measure((8, 32), "c'32 c'32 c'16 c'16. c'32"),
	Measure((12, 32), "c'32 c'32 c'32 c'16 c'16. c'32 c'32 c'32 c'32")]
