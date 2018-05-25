import abjad
import typing


class StageMeasureMap(abjad.AbjadObject):
    r"""
    Stage measure map.

    ..  container:: example

        >>> stages = baca.StageMeasureMap([
        ...     4,
        ...     4,
        ...     4, abjad.TimeSignature((1, 4)),
        ...     4,
        ...     ])

        >>> abjad.f(stages, strict=89)
        baca.StageMeasureMap(
            items=(
                4,
                4,
                4,
                abjad.TimeSignature((1, 4)),
                4,
                ),
            )

    ..  container:: example

        >>> stages = baca.StageMeasureMap([
        ...     4,
        ...     4,
        ...     4, [abjad.TimeSignature((5, 4)), abjad.TimeSignature((5, 4))],
        ...     4,
        ...     ])

        >>> abjad.f(stages, strict=89)
        baca.StageMeasureMap(
            items=(
                4,
                4,
                4,
                [
                    abjad.TimeSignature((5, 4)),
                    abjad.TimeSignature((5, 4)),
                    ],
                4,
                ),
            )

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_items',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    item_type = typing.Union[
        int,
        abjad.Accelerando,
        abjad.Fermata,
        abjad.Ritardando,
        abjad.TimeSignature, 
        ]

    def __init__(
        self,
        items: typing.List[item_type] = None,
        ) -> None:
        items = items or []
        self._items = tuple(items)

    ### SPECIAL METHODS ###

    def __getitem__(self, argument) -> item_type:
        """
        Gets item identified by ``argument``.

        ..  container:: example

            >>> stages = baca.StageMeasureMap([
            ...     4,
            ...     4,
            ...     4, abjad.TimeSignature((1, 4)),
            ...     4,
            ...     ])

            >>> stages[0]
            4

        """
        return self.items.__getitem__(argument)

    ### PRIVATE METHODS ###

    def _make_fermata_entries(self):
        fermata_entries = []
        for stage_index, item in enumerate(self):
            if isinstance(item, abjad.Fermata):
                stage_number = stage_index + 1
                fermata_entry = (stage_number, item)
                fermata_entries.append(fermata_entry)
        fermata_entries = tuple(fermata_entries)
        return fermata_entries

    ### PUBLIC PROPERTIES ###

    @property
    def items(self) -> typing.Tuple[item_type, ...]:
        """
        Gets items.

        ..  container:: example

            >>> stages = baca.StageMeasureMap([
            ...     4,
            ...     4,
            ...     4, abjad.TimeSignature((1, 4)),
            ...     4,
            ...     ])

            >>> stages.items
            (4, 4, 4, TimeSignature((1, 4)), 4)

        """
        return self._items

    @property
    def stage_count(self) -> int:
        """Gets stage count.

        ..  container:: example

            >>> stages = baca.StageMeasureMap([
            ...     4,
            ...     4,
            ...     4, abjad.TimeSignature((1, 4)),
            ...     4,
            ...     ])

            >>> stages.stage_count
            5

        """
        return len(self.items)
