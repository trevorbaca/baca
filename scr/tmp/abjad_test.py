from abjad import *


t = DynamicMeasure(construct.scale(2))
Beam(t[:])
label.measure_numbers(t)
layout.insert_measure_padding_rest(
   t, Rational(1, 32), Rational(1, 64), splice = True)
