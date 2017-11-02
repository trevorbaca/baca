from baca import tools
# TODO: eliminate explicit class imports in favor of from baca.tools import *
from baca.tools.CollectionList import CollectionList
from baca.tools.Cursor import Cursor
from baca.tools.Expression import Expression
from baca.tools.LibraryAM import LibraryAM
from baca.tools.LibraryNZ import LibraryNZ
from baca.tools.MapCommand import MapCommand
from baca.tools.MarkupLibrary import MarkupLibrary
from baca.tools.MusicMaker import MusicMaker
from baca.tools.PitchClassSegment import PitchClassSegment
from baca.tools.PitchClassSegment import \
    _pitch_class_segment as pitch_class_segment
from baca.tools.PitchClassSet import PitchClassSet
from baca.tools.PitchClassSet import _pitch_class_set as pitch_class_set
from baca.tools.PitchSegment import PitchSegment
from baca.tools.PitchSegment import _pitch_segment as pitch_segment
from baca.tools.PitchSet import PitchSet
from baca.tools.PitchSet import _pitch_set as pitch_set
from baca.tools.SegmentMaker import SegmentMaker
from baca.tools.Selection import Selection
from baca.tools.Selection import _select as select
from baca.tools.Sequence import Sequence
from baca.tools.Sequence import _sequence as sequence
from baca.tools import *

def map(commands, selector):
    return MapCommand(commands, selector)

def _import_static_methods(class_):
    for name in dir(class_):
        if name.startswith('_'):
            continue
        statement = f'{name} = {class_.__name__}.{name}'
        exec(statement, globals())


_import_static_methods(LibraryAM)
_import_static_methods(LibraryNZ)
markup = MarkupLibrary()
