from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import sequencetools
from baca.scf.UserInputHandlingMaterialProxy import UserInputHandlingMaterialProxy
from baca.scf.UserInputWrapper import UserInputWrapper


class SargassoMeasureMaterialProxy(UserInputHandlingMaterialProxy):

    def __init__(self, package_importable_name=None, session=None):
        UserInputHandlingMaterialProxy.__init__(
            self, package_importable_name=package_importable_name, session=session)
        self._generic_output_name = 'sargasso measures'

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    output_data_module_import_statements = [
        'from abjad.tools.measuretools.Measure import Measure',]
            
    user_input_demo_values = [
        ('measure_denominator', 4),
        ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
        ('measure_division_denominator', 16),
        ('measure_division_talea', [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
        ('total_duration', durationtools.Duration(44, 8)),
        ('measures_are_scaled', True),
        ('measures_are_split', True),
        ('measures_are_shuffled', True),]

    user_input_module_import_statements = [
        'from abjad.tools.durationtools import Duration',
        'from baca.scf import UserInputWrapper',]

    user_input_tests = [
        ('measure_denominator', mathtools.is_positive_integer_power_of_two),
        ('measure_numerator_talea', sequencetools.all_are_nonnegative_integers),
        ('measure_division_denominator', mathtools.is_nonnegative_integer_power_of_two),
        ('measure_division_talea', sequencetools.all_are_nonnegative_integers),
        ('total_duration', durationtools.is_duration_token, 'value = Duration({})'),
        ('measures_are_scaled', bool),
        ('measures_are_split', bool),
        ('measures_are_shuffled', bool),]

    ### PUBLIC METHODS ###

    def get_output_data_file_lines(self, measures, material_underscored_name):
        output_file_lines = []
        output_file_lines.append('%s = [' % material_underscored_name)
        for measure in measures[:-1]:
            line = measuretools.measure_to_one_line_input_string(measure)
            output_file_lines.append('\t%s,' % line)
        line = measuretools.measure_to_one_line_input_string(measures[-1])
        output_file_lines.append('\t%s]' % line)
        return output_file_lines

    def make(self, measure_denominator, measure_numerator_talea, 
        measure_division_denominator, measure_division_talea, total_duration,
        measures_are_scaled, measures_are_split, measures_are_shuffled):
        import baca
        return baca.music.make_sargasso_measures(measure_denominator, measure_numerator_talea,
            measure_division_denominator, measure_division_talea, total_duration,
            measures_are_scaled, measures_are_split, measures_are_shuffled)

    def make_lilypond_file_from_output_material(self, material):
        from baca.music.make_sargasso_measures import make_lilypond_file_from_output_material
        return make_lilypond_file_from_output_material(material)
