import abjad
from .library import *
from .classes import *
from .commands import *
from .divisions import *
from .dynamics import *
from .indicators import *
from .markups import Markup
from .overrides import *
from .pitcharray import *
from .pitchcommands import *
from .pitchclasses import *
from .rhythmcommands import *
from .scoping import *
from .segmentclasses import *
from .spannercommands import *
from .templates import *
from . import markups

# classes
from .AnchorSpecifier import AnchorSpecifier
from .Coat import Coat
from .Expression import Expression
from .ExpressionGallery import ExpressionGallery
from .ImbricationCommand import ImbricationCommand
from .LMRSpecifier import LMRSpecifier
from .MusicAccumulator import MusicAccumulator
from .MusicContribution import MusicContribution
from .MusicMaker import MusicMaker
from .NestingCommand import NestingCommand
from .PersistentIndicatorTests import PersistentIndicatorTests
from .PitchSpecifier import PitchSpecifier
from .RestAffixSpecifier import RestAffixSpecifier
from .SchemeManifest import SchemeManifest
from .SegmentMaker import SegmentMaker
from .SegmentMaker import WellformednessManager
from .Selection import Selection
from .Sequence import Sequence

# expression constructors
from .pitchclasses import _pitch_class_segment as pitch_class_segment
from .pitchclasses import _pitch_class_set as pitch_class_set
from .pitchclasses import _pitch_set as pitch_set
from .pitchclasses import _pitch_segment as pitch_segment
from .Selection import _select as select
from .Sequence import _sequence as sequence

def _publish_selectors(class_):
    for name in dir(class_):
        if name.startswith('_'):
            continue
        if name in ('map',):
            continue
        statement = f"""def {name}(*arguments, **keywords):
            return select().{name}(*arguments, **keywords)"""
        exec(statement, globals())

from .LibraryAF import *
from .LibraryGM import *
from .LibraryNS import *
from .LibraryTZ import *

_publish_selectors(Selection)
