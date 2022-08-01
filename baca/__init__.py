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
from .articulations import *
from .command import *
from .commands import *
from .constellation import *
from .cursor import Cursor
from .docs import global_context_string
from .figures import *
from .indicatorclasses import *
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
from .overrides import *
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
from .piecewise import *
from .pitchfunctions import *
from .rhythmcommands import *
from .select import *
from .spanners import *

if sys.version_info[:2] < (3, 10):
    raise ImportError("Requires Python 3.10 or later")
del sys
