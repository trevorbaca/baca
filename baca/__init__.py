import abjad
from .classes import *
from .commands import *
from .divisions import *
from .indicatorcommands import *
from .indicators import *
from .mmaker import *
from .overrides import *
from .persistence import *
from .piecewise import *
from .pitcharray import *
from .pitchcommands import *
from .pitchclasses import *
from .rhythmcommands import *
from .scoping import *
from .segmentclasses import *
from .segmentmaker import *
from .spannercommands import *
from .templates import *
from . import const
from . import markups

# expression constructors
from .classes import _select as select
from .classes import _sequence as sequence
from .pitchclasses import _pitch_class_segment as pitch_class_segment
from .pitchclasses import _pitch_class_set as pitch_class_set
from .pitchclasses import _pitch_set as pitch_set
from .pitchclasses import _pitch_segment as pitch_segment

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
