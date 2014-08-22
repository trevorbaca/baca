from abjad.tools import handlertools
from abjad.tools import sequencetools
import baca
__all__ = []


accents = handlertools.ReiteratedArticulationHandler(['accent'])
__all__.append('accents')


pattern = [
    ['upbow', 'upbow', 'downbow'], 
    ['upbow', 'upbow', 'downbow', 'downbow'],
    ]
pattern = baca.utilities.helianthate(pattern, 1, 1)
pattern = sequencetools.flatten_sequence(pattern)
pattern = [[x] for x in pattern]
serration_bow_strokes = handlertools.PatternedArticulationsHandler(pattern)
__all__.append('serration_bow_strokes')


stem_tremolo_32 = handlertools.StemTremoloHandler([32])
__all__.append('stem_tremolo_32')