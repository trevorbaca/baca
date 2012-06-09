from abjad.tools import sequencetools
from baca.handlertools.dynamics import *
import baca
__all__ = []


quiet_swells = NoteAndChordHairpinHandler(('pp', '<', 'p'), ('p', '>', 'pp'))
__all__.append('quiet_swells')


tokens = [['ff', 'ff', 'fff'], ['ff', 'ff', 'fff'], ['f', 'fff'], ['ff', 'fff']]
tokens = baca.util.helianthate(tokens, 1, -1)
tokens = sequencetools.flatten_sequence(tokens)
terraced_fortissimo = TerracedDynamicsHandler(tokens)
__all__.append('terraced_fortissimo')


tokens = [['pp', 'pp', 'ppp'], ['pp', 'pp', 'ppp'], ['p', 'ppp'], ['pp', 'ppp']]
tokens = baca.util.helianthate(tokens, 1, -1)
tokens = sequencetools.flatten_sequence(tokens)
terraced_pianissimo = TerracedDynamicsHandler(tokens)
__all__.append('terraced_pianissimo')
