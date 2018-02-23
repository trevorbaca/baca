import abjad
import baca
import typing
from abjad import rhythmmakertools as rhythmos
from .Command import Command
from .DivisionMaker import DivisionMaker


class RhythmCommand(Command):
    r'''Rhythm command.

    >>> from abjad import rhythmmakertools as rhythmos

    ..  container:: example

        >>> command = baca.RhythmCommand(
        ...     rhythm_maker=rhythmos.NoteRhythmMaker(),
        ...     )

    ..  container:: example

        >>> command = baca.RhythmCommand(
        ...     division_expression=abjad.sequence().sum().sequence(),
        ...     rhythm_maker=rhythmos.NoteRhythmMaker(),
        ...     )

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_division_maker',
        '_division_expression',
        '_left_broken',
        '_persist',
        '_reference_meters',
        '_rewrite_meter',
        '_rhythm_maker',
        '_rhythm_overwrites',
        '_right_broken',
        '_split_at_measure_boundaries',
        '_stages',
        '_state',
        '_tie_first',
        '_tie_last',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        division_maker: DivisionMaker = None,
        division_expression: abjad.Expression = None,
        left_broken: bool = None,
        persist: str = None,
        reference_meters: typing.List = None,
        rewrite_meter: bool = None,
        rhythm_maker: typing.Union[
            rhythmos.RhythmMaker, abjad.Selection] = None,
        rhythm_overwrites=None,
        right_broken: bool = None,
        split_at_measure_boundaries: bool = None,
        stages: typing.Tuple[int, int] = None,
        tie_first: bool = None,
        tie_last: bool = None,
        ) -> None:
        if division_expression is not None and division_maker is not None:
            message = 'can not set both division expression and division-maker'
            message += f':\n{division_expression} {division_maker}.'
            raise Exception(message)
        self._division_maker: DivisionMaker = division_maker
        self._division_expression: abjad.Expression = division_expression
        if left_broken is not None:
            left_broken = bool(left_broken)
        self._left_broken: bool = left_broken
        if persist is not None:
            assert isinstance(persist, str), repr(persist)
        self._persist: str = persist
        self._reference_meters: typing.List = reference_meters
        self._rewrite_meter: bool = rewrite_meter
        self._rhythm_maker: typing.Union[
            rhythmos.RhythmMaker, abjad.Selection] = rhythm_maker
        self._rhythm_overwrites = rhythm_overwrites
        if right_broken is not None:
            right_broken = bool(right_broken)
        self._right_broken: bool = right_broken
        self._split_at_measure_boundaries: bool = split_at_measure_boundaries
        self._stages: typing.Tuple[int, int] = stages
        self._state: abjad.OrderedDict = None
        self._tie_first: bool = tie_first
        self._tie_last: bool = tie_last

    ### SPECIAL METHODS ###

    def __call__(
        self,
        start_offset: abjad.Offset = None,
        time_signatures: typing.List[abjad.TimeSignature] = None,
        ) -> abjad.AnnotatedTimespan:
        r'''Calls command on ``start_offset`` and ``time_signatures``.
        '''
        music, start_offset = self._make_rhythm(start_offset, time_signatures)
        assert isinstance(music, (tuple, list, abjad.Voice))
        first_leaf = abjad.inspect(music).get_leaf(0)
        last_leaf = abjad.inspect(music).get_leaf(-1)
        pitched_prototype = (abjad.Note, abjad.Chord)
        if self.tie_first and isinstance(first_leaf, pitched_prototype):
            abjad.attach(abjad.tags.TIE_TO, first_leaf)
            if self.repeat_ties:
                abjad.attach(abjad.tags.REPEAT_TIE, first_leaf)
        if self.tie_last and isinstance(last_leaf, pitched_prototype):
            abjad.attach(abjad.tags.TIE_FROM, last_leaf)
            if self.repeat_ties:
                abjad.attach(abjad.tags.REPEAT_TIE, last_leaf)
        return abjad.AnnotatedTimespan(
            start_offset=start_offset,
            stop_offset=None,
            annotation=music,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _default_division_maker(self):
        division_maker = baca.DivisionMaker()
        return division_maker

    @property
    def _default_rhythm_maker(self):
        mask = abjad.silence([0], 1, use_multimeasure_rests=True)
        multimeasure_rests = rhythmos.NoteRhythmMaker(division_masks=[mask])
        return multimeasure_rests

    ### PRIVATE METHODS ###

    @staticmethod
    def _all_are_selections(argument):
        return all(
            isinstance(_, abjad.Selection) for _ in argument)

    @staticmethod
    def _annotate_unpitched_notes(argument):
        rest_prototype = (
            abjad.MultimeasureRest,
            abjad.Rest,
            abjad.Skip,
            )
        for leaf in abjad.iterate(argument).leaves():
            if isinstance(leaf, abjad.Chord):
                message = f'rhythm-makers make only notes and rests: {leaf!r}.'
                raise Exception(message)
            elif isinstance(leaf, abjad.Note):
                abjad.attach(abjad.tags.NOT_YET_PITCHED, leaf, tag=None)
            elif isinstance(leaf, rest_prototype):
                pass
            else:
                raise TypeError(leaf)

    @staticmethod
    def _durations_to_divisions(durations, start_offset):
        divisions = [baca.Division(_) for _ in durations]
        durations = [_.duration for _ in divisions]
        start_offset = abjad.Offset(start_offset)
        durations.insert(0, start_offset)
        start_offsets = abjad.mathtools.cumulative_sums(durations)[1:-1]
        assert len(divisions) == len(start_offsets)
        divisions_ = []
        for division, start_offset in zip(divisions, start_offsets):
            division_ = baca.Division(
                division,
                start_offset=start_offset,
                )
            divisions_.append(division_)
        assert not any(_.start_offset is None for _ in divisions_)
        return divisions_

    def _get_storage_format_specification(self):
        agent = abjad.StorageFormatManager(self)
        keyword_argument_names = agent.signature_keyword_names
        if not self.rhythm_overwrites:
            keyword_argument_names = list(keyword_argument_names)
            keyword_argument_names.remove('rhythm_overwrites')
        return abjad.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    def _handle_rhythm_overwrites(self, time_signatures, selections):
        if not self.rhythm_overwrites:
            selections
        maker = abjad.MeasureMaker()
        dummy_measures = maker(time_signatures)
        dummy_time_signature_voice = abjad.Voice(dummy_measures)
        dummy_music_voice = abjad.Voice()
        dummy_music_voice.extend(selections)
        dummy_staff = abjad.Staff([
            dummy_time_signature_voice,
            dummy_music_voice,
            ])
        dummy_staff.is_simultaneous = True
        assert len(self.rhythm_overwrites) == 1, repr(self.rhythm_overwrites)
        selector, division_maker, rhythm_maker = self.rhythm_overwrites[0]
        old_selection = selector(dummy_music_voice)
        old_selection = abjad.select(old_selection)
        result = old_selection._get_parent_and_start_stop_indices()
        parent, start_index, stop_index = result
        old_duration = abjad.inspect(old_selection).get_duration()
        division_lists = division_maker([old_duration])
        assert len(division_lists) == 1
        division_list = division_lists[0]
        new_selection = rhythm_maker(division_list)
        stop_index += 1
        dummy_music_voice[start_index:stop_index] = new_selection
        music = dummy_music_voice[:]
        selections = [abjad.select(_) for _ in music]
        return selections

    def _make_rhythm(self, start_offset, time_signatures):
        rhythm_maker = self.rhythm_maker or self._default_rhythm_maker
        if isinstance(rhythm_maker, abjad.Selection):
            selections = [rhythm_maker]
        else:
            if not isinstance(rhythm_maker, rhythmos.RhythmMaker):
                message = f'rhythm-maker or selection: {rhythm_maker!r}.'
                raise TypeError(message)
            division_maker = self.division_maker
            if division_maker is None:
                division_maker = self._default_division_maker
            divisions = self._durations_to_divisions(
                time_signatures,
                start_offset,
                )
            divisions = division_maker(divisions)
            divisions = baca.sequence(divisions).flatten(depth=-1)
            divisions = self._transform_divisions(divisions)
            start_offset = divisions[0].start_offset
            previous_state = None
            dictionary = self.previous_segment_voice_metadata
            if dictionary:
                previous_state = dictionary.get(abjad.tags.RHYTHM)
            selections = rhythm_maker(divisions, previous_state=previous_state)
            self._annotate_unpitched_notes(selections)
            self._state = rhythm_maker.state
        assert self._all_are_selections(selections), repr(selections)
        if self.split_at_measure_boundaries:
            specifier = rhythmos.DurationSpecifier
            selections = specifier._split_at_measure_boundaries(
                selections,
                time_signatures,
                repeat_ties=self.repeat_ties,
                )
            assert self._all_are_selections(selections), repr(selections)
        if self.rewrite_meter:
            selections = rhythmos.DurationSpecifier._rewrite_meter_(
                selections,
                time_signatures,
                reference_meters=self.reference_meters,
                rewrite_tuplets=False,
                repeat_ties=self.repeat_ties,
                )
        if self.rhythm_overwrites:
            selections = self._handle_rhythm_overwrites(
                time_signatures,
                selections,
                )
        self._tag_broken_ties(selections)
        return selections, start_offset

    def _tag_broken_ties(self, selections):
        if not isinstance(self.rhythm_maker, rhythmos.RhythmMaker):
            return
        if (self.left_broken and
            self.rhythm_maker.previous_state.get('incomplete_last_note')):
            if not self.repeat_ties:
                raise Exception('left-broken ties must be repeat ties.')
            first_leaf = abjad.select(selections).leaf(0)
            if isinstance(first_leaf, abjad.Note):
                abjad.attach(abjad.tags.LEFT_BROKEN_REPEAT_TIE_TO, first_leaf)
        if (self.right_broken and
            self.rhythm_maker.state.get('incomplete_last_note')):
            if self.repeat_ties:
                raise Exception('right-broken ties must be conventional.')
            last_leaf = abjad.select(selections).leaf(-1)
            if isinstance(last_leaf, abjad.Note):
                abjad.attach(abjad.tags.RIGHT_BROKEN_TIE_FROM, last_leaf)

    def _transform_divisions(
        self,
        divisions,
        ) -> typing.Optional[abjad.Sequence]:
        if self.division_expression is not None:
            divisions = self.division_expression(divisions)
            assert isinstance(divisions, abjad.Sequence), repr(divisions)
        return divisions

    ### PUBLIC PROPERTIES ###

    @property
    def division_expression(self) -> typing.Optional[abjad.Expression]:
        r'''Gets division expression.
        '''
        return self._division_expression

    @property
    def division_maker(self) -> typing.Optional[DivisionMaker]:
        r'''Gets division-maker.
        '''
        return self._division_maker

    @property
    def left_broken(self) -> bool:
        r'''Is true when rhythm is left-broken.
        '''
        return self._left_broken

    @property
    def parameter(self) -> str:
        r'''Gets persistence parameter.

        ..  container:: example

            >>> baca.RhythmCommand().parameter
            'RHYTHM'

        '''
        return abjad.tags.RHYTHM

    @property
    def persist(self) -> typing.Optional[str]:
        '''Gets persist name.
        '''
        return self._persist

    @property
    def reference_meters(self) -> typing.List:
        r'''Gets reference meters.

        Only used to rewrite meters.

        Set to list of meters or none.
        '''
        return self._reference_meters

    @property
    def repeat_ties(self) -> bool:
        tie_specifier = getattr(self.rhythm_maker, 'tie_specifier', None)
        if tie_specifier is None:
            return False
        return tie_specifier.repeat_ties

    @property
    def rewrite_meter(self) -> bool:
        r'''Is true when command rewrites meter.
        '''
        return self._rewrite_meter

    @property
    def rhythm_maker(self) -> typing.Optional[
        typing.Union[rhythmos.RhythmMaker, abjad.Selection]
        ]:
        r'''Gets rhythm-maker (or selection).
        '''
        return self._rhythm_maker

    @property
    def rhythm_overwrites(self) -> typing.List:
        r'''Gets rhythm overwrites.
        '''
        return self._rhythm_overwrites

    @property
    def right_broken(self) -> bool:
        r'''Is true when rhythm is right-broken.
        '''
        return self._right_broken

    @property
    def split_at_measure_boundaries(self) -> bool:
        r'''Is true when command splits at measure boundaries.
        '''
        return self._split_at_measure_boundaries

    @property
    def stages(self) -> typing.Tuple[int, int]:
        r'''Gets stages.
        '''
        return self._stages

    @property
    def start_stage(self) -> int:
        r'''Gets start stage.
        '''
        return self.stages[0]

    @property
    def state(self) -> abjad.OrderedDict:
        r'''Gets postcall state of rhythm command.

        Populated by segment-maker.
        '''
        return self._state

    @property
    def stop_stage(self) -> int:
        r'''Gets stop stage.
        '''
        return self.stages[-1]

    @property
    def tie_first(self) -> bool:
        r'''Is true when command ties into first note or chord.
        '''
        return self._tie_first

    @property
    def tie_last(self) -> bool:
        r'''Is true when command ties into last note or chord.
        '''
        return self._tie_last
