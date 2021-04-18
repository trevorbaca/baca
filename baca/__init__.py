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
    leaves_in_each_plt,
    leaves_in_each_run,
    leaves_in_each_tuplet,
    rleak_runs,
)
from .spannercommands import *
from .templates import *
from .typings import *

Path = ide.Path
tags = ide.tags


def chead(*arguments, **keywords):
    return select().chead(*arguments, **keywords)


chead.__doc__ = Selection.chead.__doc__


def cheads(*arguments, **keywords):
    return select().cheads(*arguments, **keywords)


cheads.__doc__ = Selection.cheads.__doc__


def chord(*arguments, **keywords):
    return select().chord(*arguments, **keywords)


chord.__doc__ = Selection.chord.__doc__


def chords(*arguments, **keywords):
    return select().chords(*arguments, **keywords)


chords.__doc__ = Selection.chords.__doc__


def clparts(*arguments, **keywords):
    return select().clparts(*arguments, **keywords)


clparts.__doc__ = Selection.clparts.__doc__


def cmgroups(*arguments, **keywords):
    return select().cmgroups(*arguments, **keywords)


cmgroups.__doc__ = Selection.cmgroups.__doc__


def components(*arguments, **keywords):
    return select().components(*arguments, **keywords)


components.__doc__ = Selection.components.__doc__


def enchain(*arguments, **keywords):
    return select().enchain(*arguments, **keywords)


enchain.__doc__ = Selection.enchain.__doc__


def grace(*arguments, **keywords):
    return select().grace(*arguments, **keywords)


grace.__doc__ = Selection.grace.__doc__


def graces(*arguments, **keywords):
    return select().graces(*arguments, **keywords)


graces.__doc__ = Selection.graces.__doc__


def group(*arguments, **keywords):
    return select().group(*arguments, **keywords)


group.__doc__ = Selection.group.__doc__


def group_by_measure(*arguments, **keywords):
    return select().group_by_measure(*arguments, **keywords)


group_by_measure.__doc__ = Selection.group_by_measure.__doc__


def hleaf(*arguments, **keywords):
    return select().hleaf(*arguments, **keywords)


hleaf.__doc__ = Selection.hleaf.__doc__


def hleaves(*arguments, **keywords):
    return select().hleaves(*arguments, **keywords)


hleaves.__doc__ = Selection.hleaves.__doc__


def leaf(*arguments, **keywords):
    return select().leaf(*arguments, **keywords)


leaf.__doc__ = Selection.leaf.__doc__


def leaves(*arguments, **keywords):
    return select().leaves(*arguments, **keywords)


leaves.__doc__ = Selection.leaves.__doc__


def lleaf(*arguments, **keywords):
    return select().lleaf(*arguments, **keywords)


lleaf.__doc__ = Selection.lleaf.__doc__


def lleak(*arguments, **keywords):
    return select().lleak(*arguments, **keywords)


lleak.__doc__ = Selection.lleak.__doc__


def lleaves(*arguments, **keywords):
    return select().lleaves(*arguments, **keywords)


lleaves.__doc__ = Selection.lleaves.__doc__


def logical_ties(*arguments, **keywords):
    return select().logical_ties(*arguments, **keywords)


logical_ties.__doc__ = Selection.logical_ties.__doc__


def lparts(*arguments, **keywords):
    return select().lparts(*arguments, **keywords)


lparts.__doc__ = Selection.lparts.__doc__


def lt(*arguments, **keywords):
    return select().lt(*arguments, **keywords)


lt.__doc__ = Selection.lt.__doc__


def ltleaf(*arguments, **keywords):
    return select().ltleaf(*arguments, **keywords)


ltleaf.__doc__ = Selection.ltleaf.__doc__


def ltleaves(*arguments, **keywords):
    return select().ltleaves(*arguments, **keywords)


ltleaves.__doc__ = Selection.ltleaves.__doc__


def ltqrun(*arguments, **keywords):
    return select().ltqrun(*arguments, **keywords)


ltqrun.__doc__ = Selection.ltqrun.__doc__


def ltqruns(*arguments, **keywords):
    return select().ltqruns(*arguments, **keywords)


ltqruns.__doc__ = Selection.ltqruns.__doc__


def ltrun(*arguments, **keywords):
    return select().ltrun(*arguments, **keywords)


ltrun.__doc__ = Selection.ltrun.__doc__


def ltruns(*arguments, **keywords):
    return select().ltruns(*arguments, **keywords)


ltruns.__doc__ = Selection.ltruns.__doc__


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


def mmrests(*arguments, **keywords):
    return select().mmrests(*arguments, **keywords)


mmrests.__doc__ = Selection.mmrests.__doc__


def note(*arguments, **keywords):
    return select().note(*arguments, **keywords)


note.__doc__ = Selection.note.__doc__


def notes(*arguments, **keywords):
    return select().notes(*arguments, **keywords)


notes.__doc__ = Selection.notes.__doc__


def ntrun(*arguments, **keywords):
    return select().ntrun(*arguments, **keywords)


ntrun.__doc__ = Selection.ntrun.__doc__


def ntruns(*arguments, **keywords):
    return select().ntruns(*arguments, **keywords)


ntruns.__doc__ = Selection.ntruns.__doc__


def omgroups(*arguments, **keywords):
    return select().omgroups(*arguments, **keywords)


omgroups.__doc__ = Selection.omgroups.__doc__


def ompltgroups(*arguments, **keywords):
    return select().ompltgroups(*arguments, **keywords)


ompltgroups.__doc__ = Selection.ompltgroups.__doc__


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


def ptlt(*arguments, **keywords):
    return select().ptlt(*arguments, **keywords)


ptlt.__doc__ = Selection.ptlt.__doc__


def ptlts(*arguments, **keywords):
    return select().ptlts(*arguments, **keywords)


ptlts.__doc__ = Selection.ptlts.__doc__


def qrun(*arguments, **keywords):
    return select().qrun(*arguments, **keywords)


qrun.__doc__ = Selection.qrun.__doc__


def qruns(*arguments, **keywords):
    return select().qruns(*arguments, **keywords)


qruns.__doc__ = Selection.qruns.__doc__


def rest(*arguments, **keywords):
    return select().rest(*arguments, **keywords)


rest.__doc__ = Selection.rest.__doc__


def rests(*arguments, **keywords):
    return select().rests(*arguments, **keywords)


rests.__doc__ = Selection.rests.__doc__


def rleaf(*arguments, **keywords):
    return select().rleaf(*arguments, **keywords)


rleaf.__doc__ = Selection.rleaf.__doc__


def rleak(*arguments, **keywords):
    return select().rleak(*arguments, **keywords)


rleak.__doc__ = Selection.rleak.__doc__


def rleaves(*arguments, **keywords):
    return select().rleaves(*arguments, **keywords)


rleaves.__doc__ = Selection.rleaves.__doc__


def rmleaves(*arguments, **keywords):
    return select().rmleaves(*arguments, **keywords)


rmleaves.__doc__ = Selection.rmleaves.__doc__


def rrun(*arguments, **keywords):
    return select().rrun(*arguments, **keywords)


rrun.__doc__ = Selection.rrun.__doc__


def rruns(*arguments, **keywords):
    return select().rruns(*arguments, **keywords)


rruns.__doc__ = Selection.rruns.__doc__


def run(*arguments, **keywords):
    return select().run(*arguments, **keywords)


run.__doc__ = Selection.run.__doc__


def runs(*arguments, **keywords):
    return select().runs(*arguments, **keywords)


runs.__doc__ = Selection.runs.__doc__


def skip(*arguments, **keywords):
    return select().skip(*arguments, **keywords)


skip.__doc__ = Selection.skip.__doc__


def skips(*arguments, **keywords):
    return select().skips(*arguments, **keywords)


skips.__doc__ = Selection.skips.__doc__


def tleaf(*arguments, **keywords):
    return select().tleaf(*arguments, **keywords)


tleaf.__doc__ = Selection.tleaf.__doc__


def tleaves(*arguments, **keywords):
    return select().tleaves(*arguments, **keywords)


tleaves.__doc__ = Selection.tleaves.__doc__


def top(*arguments, **keywords):
    return select().top(*arguments, **keywords)


top.__doc__ = Selection.top.__doc__


def tuplet(*arguments, **keywords):
    return select().tuplet(*arguments, **keywords)


tuplet.__doc__ = Selection.tuplet.__doc__


def tuplets(*arguments, **keywords):
    return select().tuplets(*arguments, **keywords)


tuplets.__doc__ = Selection.tuplets.__doc__


def wleaf(*arguments, **keywords):
    return select().wleaf(*arguments, **keywords)


wleaf.__doc__ = Selection.wleaf.__doc__


def wleaves(*arguments, **keywords):
    return select().wleaves(*arguments, **keywords)


wleaves.__doc__ = Selection.wleaves.__doc__
