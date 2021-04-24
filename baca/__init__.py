import abjad
import ide

from . import const
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
from .selectors import (
    leaf_after_each_ptail,
    leaf_in_each_rleak_run,
    leaf_in_each_run,
    leaf_in_each_tuplet,
    leaves_in_each_lt,
    leaves_in_each_plt,
    leaves_in_each_run,
    leaves_in_each_tuplet,
    leaves_in_exclude_tuplets,
    leaves_in_get_tuplets,
    pleaf_in_each_tuplet,
    ptail_in_each_tuplet,
    rleak_runs,
)
from .spannercommands import *
from .templates import *
from .typings import *

Path = ide.Path
tags = ide.tags


def leaf(*arguments, **keywords):
    return select().leaf(*arguments, **keywords)


leaf.__doc__ = Selection.leaf.__doc__


def leaves(*arguments, **keywords):
    return select().leaves(*arguments, **keywords)


leaves.__doc__ = Selection.leaves.__doc__


def lt(*arguments, **keywords):
    return select().lt(*arguments, **keywords)


lt.__doc__ = Selection.lt.__doc__


def lts(*arguments, **keywords):
    return select().lts(*arguments, **keywords)


lts.__doc__ = Selection.lts.__doc__


def note(*arguments, **keywords):
    return select().note(*arguments, **keywords)


note.__doc__ = Selection.note.__doc__


def notes(*arguments, **keywords):
    return select().notes(*arguments, **keywords)


notes.__doc__ = Selection.notes.__doc__


def phead(*arguments, **keywords):
    return select().phead(*arguments, **keywords)


phead.__doc__ = Selection.phead.__doc__


def pheads(*arguments, **keywords):
    return select().pheads(*arguments, **keywords)


pheads.__doc__ = Selection.pheads.__doc__


def pleaf(*arguments, **keywords):
    return select().pleaf(*arguments, **keywords)


pleaf.__doc__ = Selection.pleaf.__doc__


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


def rleaves(*arguments, **keywords):
    return select().rleaves(*arguments, **keywords)


rleaves.__doc__ = Selection.rleaves.__doc__


def run(*arguments, **keywords):
    return select().run(*arguments, **keywords)


run.__doc__ = Selection.run.__doc__


def skip(*arguments, **keywords):
    return select().skip(*arguments, **keywords)


skip.__doc__ = Selection.skip.__doc__


def tleaves(*arguments, **keywords):
    return select().tleaves(*arguments, **keywords)


tleaves.__doc__ = Selection.tleaves.__doc__


def tuplet(*arguments, **keywords):
    return select().tuplet(*arguments, **keywords)


tuplet.__doc__ = Selection.tuplet.__doc__


def tuplets(*arguments, **keywords):
    return select().tuplets(*arguments, **keywords)


tuplets.__doc__ = Selection.tuplets.__doc__
