from abjad.tools import systemtools


systemtools.ImportManager.import_structured_package(
    __path__[0], 
    globals(), 
    )

## must be done manually because C, CC, D are neither functions nor classes
from C import C
from CC import CC
from D import D

del Constellation
del ConstellationCircuit
del constellate