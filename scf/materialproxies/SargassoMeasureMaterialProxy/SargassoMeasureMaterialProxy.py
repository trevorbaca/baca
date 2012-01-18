from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import sequencetools
from baca.music.make_sargasso_measures import make_illustration_from_output_material
from baca.scf.UserInputHandlingMaterialProxy import UserInputHandlingMaterialProxy
from baca.scf.UserInputWrapper import UserInputWrapper
import baca


class SargassoMeasureMaterialProxy(UserInputHandlingMaterialProxy):

    def __init__(self, package_importable_name=None, session=None):
        UserInputHandlingMaterialProxy.__init__(
            self, package_importable_name=package_importable_name, session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    generic_output_name = 'sargasso measures'

    illustration_maker = staticmethod(make_illustration_from_output_material)

    # TODO: implement measuretools predicate
    output_material_checker = staticmethod(
        lambda x: componenttools.all_are_components(x, klasses=measuretools.Measure))
            
    output_material_maker = staticmethod(baca.music.make_sargasso_measures)

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
        ('measures_are_scaled', bool),
        ('measures_are_split', bool),
        ('measures_are_shuffled', bool),
        ]

    ### PUBLIC METHODS ###

    def make_output_material_module_body_lines(self):
        lines = []
        output_material = self.make_output_material()
        lines.append('{} = ['.format(self.material_underscored_name))
        for measure in output_material[:-1]:
            line = measuretools.measure_to_one_line_input_string(measure)
            lines.append('\t{},'.format(line))
        line = measuretools.measure_to_one_line_input_string(output_material[-1])
        lines.append('\t%{}]'.format(line))
        return lines
