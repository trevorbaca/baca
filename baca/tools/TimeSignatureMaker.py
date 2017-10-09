import abjad
import baca


class TimeSignatureMaker(abjad.AbjadObject):
    r'''Time signature maker.

    ..  container:: example

        ::

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

        ::

            >>> measures_per_stage
            [2, 2, 1]

        ::

            >>> time_signatures
            Sequence([(1, 16), (2, 16), (3, 16), (1, 8), TimeSignature((1, 4))])

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_repeat_count',
        '_rotation',
        '_stage_measure_map',
        '_tempo_map',
        '_time_signatures',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        time_signatures,
        repeat_count=None,
        rotation=None,
        stage_measure_map=None,
        metronome_mark_measure_map=None,
        ):
        self._time_signatures = time_signatures
        self._rotation = rotation
        self._stage_measure_map = stage_measure_map
        self._tempo_map = metronome_mark_measure_map
        self._repeat_count = repeat_count

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls time signature maker.

        Returns measures per stage, tempo map and time signatures.
        '''
        time_signatures = abjad.sequence(self.time_signatures)
        time_signatures = time_signatures.rotate(self.rotation)
        time_signatures = time_signatures.flatten(depth=1)
        items = []
        for item in self.stage_measure_map:
            if isinstance(item, abjad.Fermata):
                item = abjad.TimeSignature((1, 4))
            items.append(item)
        stage_measure_map = baca.StageMeasureMap(items=items)
        time_signature_groups = self._make_time_signature_groups(
            self.repeat_count,
            stage_measure_map,
            time_signatures,
            )
        measures_per_stage = [len(_) for _ in time_signature_groups]
        time_signatures = baca.Sequence(time_signature_groups).flatten(depth=1)
        fermata_entries = self.stage_measure_map._make_fermata_entries()
        items = self.metronome_mark_measure_map.items + fermata_entries
        metronome_mark_measure_map = baca.MetronomeMarkMeasureMap(items=items)
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
        for x in stage_measure_map:
            if isinstance(x, abjad.TimeSignature):
                time_signature_list = [x]
            elif isinstance(x, (tuple, list)):
                time_signature_list = list(x)
            else:
                stop = index + x
                time_signature_list = time_signatures[index:stop]
                time_signature_list = list(time_signature_list)
                index += x
            time_signature_lists.append(time_signature_list)
        repeat_count = repeat_count or 1
        time_signature_lists *= repeat_count
        return time_signature_lists

    ### PUBLIC PROPERTIES ###

    @property
    def metronome_mark_measure_map(self):
        r'''Gets tempo map.

        Returns tempo map.
        '''
        return self._tempo_map

    @property
    def repeat_count(self):
        r'''Gets repeat count.

        Returns nonnegative integer or none.
        '''
        return self._repeat_count

    @property
    def rotation(self):
        r'''Gets rotation.

        Returns integer or none.
        '''
        return self._rotation

    @property
    def stage_measure_map(self):
        r'''Gets stage specifier.

        Returns stage specifier.
        '''
        return self._stage_measure_map

    @property
    def time_signatures(self):
        r'''Gets time signatures.

        Returns list of time signatures.
        '''
        return self._time_signatures
