import sys

import abjad

from . import build
from . import const
from . import jobs
from . import selectors
from .accumulator import CommandAccumulator, segments
from .array import *
from .classes import *
from .commandclasses import *
from .commands import *
from .constellation import *
from .docs import global_context_string
from .figures import *
from .indicatorcommands import *
from .indicators import *
from .interpret import interpret_commands
from .layout import *
from .math import *
from .memento import *
from .overrides import *
from .parts import *
from .path import *
from .persistence import *
from .piecewise import *
from .pitchclasses import *
from .pitchcommands import *
from .rhythmcommands import *
from .scoping import *
from .selection import *
from .sequence import *
from .spannercommands import *
from .templates import *
from .typings import *


def pleaves(*arguments, **keywords):
    return select().pleaves(*arguments, **keywords)


pleaves.__doc__ = Selection.pleaves.__doc__

if sys.version_info[:2] < (3, 9):
    raise ImportError("Requires Python 3.9 or later")
del sys
