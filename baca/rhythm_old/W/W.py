# -*- coding: utf-8 -*-
import abjad


class W(abjad.datastructuretools.Matrix):
    '''W-rhythm.

    ::

        >>> import baca

    ..  container:: example

        ::

            >>> baca.rhythm_old.W((10, 8), (3, 3, 6, 10), 3)
            W(3x22)

    '''

    ### INITIALIZER ###

    def __init__(self, measure_numerators, talea, n_voices):
        measures = self._measures = self._make_nested_measure_lists(
            measure_numerators, talea, n_voices)
        abjad.datastructuretools.Matrix.__init__(self, columns = measures)

    ### PRIVATE METHODS ###

    def _make_nested_measure_lists(self, measure_numerators, talea, n_voices):
        assert all([
            abjad.mathtools.is_positive_integer(x) 
            for x in measure_numerators
            ])
        assert all([abjad.mathtools.is_positive_integer(x) for x in talea])
        assert abjad.mathtools.is_nonnegative_integer(n_voices)
        args = (
            n_voices * sum(measure_numerators), abjad.mathtools.weight(talea))
        lcm = abjad.mathtools.least_common_multiple(*args)
        part_measure_weights = [n_voices * [x] for x in measure_numerators]
        part_measure_weights = abjad.sequencetools.flatten_sequence(
            part_measure_weights)
        all_measure_weights = abjad.sequencetools.repeat_sequence_to_weight(
            part_measure_weights, lcm)
        all_measure_divisions = abjad.sequencetools.repeat_sequence_to_weight(
            talea, lcm)
        all_measure_divisions = abjad.sequencetools.split_sequence(
            all_measure_weights,
            all_measure_divisions,
            cyclic=False,
            overhang=True,
            )
        all_measure_divisions = abjad.sequencetools.flatten_sequence(
            all_measure_divisions)
        args = (all_measure_divisions, all_measure_weights)
        all_measure_divisions = abjad.sequencetools.partition_sequence_by_weights(
            all_measure_divisions, 
            all_measure_weights, 
            cyclic=False, 
            overhang=True,
            )
        #args = (all_measure_divisions, [n_voices])
        all_measure_divisions = abjad.sequencetools.partition_sequence_by_counts(
            all_measure_divisions,
            [n_voices],
            cyclic=True,
            overhang=True,
            )
        return all_measure_divisions

    ### PUBLIC PROPERTIES ###

    @property
    def measures(self):
        '''Gets read-only zero-indexed measures.

        ..  container:: example

            >>> W = baca.rhythm_old.W((10, 8), (3, 3, 6, 10), 3)
            >>> W.measures[10]
            ([6, 4], [6, 3, 1], [2, 6, 2])

        Returns list of lists.
        '''
        return self._columns

    @property
    def voices(self):
        '''Gets read-only zero-indexed voices.

        ..  container:: example

            >>> W = baca.rhythm_old.W((10, 8), (3, 3, 6, 10), 3)
            >>> W.voices[0][10]
            [6, 4]

        Returns list of lists.
        '''
        return self._rows
