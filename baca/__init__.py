from baca import tools
from baca.tools import *
from baca.tools.PitchClassSegment import \
    _pitch_class_segment as pitch_class_segment
from baca.tools.PitchClassSet import _pitch_class_set as pitch_class_set
from baca.tools.PitchSegment import _pitch_segment as pitch_segment
from baca.tools.PitchSet import _pitch_set as pitch_set
from baca.tools.Selection import _select as select
from baca.tools.Sequence import _sequence as sequence

def _import_static_methods(class_):
    for name in dir(class_):
        if name.startswith('_'):
            continue
        statement = f'{name} = {class_.__name__}.{name}'
        exec(statement, globals())

def _publish_selectors(class_):
    for name in dir(class_):
        if name.startswith('_'):
            continue
        if name in ('map',):
            continue
        statement = f'''def {name}(*arguments, **keywords):
            return select().{name}(*arguments, **keywords)'''
        exec(statement, globals())

_import_static_methods(LibraryAF)
_import_static_methods(LibraryGM)
_import_static_methods(LibraryNS)
_import_static_methods(LibraryTZ)
_publish_selectors(Selection)
markup = MarkupLibrary
make_markup = MarkupLibrary.make_markup

def map(commands, selector):
    r'''Maps `commands` to result of `selector`.

    Returns map command.
    '''
    return MapCommand(commands, selector)
