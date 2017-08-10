# -*- coding: utf-8 -*-
import abjad
import baca


class ZaggedPitchClassMaker(abjad.AbjadObject):
    r'''Zagged pitch-class maker.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> maker = baca.ZaggedPitchClassMaker(
            ...     pc_cells=[
            ...         [7, 1, 3, 4, 5, 11],
            ...         [3, 5, 6, 7],
            ...         [9, 10, 0, 8],
            ...         ],
            ...     division_ratios=[
            ...         [[1], [1], [1], [1, 1]],
            ...         [[1], [1], [1], [1, 1, 1], [1, 1, 1]],
            ...         ],
            ...         grouping_counts=[1, 1, 1, 2, 3],
            ...     )
            >>> pitch_class_tree = maker()
            >>> show(pitch_class_tree) # doctest: +SKIP

        ::

            >>> for tree in pitch_class_tree:
            ...     tree.get_payload(nested=True)
            [[NumberedPitchClass(7), NumberedPitchClass(1), NumberedPitchClass(3), NumberedPitchClass(4), NumberedPitchClass(5), NumberedPitchClass(11)]]
            [[NumberedPitchClass(3), NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7)]]
            [[NumberedPitchClass(9), NumberedPitchClass(10), NumberedPitchClass(0), NumberedPitchClass(8)]]
            [[NumberedPitchClass(7), NumberedPitchClass(3)], [NumberedPitchClass(5), NumberedPitchClass(6)]]
            [[NumberedPitchClass(8), NumberedPitchClass(9), NumberedPitchClass(10), NumberedPitchClass(0)], [NumberedPitchClass(11), NumberedPitchClass(7), NumberedPitchClass(1), NumberedPitchClass(3), NumberedPitchClass(4), NumberedPitchClass(5)], [NumberedPitchClass(0), NumberedPitchClass(8), NumberedPitchClass(9), NumberedPitchClass(10)]]
            [[NumberedPitchClass(5), NumberedPitchClass(11)]]
            [[NumberedPitchClass(7), NumberedPitchClass(1)]]
            [[NumberedPitchClass(3), NumberedPitchClass(4)]]
            [[NumberedPitchClass(6)], [NumberedPitchClass(7), NumberedPitchClass(3)]]
            [[NumberedPitchClass(5)], [NumberedPitchClass(4), NumberedPitchClass(5)], [NumberedPitchClass(11), NumberedPitchClass(7)]]
            [[NumberedPitchClass(1), NumberedPitchClass(3)]]
            [[NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(3)]]
            [[NumberedPitchClass(10), NumberedPitchClass(0), NumberedPitchClass(8), NumberedPitchClass(9)]]
            [[NumberedPitchClass(3), NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7)], [NumberedPitchClass(9)]]
            [[NumberedPitchClass(10), NumberedPitchClass(0)], [NumberedPitchClass(8)], [NumberedPitchClass(3), NumberedPitchClass(4), NumberedPitchClass(5)]]
            [[NumberedPitchClass(11), NumberedPitchClass(7), NumberedPitchClass(1)]]
            [[NumberedPitchClass(8), NumberedPitchClass(9), NumberedPitchClass(10), NumberedPitchClass(0)]]
            [[NumberedPitchClass(1), NumberedPitchClass(3), NumberedPitchClass(4), NumberedPitchClass(5), NumberedPitchClass(11), NumberedPitchClass(7)]]
            [[NumberedPitchClass(7), NumberedPitchClass(3), NumberedPitchClass(5), NumberedPitchClass(6)], [NumberedPitchClass(7), NumberedPitchClass(1), NumberedPitchClass(3), NumberedPitchClass(4), NumberedPitchClass(5), NumberedPitchClass(11)]]
            [[NumberedPitchClass(6), NumberedPitchClass(7)], [NumberedPitchClass(3), NumberedPitchClass(5)], [NumberedPitchClass(0), NumberedPitchClass(8), NumberedPitchClass(9), NumberedPitchClass(10)]]
            [[NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(3)]]
            [[NumberedPitchClass(10)]]
            [[NumberedPitchClass(0), NumberedPitchClass(8)]]
            [[NumberedPitchClass(9)], [NumberedPitchClass(11), NumberedPitchClass(7)]]
            [[NumberedPitchClass(1), NumberedPitchClass(3)], [NumberedPitchClass(4), NumberedPitchClass(5)], [NumberedPitchClass(9), NumberedPitchClass(10), NumberedPitchClass(0), NumberedPitchClass(8)]]
            [[NumberedPitchClass(5), NumberedPitchClass(11), NumberedPitchClass(7), NumberedPitchClass(1), NumberedPitchClass(3), NumberedPitchClass(4)]]
            [[NumberedPitchClass(3), NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7)]]
            [[NumberedPitchClass(4), NumberedPitchClass(5), NumberedPitchClass(11), NumberedPitchClass(7), NumberedPitchClass(1), NumberedPitchClass(3)]]
            [[NumberedPitchClass(7)], [NumberedPitchClass(3), NumberedPitchClass(5)]]
            [[NumberedPitchClass(6)], [NumberedPitchClass(8)], [NumberedPitchClass(9), NumberedPitchClass(10)]]
            [[NumberedPitchClass(0)]]
            [[NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(3), NumberedPitchClass(5)]]
            [[NumberedPitchClass(0), NumberedPitchClass(8), NumberedPitchClass(9), NumberedPitchClass(10)]]
            [[NumberedPitchClass(3), NumberedPitchClass(4), NumberedPitchClass(5), NumberedPitchClass(11), NumberedPitchClass(7), NumberedPitchClass(1)], [NumberedPitchClass(10), NumberedPitchClass(0), NumberedPitchClass(8), NumberedPitchClass(9)]]
            [[NumberedPitchClass(1), NumberedPitchClass(3), NumberedPitchClass(4)], [NumberedPitchClass(5), NumberedPitchClass(11), NumberedPitchClass(7)], [NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(3)]]

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Utilities'

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
        r'''Calls zagged pitch-class maker.

        Returns pitch-class tree.
        '''
        pc_cells = baca.helianthate(
            self.pc_cells,
            -1,
            1,
            )
        prototype = (tuple, abjad.Ratio)
        if self.division_ratios is None:
            division_ratios = [[1]]
        elif all(isinstance(_, prototype) for _ in self.division_ratios):
            division_ratios = self.division_ratios
        elif all(isinstance(_, list) for _ in self.division_ratios):
            division_ratios = baca.helianthate(
                self.division_ratios,
                -1,
                1,
                )
            division_ratios = baca.Sequence(division_ratios).flatten(depth=1)
        division_ratios = [abjad.Ratio(_) for _ in division_ratios]
        division_ratios = abjad.CyclicTuple(division_ratios)
        pc_cells_copy = pc_cells[:]
        pc_cells = []
        for i, pc_segment in enumerate(pc_cells_copy):
            parts = baca.Sequence(pc_segment).partition_by_ratio_of_lengths(
                division_ratios[i],
                )
            pc_cells.extend(parts)
        grouping_counts = self.grouping_counts or [1]
        pc_cells = baca.Sequence(pc_cells).partition_by_counts(
            grouping_counts,
            cyclic=True,
            overhang=True,
            )
        # this block was uncommented during krummzeit
        #pc_cells = [abjad.join_subsequences(x) for x in pc_cells]
        #pc_cells = baca.Sequence(pc_cells).partition_by_counts(
        #    grouping_counts,
        #    cyclic=True,
        #    overhang=True,
        #    )
        material = baca.PitchTree(
            items=pc_cells,
            item_class=abjad.NumberedPitchClass,
            )
        return material

    def __eq__(self, argument):
        r'''Is true when `argument` is a zagged pitch-class with type and
        public properties equal to those of this zagged pitch-class maker.
        Otherwise false.

        Returns boolean.
        '''
        agent = abjad.StorageFormatAgent(self)
        return agent.compare(argument)

    def __hash__(self):
        r'''Hashes zagged pitch-class maker.
        '''
        agent = abjad.StorageFormatAgent(self)
        return hash(agent.hash_values)

    ### PUBLIC PROPERTIES ###

    @property
    def division_ratios(self):
        r'''Gets division cells of maker.

        ..  container:: example

            Same as helianthation when division ratios and grouping counts are
            both none:

            ::


                >>> maker = baca.ZaggedPitchClassMaker(
                ...     pc_cells=[[0, 1, 2], [3, 4]],
                ...     division_ratios=None,
                ...     grouping_counts=None,
                ...     )
                >>> pitch_class_tree = maker()
                >>> show(pitch_class_tree) # doctest: +SKIP

            ::

                >>> for tree in pitch_class_tree:
                ...     tree.get_payload(nested=True)
                [[NumberedPitchClass(0), NumberedPitchClass(1), NumberedPitchClass(2)]]
                [[NumberedPitchClass(3), NumberedPitchClass(4)]]
                [[NumberedPitchClass(4), NumberedPitchClass(3)]]
                [[NumberedPitchClass(2), NumberedPitchClass(0), NumberedPitchClass(1)]]
                [[NumberedPitchClass(1), NumberedPitchClass(2), NumberedPitchClass(0)]]
                [[NumberedPitchClass(3), NumberedPitchClass(4)]]
                [[NumberedPitchClass(4), NumberedPitchClass(3)]]
                [[NumberedPitchClass(0), NumberedPitchClass(1), NumberedPitchClass(2)]]
                [[NumberedPitchClass(2), NumberedPitchClass(0), NumberedPitchClass(1)]]
                [[NumberedPitchClass(3), NumberedPitchClass(4)]]
                [[NumberedPitchClass(4), NumberedPitchClass(3)]]
                [[NumberedPitchClass(1), NumberedPitchClass(2), NumberedPitchClass(0)]]

        ..  container:: example

            Divides every cell in half:

            ::


                >>> maker = baca.ZaggedPitchClassMaker(
                ...     pc_cells=[[0, 1, 2, 3], [4, 5, 6, 7]],
                ...     division_ratios=[[(1, 1)]],
                ...     grouping_counts=None,
                ...     )
                >>> pitch_class_tree = maker()
                >>> show(pitch_class_tree) # doctest: +SKIP

            ::

                >>> for tree in pitch_class_tree:
                ...     tree.get_payload(nested=True)
                [[NumberedPitchClass(0), NumberedPitchClass(1)]]
                [[NumberedPitchClass(2), NumberedPitchClass(3)]]
                [[NumberedPitchClass(4), NumberedPitchClass(5)]]
                [[NumberedPitchClass(6), NumberedPitchClass(7)]]
                [[NumberedPitchClass(7), NumberedPitchClass(4)]]
                [[NumberedPitchClass(5), NumberedPitchClass(6)]]
                [[NumberedPitchClass(3), NumberedPitchClass(0)]]
                [[NumberedPitchClass(1), NumberedPitchClass(2)]]
                [[NumberedPitchClass(2), NumberedPitchClass(3)]]
                [[NumberedPitchClass(0), NumberedPitchClass(1)]]
                [[NumberedPitchClass(6), NumberedPitchClass(7)]]
                [[NumberedPitchClass(4), NumberedPitchClass(5)]]
                [[NumberedPitchClass(5), NumberedPitchClass(6)]]
                [[NumberedPitchClass(7), NumberedPitchClass(4)]]
                [[NumberedPitchClass(1), NumberedPitchClass(2)]]
                [[NumberedPitchClass(3), NumberedPitchClass(0)]]

        Returns list of lists.
        '''
        return self._division_ratios

    @property
    def grouping_counts(self):
        r'''Gets grouping counts of maker.

        ..  container:: example

            Groups helianthated cells:

            ::


                >>> maker = baca.ZaggedPitchClassMaker(
                ...     pc_cells=[[0, 1, 2], [3, 4]],
                ...     division_ratios=None,
                ...     grouping_counts=[1, 2],
                ...     )
                >>> pitch_class_tree = maker()
                >>> show(pitch_class_tree) # doctest: +SKIP

            ::

                >>> for tree in pitch_class_tree:
                ...     tree.get_payload(nested=True)
                [[NumberedPitchClass(0), NumberedPitchClass(1), NumberedPitchClass(2)]]
                [[NumberedPitchClass(3), NumberedPitchClass(4)], [NumberedPitchClass(4), NumberedPitchClass(3)]]
                [[NumberedPitchClass(2), NumberedPitchClass(0), NumberedPitchClass(1)]]
                [[NumberedPitchClass(1), NumberedPitchClass(2), NumberedPitchClass(0)], [NumberedPitchClass(3), NumberedPitchClass(4)]]
                [[NumberedPitchClass(4), NumberedPitchClass(3)]]
                [[NumberedPitchClass(0), NumberedPitchClass(1), NumberedPitchClass(2)], [NumberedPitchClass(2), NumberedPitchClass(0), NumberedPitchClass(1)]]
                [[NumberedPitchClass(3), NumberedPitchClass(4)]]
                [[NumberedPitchClass(4), NumberedPitchClass(3)], [NumberedPitchClass(1), NumberedPitchClass(2), NumberedPitchClass(0)]]

        Returns nonempty list of positive integers.
        '''
        return self._grouping_counts

    @property
    def pc_cells(self):
        r'''Gets pitch-class cells of maker.

        Returns list of number lists.
        '''
        return self._pc_cells
