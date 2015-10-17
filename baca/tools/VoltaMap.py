# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class VoltaMap(AbjadObject):
    r'''Volta map.

    ..  container:: example

        **Example.**

        ::

            >>> import baca

        ::

            >>> volta_map = baca.tools.VoltaMap([
            ...     baca.tools.MeasureExpression(2, 4),
            ...     baca.tools.MeasureExpression(16, 18),
            ...     ])

        ::

            >>> print(format(volta_map))
            baca.tools.VoltaMap(
                items=(
                    baca.tools.MeasureExpression(
                        start_number=2,
                        stop_number=4,
                        ),
                    baca.tools.MeasureExpression(
                        start_number=16,
                        stop_number=18,
                        ),
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        )

    ### INITIALIZER ###

    def __init__(self, items=None):
        if items is not None:
            items = tuple(items)
        self._items = items

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        r'''Gets item.

        ..  container:: example

            **Example.** Gets items:

            ::

                >>> volta_map = baca.tools.VoltaMap([
                ...     baca.tools.MeasureExpression(2, 4),
                ...     baca.tools.MeasureExpression(16, 18),
                ...     ])

            ::

                >>> volta_map[1]
                MeasureExpression(start_number=16, stop_number=18)

        Returns item.
        '''
        return self.items.__getitem__(expr)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            **Example.**

            ::

                >>> volta_map = baca.tools.VoltaMap([
                ...     baca.tools.MeasureExpression(2, 4),
                ...     baca.tools.MeasureExpression(16, 18),
                ...     ])

            ::

                >>> for item in volta_map.items:
                ...     item
                MeasureExpression(start_number=2, stop_number=4)
                MeasureExpression(start_number=16, stop_number=18)

        Defaults to none.

        Set to tuple or none.

        Returns tuple or none.
        '''
        return self._items