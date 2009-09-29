from abjad import *

t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
pitchtools.diatonicize(t)
layout.line_break_every_prolated(t, Rational(4, 8))      

systems = SystemYOffsets(40, 5)
staves = StaffAlignmentOffsets(0, -15)
positioning = FixedStaffPositioning(systems, staves)
layout.apply_fixed_staff_positioning(t, positioning)
