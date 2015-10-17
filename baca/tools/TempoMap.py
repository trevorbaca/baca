# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class TempoMap(AbjadObject):
    r'''Tempo map.

    ..  container:: example

        **Example.**

        ::

            >>> import baca
            >>> tempo_map = baca.tools.TempoMap([
            ...     (1, Tempo(Duration(1, 4), 90)),
            ...     (1, Accelerando()),
            ...     (4, Tempo(Duration(1, 4), 120)),
            ...     ])

        ::

            >>> print(format(tempo_map))
            baca.tools.TempoMap(
                items=(
                    (
                        1,
                        indicatortools.Tempo(
                            reference_duration=durationtools.Duration(1, 4),
                            units_per_minute=90,
                            ),
                        ),
                    (
                        1,
                        indicatortools.Accelerando(),
                        ),
                    (
                        4,
                        indicatortools.Tempo(
                            reference_duration=durationtools.Duration(1, 4),
                            units_per_minute=120,
                            ),
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

                >>> tempo_map = baca.tools.TempoMap([
                ...     (1, Tempo(Duration(1, 4), 90)),
                ...     (1, Accelerando()),
                ...     (4, Tempo(Duration(1, 4), 120)),
                ...     ])

            ::

                >>> tempo_map[1]
                (1, Accelerando())

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

                >>> import baca
                >>> tempo_map = baca.tools.TempoMap([
                ...     (1, Tempo(Duration(1, 4), 90)),
                ...     (1, Accelerando()),
                ...     (4, Tempo(Duration(1, 4), 120)),
                ...     ])

            ::

                >>> for item in tempo_map.items:
                ...     item
                (1, Tempo(reference_duration=Duration(1, 4), units_per_minute=90))
                (1, Accelerando())
                (4, Tempo(reference_duration=Duration(1, 4), units_per_minute=120))

        Defaults to none.

        Set to tuple or none.

        Returns tuple or none.
        '''
        return self._items