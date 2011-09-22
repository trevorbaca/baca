from baca.makers._InteractiveMaterialMaker import _InteractiveMaterialMaker
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import sequencetools
import fractions


class SargassoMeasureMaker(_InteractiveMaterialMaker):

    def __init__(self):
        pass

    ### PUBLIC METHODS ###

    def conclude(self):
        print 'Making ended.'
        response = raw_input('Press return to continue.')

    def get_possible_meter_multipliers(self, multiplied_measure_numerator):
        possible_meter_multipliers = []
        for denominator in range(multiplied_measure_numerator, 2 * multiplied_measure_numerator):
            possible_meter_multiplier = fractions.Fraction(multiplied_measure_numerator, denominator)
            possible_meter_multipliers.append(possible_meter_multiplier)
        return possible_meter_multipliers

    def get_user_input(self):

        return (4, [2, 2, 2, 2, 1, 1, 4, 4], 
                16, [2, 2, 2, 2, 1, 1, 4, 4, 3, 3, 1, 1, 1, 1],
                durationtools.Duration(66, 8))

        print 'Welcome to sargasso measure maker.\n'

        output_header_lines = [
            'from abjad import *',
            'from abjad.tools import sequencetools',]

        for header_line in output_header_lines:
            exec(header_line)

        output_body_lines = []

        response = raw_input('Measure unit duration: ')
        line = 'measure_unit_duration = Duration(%s)' % response
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

        print 'Measure talea is now %s.' % measure_talea
        print ''

        response = raw_input('Division unit duration: ')
        line = 'division_unit_duration = %s' % response
        exec(line)
        output_body_lines.append(line)
        print ''

        response = raw_input('Division talea: ')
        line = 'division_talea = %s' % response
        exec(line)
        output_body_lines.append(line)
        print ''

        line = 'division_talea = sequencetools.repeat_sequence_to_weight_exactly(division_talea, weight_of_talea)'
        exec(line)
        output_body_lines.append(line)
        print ''

        for line in output_header_lines:
            print line
        print ''
        for line in output_body_lines:
            print line
        print ''

    def make_lilypond_file(self, measures):
        from abjad.tools import leaftools
        from abjad.tools import lilypondfiletools
        from abjad.tools import layouttools
        from abjad.tools import markuptools
        from abjad.tools import measuretools
        from abjad.tools import schemetools
        from abjad.tools import scoretools
        from abjad.tools import stafftools
        staff = stafftools.RhythmicStaff(measures)
        score = scoretools.Score([staff])
        leaf = leaftools.get_leaf_in_expr_with_minimum_prolated_duration(score)
        scheme_moment = schemetools.SchemeMoment(fractions.Fraction(2, 3) * leaf.prolated_duration)
        score.override.bar_number.transparent = True
        score.set.proportional_notation_duration = scheme_moment
        measuretools.apply_beam_spanners_to_measures_in_expr(score)
        scoretools.add_double_bar_to_end_of_score(score)
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score) 
        lilypond_file.default_paper_size = 'letter', 'portrait'
        lilypond_file.global_staff_size = 14
        lilypond_file.header_block.title = markuptools.Markup('Sargasso measures')
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.ragged_right = True
        lilypond_file.paper_block.markup_system_spacing = layouttools.make_spacing_vector(0, 0, 12, 0)
        lilypond_file.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 10, 0)
        return lilypond_file

    def make_material_interactively(self):
        from abjad.tools import iotools
        measures = self.make_sargasso_measures(*self.get_user_input()) 
        lilypond_file = self.make_lilypond_file(measures) 
        iotools.show(lilypond_file)
        self.conclude()

    def make_sargasso_measures(self, measure_denominator, measure_numerator_talea, 
        measure_division_denominator, measure_division_talea, total_duration):

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

        divided_measure_tokens = []
        for meter_multiplier, measure_divisions in measure_tokens:
            division_lists = sequencetools.partition_sequence_by_ratio_of_lengths(measure_divisions, [1, 1])
            for division_list in division_lists:
                if division_list:
                    divided_measure_tokens.append((meter_multiplier, division_list))
        #for x in divided_measure_tokens: print x

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

    def permute_divided_measure_tokens(self, divided_measure_tokens):
        '''This can be extended later.'''
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

