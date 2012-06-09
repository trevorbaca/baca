from abjad.tools import markuptools
from baca.handlertools.articulations import *
import baca
__all__ = []


markups = [markuptools.Markup(r'\italic { "molto sul ponticello" }')]
molto_sul_ponticello = RepeatedMarkupHandler(markups)
__all__.append('molto_sul_ponticello')

markups = [markuptools.Markup(r'\italic { "flautando molto" }')]
flautando_molto = RepeatedMarkupHandler(markups)
__all__.append('flautando_molto')
