import abjad
import baca
import typing
from .MetronomeMarkMeasureMap import MetronomeMarkMeasureMap
from .StageMeasureMap import StageMeasureMap


class TimeSignatureMaker(abjad.AbjadObject):
    r'''Time-signature-maker.

    ..  container:: example

        >>> time_signatures = [
        ...     [(1, 16), (2, 16), (3, 16)],
        ...     [(1, 8), (2, 8), (3, 8)],
        ...     ]
        >>> stage_measure_map = baca.StageMeasureMap([
        ...     2,
        ...     2,
        ...     abjad.Fermata('longfermata'),
        ...     ])
        >>> metronome_mark_measure_map = baca.MetronomeMarkMeasureMap([
        ...     (1, abjad.MetronomeMark((1, 4), 90)),
        ...     ])
        >>> maker = baca.TimeSignatureMaker(
        ...     time_signatures=time_signatures,
        ...     stage_measure_map=stage_measure_map,
        ...     metronome_mark_measure_map=metronome_mark_measure_map,
        ...     )
        >>> measures_per_stage, metronome_mark_measure_map, time_signatures = maker()

        >>> measures_per_stage
        [2, 2, 1]

        >>> time_signatures
        Sequence([(1, 16), (2, 16), (3, 16), (1, 8), TimeSignature((1, 4))])

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_metronome_mark_measure_map',
        '_repeat_count',
        '_rotation',
        '_stage_measure_map',
        '_time_signatures',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        time_signatures,
        metronome_mark_measure_map: MetronomeMarkMeasureMap = None,
        repeat_count: int = None,
        rotation: int = None,
        stage_measure_map: StageMeasureMap = None,
        ) -> None:
        self._time_signatures = time_signatures
        self._metronome_mark_measure_map = metronome_mark_measure_map
        self._repeat_count = repeat_count
        self._rotation = rotation
        self._stage_measure_map = stage_measure_map

    ### SPECIAL METHODS ###

    def __call__(self) -> typing.Tuple[
        typing.List[int],
        MetronomeMarkMeasureMap,
        typing.List[abjad.TimeSignature],
        ]:
        r'''Calls time-signature-maker.
        '''
        time_signatures = baca.sequence(self.time_signatures)
        time_signatures = time_signatures.rotate(self.rotation)
        time_signatures = time_signatures.flatten(depth=1)
        items = []
        for item in self.stage_measure_map.items:
            if isinstance(item, abjad.Fermata):
                item = abjad.TimeSignature((1, 4))
            items.append(item)
        stage_measure_map = StageMeasureMap(items=items)
        time_signature_groups = self._make_time_signature_groups(
            self.repeat_count,
            stage_measure_map,
            time_signatures,
            )
        measures_per_stage = [len(_) for _ in time_signature_groups]
        time_signatures = baca.sequence(time_signature_groups).flatten(depth=1)
        fermata_entries = self.stage_measure_map._make_fermata_entries()
        if self.metronome_mark_measure_map:
            items = self.metronome_mark_measure_map.items
        else:
            items = []
        items = list(items) + list(fermata_entries)
        metronome_mark_measure_map = MetronomeMarkMeasureMap(items=items)
        return measures_per_stage, metronome_mark_measure_map, time_signatures

    ### PRIVATE METHODS ###

    def _make_time_signature_groups(
        self,
        repeat_count,
        stage_measure_map,
        time_signatures,
        ):
        time_signatures = abjad.CyclicTuple(time_signatures)
        time_signature_lists = []
        index = 0
        for item in stage_measure_map:
            if isinstance(item, abjad.TimeSignature):
                time_signature_list = [item]
            elif isinstance(item, (tuple, list)):
                time_signature_list = list(item)
            else:
                stop = index + item
                time_signature_list = time_signatures[index:stop]
                time_signature_list = list(time_signature_list)
                index += item
            time_signature_lists.append(time_signature_list)
        repeat_count = repeat_count or 1
        time_signature_lists *= repeat_count
        return time_signature_lists

    ### PUBLIC PROPERTIES ###

    @property
    def metronome_mark_measure_map(self) -> typing.Optional[
        MetronomeMarkMeasureMap
        ]:
        r'''Gets metronome mark measure map.
        '''
        return self._metronome_mark_measure_map

    @property
    def repeat_count(self) -> typing.Optional[int]:
        r'''Gets repeat count.
        '''
        return self._repeat_count

    @property
    def rotation(self) -> typing.Optional[int]:
        r'''Gets rotation.
        '''
        return self._rotation

    @property
    def stage_measure_map(self) -> typing.Optional[StageMeasureMap]:
        r'''Gets stage measure map.
        '''
        return self._stage_measure_map

    @property
    def time_signatures(self) -> typing.List[abjad.TimeSignature]:
        r'''Gets time signatures.
        '''
        return self._time_signatures
