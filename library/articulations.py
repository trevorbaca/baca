from abjad.tools import sequencetools
from baca.handlers.dynamics import *
from fractions import Fraction
import baca
__all__ = []


pattern = [['upbow', 'upbow', 'downbow'], ['upbow', 'upbow', 'downbow', 'downbow']]
pattern = baca.util.helianthate(pattern, 1, 1)
pattern = sequencetools.flatten_sequence(pattern)
pattern = [[x] for x in pattern]
serration_bow_strokes = baca.handlers.articulations.PatternedArticulationsHandler(pattern)
__all__.append('serration_bow_strokes')
