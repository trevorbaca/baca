from abjad.tools import sequencetools
import handlertools
__all__ = []


repeated_quarter_divisions_left = handlertools.divisions.RepeatedDivisions([(2, 8)], remainder='left')
__all__.append('repeated_quarter_divisions_left')

repeated_quarter_divisions_right = handlertools.divisions.RepeatedDivisions([(2, 8)], remainder='right')
__all__.append('repeated_quarter_divisions_right')
