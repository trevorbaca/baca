from handlers.pitch.OctaveTranspositionHandler import OctaveTranspositionHandler as handler


piano_upper_tenth = handler(['[A0, C4) => C6', '[C4, C8] => E6'])

cello_treble = handler(['[A0, C4) => F#4', '[C4, C8] => A#4'])
cello_baritone = handler(['[A0, C4) => F2', '[C4, C8] => Ab3'])
