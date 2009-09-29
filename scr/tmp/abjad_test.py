from abjad import *


t = Staff(construct.scale(4))
spacing_spanner_1 = SpacingSpanner(t[:2])
spacing_spanner_1.new_section = True
spacing_spanner_1.proportional_notation_duration = Rational(1, 15)
spacing_spanner_2 = SpacingSpanner(t[2:])
spacing_spanner_2.new_section = True
spacing_spanner_2.proportional_notation_duration = Rational(1, 30)
