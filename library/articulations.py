from abjad.tools import sequencetools
import baca
__all__ = []


accents = baca.handlertools.articulations.ReiteratedArticulationHandler(['accent'])
__all__.append('accents')


pattern = [['upbow', 'upbow', 'downbow'], ['upbow', 'upbow', 'downbow', 'downbow']]
pattern = baca.util.helianthate(pattern, 1, 1)
pattern = sequencetools.flatten_sequence(pattern)
pattern = [[x] for x in pattern]
serration_bow_strokes = baca.handlertools.articulations.PatternedArticulationsHandler(pattern)
__all__.append('serration_bow_strokes')


stem_tremolo_32 = baca.handlertools.articulations.StemTremoloHandler([32])
__all__.append('stem_tremolo_32')
