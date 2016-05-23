# -*- coding: utf-8 -*-
import abjad
import baca


class RhythmSpecifier(abjad.abctools.AbjadObject):
    r'''Rhythm specifier.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** Specifies rhythm:

        ::

            >>> rhythm_specifier = baca.tools.RhythmSpecifier(
            ...     rhythm_maker = rhythmmakertools.NoteRhythmMaker(),
            ...     )

        ::

            >>> print(format(rhythm_specifier))
            baca.tools.RhythmSpecifier(
                rhythm_maker=rhythmmakertools.NoteRhythmMaker(),
                )

    ..  container:: example

        **Example 2.** Specifies rhythm:

        ::

            >>> rhythm_specifier = baca.tools.RhythmSpecifier(
            ...     division_expression=sequence().sum().sequence(),
            ...     rhythm_maker = rhythmmakertools.NoteRhythmMaker(),
            ...     )

        ::

            >>> print(format(rhythm_specifier))
            baca.tools.RhythmSpecifier(
                division_expression=expressiontools.SequenceExpression(
                    callbacks=(
                        expressiontools.Callback(
                            name='Sequence.sum',
                            ),
                        expressiontools.Callback(
                            name='Sequence.__init__',
                            ),
                        ),
                    ),
                rhythm_maker=rhythmmakertools.NoteRhythmMaker(),
                )

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_clef', # remove
        '_division_maker',
        '_division_expression',
        '_hide_untuned_percussion_markup', # remove
        '_instrument', # remove
        '_patterns',
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

    ### INITIALIZER ###    

    def __init__(
        self,
        clef=None,
        division_maker=None,
        division_expression=None,
        instrument=None,
        patterns=None,
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
            message = 'can not set both division expression and division maker'
            message += ':\n{} {}.'
            message = message.format(division_expression, division_maker)
            raise Exception(message)
        self._division_maker = division_maker
        if division_expression is not None:
            prototype = abjad.expressiontools.SequenceExpression
            assert isinstance(division_expression, prototype), repr(
                division_expression)
        self._division_expression = division_expression
        self._hide_untuned_percussion_markup = False
        self._instrument = instrument
        if patterns is not None:
            prototype = (
                abjad.patterntools.CompoundPattern,
                abjad.patterntools.Pattern,
                abjad.patterntools.PatternInventory,
                )
            if isinstance(patterns, prototype):
                patterns = [patterns]
            for pattern in patterns:
                assert isinstance(pattern, prototype), repr(pattern)
        self._patterns = patterns
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
            prototype = abjad.indicatortools.TimeSignature
            assert isinstance(time_signature, prototype), repr(time_signature)
        if start_offset is not None:
            assert isinstance(start_offset, abjad.durationtools.Offset)
        music, start_offset = self._make_rhythm(time_signatures, start_offset)
        assert isinstance(music, (tuple, list, abjad.scoretools.Voice))
        first_leaf = self._get_first_leaf(music)
        last_leaf = self._get_last_leaf(music)
        prototype = abjad.instrumenttools.Percussion
        if self.instrument is not None:
            self._attach_instrument(
                self.instrument, 
                first_leaf, 
                effective_staff_name, 
                scope=Staff,
                )
        if self.clef is not None:
            abjad.attach(self.clef, first_leaf, scope=abjad.scoretools.Staff)
        pitched_prototype = (abjad.scoretools.Note, abjad.scoretools.Chord)
        if self.staff_line_count is not None:
            self._set_staff_line_count(first_leaf, self.staff_line_count)
        elif self.clef == abjad.indicatortools.Clef('percussion'):
            self._set_staff_line_count(first_leaf, 1)
        if self.tie_first and isinstance(first_leaf, pitched_prototype):
            abjad.attach('tie to me', first_leaf)
            if self._use_messiaen_style_ties:
                abjad.attach('use messiaen style ties', first_leaf)
        if self.tie_last and isinstance(last_leaf, pitched_prototype):
            abjad.attach('tie from me', last_leaf)
            if self._use_messiaen_style_ties:
                abjad.attach('use messiaen style ties', last_leaf)
        contribution = baca.tools.Contribution(
            payload=music,
            start_offset=start_offset,
            )
        return contribution

    ### PRIVATE PROPERTIES ###

    @property
    def _default_division_maker(self):
        division_maker = baca.tools.DivisionMaker()
        return division_maker

    @property
    def _default_rhythm_maker(self):
        mask = abjad.rhythmmakertools.silence_all(use_multimeasure_rests=True) 
        multimeasure_rests = abjad.rhythmmakertools.NoteRhythmMaker(
            division_masks=[mask],
            )
        return multimeasure_rests

    @property
    def _storage_format_specification(self):
        manager = abjad.systemtools.StorageFormatManager
        keyword_argument_names = \
            manager.get_signature_keyword_argument_names(self)
        if not self.rhythm_overwrites:
            keyword_argument_names = list(keyword_argument_names)
            keyword_argument_names.remove('rhythm_overwrites')
        return abjad.systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    @property
    def _use_messiaen_style_ties(self):
        if self.rhythm_maker.tie_specifier is None:
            return False
        return self.rhythm_maker.tie_specifier.use_messiaen_style_ties

    ### PRIVATE METHODS ###

    @staticmethod
    def _all_are_selections(expr):
        return all(isinstance(_, abjad.selectiontools.Selection) for _ in expr)

    def _apply_figure_rhythm_maker(self, figure_list, figure_token):
        assert len(figure_list) == len(figure_token)
        total_length = len(figure_list)
        patterns = self._get_patterns()
        for index, stage_token in enumerate(figure_token):
            for pattern in patterns:
                if pattern.matches_index(
                    index=index,
                    total_length=total_length,
                    ):
                    stage_selection = self._apply_payload(stage_token)
                    figure_list[index] = stage_selection
        return figure_list

    def _apply_payload(self, stage_token):
        rhythm_maker = self._get_rhythm_maker()
        stage_selections, state_manifest = rhythm_maker([stage_token])
        assert len(stage_selections) == 1, repr(stage_selections)
        stage_selection = stage_selections[0]
        return stage_selection

    def _attach_instrument(
        self, 
        instrument, 
        component, 
        effective_staff_name, 
        materials_package,
        scope=None,
        ):
        self._check_instrument(
            instrument, 
            effective_staff_name,
            materials_package,
            )
        abjad.attach(instrument, component, scope=scope)

    def _attach_untuned_percussion_markup(self, leaf):
        name = self.instrument.instrument_name
        name = name.lower()
        markup = abjad.markuptools.Markup(name, direction=Up)
        markup = markup.box().override(('box-padding', 0.5))
        abjad.attach(markup, leaf)

    def _check_instrument(
        self, 
        instrument, 
        effective_staff_name,
        materials_package,
        ):
        message = 'can not attach {!r} to {}.'
        message = message.format(instrument, effective_staff_name)
        allowable_instruments = \
            materials_package.score_setup[effective_staff_name]
        if not isinstance(instrument, allowable_instruments):
            raise Exception(message)

    @staticmethod
    def _durations_to_divisions(durations, start_offset):
        divisions = [abjad.durationtools.Division(_) for _ in durations]
        durations = [_.duration for _ in divisions]
        start_offset = abjad.durationtools.Offset(start_offset)
        durations.insert(0, start_offset)
        start_offsets = abjad.mathtools.cumulative_sums(durations)[1:-1]
        assert len(divisions) == len(start_offsets)
        divisions_ = []
        for division, start_offset in zip(divisions, start_offsets):
            division_ = abjad.durationtools.Division(
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
        if isinstance(first_item, abjad.selectiontools.Selection):
            first_component = first_item[0]
        else:
            first_component = first_item
        first_leaf = abjad.inspect_(first_component).get_leaf(0)
        assert isinstance(first_leaf, abjad.scoretools.Leaf), repr(first_leaf)
        return first_leaf

    def _get_last_leaf(self, music):
        last_item = music[-1]
        if isinstance(last_item, abjad.selectiontools.Selection):
            last_component = last_item[-1]
        else:
            last_component = last_item
        assert isinstance(last_component, abjad.scoretools.Component)
        if isinstance(last_component, abjad.scoretools.Leaf):
            last_leaf = last_component
        else:
            last_leaf = abjad.inspect_(last_component).get_leaf(-1)
        assert isinstance(last_leaf, abjad.scoretools.Leaf)
        return last_leaf

    def _get_patterns(self):
        if self.patterns is None:
            return [abjad.patterntools.select_all()]
        return self.patterns

#    def _get_rhythm_maker(self):
#        if self.rhythm_maker is None:
#            return baca.tools.FigureRhythmMaker()
#        return self.rhythm_maker

    def _get_rhythm_maker(self):
        if self.rhythm_maker is not None:
            return self.rhythm_maker
        return self._default_rhythm_maker

    def _make_rhythm(self, time_signatures, start_offset):
        rhythm_maker = self._get_rhythm_maker()
        if isinstance(rhythm_maker, abjad.selectiontools.Selection):
            selections = [rhythm_maker]
        elif isinstance(rhythm_maker, abjad.rhythmmakertools.RhythmMaker):
            division_maker = self._get_division_maker()
            divisions = self._durations_to_divisions(
                time_signatures,
                start_offset,
                )
            divisions = division_maker(divisions)
            divisions = abjad.sequencetools.flatten_sequence(divisions)
            contribution = self._select_divisions(divisions, start_offset)
            divisions = contribution.payload
            start_offset = contribution.start_offset
            selections = rhythm_maker(divisions)
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
        dummy_measures = abjad.scoretools.make_spacer_skip_measures(
            time_signatures)
        dummy_time_signature_voice = abjad.scoretools.Voice(dummy_measures)
        dummy_music_voice = abjad.scoretools.Voice()
        dummy_music_voice.extend(selections)
        dummy_staff = Staff([dummy_time_signature_voice, dummy_music_voice])
        dummy_staff.is_simultaneous = True
        for rhythm_overwrite in self.rhythm_overwrites:
            selector, division_maker, rhythm_maker = rhythm_overwrite
            old_music_selection = selector(dummy_music_voice)
            prototype = abjad.selectiontools.Selection
            #if 1 < len(old_music_selection):
            if True:
                old_music_selection = abjad.selectiontools.SliceSelection(
                    old_music_selection)
                result = old_music_selection._get_parent_and_start_stop_indices()
                parent, start_index, stop_index = result
                old_duration = old_music_selection.get_duration()
                division_lists = division_maker([old_duration])
                assert len(division_lists) == 1
                division_list = division_lists[0]
                new_music_selection = rhythm_maker(division_list)
                dummy_music_voice[start_index:stop_index+1] = \
                    new_music_selection
            #elif len(old_music_selection) == 1:
            #    prototype = abjad.selectiontools.Selection
            #    assert isinstance(old_music_selection[0], prototype)
            #    old_music_selection = old_music_selection[0]
            #    old_duration = old_music_selection.get_duration()
            #    division_lists = division_maker([old_duration])
            #    assert len(division_lists) == 1
            #    division_list = division_lists[0]
            #    new_music_selection = rhythm_maker(division_list)
            #    old_component = old_music_selection[0]
            #    index = dummy_music_voice.index(old_component)
            #    dummy_music_voice[index:index+1] = new_music_selection
        music = dummy_music_voice[:]
        return dummy_music_voice, start_offset

    def _select_divisions(self, divisions, start_offset):
        if self.division_expression is not None:
            divisions = self.division_expression(divisions)
            if not isinstance(divisions, abjad.sequencetools.Sequence):
                message = 'must be division sequence: {!r}.'
                message = message.format(divisions)
                raise Exception(message)
        new_start_offset = divisions[0].start_offset
        contribution = baca.tools.Contribution(
            payload=divisions,
            start_offset=new_start_offset,
            )
        return contribution

    def _set_staff_line_count(self, first_leaf, staff_line_count):
        command = abjad.indicatortools.LilyPondCommand('stopStaff')
        abjad.attach(command, first_leaf)
        string = "override Staff.StaffSymbol #'line-count = #{}"
        string = string.format(staff_line_count)
        command = abjad.indicatortools.LilyPondCommand(string)
        abjad.attach(command, first_leaf)
        command = abjad.indicatortools.LilyPondCommand('startStaff')
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
        r'''Gets division maker.

        Set to none or division maker.

        Returns none or division maker.
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
    def patterns(self):
        r'''Gets patterns.

        Set to patterns or none.

        Defaults to none.

        Returns patterns or none.
        '''
        return self._patterns

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