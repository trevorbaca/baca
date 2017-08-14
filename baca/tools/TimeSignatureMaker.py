import abjad
import baca


class TimeSignatureMaker(abjad.AbjadObject):
    r'''Time signature maker.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> time_signatures = [
            ...     [(1, 16), (2, 16), (3, 16)],
            ...     [(1, 8), (2, 8), (3, 8)],
            ...     ]
            >>> stage_specifier = baca.StageSpecifier([
            ...     2,
            ...     2,
            ...     abjad.Fermata('longfermata'),
            ...     ])
            >>> tempo_specifier = baca.TempoSpecifier([
            ...     (1, abjad.MetronomeMark((1, 4), 90)),
            ...     ])
            >>> maker = baca.TimeSignatureMaker(
            ...     time_signatures=time_signatures,
            ...     stage_specifier=stage_specifier,
            ...     tempo_specifier=tempo_specifier,
            ...     )
            >>> measures_per_stage, tempo_specifier, time_signatures = maker()

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
        '_stage_specifier',
        '_tempo_map',
        '_time_signatures',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        time_signatures,
        repeat_count=None,
        rotation=None,
        stage_specifier=None,
        tempo_specifier=None,
        ):
        self._time_signatures = time_signatures
        self._rotation = rotation
        self._stage_specifier = stage_specifier
        self._tempo_map = tempo_specifier
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
        for item in self.stage_specifier:
            if isinstance(item, abjad.Fermata):
                item = abjad.TimeSignature((1, 4))
            items.append(item)
        stage_specifier = baca.StageSpecifier(items=items)
        time_signature_groups = self._make_time_signature_groups(
            self.repeat_count,
            stage_specifier,
            time_signatures,
            )
        measures_per_stage = [len(_) for _ in time_signature_groups]
        time_signatures = baca.Sequence(time_signature_groups).flatten(depth=1)
        fermata_entries = self.stage_specifier._make_fermata_entries()
        items = self.tempo_specifier.items + fermata_entries
        tempo_specifier = baca.TempoSpecifier(items=items)
        return measures_per_stage, tempo_specifier, time_signatures

    ### PRIVATE METHODS ###

    def _make_time_signature_groups(
        self,
        repeat_count,
        stage_specifier,
        time_signatures,
        ):
        time_signatures = abjad.CyclicTuple(time_signatures)
        time_signature_lists = []
        index = 0
        for x in stage_specifier:
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
    def stage_specifier(self):
        r'''Gets stage specifier.

        Returns stage specifier.
        '''
        return self._stage_specifier

    @property
    def tempo_specifier(self):
        r'''Gets tempo map.

        Returns tempo map.
        '''
        return self._tempo_map

    @property
    def time_signatures(self):
        r'''Gets time signatures.

        Returns list of time signatures.
        '''
        return self._time_signatures
