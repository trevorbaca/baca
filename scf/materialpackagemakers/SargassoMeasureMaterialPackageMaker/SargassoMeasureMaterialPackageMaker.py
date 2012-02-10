from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import sequencetools
from baca.music.make_sargasso_measures import make_illustration_from_output_material
from baca.scf.MaterialPackageMaker import MaterialPackageMaker
from baca.scf.UserInputWrapper import UserInputWrapper
from baca.scf import predicates
import baca


class SargassoMeasureMaterialPackageMaker(MaterialPackageMaker):

    def __init__(self, package_importable_name=None, session=None):
        MaterialPackageMaker.__init__(
            self, package_importable_name=package_importable_name, session=session)

    ### PUBLIC CLASS ATTRIBUTES ###

    generic_output_name = 'sargasso measures'

    illustration_maker = staticmethod(make_illustration_from_output_material)

    output_material_checker = staticmethod(measuretools.all_are_measures)
            
    output_material_maker = staticmethod(baca.music.make_sargasso_measures)

    # TODO: 
    #output_material_module_import_statements = [
    #    'from abjad.tools import measuretools',
    #]
    output_material_module_import_statements = [
        'from abjad.tools.measuretools.Measure import Measure',
        ]

    user_input_demo_values = [
        ('measure_denominator', 4),
        ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
        ('measure_division_denominator', 16),
        ('measure_division_talea', [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
        ('total_duration', durationtools.Duration(44, 8)),
        ('measures_are_scaled', True),
        ('measures_are_split', True),
        ('measures_are_shuffled', True),
        ]

    # TODO:
    #user_input_module_import_statements = [
    #    'from abjad.tools import durationtools',
    #]
    user_input_module_import_statements = [
        'from abjad.tools.durationtools import Duration',
        'from baca.scf import UserInputWrapper',
        ]

    user_input_tests = [
        ('measure_denominator', mathtools.is_positive_integer_power_of_two),
        ('measure_numerator_talea', sequencetools.all_are_nonnegative_integers),
        ('measure_division_denominator', mathtools.is_nonnegative_integer_power_of_two),
        ('measure_division_talea', sequencetools.all_are_nonnegative_integers),
        ('total_duration', durationtools.is_duration_token, 'value = Duration({})'),
        ('measures_are_scaled', predicates.is_boolean),
        ('measures_are_split', predicates.is_boolean),
        ('measures_are_shuffled', predicates.is_boolean),
        ]

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    def make_output_material_module_body_lines(self, output_material):
        lines = []
        lines.append('{} = ['.format(self.material_underscored_name))
        for measure in output_material[:-1]:
            line = measuretools.measure_to_one_line_input_string(measure)
            lines.append('\t{},'.format(line))
        line = measuretools.measure_to_one_line_input_string(output_material[-1])
        lines.append('\t{}]'.format(line))
        lines = [line + '\n' for line in lines]
        return lines
