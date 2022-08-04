import sys

import abjad

from . import array
from . import build
from . import math
from . import jobs
from . import score
from . import select
from . import sequence
from . import typings
from .enums import colors, enums
from .accumulator import (
    CommandAccumulator,
)
from .command import *
from .commands import *
from .constellation import *
from .cursor import Cursor
from .docs import global_context_string
from .figures import *
from .indicatorclasses import *
from .indicatorcommands import *
from .interpret import (
    append_anchor_note,
    append_anchor_note_function,
    reapply,
    reapply_persistent_indicators,
    scope,
    update_voice_metadata,
)
from .layout import *
from .lilypond import file, make_lilypond_file
from .memento import *
from .overridecommands import *
from .othercommands import assign_part, assign_part_function
from .parts import Part, PartAssignment
from .path import *
from .pcollections import (
    ArpeggiationSpacingSpecifier,
    ChordalSpacingSpecifier,
    HarmonicSeries,
    Partial,
    Registration,
    RegistrationComponent,
)
from .piecewisecommands import (
    PiecewiseCommand,
    bow_speed_spanner,
    circle_bow_spanner,
    clb_spanner,
    clb_spanner_function,
    covered_spanner,
    damp_spanner,
    hairpin,
    hairpin_function,
    half_clt_spanner,
    material_annotation_spanner,
    material_annotation_spanner_function,
    metric_modulation_spanner,
    parse_hairpin_descriptor,
    pitch_annotation_spanner,
    pizzicato_spanner,
    rhythm_annotation_spanner,
    scp_spanner,
    scp_spanner_function,
    spazzolato_spanner,
    spazzolato_spanner_function,
    string_number_spanner,
    tasto_spanner,
    text_spanner,
    text_spanner_function,
    vibrato_spanner,
    vibrato_spanner_function,
    xfb_spanner,
    xfb_spanner_function,
)
from .pitchcommands import *
from .rhythmcommands import *
from .spannercommands import (
    beam,
    beam_function,
    ottava,
    ottava_function,
    ottava_bassa,
    ottava_bassa_function,
    slur,
    slur_function,
    sustain_pedal,
    trill_spanner,
    trill_spanner_function,
)

if sys.version_info[:2] < (3, 10):
    raise ImportError("Requires Python 3.10 or later")
del sys
