import sys
import types

SimpleNamespace = types.SimpleNamespace

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
from .accumulator import (
    Accumulator,
    anchor,
    anchor_after,
    anchor_to_figure,
    label_figure,
    resume,
    resume_after,
)
from .commands import *
from .constellation import *
from .cursor import Cursor
from .docs import global_context_string
from .imbricate import imbricate
from .indicatorclasses import *
from .indicatorcommands import *
from .layout import *
from .lilypond import file
from .memento import *
from .overridecommands import *
from .othercommands import assign_part, call
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
from .rhythm import (
    Grace,
    LMR,
    OBGC,
    attach_bgcs,
    from_collection,
    get_previous_rhythm_state,
    make_accelerando,
    make_bgcs,
    make_even_divisions,
    make_mmrests,
    make_monads,
    make_notes,
    make_repeat_tied_notes,
    make_repeated_duration_notes,
    make_rests,
    make_rhythm,
    make_single_attack,
    make_tied_notes,
    make_tied_repeated_durations,
    make_time_signatures,
    nest,
    parse,
    prolate,
    style_accelerando,
    style_ritardando,
)
from .scope import scope
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
