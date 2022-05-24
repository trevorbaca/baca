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
from .accumulator import (
    CommandAccumulator,
    section_accumulation_defaults,
)
from .command import *
from .commands import *
from .constellation import *
from .cursor import Cursor
from .docs import global_context_string
from .enums import colors, enums
from .figures import *
from .indicators import *
from .interpret import (
    append_anchor_note,
    append_phantom_measure,
    interpreter,
    make_lilypond_file,
    reapply_persistent_indicators,
    score_interpretation_defaults,
)
from .layout import *
from .memento import *
from .overrides import *
from .parts import *
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
from .rhythmcommands import *
from .scope import *
from .select import *
from .spanners import *

if sys.version_info[:2] < (3, 10):
    raise ImportError("Requires Python 3.10 or later")
del sys
