# -*- coding: utf-8 -*-
from abjad.tools import abctools


class StageSpecifier(abctools.AbjadObject):
    r'''Stage specifier.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** Counts with a single explicit time signature mixed in:

        ::

            >>> specifier = baca.tools.StageSpecifier([
            ...     4,
            ...     4,
            ...     4, TimeSignature((1, 4)),
            ...     4,
            ...     ])

        ::

            >>> print(format(specifier))
            baca.tools.StageSpecifier(
                items=(
                    4,
                    4,
                    4,
                    indicatortools.TimeSignature((1, 4)),
                    4,
                    ),
                )

    ..  container:: example

        **Example 2.** Counts with a run of explicit time signatures mixed in:

        ::

            >>> specifier = baca.tools.StageSpecifier([
            ...     4,
            ...     4,
            ...     4, [TimeSignature((5, 4)), TimeSignature((5, 4))],
            ...     4,
            ...     ])

        ::

            >>> print(format(specifier))
            baca.tools.StageSpecifier(
                items=(
                    4,
                    4,
                    4,
                    [
                        indicatortools.TimeSignature((5, 4)),
                        indicatortools.TimeSignature((5, 4)),
                        ],
                    4,
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

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

                >>> specifier = baca.tools.StageSpecifier([
                ...     4,
                ...     4,
                ...     4, TimeSignature((1, 4)),
                ...     4,
                ...     ])

            ::

                >>> specifier[0]
                4

        Returns item.
        '''
        return self.items.__getitem__(expr)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            **Example.** Gets items:

            ::

                >>> specifier = baca.tools.StageSpecifier([
                ...     4,
                ...     4,
                ...     4, TimeSignature((1, 4)),
                ...     4,
                ...     ])

            ::

                >>> specifier.items
                (4, 4, 4, TimeSignature((1, 4)), 4)

        Defaults to none.

        Set to tuple or none.

        Returns tuple or none.
        '''
        return self._items

    @property
    def stage_count(self):
        r'''Gets stage count.

        ..  container:: example

            **Example.** Gets stage count:

            ::

                >>> specifier = baca.tools.StageSpecifier([
                ...     4,
                ...     4,
                ...     4, TimeSignature((1, 4)),
                ...     4,
                ...     ])

            ::

                >>> specifier.stage_count
                5

        Returns nonnegative integer.
        '''
        return len(self.items)

    ### PUBLIC METHODS ###

    def make_fermata_entries(self):
        r'''Makes fermata entries.

        Returns tuple of pairs.
        '''
        from abjad.tools import indicatortools
        fermata_entries = []
        for stage_index, item in enumerate(self):
            if isinstance(item, indicatortools.Fermata):
                stage_number = stage_index + 1
                fermata_entry = (stage_number, item)
                fermata_entries.append(fermata_entry)
        fermata_entries = tuple(fermata_entries)
        return fermata_entries