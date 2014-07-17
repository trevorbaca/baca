# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import idetools
import baca


class ZaggedPitchClassMaker(abctools.AbjadObject):
    r'''Zagged pitch-class maker.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_division_cells',
        '_grouping_counts',
        '_pc_cells',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pc_cells=None,
        division_cells=None,
        grouping_counts=None,
        ):
        self._pc_cells = pc_cells
        self._division_cells = division_cells
        self._grouping_counts = grouping_counts

    ### SPECIAL METHODS ###

    def __call__(self):
        pc_cells = baca.utilities.helianthate(
            self.pc_cells, 
            -1, 
            1,
            )
        division_cells = baca.utilities.helianthate(
            self.division_cells, 
            -1, 
            1,
            )
        division_cells = sequencetools.flatten_sequence(
            division_cells, 
            depth=1,
            )
        division_cells = datastructuretools.CyclicTuple(division_cells)
        tmp = []
        for i, pc_segment in enumerate(pc_cells):
            parts = sequencetools.partition_sequence_by_ratio_of_lengths(
                pc_segment, 
                division_cells[i],
                )
            tmp.extend(parts)
        pc_cells = tmp
        pc_cells = sequencetools.partition_sequence_by_counts(
            pc_cells, 
            self.grouping_counts, 
            cyclic=True, 
            overhang=True,
            )
        pc_cells = [sequencetools.join_subsequences(x) for x in pc_cells]
        pc_cells = sequencetools.partition_sequence_by_counts(
            pc_cells, 
            self.grouping_counts, 
            cyclic=True, 
            overhang=True,
            )
        material = pitchtools.PitchClassTree(
            items=pc_cells,
            item_class=pitchtools.NumberedPitchClass,
            )
        material = [material]
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
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='pc_cells',
                command='pc',
                editor=idetools.getters.get_lists,
                ),
            systemtools.AttributeDetail(
                name='division_cells',
                command='dc',
                editor=idetools.getters.get_lists,
                ),
            systemtools.AttributeDetail(
                name='grouping_counts',
                command='gc',
                editor=idetools.getters.get_nonnegative_integers,
                ),
            )

    @property
    def _input_demo_values(self):
        return [
        ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8], [5, 4, 2, 11, 10, 9]]),
        ('division_cells', 
            [[[1], [1], [1], [1, 1]], [[1], [1], [1], [1, 1, 1], [1, 1, 1]]]),
        ('grouping_counts', [1, 1, 2, 3]),
        ]

    ### PRIVATE METHODS ###

    ### PUBLIC PROPERTIES ###

    @property
    def division_cells(self):
        r'''Gets division cells of maker.

        Returns list of lists.
        '''
        return self._division_cells

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