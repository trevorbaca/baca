import sys
import types

SimpleNamespace = types.SimpleNamespace

import abjad

from . import (
    array,
    build,
    dynamics,
    layout,
    math,
    override,
    path,
    score,
    section,
    select,
    sequence,
    spanners,
    tweak,
    typings,
)
from ._version import __version__
from .anchor import (
    anchor,
    anchor_after,
    anchor_to_figure,
    label_figure,
    resume,
    resume_after,
)
from .classes import *
from .commands import (
    bcps,
    durations,
    finger_pressure_transition,
    force_accidental,
    glissando,
    levine_multiphonic,
    untie,
)
from .constellation import *
from .docs import global_context_string
from .enums import colors, enums
from .hairpins import hairpin
from .helpers import call
from .imbricate import imbricate
from .indicators import *
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
    LMR,
    from_collection,
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
