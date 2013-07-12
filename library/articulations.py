from abjad.tools import sequencetools
import baca
__all__ = []


accents = baca.handlertools.ReiteratedArticulationHandler(['accent'])
__all__.append('accents')


pattern = [
    ['upbow', 'upbow', 'downbow'], 
    ['upbow', 'upbow', 'downbow', 'downbow'],
    ]
pattern = baca.utilities.helianthate(pattern, 1, 1)
pattern = sequencetools.flatten_sequence(pattern)
pattern = [[x] for x in pattern]
serration_bow_strokes = baca.handlertools.PatternedArticulationsHandler(pattern)
__all__.append('serration_bow_strokes')


stem_tremolo_32 = baca.handlertools.StemTremoloHandler([32])
__all__.append('stem_tremolo_32')
