import abjad
from .library import *
from .classes import *
from .commands import *
from .divisions import *
from .dynamics import *
from .indicatorcommands import *
from .indicators import *
from .musicmaker import *
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
from .Expression import Expression
from .PersistentIndicatorTests import PersistentIndicatorTests
from .SchemeManifest import SchemeManifest
from .segmentmaker import *
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

_publish_selectors(Selection)

from .Selection import _select
# TODO: move to baca.Selection
def mleaves(count: int) -> abjad.Expression:
    """
    Selects all leaves in ``count`` measures.
    """
    assert isinstance(count, int), repr(count)
    selector = _select().leaves().group_by_measure()
    if 0 < count:
        selector = selector[:count].flatten()
    elif count < 0:
        selector = selector[-count:].flatten()
    else:
        raise Exception(count)
    return selector

# TODO: move to baca.Selection
def rmleaves(count: int) -> abjad.Expression:
    """
    Selects all leaves in ``count`` measures, leaked one leaf to the right.
    """
    assert isinstance(count, int), repr(count)
    selector = _select().leaves().group_by_measure()
    selector = selector[:count].flatten().rleak()
    return selector

