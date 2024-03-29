import sys
import types

SimpleNamespace = types.SimpleNamespace

import abjad

from . import array
from . import build
from . import dynamics
from . import math
from . import override
from . import path
from . import postevent
from . import score
from . import section
from . import select
from . import sequence
from . import spanners
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
from .commands import (
    bcps,
    color,
    durations,
    finger_pressure_transition,
    force_accidental,
    glissando,
    levine_multiphonic,
    untie,
)
from .constellation import *
from .docs import global_context_string
from .imbricate import imbricate
from .classes import *
from .hairpins import hairpin
from .helpers import call
from .indicators import *
from .layout import *
from .lilypond import file
from .memento import *
from .parts import Part, PartAssignment, assign_part
from .pcollections import (
    ArpeggiationSpacingSpecifier,
    ChordalSpacingSpecifier,
    HarmonicSeries,
    Partial,
    Registration,
    RegistrationComponent,
)
from .pitchtools import *

from .rhythm import (
    from_collection,
    LMR,
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

if sys.version_info[:2] < (3, 10):
    raise ImportError("Requires Python 3.10 or later")
del sys
