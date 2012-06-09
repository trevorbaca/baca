from handlertools.pitch.OctaveTranspositionHandler import OctaveTranspositionHandler as handler
__all__ = []


piano_upper_tenth = handler(['[A0, C4) => C6', '[C4, C8] => E6'])
__all__.append('piano_upper_tenth')

cello_treble = handler(['[A0, C4) => F#4', '[C4, C8] => A#4'])
__all__.append('cello_treble')

cello_baritone = handler(['[A0, C4) => F2', '[C4, C8] => Ab3'])
__all__.append('cello_baritone')
