import sys

import abjad

from . import build
from . import const
from . import jobs
from . import score
from . import select
from . import selectors
from . import sequence
from .accumulator import (
    CommandAccumulator,
    segment_accumulation_defaults,
)
from .array import *
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
from .math import *
from .memento import *
from .overrides import *
from .parts import *
from .path import *
from .pcollections import *
from .persistence import *
from .piecewise import *
from .rhythmcommands import *
from .scoping import *
from .select import *
from .spannercommands import *
from .typings import *


if sys.version_info[:2] < (3, 10):
    raise ImportError("Requires Python 3.10 or later")
del sys
