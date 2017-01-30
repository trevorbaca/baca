# -*- coding: utf-8 -*-
from baca import tools
from baca.tools.ArticulationInterface import ArticulationInterface as \
    articulations
from baca.tools.DynamicInterface import DynamicInterface as dynamics
from baca.tools.MarkupInterface import MarkupInterface as markup
from baca.tools.OverrideInterface import OverrideInterface as overrides
from baca.tools.PitchInterface import PitchInterface as pitch
from baca.tools.RhythmInterface import RhythmInterface as rhythm
from baca.tools.SelectInterface import SelectInterface as select
from baca.tools.SpannerInterface import SpannerInterface as spanners
from baca.tools.TransformInterface import TransformInterface as transforms
from baca.tools.WrapInterface import WrapInterface as wrap

### toplevel functions ###

from baca.tools.Expression import Expression
from baca.tools.PitchClassSegment import PitchClassSegment
from baca.tools.PitchClassSegment import \
    _pitch_class_segment as pitch_class_segment
from baca.tools.Sequence import Sequence
from baca.tools.Sequence import _sequence as sequence

def _import_static_methods(interface_class, interface_class_name):
    for name in dir(interface_class):
        if name.startswith('_'):
            continue
        statement = '{} = {}.{}'
        statement = statement.format(name, interface_class_name, name)
        exec(statement, globals())

_import_static_methods(articulations, 'articulations')
_import_static_methods(dynamics, 'dynamics')
_import_static_methods(overrides, 'overrides')
_import_static_methods(pitch, 'pitch')
_import_static_methods(rhythm, 'rhythm')
_import_static_methods(spanners, 'spanners')
_import_static_methods(transforms, 'transforms')

# these interfaces must be module-referenced:
# baca.markup.*()
# baca.select.*()
# baca.wrap.*()

make_markup_specifier = markup.make_markup_specifier
