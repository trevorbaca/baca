from baca.makers._InteractiveMaterialMaker import _InteractiveMaterialMaker
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import sequencetools
import fractions
import os


class SargassoMeasureMaker(_InteractiveMaterialMaker):

    ### PUBLIC METHODS ###

    def conclude(self):
        response = raw_input('Press return to continue.')

    def format_user_input(self, user_input_pairs):
        formatted_user_input_lines = []
        for name, value in user_input_pairs:
            line = '%s = %r' % (name, value)
            formatted_user_input_lines.append(line)
        return formatted_user_input_lines
            
    def get_possible_meter_multipliers(self, multiplied_measure_numerator):
        possible_meter_multipliers = []
        for denominator in range(multiplied_measure_numerator, 2 * multiplied_measure_numerator):
            possible_meter_multiplier = fractions.Fraction(multiplied_measure_numerator, denominator)
            possible_meter_multipliers.append(possible_meter_multiplier)
        return possible_meter_multipliers

    def get_primary_input_lines(self, user_input_pairs):
        lines = []
        lines.append('from baca.makers import SargassoMeasureMaker')
        lines.append('maker = SargassoMeasureMaker()')
        user_input_names = [pair[0] for pair in user_input_pairs]
        user_input_string = ', '.join([str(x) for x in user_input_names])
        line = 'maker.make_sargasso_measures(%s)' % user_input_string
        lines.append(line)
        return lines
            
    def get_new_material_package_directory_from_user(self):
        from baca.scf.CatalogProxy import CatalogProxy
        from baca.scf.SharedMaterialsProxy import SharedMaterialsProxy
        while True:
            response = raw_input('Save to shared materials (m)? Or to existing score (s)? ')
            print ''
            if response == 'm':
                score_package_name = None
                base_directory = self.shared_materials_directory
                break
            elif response == 's':
                catalog_proxy = CatalogProxy()
                score_package_name = catalog_proxy.get_score_package_name_from_user()
                base_directory = os.path.join(
                    self.scores_directory, score_package_name, 'mus', 'materials')
                break
        response = raw_input('material name: ')
        print ''
        response = response.lower()
        response = response.replace(' ', '_')
        if score_package_name is not None:
            material_package_name = '%s_%s' % (score_package_name, response)
        else:
            material_package_name = response
        print 'package name will be %s\n' % material_package_name
        response = raw_input('ok? ')
        if not response == 'y':
            return
        print ''
        target = os.path.join(base_directory, material_package_name)
        if os.path.exists(target):
            raise OSError('directory %r already exists.' % target)
        return target

    def get_user_input_pairs(self):

#        return (4, [2, 2, 2, 2, 1, 1, 4, 4], 
#                16, [2, 2, 2, 2, 1, 1, 4, 4, 3, 3, 1, 1, 1, 1],
#                durationtools.Duration(66, 8),
#                True, True, True,
#                )

        result = [
                ('measure_denominator', 4) ,
                ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
                ('measure_division_denominator', 16),
                ('measure_division_talea', [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
                ('total_duration', durationtools.Duration(44, 8)),
                ('measures_are_scaled', True),
                ('measures_are_split', True),
                ('measures_are_shuffled', True),
                ]

        return result

        print 'Welcome to sargasso measure maker.\n'

        output_header_lines = [
            'from abjad import *',
            'from abjad.tools import sequencetools',]

        for header_line in output_header_lines:
            exec(header_line)

        output_body_lines = []

        response = raw_input('Measure denominator: ')
        line = 'measure_denominator = %s' % response
        exec(line)
        output_body_lines.append(line)
        print ''

        response = raw_input('Measure numerator talea: ')
        line = 'measure_numerator_talea = %s' % response
        exec(line)
        output_body_lines.append(line)
        print ''

        response = raw_input('Measure division denominator: ')
        line = 'measure_division_denominator = %s' % response
        exec(line)
        output_body_lines.append(line)
        print ''

        response = raw_input('Measure division talea: ')
        line = 'measure_division_talea = %s' % response
        exec(line)
        output_body_lines.append(line)
        print ''

        response = raw_input('Total duration: ')
        exec('duration = Duration(%s)' % response)
        line = 'total_duration = %s' % duration
        exec(line)
        output_body_lines.append(line)
        print ''

        response = raw_input('Scale measures? ')
        response = response == 'y'
        line = 'measures_are_scaled = %s' % response
        exec(line)
        output_body_lines.append(line)
        print ''

        response = raw_input('Split measures? ')
        response = response == 'y'
        line = 'measures_are_split = %s' % response
        exec(line)
        output_body_lines.append(line)
        print ''

        response = raw_input('Shuffle measures? ')
        response = response == 'y'
        line = 'measures_are_shuffled = %s' % response
        exec(line)
        output_body_lines.append(line)
        print ''

        #for line in output_header_lines:
        #    print line
        #print ''
        for line in output_body_lines:
            print line
        print ''

        return (measure_denominator, measure_numerator_talea, 
            measure_division_denominator, measure_division_talea, total_duration, 
            measures_are_scaled, measures_are_split, measures_are_shuffled)

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
        score.override.time_signature.break_visibility = schemetools.SchemeVariable('end-of-line-invisible')
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
        user_input_pairs = self.get_user_input_pairs()
        user_input_values = [pair[1] for pair in user_input_pairs]
        measures = self.make_sargasso_measures(*user_input_values)
        lilypond_file = self.make_lilypond_file(measures) 
        iotools.show(lilypond_file)
        self.write_material_to_disk(user_input_pairs, lilypond_file)
        self.conclude()

    def make_sargasso_measures(self, measure_denominator, measure_numerator_talea, 
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

    def permute_divided_measure_tokens(self, divided_measure_tokens):
        '''This can be extended later.'''
        modulus_of_permutation = 5
        len_divided_measure_tokens = len(divided_measure_tokens)
        assert mathtools.are_relatively_prime([modulus_of_permutation, len_divided_measure_tokens])
        permutation = [(5 * x) % len_divided_measure_tokens for x in range(len_divided_measure_tokens)]
        divided_measure_tokens = sequencetools.permute_sequence(divided_measure_tokens, permutation)
        return divided_measure_tokens

#    def write_material_to_disk(self, user_input_pairs, lilypond_score):
#        material_package_directory = self.get_new_material_package_directory_from_user()
#        print material_package_directory
#        os.mkdir(material_package_directory)
#        initializer = file(os.path.join(material_package_directory, '__init__.py'), 'w')
#        initializer.write('from output import *\n')
#        initializer.close()
#        user_input_lines = self.format_user_input(user_input_pairs)
#        input_file = file(os.path.join(material_package_directory, 'input.py'), 'w')
#        for line in user_input_lines:
#            input_file.write(line + '\n')
#        input_file.write('\n')
#        for line in self.get_primary_input_lines(user_input_pairs):
#            input_file.write(line + '\n')
#        input_file.close()
        
    def select_meter_multiplier(self, possible_meter_multipliers, measure_index):
        possible_meter_multipliers = sequencetools.CyclicTuple(possible_meter_multipliers)
        meter_multiplier = possible_meter_multipliers[5 * measure_index]
        return meter_multiplier
