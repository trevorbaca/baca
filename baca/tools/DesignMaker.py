import abjad
import baca


class DesignMaker(abjad.AbjadObject):
    r'''Design-maker.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Initializes design-maker:

        ::

            >>> baca.DesignMaker()
            DesignMaker()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_result',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._result = []

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls design-maker.

        Returns pitch-class tree.
        '''
        design = baca.PitchTree(items=self._result)
        self._check_duplicate_pitch_classes(design)
        return design

    ### PRIVATE METHODS ###

    @staticmethod
    def _apply_operator(segment, operator):
        assert isinstance(segment, baca.PitchClassSegment)
        assert isinstance(operator, str), repr(operator)
        if operator.startswith('T'):
            index = int(operator[1:])
            segment = segment.transpose(index)
        elif operator == 'I':
            segment = segment.invert()
        elif operator.startswith('M'):
            index = int(operator[1:])
            segment = segment.multiply(index)
        elif operator == 'alpha':
            segment = segment.alpha()
        else:
            message = 'unrecognized operator: {!r}.'
            message = message.format(operator)
            raise Exception(message)
        return segment

    @staticmethod
    def _check_duplicate_pitch_classes(design):
        leaves = design.get_payload()
        for leaf_1, leaf_2 in abjad.Sequence(leaves).nwise():
            if leaf_1 == leaf_2:
                message = 'duplicate {!r}.'
                message = message.format(leaf_1)
                raise Exception(message)

    ### PUBLIC METHODS ###

    def partition(self, cursor, number, counts, operators=None):
        r'''Partitions next `number` cells in `cursor` by `counts`.

        Appies optional `operators` to resulting parts of partition.

        Returns none.
        '''
        cells = cursor.next(number)
        list_ = []
        for cell in cells:
            list_.extend(cell)
        segment = baca.PitchClassSegment(items=list_)
        operators = operators or []
        for operator in operators:
            segment = self._apply_operator(segment, operator)
        sequence = abjad.sequence(segment)
        parts = sequence.partition_by_counts(counts, overhang=True)
        parts = [baca.PitchClassSegment(_) for _ in parts]
        self._result.extend(parts)

    def partition_cyclic(self, cursor, number, counts, operators=None):
        r'''Partitions next `number` cells in `cursor` cyclically by `counts`.

        Applies optional `operators` to parts in resulting partition.

        Returns none.
        '''
        cells = cursor.next(number)
        list_ = []
        for cell in cells:
            list_.extend(cell)
        segment = baca.PitchClassSegment(items=list_)
        operators = operators or []
        for operator in operators:
            segment = self._apply_operator(segment, operator)
        sequence = abjad.sequence(segment)
        parts = sequence.partition_by_counts(
            counts,
            cyclic=True,
            overhang=True,
            )
        parts = [baca.PitchClassSegment(_) for _ in parts]
        self._result.extend(parts)
