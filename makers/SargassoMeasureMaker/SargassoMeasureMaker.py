from baca.makers._InteractiveMaterialMaker import _InteractiveMaterialMaker
from abjad.tools import durationtools


class SargassoMeasureMaker(_InteractiveMaterialMaker):

    def __init__(self):
        pass

    ### PUBLIC METHODS ###

    def main(self):
        print 'Welcome to sargasso measure maker.'
        print 'Unit duration of measures:'
        print '(Ex.: Duration(1, 4))'
        response = raw_input('Your choice: ')
        exec('measure_unit_duration = durationtools.Duration(%s)' % response)
        print measure_unit_duration
