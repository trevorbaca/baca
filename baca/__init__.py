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

from baca.tools.Accumulator import _accumulate as accumulate
from baca.tools.PitchClassSegment import PitchClassSegment
from baca.tools.PitchClassSegment import \
    _pitch_class_segment as pitch_class_segment
from baca.tools.Sequence import Sequence
from baca.tools.Sequence import _sequence as sequence
