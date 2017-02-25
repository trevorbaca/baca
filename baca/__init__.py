# -*- coding: utf-8 -*-
from baca import tools
from baca.tools.Library import Library as library
from baca.tools.MarkupLibrary import MarkupLibrary as markup

### toplevel functions ###

from baca.tools.Cursor import Cursor
from baca.tools.Expression import Expression
from baca.tools.PitchClassSegment import PitchClassSegment
from baca.tools.PitchClassSegment import \
    _pitch_class_segment as pitch_class_segment
from baca.tools.SegmentList import SegmentList
from baca.tools.Sequence import Sequence
from baca.tools.Sequence import _sequence as sequence

def _import_static_methods(interface_class, interface_class_name):
    for name in dir(interface_class):
        if name.startswith('_'):
            continue
        statement = '{} = {}.{}'
        statement = statement.format(name, interface_class_name, name)
        exec(statement, globals())

# baca.markup.*() must be module-referenced
_import_static_methods(library, 'library')
