from abjad import *
from abjad.tools import sequencetools
from handlers import divisions
import baca
__all__ = []


repeated_quarter_divisions_left = divisions.RepeatedDivisions([(2, 8)], remainder='left')
__all__.append('repeated_quarter_divisions_left')

repeated_quarter_divisions_right = divisions.RepeatedDivisions([(2, 8)], remainder='right')
__all__.append('repeated_quarter_divisions_right')
