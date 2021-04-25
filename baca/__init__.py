import abjad
import ide

from . import const
from . import selectors
from . import tonality
from .classes import *
from .commandclasses import *
from .commands import *
from .figuremaker import *
from .indicatorcommands import *
from .indicators import *
from .mathx import *
from .overrides import *
from .persistence import *
from .piecewise import *
from .pitcharray import *
from .pitchclasses import *
from .pitchcommands import *
from .rhythmcommands import *
from .scoping import *
from .segmentclasses import *
from .segmentmaker import *
from .spannercommands import *
from .templates import *
from .typings import *

Path = ide.Path
tags = ide.tags


def leaves(*arguments, **keywords):
    return select().leaves(*arguments, **keywords)


leaves.__doc__ = Selection.leaves.__doc__


def lts(*arguments, **keywords):
    return select().lts(*arguments, **keywords)


lts.__doc__ = Selection.lts.__doc__


def pleaves(*arguments, **keywords):
    return select().pleaves(*arguments, **keywords)


pleaves.__doc__ = Selection.pleaves.__doc__


def plt(*arguments, **keywords):
    return select().plt(*arguments, **keywords)


plt.__doc__ = Selection.plt.__doc__


def plts(*arguments, **keywords):
    return select().plts(*arguments, **keywords)


plts.__doc__ = Selection.plts.__doc__


def ptail(*arguments, **keywords):
    return select().ptail(*arguments, **keywords)


ptail.__doc__ = Selection.ptail.__doc__


def ptails(*arguments, **keywords):
    return select().ptails(*arguments, **keywords)


ptails.__doc__ = Selection.ptails.__doc__


def rest(*arguments, **keywords):
    return select().rest(*arguments, **keywords)


rest.__doc__ = Selection.rest.__doc__


def rests(*arguments, **keywords):
    return select().rests(*arguments, **keywords)


rests.__doc__ = Selection.rests.__doc__


def run(*arguments, **keywords):
    return select().run(*arguments, **keywords)


run.__doc__ = Selection.run.__doc__


def skip(*arguments, **keywords):
    return select().skip(*arguments, **keywords)


skip.__doc__ = Selection.skip.__doc__
