import sys

import abjad

from . import array
from . import build
from . import math
from . import jobs
from . import path
from . import score
from . import select
from . import sequence
from . import typings
from .enums import colors, enums
from .commands import *
from .constellation import *
from .cursor import Cursor
from .docs import global_context_string
from .figures import (
    LMR,
    anchor,
    anchor_after,
    anchor_to_figure,
    figure,
    imbricate,
    lmr,
    make_figures,
    nest,
    rests_after,
    rests_after,
    rests_around,
    rests_around,
    rests_before,
    rests_before,
    resume,
    resume_after,
    skips_before,
)
from .indicatorclasses import *
from .indicatorcommands import *
from .layout import *
from .lilypond import file
from .memento import *
from .overridecommands import *
from .othercommands import assign_part
from .parts import Part, PartAssignment
from .pcollections import (
    ArpeggiationSpacingSpecifier,
    ChordalSpacingSpecifier,
    HarmonicSeries,
    Partial,
    Registration,
    RegistrationComponent,
)
from .piecewisecommands import (
    bow_speed_spanner,
    circle_bow_spanner,
    clb_spanner,
    covered_spanner,
    damp_spanner,
    hairpin,
    half_clt_spanner,
    material_annotation_spanner,
    metric_modulation_spanner,
    parse_hairpin_descriptor,
    pizzicato_spanner,
    scp_spanner,
    spazzolato_spanner,
    string_number_spanner,
    tasto_spanner,
    text_spanner,
    vibrato_spanner,
    xfb_spanner,
)
from .pitchcommands import *
from .rhythmcommands import *
from .section import scope, time_signatures
from .spannercommands import (
    beam,
    ottava,
    ottava_bassa,
    slur,
    sustain_pedal,
    trill_spanner,
)

if sys.version_info[:2] < (3, 10):
    raise ImportError("Requires Python 3.10 or later")
del sys
