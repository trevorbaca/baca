import abjad
import baca
import typing
from abjad import rhythmmakertools as rhythmos
from .Command import Command


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
        '_previous_state',
        '_reference_meters',
        '_rewrite_meter',
        '_rhythm_maker',
        '_rhythm_overwrites',
        '_split_at_measure_boundaries',
        '_stages',
        '_state',
        '_state_dictionary_name',
        '_tie_first',
        '_tie_last',
        '_voice_metadata',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        division_maker=None,
        division_expression=None,
        reference_meters=None,
        rewrite_meter: bool = None,
        rhythm_maker=None,
        rhythm_overwrites=None,
        split_at_measure_boundaries: bool = None,
        stages=None,
        state_dictionary_name: str = None,
        tie_first: bool = None,
        tie_last: bool = None,
        ) -> None:
        if division_expression is not None and division_maker is not None:
            message = 'can not set both division expression and division-maker'
            message += f':\n{division_expression} {division_maker}.'
            raise Exception(message)
        self._division_maker = division_maker
        self._division_expression: abjad.Expression = division_expression
        self._previous_state: abjad.OrderedDict = None
        self._reference_meters = reference_meters
        self._rewrite_meter: bool = rewrite_meter
        self._rhythm_maker = rhythm_maker
        self._rhythm_overwrites = rhythm_overwrites
        self._split_at_measure_boundaries: bool = split_at_measure_boundaries
        self._stages = stages
        self._state: typing.Optional[abjad.OrderedDict] = None
        self._state_dictionary_name: str = state_dictionary_name
        self._tie_first: bool = tie_first
        self._tie_last: bool = tie_last
        self._voice_metadata: typing.Optional[abjad.OrderedDict] = None

    ### SPECIAL METHODS ###

    def __call__(
        self,
        start_offset: abjad.Offset = None,
        time_signatures: typing.List[abjad.TimeSignature] = None,
        ) -> abjad.AnnotatedTimespan:
        r'''Calls command on `start_offset` and `time_signatures`.
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

    def _make_rhythm(self, start_offset, time_signatures):
        rhythm_maker = self.rhythm_maker or self._default_rhythm_maker
        if isinstance(rhythm_maker, abjad.Selection):
            selections = [rhythm_maker]
        elif not isinstance(rhythm_maker, rhythmos.RhythmMaker):
            raise TypeError(f'rhythm-maker or selection: {rhythm_maker!r}.')
        else:
            state = self._previous_state or abjad.OrderedDict()
            #pairs = state.get(self.state_dictionary_name, [])
            #state = abjad.OrderedDict(pairs)
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
            selections = rhythm_maker(divisions, state=state)
            self._annotate_unpitched_notes(selections)
        if hasattr(rhythm_maker, 'state'):
            self._make_voice_metadata(rhythm_maker.state)
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
            specifier = rhythmos.DurationSpecifier
            selections = specifier._rewrite_meter_(
                selections,
                time_signatures,
                reference_meters=self.reference_meters,
                rewrite_tuplets=False,
                repeat_ties=self.repeat_ties,
                )
        if not self.rhythm_overwrites:
            return selections, start_offset
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
        return selections, start_offset

    def _make_voice_metadata(self, state: abjad.OrderedDict):
        if not self.state_dictionary_name:
            return
        voice_metadata = abjad.OrderedDict()
        voice_metadata[self.state_dictionary_name] = state
        self._voice_metadata = voice_metadata

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
    def division_expression(self):
        r'''Gets division expression.

        Set to none or division expresion.

        Returns none or division expression.
        '''
        return self._division_expression

    @property
    def division_maker(self):
        r'''Gets division-maker.

        Set to none or division-maker.

        Returns none or division-maker.
        '''
        return self._division_maker

    @property
    def reference_meters(self):
        r'''Gets reference meters.

        Only used to rewrite meters.

        Set to list of meters or none.

        Defaults to none.

        Returns list of meters or none.
        '''
        return self._reference_meters

    @property
    def repeat_ties(self):
        if self.rhythm_maker.tie_specifier is None:
            return False
        return self.rhythm_maker.tie_specifier.repeat_ties

    @property
    def rewrite_meter(self):
        r'''Is true when command rewrites meter.

        Set to true or false.

        Returns true or false.
        '''
        return self._rewrite_meter

    @property
    def rhythm_maker(self):
        r'''Gets rhythm-maker.

        Set to rhythm-maker, music or none.

        Returns rhythm-maker or music.
        '''
        return self._rhythm_maker

    @property
    def rhythm_overwrites(self):
        r'''Gets rhythm overwrites.

        Returns list.
        '''
        return self._rhythm_overwrites

    @property
    def split_at_measure_boundaries(self):
        r'''Is true when command splits at measure boundaries.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._split_at_measure_boundaries

    @property
    def stages(self):
        r'''Gets stages.

        Returns pair of positive integers.
        '''
        return self._stages

    @property
    def start_stage(self):
        r'''Gets start stage.

        Returns positive integer.
        '''
        return self.stages[0]

    @property
    def state(self) -> abjad.OrderedDict:
        r'''Gets postcall state of rhythm command.

        Populated by segment-maker.
        '''
        return self._state

    @property
    def state_dictionary_name(self) -> typing.Optional[str]:
        '''Gets state dictionary name.
        '''
        return self._state_dictionary_name

    @property
    def stop_stage(self):
        r'''Gets stop stage.

        Returns positive integer.
        '''
        return self.stages[-1]

    @property
    def tie_first(self):
        r'''Is true when command ties into first note or chord.
        Otherwise false.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._tie_first

    @property
    def tie_last(self):
        r'''Is true when command ties into last note or chord.
        Otherwise false.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._tie_last

    @property
    def voice_metadata(self) -> typing.Optional[abjad.OrderedDict]:
        r'''Gets voice metadata.
        '''
        return self._voice_metadata
