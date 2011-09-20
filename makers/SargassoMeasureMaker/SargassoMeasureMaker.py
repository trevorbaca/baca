from baca.makers._InteractiveMaterialMaker import _InteractiveMaterialMaker
#from abjad.tools import sequencetools
#from abjad.tools.durationtools import Duration


class SargassoMeasureMaker(_InteractiveMaterialMaker):

    def __init__(self):
        pass

    ### PUBLIC METHODS ###

    def conclude(self):
        print 'Making ended.'
        response = raw_input('Press any key to continue.')

    def make_material_interactively(self):
        print 'Welcome to sargasso measure maker.\n'

        output_header_lines = [
            'from abjad import *',
            'from abjad.tools import sequencetools',]

        for header_line in output_header_lines:
            exec(header_line)

        output_body_lines = []

        response = raw_input('Talea unit duration: ')
        line = 'talea_unit_duration = Duration(%s)' % response
        exec(line)
        output_body_lines.append(line)
        print ''

        response = raw_input('Measure talea: ')
        line = 'measure_talea = %s' % response
        exec(line)
        output_body_lines.append(line)
        print ''

        response = raw_input('Repeat talea to weight exactly: ')
        line = 'weight_of_talea = %s' % response
        exec(line)
        output_body_lines.append(line)
        print ''

        line = 'measure_talea = sequencetools.repeat_sequence_to_weight_exactly(measure_talea, weight_of_talea)'
        exec(line)
        output_body_lines.append(line)
        print ''

        print talea_unit_duration
        print weight_of_talea
        print measure_talea
        print ''

        for line in output_header_lines:
            print line
        print ''
        for line in output_body_lines:
            print line
        print ''

        self.conclude()
