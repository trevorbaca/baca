from abjad import *


class W(datastructuretools.Matrix):
    '''W-rhythm.

    ::

        abjad> baca.rhythm.W((10, 8), (3, 3, 6, 10), 3)
        W(3x22)

    '''

    ### INITIALIZER ###

    def __init__(self, measure_numerators, talea, n_voices):
        measures = self._measures = self._make_nested_measure_lists(
            measure_numerators, talea, n_voices)
        datastructuretools.Matrix.__init__(self, columns = measures)

    ### PRIVATE METHODS ###

    def _make_nested_measure_lists(self, measure_numerators, talea, n_voices):
        assert all([mathtools.is_positive_integer(x) for x in measure_numerators])
        assert all([mathtools.is_positive_integer(x) for x in talea])
        assert mathtools.is_nonnegative_integer(n_voices)
        args = (n_voices * sum(measure_numerators), mathtools.weight(talea))
        lcm = mathtools.least_common_multiple(*args)
        part_measure_weights = [n_voices * [x] for x in measure_numerators]
        part_measure_weights = sequencetools.flatten_sequence(part_measure_weights)
        all_measure_weights = sequencetools.repeat_sequence_to_weight(
            part_measure_weights, lcm)
        all_measure_divisions = sequencetools.repeat_sequence_to_weight(
            talea, lcm)
        args = (all_measure_weights, all_measure_divisions)
        all_measure_divisions = sequencetools.split_sequence_by_weights(
            *args, cyclic=False, overhang=True)
        all_measure_divisions = sequencetools.flatten_sequence(all_measure_divisions)
        args = (all_measure_divisions, all_measure_weights)
        all_measure_divisions = sequencetools.partition_sequence_by_weights(
            all_measure_divisions, 
            all_measure_weights, 
            cyclic=False, 
            overhang=True,
            )
        args = (all_measure_divisions, [n_voices])
        all_measure_divisions = sequencetools.partition_sequence_by_counts(
            *args, cyclic=True, overhang=True)
        return all_measure_divisions

    ### PUBLIC PROPERTIES ###

    @property
    def measures(self):
        '''Read-only zero-indexed measures::

            abjad> W = baca.rhythm.W((10, 8), (3, 3, 6, 10), 3)
            abjad> W.measures[10]
            [[6, 4], [6, 3, 1], [2, 6, 2]]

        Return list of lists.
        '''
        return self._columns

    @property
    def voices(self):
        '''Read-only zero-indexed voices::

            abjad> W = baca.rhythm.W((10, 8), (3, 3, 6, 10), 3)
            abjad> W.voices[0][10]
            [6, 4]

        Return list of lists.
        '''
        return self._rows
