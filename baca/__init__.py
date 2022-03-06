import sys

import abjad

from . import array
from . import build
from . import const

# from . import math
from . import jobs
from . import score
from . import select
from . import selectors
from . import sequence
from . import typings
from .accumulator import (
    CommandAccumulator,
    segment_accumulation_defaults,
)
from .classes import *
from .commandclasses import *
from .commands import *
from .constellation import *
from .docs import global_context_string
from .figures import *
from .indicatorcommands import *
from .indicators import *
from .interpret import (
    interpreter,
    make_lilypond_file,
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
from .scoping import *
from .select import *
from .spanners import *

del math
from . import math


if sys.version_info[:2] < (3, 10):
    raise ImportError("Requires Python 3.10 or later")
del sys
