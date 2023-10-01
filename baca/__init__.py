import sys
import types

SimpleNamespace = types.SimpleNamespace

import abjad

from . import array
from . import build
from . import math
from . import path
from . import score
from . import section
from . import select
from . import sequence
from . import typings
from .enums import colors, enums
from .anchor import (
    anchor,
    anchor_after,
    anchor_to_figure,
    label_figure,
    resume,
    resume_after,
)
from .commands import *
from .constellation import *
from .docs import global_context_string
from .imbricate import imbricate
from .classes import *
from .helpers import call
from .indicators import *
from .layout import *
from .lilypond import file
from .memento import *
from .overrides import *
from .parts import Part, PartAssignment, assign_part
from .pcollections import (
    ArpeggiationSpacingSpecifier,
    ChordalSpacingSpecifier,
    HarmonicSeries,
    Partial,
    Registration,
    RegistrationComponent,
)
from .piecewise import (
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
from .pitchtools import *
from .rhythm import (
    AfterGrace,
    BeamLeft,
    BeamRight,
    Container,
    Feather,
    Grace,
    InvisibleMusic,
    LMR,
    OBGC,
    RepeatTie,
    Tie,
    Tuplet,
    WrittenDuration,
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
    prolate,
    style_accelerando,
    style_ritardando,
)
from .scope import scope
from .spanners import (
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
