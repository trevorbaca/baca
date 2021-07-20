import abjad

from . import build
from . import const
from . import jobs
from . import selectors
from . import tonality
from .classes import *
from .commandclasses import *
from .commands import *
from .figuremaker import *
from .indicatorcommands import *
from .indicators import *
from .math import *
from .overrides import *
from .path import *
from .persistence import *
from .piecewise import *
from .pitcharray import *
from .pitchclasses import *
from .pitchcommands import *
from .rhythmcommands import *
from .scoping import *
from .segmentclasses import *
from .segmentmaker import *
from .segments import *
from .spannercommands import *
from .templates import *
from .typings import *


def pleaves(*arguments, **keywords):
    return select().pleaves(*arguments, **keywords)


pleaves.__doc__ = Selection.pleaves.__doc__
