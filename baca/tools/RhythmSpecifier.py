# -*- coding: utf-8 -*-
import abjad
import baca


class RhythmSpecifier(abjad.abctools.AbjadObject):
    r'''Rhythm specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Specifies rhythm:

        ::

            >>> rhythm_specifier = baca.RhythmSpecifier(
            ...     rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(),
            ...     )

        ::

            >>> f(rhythm_specifier)
            baca.tools.RhythmSpecifier(
                rhythm_maker=rhythmmakertools.NoteRhythmMaker(),
                )

    ..  container:: example

        Specifies rhythm:

        ::

            >>> rhythm_specifier = baca.RhythmSpecifier(
            ...     division_expression=abjad.sequence().sum().sequence(),
            ...     rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(),
            ...     )

        ::

            >>> f(rhythm_specifier)
            baca.tools.RhythmSpecifier(
                division_expression=abjad.Expression(
                    callbacks=[
                        abjad.Expression(
                            evaluation_template='abjad.sequencetools.Sequence',
                            is_initializer=True,
                            markup_expression=abjad.Expression(
                                callbacks=[
                                    abjad.Expression(
                                        evaluation_template='abjad.markuptools.Markup',
                                        is_initializer=True,
                                        ),
                                    ],
                                proxy_class=abjad.Markup,
                                ),
                            string_template='{}',
                            ),
                        abjad.Expression(
                            evaluation_template='{}.sum()',
                            markup_expression=abjad.Expression(
                                callbacks=[
                                    abjad.Expression(
                                        evaluation_template='[{}]',
                                        ),
                                    abjad.Expression(
                                        evaluation_template='abjad.markuptools.MarkupList',
                                        is_initializer=True,
                                        ),
                                    abjad.Expression(
                                        evaluation_template="{}.insert(i=0, item='sum(')",
                                        force_return=True,
                                        ),
                                    abjad.Expression(
                                        evaluation_template="{}.append(item=')')",
                                        force_return=True,
                                        ),
                                    abjad.Expression(
                                        evaluation_template='{}.concat()',
                                        ),
                                    ],
                                has_parentheses=True,
                                proxy_class=abjad.MarkupList,
                                ),
                            string_template='sum({})',
                            ),
                        abjad.Expression(
                            evaluation_template='abjad.sequencetools.Sequence',
                            is_initializer=True,
                            markup_expression=abjad.Expression(
                                callbacks=[
                                    abjad.Expression(
                                        evaluation_template='abjad.markuptools.Markup',
                                        is_initializer=True,
                                        ),
                                    ],
                                proxy_class=abjad.Markup,
                                ),
                            string_template='{}',
                            ),
                        ],
                    proxy_class=abjad.Sequence,
                    ),
                rhythm_maker=rhythmmakertools.NoteRhythmMaker(),
                )

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Segments'

    __slots__ = (
        '_clef', # remove
        '_division_maker',
        '_division_expression',
        '_hide_untuned_percussion_markup', # remove
        '_instrument', # remove
        '_reference_meters',
        '_rewrite_meter',
        '_rhythm_maker',
        '_rhythm_overwrites',
        '_split_at_measure_boundaries',
        '_staff_line_count', # remove
        '_stages',
        '_start_tempo', # remove
        '_stop_tempo', # remove
        '_tie_first',
        '_tie_last',
        )

    _publish_storage_format = True

    ### INITIALIZER ###    

    def __init__(
        self,
        clef=None,
        division_maker=None,
        division_expression=None,
        instrument=None,
        reference_meters=None,
        rewrite_meter=None,
        rhythm_maker=None,
        rhythm_overwrites=None,
        split_at_measure_boundaries=None,
        staff_line_count=None,
        stages=None,
        start_tempo=None,
        stop_tempo=None,
        tie_first=None,
        tie_last=None,
        ):
        self._clef = clef
        if division_expression is not None and division_maker is not None:
            message = 'can not set both division expression and division-maker'
            message += ':\n{} {}.'
            message = message.format(division_expression, division_maker)
            raise Exception(message)
        self._division_maker = division_maker
        if division_expression is not None:
            prototype = abjad.expressiontools.Expression
            assert isinstance(division_expression, prototype), repr(
                division_expression)
        self._division_expression = division_expression
        self._hide_untuned_percussion_markup = False
        self._instrument = instrument
        self._reference_meters = reference_meters
        if rewrite_meter is not None:
            rewrite_meter = bool(rewrite_meter)
        self._rewrite_meter = rewrite_meter
        self._rhythm_maker = rhythm_maker
        self._rhythm_overwrites = rhythm_overwrites
        self._split_at_measure_boundaries = split_at_measure_boundaries
        self._staff_line_count = staff_line_count
        if isinstance(stages, int):
            stages = (stages, stages)
        self._stages = stages
        self._start_tempo = start_tempo
        self._stop_tempo = stop_tempo
        if tie_first is not None:
            tie_first = bool(tie_first)
        self._tie_first = tie_first
        if tie_last is not None:
            tie_last = bool(tie_last)
        self._tie_last = tie_last

    ### SPECIAL METHODS ###

    def __call__(
        self, 
        effective_staff_name, 
        start_offset=None,
        time_signatures=None,
        ):
        r'''Calls rhythm specifier.

        Returns contribution with music payload.
        '''
        for time_signature in time_signatures:
            prototype = abjad.TimeSignature
            assert isinstance(time_signature, prototype), repr(time_signature)
        if start_offset is not None:
            assert isinstance(start_offset, abjad.Offset)
        music, start_offset = self._make_rhythm(time_signatures, start_offset)
        assert isinstance(music, (tuple, list, abjad.Voice))
        first_leaf = self._get_first_leaf(music)
        last_leaf = self._get_last_leaf(music)
        prototype = abjad.instrumenttools.Percussion
        if self.instrument is not None:
            abjad.attach(self.instrument, first_leaf, scope=abjad.Staff)
        if self.clef is not None:
            abjad.attach(self.clef, first_leaf, scope=abjad.Staff)
        pitched_prototype = (abjad.Note, abjad.Chord)
        if self.staff_line_count is not None:
            self._set_staff_line_count(first_leaf, self.staff_line_count)
        elif self.clef == abjad.Clef('percussion'):
            self._set_staff_line_count(first_leaf, 1)
        if self.tie_first and isinstance(first_leaf, pitched_prototype):
            abjad.attach('tie to me', first_leaf)
            if self._use_messiaen_style_ties:
                abjad.attach('use messiaen style ties', first_leaf)
        if self.tie_last and isinstance(last_leaf, pitched_prototype):
            abjad.attach('tie from me', last_leaf)
            if self._use_messiaen_style_ties:
                abjad.attach('use messiaen style ties', last_leaf)
        contribution = baca.Contribution(
            payload=music,
            start_offset=start_offset,
            )
        return contribution

    ### PRIVATE PROPERTIES ###

    @property
    def _default_division_maker(self):
        division_maker = baca.DivisionMaker()
        return division_maker

    @property
    def _default_rhythm_maker(self):
        mask = abjad.silence_all(use_multimeasure_rests=True) 
        multimeasure_rests = abjad.rhythmmakertools.NoteRhythmMaker(
            division_masks=[mask],
            )
        return multimeasure_rests

    @property
    def _use_messiaen_style_ties(self):
        if self.rhythm_maker.tie_specifier is None:
            return False
        return self.rhythm_maker.tie_specifier.use_messiaen_style_ties

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
        for leaf in abjad.iterate(argument).by_leaf():
            if isinstance(leaf, abjad.Chord):
                message = 'rhythm-makers produce only notes and rests: {!r}.'
                message = message.format(leaf)
                raise Exception(message)
            elif isinstance(leaf, abjad.Note):
                abjad.attach('not yet pitched', leaf)
            elif isinstance(leaf, rest_prototype):
                pass
            else:
                raise TypeError(leaf)

    def _attach_untuned_percussion_markup(self, leaf):
        name = self.instrument.instrument_name
        name = name.lower()
        markup = abjad.markuptools.Markup(name, direction=Up)
        markup = markup.box().override(('box-padding', 0.5))
        abjad.attach(markup, leaf)

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
        
    def _get_division_maker(self):
        if self.division_maker is not None:
            return self.division_maker
        return self._default_division_maker

    def _get_first_leaf(self, music):
        first_item = music[0]
        if isinstance(first_item, abjad.Selection):
            first_component = first_item[0]
        else:
            first_component = first_item
        first_leaf = abjad.inspect(first_component).get_leaf(0)
        assert isinstance(first_leaf, abjad.Leaf), repr(first_leaf)
        return first_leaf

    def _get_last_leaf(self, music):
        last_item = music[-1]
        if isinstance(last_item, abjad.Selection):
            last_component = last_item[-1]
        else:
            last_component = last_item
        assert isinstance(last_component, abjad.Component)
        if isinstance(last_component, abjad.Leaf):
            last_leaf = last_component
        else:
            last_leaf = abjad.inspect(last_component).get_leaf(-1)
        assert isinstance(last_leaf, abjad.Leaf)
        return last_leaf

    def _get_storage_format_specification(self):
        agent = abjad.systemtools.StorageFormatAgent(self)
        keyword_argument_names = agent.signature_keyword_names
        if not self.rhythm_overwrites:
            keyword_argument_names = list(keyword_argument_names)
            keyword_argument_names.remove('rhythm_overwrites')
        return abjad.systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    def _make_rhythm(self, time_signatures, start_offset):
        rhythm_maker = self.rhythm_maker or self._default_rhythm_maker
        if isinstance(rhythm_maker, abjad.Selection):
            selections = [rhythm_maker]
        elif isinstance(rhythm_maker, abjad.rhythmmakertools.RhythmMaker):
            division_maker = self._get_division_maker()
            divisions = self._durations_to_divisions(
                time_signatures,
                start_offset,
                )
            divisions = division_maker(divisions)
            divisions = baca.Sequence(divisions).flatten()
            contribution = self._select_divisions(divisions, start_offset)
            divisions = contribution.payload
            start_offset = contribution.start_offset
            selections = rhythm_maker(divisions)
            self._annotate_unpitched_notes(selections)
        else:
            message = 'must be rhythm-maker or explicit selection: {!r}.'
            message = message.format(rhythm_maker)
            raise TypeError(message)
        assert self._all_are_selections(selections), repr(selections)
        if self.split_at_measure_boundaries:
            specifier = abjad.rhythmmakertools.DurationSpellingSpecifier
            selections = specifier._split_at_measure_boundaries(
                selections, 
                time_signatures,
                use_messiaen_style_ties=self._use_messiaen_style_ties,
                )
            assert self._all_are_selections(selections), repr(selections)
        if self.rewrite_meter:
            specifier = abjad.rhythmmakertools.DurationSpellingSpecifier
            selections = specifier._rewrite_meter_(
                selections, 
                time_signatures,
                reference_meters=self._reference_meters,
                rewrite_tuplets=False,
                use_messiaen_style_ties=self._use_messiaen_style_ties,
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
        for rhythm_overwrite in self.rhythm_overwrites:
            selector, division_maker, rhythm_maker = rhythm_overwrite
            old_selection = selector(dummy_music_voice)
            #if 1 < len(old_selection):
            if True:
                old_selection = abjad.select(old_selection)
                result = old_selection._get_parent_and_start_stop_indices()
                parent, start_index, stop_index = result
                old_duration = old_selection.get_duration()
                division_lists = division_maker([old_duration])
                assert len(division_lists) == 1
                division_list = division_lists[0]
                new_selection = rhythm_maker(division_list)
                dummy_music_voice[start_index:stop_index+1] = new_selection
            #elif len(old_selection) == 1:
            #    assert isinstance(old_selection[0], abjad.Selection)
            #    old_selection = old_selection[0]
            #    old_duration = old_selection.get_duration()
            #    division_lists = division_maker([old_duration])
            #    assert len(division_lists) == 1
            #    division_list = division_lists[0]
            #    new_selection = rhythm_maker(division_list)
            #    old_component = old_selection[0]
            #    index = dummy_music_voice.index(old_component)
            #    dummy_music_voice[index:index+1] = new_selection
        music = dummy_music_voice[:]
        #return dummy_music_voice, start_offset
        selections = [abjad.select(_) for _ in music]
        return selections, start_offset

    def _select_divisions(self, divisions, start_offset):
        if self.division_expression is not None:
            divisions = self.division_expression(divisions)
            if not isinstance(divisions, abjad.sequencetools.Sequence):
                message = 'must be division sequence: {!r}.'
                message = message.format(divisions)
                raise Exception(message)
        new_start_offset = divisions[0].start_offset
        contribution = baca.Contribution(
            payload=divisions,
            start_offset=new_start_offset,
            )
        return contribution

    def _set_staff_line_count(self, first_leaf, staff_line_count):
        command = abjad.LilyPondCommand('stopStaff')
        abjad.attach(command, first_leaf)
        string = "override Staff.StaffSymbol #'line-count = #{}"
        string = string.format(staff_line_count)
        command = abjad.LilyPondCommand(string)
        abjad.attach(command, first_leaf)
        command = abjad.LilyPondCommand('startStaff')
        abjad.attach(command, first_leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def clef(self):
        '''Gets clef.

        Returns clef or none.
        '''
        return self._clef

    @property
    def division_expression(self):
        r'''Gets division callbacks.

        Set to none or division selector.

        Returns none or division selector.
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
    def instrument(self):
        r'''Gets instrument.

        Set to instrument or none.

        Returns instrument or none.
        '''
        return self._instrument

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
    def rewrite_meter(self):
        r'''Is true when specifier rewrites meter.

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
        r'''Is true when specifier splits at measure boundaries.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._split_at_measure_boundaries

    @property
    def staff_line_count(self):
        r'''Gets staff line count.

        Returns nonnegative integer or none.

        Xylophone music-maker always returns 5.
        '''
        if isinstance(self.instrument, abjad.instrumenttools.Xylophone):
            return 5
        return self._staff_line_count

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
    def start_tempo(self):
        r'''Gets start tempo.

        Set to tempo or none.

        Returns tempo or none.
        '''
        return self._start_tempo

    @property
    def stop_stage(self):
        r'''Gets stop stage.

        Returns positive integer.
        '''
        return self.stages[-1]

    @property
    def stop_tempo(self):
        r'''Gets stop tempo.

        Set to tempo or none.

        Returns tempo or none.
        '''
        return self._stop_tempo

    @property
    def tie_first(self):
        r'''Is true when specifier ties into first note or chord.
        Otherwise false.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._tie_first

    @property
    def tie_last(self):
        r'''Is true when specifier ties into last note or chord.
        Otherwise false.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._tie_last
