# -*- coding: utf-8 -*-
from abjad import *
import baca


class ZaggedPitchClassMaker(abctools.AbjadObject):
    r'''Zagged pitch-class maker.

    Object-oriented extension to helianthation.

    Same as helianthation when `division_ratios` and `grouping_counts` are
    none.

    Extensions provided by `division_ratios` and `grouping_counts`.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_division_ratios',
        '_grouping_counts',
        '_pc_cells',
        )

    _call_before_persisting_to_disk = True

    ### INITIALIZER ###

    def __init__(
        self,
        pc_cells=None,
        division_ratios=None,
        grouping_counts=None,
        ):
        self._pc_cells = pc_cells
        self._division_ratios = division_ratios
        self._grouping_counts = grouping_counts

    ### SPECIAL METHODS ###

    def __call__(self):
        pc_cells = baca.tools.helianthate(
            self.pc_cells, 
            -1, 
            1,
            )
        prototype = (tuple, mathtools.Ratio)
        if self.division_ratios is None:
            division_ratios = [[1]]
        elif all(isinstance(_, prototype) for _ in self.division_ratios):
            division_ratios = self.division_ratios
        elif all(isinstance(_, list) for _ in self.division_ratios):
            division_ratios = baca.tools.helianthate(
                self.division_ratios, 
                -1, 
                1,
                )
            division_ratios = sequencetools.flatten_sequence(
                division_ratios, 
                depth=1,
                )
        division_ratios = [mathtools.Ratio(_) for _ in division_ratios]
        division_ratios = datastructuretools.CyclicTuple(division_ratios)
        pc_cells_copy = pc_cells[:]
        pc_cells = []
        for i, pc_segment in enumerate(pc_cells_copy):
            parts = sequencetools.partition_sequence_by_ratio_of_lengths(
                pc_segment, 
                division_ratios[i],
                )
            pc_cells.extend(parts)
        grouping_counts = self.grouping_counts or [1]
        pc_cells = sequencetools.partition_sequence_by_counts(
            pc_cells, 
            grouping_counts, 
            cyclic=True, 
            overhang=True,
            )
        # this block was uncommented during krummzeit
        #pc_cells = [sequencetools.join_subsequences(x) for x in pc_cells]
        #pc_cells = sequencetools.partition_sequence_by_counts(
        #    pc_cells, 
        #    grouping_counts, 
        #    cyclic=True, 
        #    overhang=True,
        #    )
        material = pitchtools.PitchClassTree(
            items=pc_cells,
            item_class=pitchtools.NumberedPitchClass,
            )
        return material

    def __eq__(self, expr):
        r'''Is true when `expr` is a zagged pitch-class with type and 
        public properties equal to those of this zagged pitch-class maker.
        Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self):
        r'''Hashes zagged pitch-class maker.
        '''
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager.get_hash_values(self)
        return hash(hash_values)

    ### PRIVATE PROPERTIES ###

    @property
    def _input_demo_values(self):
        return [
        ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8], [5, 4, 2, 11, 10, 9]]),
        ('division_ratios', 
            [[[1], [1], [1], [1, 1]], [[1], [1], [1], [1, 1, 1], [1, 1, 1]]]),
        ('grouping_counts', [1, 1, 2, 3]),
        ]

    ### PUBLIC PROPERTIES ###

    @property
    def division_ratios(self):
        r'''Gets division cells of maker.

        Returns list of lists.
        '''
        return self._division_ratios

    @property
    def grouping_counts(self):
        r'''Gets grouping counts of maker.

        Returns nonempty list of positive integers.
        '''
        return self._grouping_counts

    @property
    def pc_cells(self):
        r'''Gets pitch-class cells of maker.

        Returns list of number lists.
        '''
        return self._pc_cells