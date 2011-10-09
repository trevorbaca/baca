from baca.scf.Maker import Maker
from baca.scf.UserInputWrapper import UserInputWrapper
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import lilypondfiletools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import stafftools
import fractions
import os


class SargassoMeasureMaker(Maker):

    def __init__(self, **kwargs):
        Maker.__init__(self, **kwargs)
        self.stylesheet = os.path.join(os.path.dirname(__file__), 'stylesheet.ly')
        self.generic_output_name = 'sargasso measures'

    ### PUBLIC ATTRIBUTES ###

    output_file_import_statements = ['from abjad.tools.measuretools.Measure import Measure']
            
    user_input_import_statements = ['from abjad.tools.durationtools import Duration',
        'from baca.makers import SargassoMeasureMaker',
        'from baca.scf import UserInputWrapper']

    user_input_template = UserInputWrapper([
        ('measure_denominator', 4),
        ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
        ('measure_division_denominator', 16),
        ('measure_division_talea', [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
        ('total_duration', durationtools.Duration(44, 8)),
        ('measures_are_scaled', True),
        ('measures_are_split', True),
        ('measures_are_shuffled', True)])

    ### PUBLIC METHODS ###

    def get_output_file_lines(self, measures, material_name):
        output_file_lines = []
        output_file_lines.append('%s = [' % material_name)
        for measure in measures[:-1]:
            line = measuretools.measure_to_one_line_input_string(measure)
            output_file_lines.append('\t%s,' % line)
        line = measuretools.measure_to_one_line_input_string(measures[-1])
        output_file_lines.append('\t%s]' % line)
        return output_file_lines

    def get_possible_meter_multipliers(self, multiplied_measure_numerator):
        possible_meter_multipliers = []
        for denominator in range(multiplied_measure_numerator, 2 * multiplied_measure_numerator):
            possible_meter_multiplier = fractions.Fraction(multiplied_measure_numerator, denominator)
            possible_meter_multipliers.append(possible_meter_multiplier)
        return possible_meter_multipliers

    def make(self, measure_denominator, measure_numerator_talea, 
        measure_division_denominator, measure_division_talea, total_duration,
        measures_are_scaled, measures_are_split, measures_are_shuffled):

        assert mathtools.is_nonnegative_integer_power_of_two(measure_denominator)
        assert mathtools.is_nonnegative_integer_power_of_two(measure_division_denominator)
        assert measure_denominator <= measure_division_denominator

        assert all([mathtools.is_positive_integer(x) for x in measure_numerator_talea])
        assert all([mathtools.is_positive_integer(x) for x in measure_division_talea])
        total_duration = durationtools.Duration(total_duration)

        weight = int(measure_denominator * total_duration)
        measure_numerators = sequencetools.repeat_sequence_to_weight_exactly(
            measure_numerator_talea, weight)
        #print measure_numerators

        weight = int(measure_division_denominator * total_duration)
        measure_divisions = sequencetools.repeat_sequence_to_weight_exactly(
            measure_division_talea, weight)
        #print measure_divisions
        
        multiplier = measure_division_denominator / measure_denominator
        multiplied_measure_numerators = [multiplier * x for x in measure_numerators]
        #print multiplied_measure_numerators
        
        measure_divisions_by_measure = sequencetools.split_sequence_cyclically_by_weights_with_overhang(
            measure_divisions, multiplied_measure_numerators)
        #print measure_divisions_by_measure

        meter_multipliers = [fractions.Fraction(1) for x in measure_divisions_by_measure]

        if measures_are_scaled:

            meter_multipliers = []
            for measure_index, multiplied_measure_numerator in enumerate(multiplied_measure_numerators):
                possible_multipliers = self.get_possible_meter_multipliers(multiplied_measure_numerator)
                meter_multiplier = self.select_meter_multiplier(possible_multipliers, measure_index)
                meter_multipliers.append(meter_multiplier)
            #print meter_multipliers

            prolated_measure_numerators = []
            for meter_multiplier, multiplied_measure_numerator in zip(
                meter_multipliers, multiplied_measure_numerators):
                prolated_measure_numerator = multiplied_measure_numerator / meter_multiplier
                assert mathtools.is_integer_equivalent_number(prolated_measure_numerator)
                prolated_measure_numerator = int(prolated_measure_numerator)
                prolated_measure_numerators.append(prolated_measure_numerator)
            #print prolated_measure_numerators

            measure_divisions = sequencetools.repeat_sequence_to_weight_exactly(
                measure_division_talea, sum(prolated_measure_numerators))
            #print measure_divisions

            measure_divisions_by_measure = sequencetools.split_sequence_cyclically_by_weights_with_overhang(
                measure_divisions, prolated_measure_numerators) 
            #print measure_divisions_by_measure
        
        measure_tokens = zip(meter_multipliers, measure_divisions_by_measure)
        #for x in measure_tokens: print x

        if measures_are_split:
            ratio = [1, 1]
        else:
            ratio = [1]

        divided_measure_tokens = []
        for meter_multiplier, measure_divisions in measure_tokens:
            division_lists = sequencetools.partition_sequence_by_ratio_of_lengths(measure_divisions, ratio)
            for division_list in division_lists:
                if division_list:
                    divided_measure_tokens.append((meter_multiplier, division_list))
        #for x in divided_measure_tokens: print x

        if measures_are_shuffled:
            divided_measure_tokens = self.permute_divided_measure_tokens(divided_measure_tokens)

        meter_tokens = []
        for meter_multiplier, measure_divisions in divided_measure_tokens:
            measure_duration = meter_multiplier * fractions.Fraction(
                sum(measure_divisions), measure_division_denominator)
            meter_base_unit = meter_multiplier * fractions.Fraction(
                min(measure_divisions), measure_division_denominator)
            meter_denominator = meter_base_unit.denominator
            meter_token = durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
                measure_duration, meter_denominator)
            meter_tokens.append(meter_token)
        #print meter_tokens

        division_tokens = []
        for measure_duration, division_token in divided_measure_tokens:
            division_tokens.append(division_token)

        measures = []
        for meter_token, division_token in zip(meter_tokens, division_tokens):
            leaves = leaftools.make_leaves_from_note_value_signal(division_token, measure_division_denominator)
            measure = measuretools.Measure(meter_token, leaves)
            measures.append(measure)
        #print measures

        return measures

    def make_lilypond_file_from_output_material(self, measures):
        staff = stafftools.RhythmicStaff(measures)
        score = scoretools.Score([staff])
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        lilypond_file.file_initial_system_comments = []
        lilypond_file.file_initial_system_includes = []
        measuretools.apply_beam_spanners_to_measures_in_expr(score)
        scoretools.add_double_bar_to_end_of_score(score)
        return lilypond_file

    def permute_divided_measure_tokens(self, divided_measure_tokens):
        modulus_of_permutation = 5
        len_divided_measure_tokens = len(divided_measure_tokens)
        assert mathtools.are_relatively_prime([modulus_of_permutation, len_divided_measure_tokens])
        permutation = [(5 * x) % len_divided_measure_tokens for x in range(len_divided_measure_tokens)]
        divided_measure_tokens = sequencetools.permute_sequence(divided_measure_tokens, permutation)
        return divided_measure_tokens

    def select_meter_multiplier(self, possible_meter_multipliers, measure_index):
        possible_meter_multipliers = sequencetools.CyclicTuple(possible_meter_multipliers)
        meter_multiplier = possible_meter_multipliers[5 * measure_index]
        return meter_multiplier
