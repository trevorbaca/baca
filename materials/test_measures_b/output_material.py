from abjad.tools.measuretools.Measure import Measure


test_measures_b = [
	Measure((16, 32), "c'32 c'32 c'32 c'32 c'16 c'16. c'32 c'32 c'32 c'32 c'16 c'32"),
	Measure((16, 32), "c'16 c'32 c'32 c'32 c'32 c'16 c'16. c'32 c'32 c'32 c'32 c'32"),
	Measure((24, 32), "c'32 c'16. c'32 c'32 c'32 c'32 c'16 c'16. c'32 c'32 c'32 c'32 c'16 c'16. c'32 c'32"),
	Measure((16, 32), "c'32 c'32 c'16 c'16. c'32 c'32 c'32 c'32 c'16 c'16."),
	Measure((16, 32), "c'32 c'32 c'32 c'32 c'16 c'16. c'32 c'32 c'32 c'32 c'16 c'32"),
	Measure((24, 32), "c'16 c'32 c'32 c'32 c'32 c'16 c'16. c'32 c'32 c'32 c'32 c'16 c'16. c'32 c'32 c'32 c'32")]
