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
    leaves_,
    rleaf_,
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


def clparts(*arguments, **keywords):
    return select().clparts(*arguments, **keywords)


clparts.__doc__ = Selection.clparts.__doc__


def cmgroups(*arguments, **keywords):
    return select().cmgroups(*arguments, **keywords)


cmgroups.__doc__ = Selection.cmgroups.__doc__


def leaf(*arguments, **keywords):
    return select().leaf(*arguments, **keywords)


leaf.__doc__ = Selection.leaf.__doc__


def leaves(*arguments, **keywords):
    return select().leaves(*arguments, **keywords)


leaves.__doc__ = Selection.leaves.__doc__


def lleaf(*arguments, **keywords):
    return select().lleaf(*arguments, **keywords)


lleaf.__doc__ = Selection.lleaf.__doc__


def logical_ties(*arguments, **keywords):
    return select().logical_ties(*arguments, **keywords)


logical_ties.__doc__ = Selection.logical_ties.__doc__


def lparts(*arguments, **keywords):
    return select().lparts(*arguments, **keywords)


lparts.__doc__ = Selection.lparts.__doc__


def lt(*arguments, **keywords):
    return select().lt(*arguments, **keywords)


lt.__doc__ = Selection.lt.__doc__


def ltleaves(*arguments, **keywords):
    return select().ltleaves(*arguments, **keywords)


ltleaves.__doc__ = Selection.ltleaves.__doc__


def ltqruns(*arguments, **keywords):
    return select().ltqruns(*arguments, **keywords)


ltqruns.__doc__ = Selection.ltqruns.__doc__


def lts(*arguments, **keywords):
    return select().lts(*arguments, **keywords)


lts.__doc__ = Selection.lts.__doc__


def mgroups(*arguments, **keywords):
    return select().mgroups(*arguments, **keywords)


mgroups.__doc__ = Selection.mgroups.__doc__


def mleaves(*arguments, **keywords):
    return select().mleaves(*arguments, **keywords)


mleaves.__doc__ = Selection.mleaves.__doc__


def mmrest(*arguments, **keywords):
    return select().mmrest(*arguments, **keywords)


mmrest.__doc__ = Selection.mmrest.__doc__


def note(*arguments, **keywords):
    return select().note(*arguments, **keywords)


note.__doc__ = Selection.note.__doc__


def notes(*arguments, **keywords):
    return select().notes(*arguments, **keywords)


notes.__doc__ = Selection.notes.__doc__


def ntruns(*arguments, **keywords):
    return select().ntruns(*arguments, **keywords)


ntruns.__doc__ = Selection.ntruns.__doc__


def omgroups(*arguments, **keywords):
    return select().omgroups(*arguments, **keywords)


omgroups.__doc__ = Selection.omgroups.__doc__


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


def qruns(*arguments, **keywords):
    return select().qruns(*arguments, **keywords)


qruns.__doc__ = Selection.qruns.__doc__


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


def runs(*arguments, **keywords):
    return select().runs(*arguments, **keywords)


runs.__doc__ = Selection.runs.__doc__


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
